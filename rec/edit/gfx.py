"""Overlay graphics for the 'KABİNE HABER' news-parody look: lower thirds, stamps, bugs, end card layers."""
import base64, html, pathlib
from playwright.sync_api import sync_playwright

SCR = pathlib.Path(__import__('os').environ.get('KABINE_ROOT', pathlib.Path(__file__).resolve().parents[2]))
OFL = SCR / 'fonts' / 'gf' / 'ofl'
FONTS = {
    'anton.ttf': OFL / 'anton' / 'Anton-Regular.ttf',
    'bungee.ttf': OFL / 'bungee' / 'Bungee-Regular.ttf',
    'pixel.ttf': OFL / 'pixelifysans' / 'PixelifySans[wght].ttf',
    'barlow.ttf': OFL / 'barlowsemicondensed' / 'BarlowSemiCondensed-Bold.ttf',
}
ICON = 'data:image/png;base64,' + base64.b64encode((SCR / 'kit' / 'img' / 'icon-512.png').read_bytes()).decode()

CSS = """
@font-face{font-family:Anton;src:url(https://f.local/anton.ttf)}
@font-face{font-family:Bungee;src:url(https://f.local/bungee.ttf)}
@font-face{font-family:Pix;font-weight:400 700;src:url(https://f.local/pixel.ttf)}
@font-face{font-family:Barlow;font-weight:700;src:url(https://f.local/barlow.ttf)}
*{box-sizing:border-box;margin:0}
html,body{background:transparent}
body{display:inline-block;padding:24px}
:root{--navy:#0b1020;--gold:#f5b83d;--red:#e43b34;--paper:#f6eed8;--purple:#8a4fd8;--ink:#141a33}
.lt{width:fit-content;max-width:900px;display:flex;flex-direction:column;align-items:flex-start;filter:drop-shadow(12px 12px 0 rgba(0,0,0,.55))}
.lt .tag{display:flex;align-items:center;gap:14px;background:var(--red);color:#fff;font:400 46px/1 Bungee;padding:14px 22px 12px;letter-spacing:.02em}
.lt .tag i{width:20px;height:20px;border-radius:50%;background:#fff;display:block}
.lt .head{background:var(--paper);color:var(--ink);font:400 104px/1.0 Anton;text-transform:uppercase;padding:16px 26px 18px;max-width:880px;border-left:16px solid var(--gold)}
.lt .strip{background:var(--navy);color:var(--gold);font:400 28px/1 Bungee;padding:10px 22px;letter-spacing:.04em;align-self:stretch;margin-left:0}
.stamp{font-family:Bungee;font-weight:400;line-height:.95;paint-order:stroke fill;text-align:center;text-shadow:12px 12px 0 rgba(0,0,0,.45);white-space:pre-line}
.bug{display:flex;align-items:stretch;filter:drop-shadow(6px 6px 0 rgba(0,0,0,.5))}
.bug b{background:var(--navy);color:var(--gold);font:400 32px/1 Bungee;padding:12px 16px 10px;border:3px solid var(--gold);border-right:0}
.bug span{background:var(--red);color:#fff;font:400 32px/1 Bungee;padding:12px 16px 10px;display:flex;align-items:center;gap:10px}
.bug span i{width:14px;height:14px;border-radius:50%;background:#fff;display:block}
.rew{font:400 92px/1 Bungee;color:#fff;text-shadow:-6px 0 0 rgba(255,40,60,.85),6px 0 0 rgba(40,220,255,.85),0 10px 24px rgba(0,0,0,.6);letter-spacing:.02em;white-space:pre-line;text-align:center}
.quote{font-family:Anton;font-weight:400;line-height:1;color:#fff;-webkit-text-stroke:14px #000;paint-order:stroke fill;text-transform:uppercase;text-align:center;white-space:pre-line;text-shadow:10px 12px 0 rgba(0,0,0,.6)}
.cap{font-family:Anton;font-weight:400;line-height:1.02;-webkit-text-stroke:12px #0b1020;paint-order:stroke fill;text-transform:uppercase;text-align:center;white-space:pre-line;text-shadow:8px 10px 0 rgba(0,0,0,.55);max-width:960px}
.badge{display:inline-flex;align-items:center;justify-content:center;width:150px;height:150px;background:var(--gold);color:var(--ink);font:400 104px/1 Bungee;box-shadow:10px 10px 0 rgba(0,0,0,.55);border:6px solid var(--ink)}
.endbg{width:1080px;height:1920px;background:radial-gradient(ellipse at 50% 34%,rgba(245,184,61,.28),transparent 52%),repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 3px,transparent 3px 7px),#0b1020;position:relative;overflow:hidden}
.endbg i{position:absolute;width:14px;height:14px;background:#fff;opacity:.85}
.icon{width:440px;height:440px;image-rendering:pixelated}
.logo{font:700 230px/0.9 Pix;color:var(--gold);text-shadow:10px 10px 0 #6b3d05,18px 18px 0 rgba(0,0,0,.45);letter-spacing:.01em}
.logo.latin{font:400 220px/0.95 Anton;letter-spacing:.02em}
.sub{font:700 56px/1 Pix;color:#fff;letter-spacing:.12em;text-shadow:5px 5px 0 #000}
.tagl{font:400 96px/1 Anton;color:#fff;text-transform:uppercase;text-shadow:8px 8px 0 rgba(0,0,0,.5);text-align:center;white-space:pre-line}
.handle{font:400 58px/1 Anton;color:var(--gold);letter-spacing:.03em}
.pill{font:400 50px/1 Bungee;background:var(--red);color:#fff;padding:18px 30px 16px;box-shadow:10px 10px 0 rgba(0,0,0,.5)}
"""
STARS = ''.join(f'<i style="left:{x}px;top:{y}px"></i>' for x, y in [(90, 210), (970, 260), (150, 1080), (940, 1160), (70, 1600), (1000, 1700), (520, 140), (820, 760), (230, 650)])


def e(s):
    return html.escape(s)


def spec_html(kind, **k):
    if kind == 'lt':
        strip = f'<div class="strip">{e(k.get("strip", "KABİNE HABER · @KABINEGAME"))}</div>' if k.get('strip', True) is not False else ''
        return f'<div class="lt"><div class="tag"><i></i>{e(k.get("tag", "SON DAKİKA"))}</div><div class="head">{e(k["head"]).replace(chr(10), "<br>")}</div>{strip}</div>'
    if kind == 'stamp':
        return f'<div class="stamp" style="font-size:{k.get("size", 190)}px;color:{k.get("color", "#e43b34")};-webkit-text-stroke:{k.get("stroke", 12)}px #fff">{e(k["text"])}</div>'
    if kind == 'bug':
        return f'<div class="bug"><b>{e(k.get("name", "KABİNE HABER"))}</b><span><i></i>{e(k.get("live", "CANLI"))}</span></div>'
    if kind == 'rew':
        return f'<div class="rew">{e(k["text"])}</div>'
    if kind == 'quote':
        return f'<div class="quote" style="font-size:{k.get("size", 150)}px">{e(k["text"])}</div>'
    if kind == 'cap':
        return f'<div class="cap" style="font-size:{k.get("size", 120)}px;color:{k.get("color", "#fff")}">{e(k["text"])}</div>'
    if kind == 'badge':
        return f'<div class="badge">{e(k["text"])}</div>'
    if kind == 'pill':
        return f'<div class="pill">{e(k["text"])}</div>'
    if kind == 'endbg':
        return f'<div class="endbg">{STARS}</div>'
    if kind == 'icon':
        return f'<img class="icon" src="{ICON}">'
    if kind == 'logo':
        cls = 'logo latin' if k.get('latin') else 'logo'
        return f'<div class="{cls}">{e(k.get("text", "KABİNE"))}</div>'
    if kind == 'sub':
        return f'<div class="sub">{e(k.get("text", "BAŞKANLIK SİMÜLATÖRÜ"))}</div>'
    if kind == 'tagl':
        return f'<div class="tagl">{e(k["text"])}</div>'
    if kind == 'handle':
        return f'<div class="handle">{e(k.get("text", "@kabinegame"))}</div>'
    raise ValueError(kind)


def render(specs, outdir):
    """specs: {name: (kind, kwargs)} -> {name: path}"""
    out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    paths = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1200, 'height': 2000}, device_scale_factor=1)

        def route(r):
            u = r.request.url
            if u.startswith('https://f.local/'):
                return r.fulfill(status=200, content_type='font/ttf', body=FONTS[u.rsplit('/', 1)[-1]].read_bytes())
            return r.abort()
        ctx.route('**/*', route)
        page = ctx.new_page()
        for name, (kind, kw) in specs.items():
            full = kind == 'endbg'
            body = spec_html(kind, **kw)
            page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="{"padding:0" if full else ""}">{body}</body></html>')
            page.evaluate('document.fonts.ready'); page.wait_for_timeout(60)
            el = page.locator('body > *').first
            path = out / f'{name}.png'
            if full:
                page.set_viewport_size({'width': 1080, 'height': 1920}); page.screenshot(path=str(path)); page.set_viewport_size({'width': 1200, 'height': 2000})
            else:
                bb = el.bounding_box(); pad = 30
                page.screenshot(path=str(path), omit_background=True, clip={'x': max(0, bb['x'] - pad), 'y': max(0, bb['y'] - pad), 'width': bb['width'] + 2 * pad, 'height': bb['height'] + 2 * pad})
            paths[name] = str(path)
        b.close()
    return paths
