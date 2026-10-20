"""Kabine kayıt yardımcıları: oyunu yerel yazı tipleriyle açar, CDP screencast ile kare kaydeder."""
import base64, json, os, subprocess, time, pathlib
from playwright.sync_api import sync_playwright

SCR = pathlib.Path(__import__('os').environ.get('KABINE_ROOT', pathlib.Path(__file__).resolve().parents[1]))
GAME = SCR / 'game' / 'kabine.html'
FONTS = SCR / 'fonts' / 'gf' / 'ofl'

FONT_FILES = {
    'pixel.ttf': FONTS / 'pixelifysans' / 'PixelifySans[wght].ttf',
    'barlow-500.ttf': FONTS / 'barlowsemicondensed' / 'BarlowSemiCondensed-Medium.ttf',
    'barlow-600.ttf': FONTS / 'barlowsemicondensed' / 'BarlowSemiCondensed-SemiBold.ttf',
    'barlow-700.ttf': FONTS / 'barlowsemicondensed' / 'BarlowSemiCondensed-Bold.ttf',
    'old-700.ttf': FONTS / 'oldstandardtt' / 'OldStandard-Bold.ttf',
    'old-400i.ttf': FONTS / 'oldstandardtt' / 'OldStandard-Italic.ttf',
}
FONT_CSS = """
@font-face{font-family:'Pixelify Sans';font-weight:400 700;src:url(https://fonts.gstatic.com/kab/pixel.ttf) format('truetype');}
@font-face{font-family:'Barlow Semi Condensed';font-weight:500;src:url(https://fonts.gstatic.com/kab/barlow-500.ttf);}
@font-face{font-family:'Barlow Semi Condensed';font-weight:600;src:url(https://fonts.gstatic.com/kab/barlow-600.ttf);}
@font-face{font-family:'Barlow Semi Condensed';font-weight:700;src:url(https://fonts.gstatic.com/kab/barlow-700.ttf);}
@font-face{font-family:'Old Standard TT';font-weight:700;font-style:normal;src:url(https://fonts.gstatic.com/kab/old-700.ttf);}
@font-face{font-family:'Old Standard TT';font-weight:400;font-style:italic;src:url(https://fonts.gstatic.com/kab/old-400i.ttf);}
"""

SETTINGS = {'lang': 'tr', 'sound': False, 'music': False, 'seen': {}}


def route_all(route):
    url = route.request.url
    if url.startswith('https://fonts.googleapis.com/css2'):
        return route.fulfill(status=200, content_type='text/css', body=FONT_CSS)
    if url.startswith('https://fonts.gstatic.com/kab/'):
        name = url.rsplit('/', 1)[-1]
        return route.fulfill(status=200, content_type='font/ttf', body=FONT_FILES[name].read_bytes())
    if url.startswith('https://kabine.local/'):
        return route.fulfill(status=200, content_type='text/html; charset=utf-8', body=GAME.read_bytes())
    return route.abort()


def open_game(p, lang='tr', seen_all=True, settings=None):
    b = p.chromium.launch(args=['--force-color-profile=srgb'])
    ctx = b.new_context(viewport={'width': 480, 'height': 854}, device_scale_factor=2.25, locale='tr-TR', has_touch=False)
    ctx.route('**/*', route_all)
    st = dict(SETTINGS, lang=lang)
    if settings: st.update(settings)
    if seen_all:
        st['seen'] = {k: 1 for k in ['rally', 'press', 'market', 'stack', 'budget', 'parliament', 'debate', 'gala', 'summit', 'bus', 'dodge', 'frame', 'poster', 'trend', 'delegate']}
        st['seen'].update({'coach': 1})
    ctx.add_init_script(f"try{{localStorage.setItem('cbs_settings_v1', {json.dumps(json.dumps(st))});}}catch(e){{}}")
    page = ctx.new_page()
    page.goto('https://kabine.local/index.html')
    page.wait_for_function('window.__cbs && document.fonts && document.fonts.status==="loaded"', timeout=20000)
    page.evaluate("document.fonts.ready")
    time.sleep(0.6)
    # Toasts must never cover the shot
    page.add_style_tag(content='#toasts{display:none!important} @keyframes kbhb{0%{background:#0b1020}100%{background:#0b1021}} #kbhb{position:fixed;left:0;top:0;width:2px;height:2px;z-index:99999;pointer-events:none;animation:kbhb .1s steps(2) infinite}')
    # heartbeat: forces a repaint every frame so the screencast never stalls on static screens
    page.evaluate("() => { const d=document.createElement('div'); d.id='kbhb'; document.body.appendChild(d); }")
    return b, ctx, page


class Recorder:
    """CDP screencast: saves every repaint as jpeg with its timestamp."""
    def __init__(self, page, outdir):
        self.page = page
        self.out = pathlib.Path(outdir)
        self.out.mkdir(parents=True, exist_ok=True)
        for f in self.out.glob('*.jpg'): f.unlink()
        self.frames = []
        self.cdp = page.context.new_cdp_session(page)
        self.cdp.on('Page.screencastFrame', self._on)

    def _on(self, ev):
        i = len(self.frames)
        fn = self.out / f'f{i:05d}.jpg'
        fn.write_bytes(base64.b64decode(ev['data']))
        self.frames.append((ev['metadata']['timestamp'], fn.name))
        try: self.cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
        except Exception: pass

    def start(self):
        self.t0 = time.time()
        self.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': 1080, 'maxHeight': 1920, 'everyNthFrame': 1})

    def mark(self):
        return time.time() - self.t0

    def stop(self):
        # flush: nudge a repaint so the last state is captured
        self.page.wait_for_timeout(250)
        self.cdp.send('Page.stopScreencast')
        self.page.wait_for_timeout(150)
        (self.out / 'frames.json').write_text(json.dumps({'t0': self.t0, 'frames': self.frames}))
        return self.frames


def frames_to_mp4(framedir, out, fps=30, start=None, end=None):
    """Turn timestamped screencast frames into a constant-frame-rate mp4 (1080x1920)."""
    d = pathlib.Path(framedir).resolve()
    meta = json.loads((d / 'frames.json').read_text())
    fr = meta['frames']; t0 = meta['t0']
    rows = [(ts - t0, name) for ts, name in fr]
    if start is not None: rows = [r for r in rows if r[0] >= start] or rows[-1:]
    if end is not None: rows = [r for r in rows if r[0] <= end]
    lines = []
    for i, (t, name) in enumerate(rows):
        nxt = rows[i + 1][0] if i + 1 < len(rows) else (end if end else t + 0.5)
        dur = max(0.001, nxt - t)
        lines.append(f"file '{d / name}'\nduration {dur:.4f}")
    lines.append(f"file '{d / rows[-1][1]}'")
    lst = d / 'concat.txt'
    lst.write_text('\n'.join(lines))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst),
                    '-vf', f'scale=1080:1920:flags=lanczos,fps={fps},format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', str(out)], check=True)
    return out
