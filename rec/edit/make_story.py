"""Instagram hikâye görseli + öne çıkanlar kapakları (1080x1920 PNG). Çıktı: cikti/v2/story/"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gfx import CSS, ICON, FONTS, STARS
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).resolve().parents[2] / 'cikti' / 'v2' / 'story'; OUT.mkdir(parents=True, exist_ok=True)
X = CSS + """
body{padding:0}
.pg{width:1080px;height:1920px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 38%,rgba(245,184,61,.30),transparent 55%),repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 3px,transparent 3px 7px),#0b1020;display:flex;flex-direction:column;align-items:center}
.pg i{position:absolute;width:14px;height:14px;background:#fff;opacity:.85}
.cov{justify-content:center}
.ring{width:620px;height:620px;border-radius:50%;border:14px solid var(--gold);display:flex;align-items:center;justify-content:center;flex-direction:column;background:rgba(245,184,61,.08)}
.glyph{font:400 230px/1 Bungee;color:var(--gold);text-shadow:10px 10px 0 #6b3d05}
.word{font:400 92px/1 Bungee;color:#fff;margin-top:18px;text-shadow:6px 6px 0 #000}
"""
STORY = f"""<div class="pg">{STARS}
<div style="height:300px"></div>
<div class="stamp" style="font-size:250px;color:#f5b83d;-webkit-text-stroke:16px #fff;transform:rotate(-5deg)">ÇIKTI!</div>
<img class="icon" src="{ICON}" style="width:380px;height:380px;margin-top:60px">
<div class="logo" style="margin-top:30px">KABİNE</div>
<div class="sub" style="margin-top:22px">BAŞKANLIK SİMÜLATÖRÜ</div>
<div class="tagl" style="margin-top:70px;font-size:84px">BELEDİYEDEN<br>BAŞKANLIĞA</div>
<div class="pill" style="margin-top:70px;transform:rotate(-2deg)">APP STORE’DA ÜCRETSİZ</div>
<div class="handle" style="margin-top:46px">@kabinegame</div>
</div>"""


def cover(glyph, word):
    return f'<div class="pg cov">{STARS}<div class="ring"><div class="glyph">{glyph}</div><div class="word">{word}</div></div></div>'


PAGES = {'story_cikti': STORY,
         'hl_cikti': cover('★', 'ÇIKTI'), 'hl_oyun': cover('▶', 'OYUN'),
         'hl_gaf': cover('?!', 'GAFLAR'), 'hl_sss': cover('i', 'SSS')}

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    def route(r):
        n = r.request.url.rsplit('/', 1)[-1]
        if n in FONTS: return r.fulfill(body=FONTS[n].read_bytes(), content_type='font/ttf')
        return r.abort()
    pg.route('https://f.local/**', route)
    for name, body in PAGES.items():
        pg.set_content(f'<html><head><style>{X}</style></head><body>{body}</body></html>')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(150)
        pg.locator('.pg').screenshot(path=str(OUT / f'{name}.png'))
        print(name)
    b.close()
