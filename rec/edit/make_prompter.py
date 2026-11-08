"""Prompter gafı reel'i — mitingde prompter donar, aday "asfaltı yedik" der, kedi evleriyle toparlar.
Kaynak: rec/v2/rally_fail (events: MANŞETLİK 2.94, GAF 4.34, PROMPTER 5.55, Anlamsız 7.65, KEDİ EVLERİ 11.93, sonuç ~13.3)."""
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


def lt(n, u0, u1, y, sc=0.9):
    w, h = size(n); return dict(img=g(n), u0=u0, u1=u1, x=20 + w * sc / 2, y=y, anim='slide', out='slideL', rot=-1.5, scale=sc)


S = str(REC / 'v2' / f'rally_fail{SUF}') if (REC / 'v2' / f'rally_fail{SUF}').exists() else str(REC / 'v2' / 'rally_fail')
BOT, MID = 1345, 1010
shots = []
# 1) SOĞUK AÇILIŞ: "asfaltı yedik!" anı, ağır çekim
shots.append(dict(src=S, dur=1.5, time=[(0, 7.62), (1.5, 7.95)],
    cam=[(0, 1.12, 540, 1250), (1.5, 1.2, 540, 1300)],
    fx=[('flash', 0.0, 0.1, 0.5), ('chroma', 0.0, 0.25, 6), ('punch', 0.3, 0.06, 0.25)],
    ov=[dict(img=g('cap_live'), u0=0.0, u1=1.5, x=W / 2, y=430, anim='pop', out='cut'),
        dict(img=g('q_asfalt'), u0=0.3, u1=1.5, x=W / 2, y=650, anim='slam', rot=-4, out='cut', wobble=1.0, scale=0.9)],
    sfx=[('swoosh', 0.0, 0.5), ('impact', 0.3, 0.9), ('scratch', 1.3, 0.8)]))
# 2) GERİ SAR: 10 saniye önce
shots.append(dict(src=S, dur=0.7, time=[(0, 7.95), (0.7, 1.6)],
    cam=[(0, 1.2, 540, 1300), (0.7, 1.0, 540, 960)],
    fx=[('vhs', 0, 0.7, 0.9)],
    ov=[dict(img=g('rew_10'), u0=0.0, u1=0.7, x=W / 2, y=640, anim='fade', out='cut')],
    sfx=[('rewind', 0.0, 0.8)]))
# 3) Her şey yolunda: meydan coşuyor
shots.append(dict(src=S, dur=1.6, time=[(0, 1.6), (1.6, 3.2)],
    cam=[(0, 1.0, 540, 960), (1.6, 1.06, 540, 900)],
    fx=[('flash', 1.34, 0.1, 0.35)],
    ov=[lt('lt_miting', 0.25, 1.6, BOT)],
    sfx=[('tap', 0.4, 0.5), ('tap', 0.8, 0.5), ('perfect', 1.34, 0.7), ('cheer', 1.34, 0.8)]))
# 4) GAF: mikrofon düştü
shots.append(dict(src=S, dur=1.6, time=[(0, 4.0), (1.6, 5.4)],
    cam=[(0, 1.06, 540, 900), (0.34, 1.12, 540, 800), (1.6, 1.08, 540, 860)],
    fx=[('shake', 0.34, 16, 0.35), ('flash', 0.34, 0.1, 0.5)],
    ov=[dict(img=g('gaf'), u0=0.34, u1=1.6, x=W / 2, y=440, anim='slam', rot=-8, out='cut'),
        lt('lt_mikrofon', 0.5, 1.6, BOT)],
    sfx=[('thud', 0.34, 0.9), ('gaffe', 0.36, 0.8), ('boo', 0.6, 0.5)]))
# 5) PROMPTER DONDU: sessizlik, tik tak
shots.append(dict(src=S, dur=2.0, time=[(0, 5.45), (2.0, 7.45)],
    cam=[(0, 1.0, 540, 960), (2.0, 1.1, 540, 1250)],
    fx=[('flash', 0.1, 0.1, 0.4), ('tint', 0.1, 2.0, (60, 40, 140), 0.10)],
    ov=[lt('lt_prompter', 0.15, 2.0, MID)],
    sfx=[('error', 0.1, 0.7), ('sting', 0.12, 0.6), ('tick', 0.6), ('tick', 1.0), ('tick', 1.4), ('heart', 1.5, 0.7), ('type', 1.75, 0.6)]))
# 6) PUNCHLINE: "Değerli hemşehrilerim, asfaltı yedik!"
shots.append(dict(src=S, dur=1.7, time=[(0, 7.45), (0.3, 7.62), (1.7, 8.0)],
    cam=[(0, 1.1, 540, 1250), (0.3, 1.18, 540, 1330), (1.7, 1.24, 540, 1340)],
    fx=[('shake', 0.3, 10, 0.3), ('tint', 0.3, 1.7, (40, 40, 200), 0.14), ('chroma', 0.3, 0.6, 5)],
    ov=[dict(img=g('q_asfalt'), u0=0.3, u1=1.7, x=W / 2, y=640, anim='slam', rot=3, out='cut', scale=0.85),
        dict(img=g('st_ne'), u0=0.6, u1=1.7, x=W - 190, y=1050, anim='slam', rot=10, out='cut', wobble=1.0, scale=0.75)],
    sfx=[('impact', 0.3, 0.8), ('trombone', 0.45, 0.9)]))
# 7) TOPARLADI: "Çocuklarımız için KEDİ EVLERİ!"
shots.append(dict(src=S, dur=2.1, time=[(0, 11.2), (2.1, 13.0)],
    cam=[(0, 1.0, 540, 960), (2.0, 1.06, 540, 1000)],
    fx=[('flash', 0.73, 0.1, 0.4), ('punch', 0.73, 0.05, 0.25)],
    ov=[lt('lt_kurtardi', 1.0, 2.0, MID)],
    sfx=[('perfect', 0.73, 0.7), ('cheer', 0.75, 0.9), ('applause', 1.0, 0.7)]))
# 8) SONUÇ: MUHTEŞEM
shots.append(dict(src=S, dur=1.3, time=[(0, 13.4), (1.3, 13.95)],
    cam=[(0, 1.0, 540, 960), (1.3, 1.05, 540, 900)],
    fx=[('flash', 0.0, 0.12, 0.5)],
    sfx=[('fanfare', 0.0, 0.7), ('ding', 0.15, 0.5)]))
# 9) KAPANIŞ
cx = W / 2
shots.append(dict(card=g('end_bg'), dur=2.6,
    ov=[dict(img=g('end_q2'), u0=0.0, u1=9, x=cx, y=470, anim='slam'),
        dict(img=g('end_icon'), u0=0.25, u1=9, x=cx, y=860, anim='drop', scale=0.62),
        dict(img=g('end_logo'), u0=0.45, u1=9, x=cx, y=1130, anim='slam', scale=0.82),
        dict(img=g('end_sub'), u0=0.6, u1=9, x=cx, y=1255, anim='fade', scale=0.85),
        dict(img=g('end_yorum'), u0=0.85, u1=9, x=cx, y=1460, anim='pop', rot=-2, pulse=True),
        dict(img=g('end_handle'), u0=1.1, u1=9, x=cx, y=1610, anim='fade')],
    fx=[('flash', 0.45, 0.1, 0.5)],
    sfx=[('impact', 0.0, 0.8), ('thud', 0.45), ('sting', 0.46, 0.6), ('pop2', 0.85, 0.6), ('ding', 0.9, 0.4)]))

bw, bh = size('bug')
glob_ov = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in shots) - 2.6, x=30 + bw / 2, y=262, anim='fade', out='cut')]
out = OUT / f'kabine_prompter_{LANG.upper()}.mp4'
print(out, round(render(shots, out, glob_ov=glob_ov), 2))
