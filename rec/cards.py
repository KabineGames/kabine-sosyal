"""Renders on-screen text cards (transparent 1080x1920 PNG) and full end cards in the game's own look."""
import sys, pathlib, base64, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from harness import route_all, FONT_CSS, SCR
from playwright.sync_api import sync_playwright

ICON = (SCR / 'kit' / 'img' / 'icon-512.png').read_bytes()
ICON_URL = 'data:image/png;base64,' + base64.b64encode(ICON).decode()

BASE_CSS = FONT_CSS + """
* { box-sizing: border-box; margin: 0; }
html, body { width: 1080px; height: 1920px; background: transparent; overflow: hidden; }
:root { --gold:#f5b83d; --gold-dk:#6b3d05; --ink:#eef1fa; --mute:#9aa6c8; --bg:#0d1222; --panel:#121a31; --line:#2f3d68; --party:#8a4fd8;
  --pc: polygon(0 12px, 6px 12px, 6px 6px, 12px 6px, 12px 0, calc(100% - 12px) 0, calc(100% - 12px) 6px, calc(100% - 6px) 6px, calc(100% - 6px) 12px, 100% 12px, 100% calc(100% - 12px), calc(100% - 6px) calc(100% - 12px), calc(100% - 6px) calc(100% - 6px), calc(100% - 12px) calc(100% - 6px), calc(100% - 12px) 100%, 12px 100%, 12px calc(100% - 6px), 6px calc(100% - 6px), 6px calc(100% - 12px), 0 calc(100% - 12px)); }
.card { position: absolute; left: 56px; width: 800px; padding: 26px 34px 32px; background: rgba(9, 13, 27, .94);
  border: 6px solid var(--gold); box-shadow: 10px 10px 0 rgba(0,0,0,.55); text-align: center; }
.t { font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 96px; line-height: .98; color: var(--gold);
  text-shadow: 5px 5px 0 var(--gold-dk), 9px 9px 0 rgba(0,0,0,.45); letter-spacing: .01em; }
.t.w { color: #fff; text-shadow: 5px 5px 0 #2a2f45, 9px 9px 0 rgba(0,0,0,.45); }
.t.sm { font-size: 80px; }
.s { margin-top: 16px; font-family: 'Barlow Semi Condensed'; font-weight: 600; font-size: 44px; line-height: 1.15; color: var(--ink); }
.tag { display: inline-block; margin-bottom: 14px; padding: 6px 18px 9px; font-family: 'Pixelify Sans'; font-weight: 700; font-size: 40px;
  background: var(--gold); color: #1c1305; clip-path: var(--pc); }
.big { position: absolute; left: 56px; width: 800px; text-align: center; font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 300px; line-height: 1;
  color: var(--gold); text-shadow: 10px 10px 0 var(--gold-dk), 18px 18px 0 rgba(0,0,0,.5); }
/* full end card */
.end { position: absolute; inset: 0; background:
   radial-gradient(ellipse at 50% 18%, rgba(245,184,61,.16), transparent 55%),
   repeating-linear-gradient(90deg, rgba(255,255,255,.025) 0 4px, transparent 4px 16px), #0b1020; }
.end .stars i { position: absolute; width: 12px; height: 12px; background: #fff; opacity: .8; }
.end .wrap { position: absolute; left: 56px; width: 800px; top: 270px; display: flex; flex-direction: column; align-items: center; gap: 30px; text-align: center; }
.end img { width: 300px; height: 300px; image-rendering: pixelated; clip-path: var(--pc); }
.logo { font-family: 'Pixelify Sans'; font-weight: 700; font-size: 168px; line-height: .9; color: var(--gold); text-shadow: 8px 8px 0 var(--gold-dk), 15px 15px 0 rgba(0,0,0,.45); }
.sub { font-family: 'Pixelify Sans'; font-weight: 700; font-size: 46px; letter-spacing: .1em; color: #fff; text-shadow: 4px 4px 0 #000; }
.line { font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 92px; line-height: 1; color: #fff; text-shadow: 5px 5px 0 #2a2f45; }
.cta { margin-top: 14px; padding: 20px 36px 26px; background: var(--gold); color: #1c1305; font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 64px; line-height: 1;
  clip-path: var(--pc); box-shadow: inset 0 -10px 0 rgba(0,0,0,.25); }
.note { font-family: 'Barlow Semi Condensed'; font-weight: 600; font-size: 40px; color: var(--mute); }
"""

STARS = ''.join(f'<i style="left:{x}px;top:{y}px"></i>' for x, y in [(90, 160), (980, 220), (160, 980), (930, 1090), (70, 1500), (1000, 1620), (520, 120), (800, 700)])


def esc(s):
    return html.escape(s).replace('\n', '<br>')


def card_html(c):
    kind = c.get('kind', 'card')
    if kind == 'big':
        return f'<div class="big" style="top:{c["y"]}px">{esc(c["text"])}</div>'
    if kind == 'end':
        parts = [f'<div class="end"><div class="stars">{STARS}</div><div class="wrap">']
        if c.get('line'): parts.append(f'<div class="line">{esc(c["line"])}</div>')
        parts.append(f'<img src="{ICON_URL}" alt="">')
        lf = ' style="font-family:\'Barlow Semi Condensed\';font-size:176px"' if c.get('logofont') == 'barlow' else ''
        parts.append(f'<div><div class="logo"{lf}>{esc(c.get("logo", "KABİNE"))}</div><div class="sub" style="margin-top:18px">{esc(c.get("sub", "BAŞKANLIK SİMÜLATÖRÜ"))}</div></div>')
        if c.get('cta'): parts.append(f'<div class="cta">{esc(c["cta"])}</div>')
        if c.get('note'): parts.append(f'<div class="note">{esc(c["note"])}</div>')
        parts.append('</div></div>')
        return ''.join(parts)
    tag = f'<div class="tag">{esc(c["tag"])}</div><br>' if c.get('tag') else ''
    t = f'<div class="t {c.get("tcls", "")}">{esc(c["text"])}</div>' if c.get('text') else ''
    s = f'<div class="s">{esc(c["sub"])}</div>' if c.get('sub') else ''
    return f'<div class="card {c.get("cls", "")}" style="top:{c["y"]}px">{tag}{t}{s}</div>'


def render(cards, outdir):
    """cards: {name: spec}. Writes outdir/name.png"""
    out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        ctx.route('**/*', route_all)
        page = ctx.new_page()
        for name, spec in cards.items():
            page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{card_html(spec)}</body></html>')
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(120)
            page.screenshot(path=str(out / f'{name}.png'), omit_background=spec.get('kind') != 'end')
        b.close()
