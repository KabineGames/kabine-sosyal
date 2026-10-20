"""Profile photo, highlight covers and the test-call carousel (TR + EN), in the game's look."""
import sys, base64, pathlib, html, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from harness import open_game, SCR
from cards import BASE_CSS, ICON_URL
from playwright.sync_api import sync_playwright

OUT = SCR / 'cikti' / 'sosyal'
SHOTS = SCR / 'rec' / 'shots'


def img_url(p):
    return 'data:image/jpeg;base64,' + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def esc(s):
    return html.escape(s).replace('\n', '<br>')


CSS = BASE_CSS + """
html, body { width: 1080px; height: 1350px; }
.slide { position: absolute; inset: 0; overflow: hidden; background:
   radial-gradient(ellipse at 22% 8%, rgba(245,184,61,.18), transparent 50%),
   repeating-linear-gradient(90deg, rgba(255,255,255,.025) 0 4px, transparent 4px 16px), #0b1020; }
.brand { position: absolute; left: 70px; top: 60px; display: flex; align-items: center; gap: 18px; }
.brand img { width: 72px; height: 72px; image-rendering: pixelated; }
.brand b { font-family: 'Pixelify Sans'; font-weight: 700; font-size: 44px; color: var(--gold); text-shadow: 3px 3px 0 var(--gold-dk); }
.brand span { font-family: 'Barlow Semi Condensed'; font-weight: 600; font-size: 30px; color: var(--mute); }
.h { position: absolute; left: 70px; font-family: 'Barlow Semi Condensed'; font-weight: 700; color: var(--gold); line-height: .95;
     text-shadow: 6px 6px 0 var(--gold-dk), 11px 11px 0 rgba(0,0,0,.45); }
.p { position: absolute; left: 70px; font-family: 'Barlow Semi Condensed'; font-weight: 600; color: var(--ink); line-height: 1.2; }
.phone { position: absolute; width: 400px; height: 711px; border: 8px solid #2f3d68; background: #000; box-shadow: 16px 16px 0 rgba(0,0,0,.55); overflow: hidden; }
.phone img { width: 100%; height: 100%; object-fit: cover; display: block; }
.num { position: absolute; left: 58px; top: 170px; font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 330px; line-height: .8; color: var(--party);
       text-shadow: 10px 10px 0 #3b2266, 18px 18px 0 rgba(0,0,0,.45); }
.chip { position: absolute; left: 70px; bottom: 70px; padding: 14px 26px 18px; background: var(--gold); color: #1c1305; font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 40px; box-shadow: 8px 8px 0 rgba(0,0,0,.5); }
.box { position: absolute; left: 70px; width: 940px; padding: 26px 30px 30px; background: rgba(9,13,27,.92); border: 5px solid var(--line); }
.box b { display: block; font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 34px; color: var(--mute); letter-spacing: .06em; margin-bottom: 6px; }
.box span { font-family: 'Barlow Semi Condensed'; font-weight: 700; font-size: 46px; color: #fff; overflow-wrap: anywhere; }
.list { position: absolute; left: 70px; width: 520px; display: flex; flex-direction: column; gap: 26px; }
.list div { display: flex; gap: 18px; align-items: flex-start; font-family: 'Barlow Semi Condensed'; font-weight: 600; font-size: 42px; color: var(--ink); line-height: 1.15; }
.list img { width: 56px; height: 56px; image-rendering: pixelated; flex: none; margin-top: 2px; }
.fine { position: absolute; left: 70px; bottom: 70px; font-family: 'Barlow Semi Condensed'; font-weight: 600; font-size: 30px; color: var(--mute); }
"""


def brand(lang):
    name = 'KABİNE' if lang == 'tr' else 'CABINET'
    bf = '' if lang == 'tr' else ' style="font-family:\'Barlow Semi Condensed\'"'
    return f'<div class="brand"><img src="{ICON_URL}"><div><b{bf}>{name}</b><br><span>@kabinegame</span></div></div>'


def slides(lang, icons):
    s = SHOTS
    if lang == 'tr':
        T = dict(c_h='KABİNE’Yİ\nHERKESTEN\nÖNCE OYNA', c_p='Android kapalı testi için\n20 oyuncu arıyoruz.', c_chip='KAYDIR →',
                 w_h='NE BU OYUN?', w=[('dome', 'Belediye meclisinden başkanlığa yüksel'), ('paper', 'Her hafta bir kriz, her kriz bir manşet'),
                                        ('mic', '15 mini oyun ve seçim geceleri'), ('star', 'Tamamen kurgusal: bol çay, bol asfalt')],
                 s1_h='GRUBA\nKATIL', s1_p='Gmail hesabınla Kabine\ntest grubuna katıl.', s1_b='LİNK PROFİLDE', s1_u='groups.google.com/g/kabine-game-test',
                 s2_h='OYUNU\nİNDİR', s2_p='Gruba katılanlara test\nlinkini gönderiyoruz.\n“Test kullanıcısı ol”a bas,\nPlay Store’dan indir.',
                 s3_h='14 GÜN\nOYNA', s3_p='Ara ara birkaç dakika oyna,\nlütfen silme. Hatayı, fikri,\nen sevdiğin krizi bize yaz.', s3_chip='KATILIM LİNKİ PROFİLDE',
                 fine='Tüm kişiler, partiler ve olaylar kurgusaldır.')
        shots = dict(cover=s / 'tr_rally.jpg', what=s / 'tr_paper.jpg', two=s / 'tr_night.jpg', three=s / 'tr_dodge.jpg', bus=s / 'tr_bus.jpg')
    else:
        T = dict(c_h='PLAY IT\nBEFORE\nEVERYONE', c_p='We’re looking for 20 players\nfor the Android closed test.', c_chip='SWIPE →',
                 w_h='WHAT IS IT?', w=[('dome', 'Rise from city council to the top'), ('paper', 'A crisis every week, a headline for every crisis'),
                                       ('mic', '15 mini-games and election nights'), ('star', 'Fully fictional. Extra asphalt.')],
                 s1_h='JOIN THE\nGROUP', s1_p='Join the Cabinet test group\nwith your Gmail account.', s1_b='LINK IN BIO', s1_u='groups.google.com/g/kabine-game-test',
                 s2_h='GET THE\nGAME', s2_p='Group members get the\ntest link from us.\nTap “Become a tester”,\ninstall from Play Store.',
                 s3_h='PLAY FOR\n14 DAYS', s3_p='Open it now and then,\nkeep it installed.\nSend us bugs, ideas and\nyour favourite crisis.', s3_chip='JOIN VIA THE LINK IN BIO',
                 fine='All characters, parties and events are fictional.')
        shots = dict(cover=s / 'en_rally.jpg', what=s / 'en_paper.jpg', two=s / 'en_night.jpg', three=s / 'tr_dodge.jpg', bus=s / 'tr_bus.jpg')
    B = brand(lang)
    out = []
    out.append(f'''<div class="slide">{B}
      <div class="h" style="top:250px;font-size:112px">{esc(T["c_h"])}</div>
      <div class="p" style="top:640px;font-size:46px">{esc(T["c_p"])}</div>
      <div class="phone" style="left:610px;top:300px;transform:rotate(4deg)"><img src="{img_url(shots["cover"])}"></div>
      <div class="chip">{esc(T["c_chip"])}</div></div>''')
    items = ''.join(f'<div><img src="{icons[k]}">{esc(t)}</div>' for k, t in T['w'])
    out.append(f'''<div class="slide">{B}
      <div class="h" style="top:220px;font-size:100px">{esc(T["w_h"])}</div>
      <div class="list" style="top:400px">{items}</div>
      <div class="phone" style="left:620px;top:330px;transform:rotate(-3deg)"><img src="{img_url(shots["what"])}"></div>
      <div class="fine">{esc(T["fine"])}</div></div>''')
    out.append(f'''<div class="slide">{B}<div class="num">1</div>
      <div class="h" style="top:220px;left:330px;font-size:120px">{esc(T["s1_h"])}</div>
      <div class="p" style="top:560px;font-size:54px">{esc(T["s1_p"])}</div>
      <div class="box" style="top:720px"><b>{esc(T["s1_b"])}</b><span>{esc(T["s1_u"])}</span></div>
      <div class="phone" style="left:560px;top:930px;width:380px;height:675px;transform:rotate(-4deg)"><img src="{img_url(shots["bus"])}"></div></div>''')
    out.append(f'''<div class="slide">{B}<div class="num">2</div>
      <div class="h" style="top:220px;left:330px;font-size:120px">{esc(T["s2_h"])}</div>
      <div class="p" style="top:560px;font-size:46px">{esc(T["s2_p"])}</div>
      <div class="phone" style="left:640px;top:520px;width:360px;height:640px;transform:rotate(3deg)"><img src="{img_url(shots["two"])}"></div></div>''')
    out.append(f'''<div class="slide">{B}<div class="num">3</div>
      <div class="h" style="top:220px;left:330px;font-size:120px">{esc(T["s3_h"])}</div>
      <div class="p" style="top:560px;font-size:46px">{esc(T["s3_p"])}</div>
      <div class="phone" style="left:640px;top:600px;width:360px;height:640px;transform:rotate(4deg)"><img src="{img_url(shots["three"])}"></div>
      <div class="chip" style="bottom:90px">{esc(T["s3_chip"])}</div></div>''')
    return out


def main():
    with sync_playwright() as p:
        b, ctx, page = open_game(p)
        icons = page.evaluate("""() => { const {P}=window.__cbs; const o={};
          for (const k of ['dome','mic','star','bus','phone','chart','tv','vote']) { try { o[k]=P.icon(k); } catch(e) {} }
          return o; }""")
        icons['paper'] = icons.get('tv')
        b.close()
        b = p.chromium.launch()
        from harness import route_all
        ctx = b.new_context(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        ctx.route('**/*', route_all)
        page = ctx.new_page()
        for lang in ('tr', 'en'):
            d = OUT / 'carousel' / lang; d.mkdir(parents=True, exist_ok=True)
            for i, sl in enumerate(slides(lang, icons), 1):
                page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{sl}</body></html>')
                page.evaluate('document.fonts.ready'); page.wait_for_timeout(150)
                page.screenshot(path=str(d / f'kabine_test_{lang}_{i}.png'))
        # profile photo + highlight covers
        prof = OUT / 'profil'; prof.mkdir(parents=True, exist_ok=True)
        page.set_viewport_size({'width': 1080, 'height': 1080})
        page.set_content(f'<html><body style="margin:0;width:1080px;height:1080px;background:linear-gradient(#0c1226,#17234e);display:grid;place-items:center"><img src="{ICON_URL}" style="width:1024px;height:1024px;image-rendering:pixelated"></body></html>')
        page.wait_for_timeout(100); page.screenshot(path=str(prof / 'profil_foto.png'))
        page.set_viewport_size({'width': 1080, 'height': 1920})
        hl = [('oynanis', 'dome'), ('mini_oyunlar', 'bus'), ('nasil_test', 'phone'), ('guncellemeler', 'chart')]
        for name, ic in hl:
            page.set_content(f'''<html><head><style>{BASE_CSS}</style></head><body style="width:1080px;height:1920px;background:#0b1020;display:grid;place-items:center">
              <div style="width:640px;height:640px;border-radius:50%;background:radial-gradient(circle,#202b4f 0 60%,#121a31 61%);box-shadow:inset 0 0 0 14px #f5b83d;display:grid;place-items:center">
              <img src="{icons[ic]}" style="width:360px;height:360px;image-rendering:pixelated"></div></body></html>''')
            page.wait_for_timeout(100); page.screenshot(path=str(prof / f'one_cikan_{name}.png'))
        b.close()
    print(json.dumps({k: (v[:40] if v else None) for k, v in icons.items()}))


if __name__ == '__main__':
    main()
