"""'KABİNE ÇIKTI!' — App Store çıkış duyurusu. Hızlı 'bu oyunda neler yapabilirsin' listesi + App Store kartı."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cv2
from engine import render, W, H

REC = pathlib.Path(__file__).resolve().parent.parent
LANG = 'tr'
G = pathlib.Path(__file__).parent / 'gfx' / LANG
OUT = REC.parent / 'cikti' / 'v2'; OUT.mkdir(parents=True, exist_ok=True)
C = json.loads((pathlib.Path(__file__).parent / 'tanitim_tr.json').read_text())
SCR = (REC / 'v2').resolve().parent  # kayıtların durduğu klasör


def g(n): return str(G / f'{n}.png')


def size(n):
    im = cv2.imread(g(n), cv2.IMREAD_UNCHANGED); return im.shape[1], im.shape[0]


def lt(n, u0, u1, y, sc=0.9):
    w, h = size(n); return dict(img=g(n), u0=u0, u1=u1, x=20 + w * sc / 2, y=y, anim='slide', out='slideL', rot=-1.5, scale=sc)


def cap(n, u0, u1, y=430):
    return dict(img=g(n), u0=u0, u1=u1, x=W / 2, y=y, anim='pop', out='cut', rot=-2)


def V(n): return str(SCR / 'v2' / n)


r = V('rally_fail'); e = str(SCR / 'sess3_1')
shots = []
ev = C['verdict']
# 0) KANCA: seçim gecesi zaferi üstüne ÇIKTI!
shots.append(dict(src=e, dur=1.7, time=[(0, C['night_start']), (1.7, C['night_start'] + 1.7)],
    cam=[(0, 1.15, 540, 980), (1.7, 1.05, 540, 980)],
    fx=[('flash', 0.0, 0.14, 0.9), ('shake', 0.05, 24, 0.4)],
    ov=[dict(img=g('st_cikti'), u0=0.05, u1=1.7, x=W / 2, y=640, anim='slam', rot=-6, out='cut', wobble=1.0, scale=0.72),
        lt('lt_cikti', 0.45, 1.7, 1240)],
    sfx=[('impact', 0.05, 1.0), ('fanfare', 0.1, 0.8), ('cheer', 0.2, 0.6)]))
shots[-1]['whip_out'] = 0.1
# 1) Kediyi meclise sok
cc = C['cat_click']
shots.append(dict(src=V('card_town_cat'), dur=1.35, whip_in=0.1,
    time=[(0, cc - 0.3), (1.35, cc + 1.05)],
    cam=[(0, 1.0, 540, 840), (1.35, 1.05, 540, 840)],
    fx=[('punch', 0.3, 0.05, 0.2), ('flash', 0.32, 0.1, 0.35)],
    ov=[cap('k1', 0.0, 1.35)],
    sfx=[('pop2', 0.0, 0.6), ('select', 0.3), ('ding', 0.5, 0.35)]))
shots[-1]['whip_out'] = 0.1
# 2) Meydanı coştur
h1 = C['hit1']
shots.append(dict(src=r, dur=1.35, whip_in=0.1,
    time=[(0, h1 - 0.35), (1.35, h1 + 1.0)],
    cam=[(0, 1.05, 540, 920), (0.35, 1.45, 540, 740), (1.35, 1.4, 540, 750)],
    fx=[('shake', 0.35, 24, 0.4), ('flash', 0.35, 0.12, 0.6)],
    ov=[cap('k2', 0.0, 1.35)],
    sfx=[('pop2', 0.0, 0.6), ('perfect', 0.35), ('cheer', 0.4), ('applause', 0.6, 0.7)]))
shots[-1]['whip_out'] = 0.1
# 3) Otobüsten simit at
st, sc = C['simit_throw'], C['simit_catch']
shots.append(dict(src=V(C['bus_src']), dur=1.5, whip_in=0.1,
    time=[(0, st - 0.25), (1.5, st + 1.25)],
    cam=[(0, 1.3, 420, 1380), (sc - st + 0.25, 1.5, C['catch_x'], C['catch_y']), (1.5, 1.55, C['catch_x'], C['catch_y'])],
    fx=[('punch', sc - st + 0.25, 0.08, 0.25), ('flash', sc - st + 0.25, 0.1, 0.3)],
    ov=[cap('k3', 0.0, 1.5)],
    sfx=[('pop2', 0.0, 0.6), ('whoosh', 0.25), ('good', sc - st + 0.25), ('applause', sc - st + 0.3, 0.7)]))
shots[-1]['whip_out'] = 0.1
# 4) Basından kaç
ct = C['caught']
shots.append(dict(src=V(C['dodge_src']), dur=1.35, whip_in=0.1,
    time=[(0, ct - 0.45), (1.35, ct + 0.9)],
    cam=[(0, 1.2, 540, C['caught_y'] + 120), (0.45, 1.42, C['caught_x'], C['caught_y']), (1.35, 1.45, C['caught_x'], C['caught_y'])],
    fx=[('shake', 0.45, 26, 0.35), ('flash', 0.45, 0.12, 0.7)],
    ov=[cap('k4', 0.0, 1.35)],
    sfx=[('pop2', 0.0, 0.6), ('tap', 0.15, 0.5), ('camera', 0.45), ('camera', 0.55), ('error', 0.48)]))
shots[-1]['whip_out'] = 0.1
# 5) Canlı yayında gaf yap (asfaltı yedik)
shots.append(dict(src=r, dur=1.6, whip_in=0.1, time=[(0, 7.55), (1.6, 7.95)],
    cam=[(0, 1.1, 540, 1200), (1.6, 1.18, 540, 1250)],
    fx=[('shake', 0.15, 14, 0.3), ('tint', 0.15, 1.6, (40, 40, 200), 0.14)],
    ov=[cap('k5', 0.0, 1.6), dict(img=g('q_asfalt'), u0=0.2, u1=1.6, x=W / 2, y=760, anim='slam', rot=3, out='cut', scale=0.8)],
    sfx=[('pop2', 0.0, 0.6), ('impact', 0.2, 0.8), ('trombone', 0.35, 0.8)]))
shots[-1]['whip_out'] = 0.1
# 6) Seçimi kıl payı al
e0 = C['night_start']
shots.append(dict(src=e, dur=2.0, whip_in=0.1,
    time=[(0, ev - 1.6), (1.0, ev), (2.0, ev + 0.9)],
    cam=[(0, 1.1, 540, 1000), (1.0, 1.25, 540, 1050), (2.0, 1.3, 540, 1040)],
    fx=[('shake', 1.0, 22, 0.4), ('flash', 1.0, 0.14, 0.8)],
    ov=[cap('k6', 0.0, 2.0), dict(img=g('st_kazandi'), u0=1.02, u1=2.0, x=W / 2, y=640, anim='slam', rot=-6, out='cut', scale=0.85)],
    sfx=[('pop2', 0.0, 0.6), ('heart', 0.3, 0.8), ('heart', 0.65, 0.9), ('win', 1.0), ('impact', 1.02, 0.8)]))
# 7) KAPANIŞ
cx = W / 2
shots.append(dict(card=g('end_bg'), dur=2.8,
    ov=[dict(img=g('end_icon'), u0=0.0, u1=9, x=cx, y=470, anim='drop', scale=0.8),
        dict(img=g('end_logo'), u0=0.28, u1=9, x=cx, y=810, anim='slam'),
        dict(img=g('end_sub'), u0=0.5, u1=9, x=cx, y=955, anim='fade'),
        dict(img=g('end_tag'), u0=0.75, u1=9, x=cx, y=1130, anim='rise'),
        dict(img=g('end_store'), u0=1.0, u1=9, x=cx, y=1320, anim='pop', rot=-3, pulse=True),
        dict(img=g('end_handle'), u0=1.2, u1=9, x=cx, y=1430, anim='fade')],
    fx=[('flash', 0.28, 0.12, 0.6)],
    sfx=[('swoosh', 0.0, 0.7), ('impact', 0.28, 0.9), ('sting', 0.3, 0.7), ('pop2', 1.0, 0.6), ('ding', 1.02, 0.4)]))

bw, bh = size('bug')
glob_ov = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in shots) - 2.8, x=30 + bw / 2, y=262, anim='fade', out='cut')]
out = OUT / 'kabine_cikti_TR.mp4'
print(out, round(render(shots, out, glob_ov=glob_ov), 2))
