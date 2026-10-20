"""Zürafa A/B reel — KABİNE HABER kurgusu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cv2
from engine import render, W, H

REC = pathlib.Path(__file__).resolve().parent.parent
LANG = sys.argv[1] if len(sys.argv) > 1 else 'tr'
SUF = '' if LANG == 'tr' else '_en'
G = pathlib.Path(__file__).parent / 'gfx' / LANG
OUT = REC.parent / 'cikti' / 'v2'; OUT.mkdir(parents=True, exist_ok=True)


def g(n): return str(G / f'{n}.png')


def size(n):
    im = cv2.imread(g(n), cv2.IMREAD_UNCHANGED); return im.shape[1], im.shape[0]


def lt(n, u0, u1, y=548, sc=0.9):
    w, h = size(n); return dict(img=g(n), u0=u0, u1=u1, x=20 + w * sc / 2, y=y, anim='slide', out='slideL', rot=-1.5, scale=sc)


A = str(REC / f'sess1_0{SUF}'); B = str(REC / f'sess1_1{SUF}')
CLK_A, CLK_B = (3.8, 3.85) if LANG == 'tr' else (3.79, 3.77)
shots = []
# 1) breaking news: the giraffe promise
shots.append(dict(src=A, dur=1.8, time=[(0, 0.85), (1.8, 2.65)],
    cam=[(0, 1.0, 540, 840), (1.8, 1.05, 540, 840)],
    fx=[('flash', 0.0, 0.12, 0.5)],
    ov=[lt('lt_zurafa', 0.0, 1.8)],
    sfx=[('sting', 0.0, 0.8), ('swoosh', 0.02, 0.5)]))
# 2) your move: freeze on the choices, 3-2-1
shots.append(dict(src=A, dur=2.5, time=[(0, 3.4), (2.5, 3.4)],
    cam=[(0, 1.05, 540, 840), (0.25, 1.06, 540, 1000), (2.5, 1.1, 540, 1000)],
    fx=[('punch', 0.0, 0.05, 0.2)],
    ov=[dict(img=g('st_senolsan'), u0=0.0, u1=2.5, x=W / 2, y=470, anim='slam', rot=-6, out='cut', wobble=1.2, scale=0.85),
        dict(img=g('b_a'), u0=0.35, u1=2.5, x=W - 130, y=1120, anim='pop', rot=8, scale=0.8),
        dict(img=g('b_b'), u0=0.5, u1=2.5, x=W - 130, y=1265, anim='pop', rot=-8, scale=0.8),
        dict(img=g('n3'), u0=0.85, u1=1.4, x=W / 2, y=1560, anim='slam', out='shrink'),
        dict(img=g('n2'), u0=1.4, u1=1.95, x=W / 2, y=1560, anim='slam', out='shrink'),
        dict(img=g('n1'), u0=1.95, u1=2.5, x=W / 2, y=1560, anim='slam', out='shrink')],
    sfx=[('impact', 0.0, 0.8), ('pop2', 0.35, 0.6), ('pop2', 0.5, 0.6), ('tick', 0.85), ('tick', 1.4), ('tick', 1.95), ('heart', 0.9, 0.6), ('heart', 1.45, 0.7), ('heart', 2.0, 0.8)]))
# 3) A: two giraffes
shots.append(dict(src=A, dur=2.7, time=[(0, CLK_A - 0.2), (2.7, CLK_A + 2.5)],
    cam=[(0, 1.1, 540, 1000), (0.25, 1.0, 540, 840), (2.7, 1.04, 540, 840)],
    fx=[('flash', 0.2, 0.12, 0.6), ('shake', 0.25, 14, 0.3)],
    ov=[lt('lt_a', 0.3, 2.7)],
    sfx=[('select', 0.2), ('cheer', 0.3), ('applause', 0.5), ('coin', 0.45, 0.7)]))
# 4) rewind: what if B?
shots.append(dict(src=A, dur=0.8, time=[(0, CLK_A + 2.5), (0.8, CLK_A - 0.4)],
    cam=[(0, 1.04, 540, 840), (0.8, 1.08, 540, 1000)],
    fx=[('vhs', 0, 0.8, 0.9)],
    ov=[dict(img=g('rew_b'), u0=0.0, u1=0.8, x=W / 2, y=640, anim='fade', out='cut')],
    sfx=[('rewind', 0.0, 0.85)]))
# 5) B: be realistic
shots.append(dict(src=B, dur=2.7, time=[(0, CLK_B - 0.3), (2.7, CLK_B + 2.4)],
    cam=[(0, 1.08, 540, 1000), (0.3, 1.0, 540, 840), (2.7, 1.04, 540, 840)],
    fx=[('flash', 0.3, 0.12, 0.5), ('tint', 0.6, 2.7, (120, 90, 60), 0.12)],
    ov=[lt('lt_b', 0.4, 2.7)],
    sfx=[('select', 0.3), ('trombone', 0.55, 0.8)]))
# 6) end card: your call
cx = W / 2
shots.append(dict(card=g('end_bg'), dur=2.6,
    ov=[dict(img=g('end_q'), u0=0.0, u1=9, x=cx, y=470, anim='slam'),
        dict(img=g('end_icon'), u0=0.25, u1=9, x=cx, y=860, anim='drop', scale=0.62),
        dict(img=g('end_logo'), u0=0.45, u1=9, x=cx, y=1130, anim='slam', scale=0.82),
        dict(img=g('end_sub'), u0=0.6, u1=9, x=cx, y=1255, anim='fade', scale=0.85),
        dict(img=g('end_ab'), u0=0.85, u1=9, x=cx, y=1460, anim='pop', rot=-2, pulse=True),
        dict(img=g('end_handle'), u0=1.1, u1=9, x=cx, y=1610, anim='fade')],
    fx=[('flash', 0.45, 0.1, 0.5)],
    sfx=[('impact', 0.0, 0.8), ('thud', 0.45), ('sting', 0.46, 0.6), ('pop2', 0.85, 0.6), ('ding', 0.9, 0.4)]))

bw, bh = size('bug')
glob_ov = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in shots) - 2.6, x=30 + bw / 2, y=262, anim='fade', out='cut')]
out = OUT / f'kabine_zurafa_v2_{LANG.upper()}.mp4'
print(out, round(render(shots, out, glob_ov=glob_ov), 2))
