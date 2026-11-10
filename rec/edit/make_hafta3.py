"""Hafta 3 (10–15 Kasım) videoları. Kullanım: python3 make_hafta3.py <dodge|kart|bus|secim|mg|kedi|all>
Çıktı: cikti/v2/h3_<isim>.mp4 (ham) — yükleme için ayrıca <10 MB'a sıkıştırılır."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cv2
from engine import render, W, H

REC = pathlib.Path(__file__).resolve().parent.parent
G = pathlib.Path(__file__).parent / 'gfx' / 'tr'
OUT = REC.parent / 'cikti' / 'v2'; OUT.mkdir(parents=True, exist_ok=True)
C = json.loads((pathlib.Path(__file__).parent / 'tanitim_tr.json').read_text())
SCR = (REC / 'v2').resolve().parent
BOT, TOP = 1345, 548


def g(n): return str(G / f'{n}.png')
def size(n): im = cv2.imread(g(n), cv2.IMREAD_UNCHANGED); return im.shape[1], im.shape[0]
def V(n): return str(REC / 'v2' / n)
def lt(n, u0, u1, y, sc=0.9):
    w, h = size(n); return dict(img=g(n), u0=u0, u1=u1, x=20 + w * sc / 2, y=y, anim='slide', out='slideL', rot=-1.5, scale=sc)
def cap(n, u0, u1, y=430, rot=-2): return dict(img=g(n), u0=u0, u1=u1, x=W / 2, y=y, anim='pop', out='cut', rot=rot)
def stamp(n, u0, u1, x=W / 2, y=640, rot=-6, sc=1.0): return dict(img=g(n), u0=u0, u1=u1, x=x, y=y, anim='slam', rot=rot, out='cut', wobble=1.0, scale=sc)


def endcard(q, extra=None, dur=2.6):
    cx = W / 2
    ov = [dict(img=g(q), u0=0.0, u1=9, x=cx, y=380, anim='slam'),
          dict(img=g('end_icon'), u0=0.2, u1=9, x=cx, y=680, anim='drop', scale=0.5),
          dict(img=g('end_logo'), u0=0.4, u1=9, x=cx, y=905 if extra else 920, anim='slam', scale=0.7 if extra else 0.78),
          dict(img=g(extra or 'end_sub'), u0=0.55, u1=9, x=cx, y=1075, anim='fade', scale=0.85 if extra else 0.8),
          dict(img=g('end_store'), u0=0.8, u1=9, x=cx, y=1230, anim='pop', rot=-3, pulse=True),
          dict(img=g('end_handle'), u0=1.0, u1=9, x=cx, y=1370, anim='fade')]
    return dict(card=g('end_bg'), dur=dur, ov=ov, fx=[('flash', 0.4, 0.1, 0.5)],
                sfx=[('impact', 0.0, 0.8), ('thud', 0.4), ('sting', 0.42, 0.6), ('pop2', 0.8, 0.6), ('ding', 0.85, 0.4)])


def whip(shots):
    for a, b in zip(shots, shots[1:]):
        if 'card' not in b: a['whip_out'] = 0.1; b['whip_in'] = 0.1


# ---------------------------------------------------------------- 1) Muhabirden Kaç
def dodge():
    s = V('dodge_0'); sh = []
    sh.append(dict(src=s, dur=1.4, time=[(0, 1.55), (1.4, 2.9)], cam=[(0, 1.1, 540, 1450), (1.4, 1.15, 560, 1400)],
        fx=[('flash', 0, 0.1, 0.4)], ov=[cap('h_dodge', 0.0, 1.4)], sfx=[('swoosh', 0, 0.6), ('tap', 0.5, 0.5), ('tap', 0.9, 0.5)]))
    sh.append(dict(src=s, dur=1.6, time=[(0, 2.9), (0.3, 3.1), (1.6, 3.5)], cam=[(0, 1.15, 600, 1450), (0.3, 1.45, C['caught_x'], C['caught_y']), (1.6, 1.4, C['caught_x'], C['caught_y'])],
        fx=[('shake', 0.3, 24, 0.4), ('flash', 0.3, 0.12, 0.7)],
        ov=[stamp('st_yorum', 0.3, 1.6, y=700), lt('lt_yak1', 0.55, 1.6, TOP)],
        sfx=[('camera', 0.3), ('camera', 0.42), ('error', 0.32), ('impact', 0.3, 0.7)]))
    # hızlı sarma: 5.7 ve 7.9'da yeniden yakalanıyor
    sh.append(dict(src=s, dur=1.8, time=[(0, 3.6), (1.8, 8.0)], cam=[(0, 1.0, 540, 980), (1.8, 1.05, 540, 1000)],
        fx=[('flash', 0.86, 0.08, 0.4), ('shake', 0.86, 14, 0.25), ('flash', 1.76, 0.08, 0.5)],
        ov=[stamp('x2', 0.86, 1.76, x=W - 220, y=700, rot=8, sc=0.8)],
        sfx=[('whoosh', 0.0, 0.5), ('camera', 0.86), ('error', 0.88, 0.6), ('camera', 1.76)]))
    sh.append(dict(src=s, dur=1.7, time=[(0, 8.0), (1.7, 9.6)], cam=[(0, 1.05, 540, 1000), (1.7, 1.12, 540, 1050)],
        fx=[('flash', 0.64, 0.1, 0.5), ('tint', 0, 0.5, (40, 40, 200), 0.12)],
        ov=[stamp('x3', 0.0, 0.6, x=W - 220, y=700, rot=8, sc=0.8), lt('lt_gozluk', 0.65, 1.7, TOP)],
        sfx=[('trombone', 0.0, 0.6), ('ding', 0.64, 0.6), ('perfect', 0.66, 0.6)]))
    sh.append(dict(src=s, dur=2.4, time=[(0, 9.6), (1.0, 11.08), (2.4, 12.3)], cam=[(0, 1.0, 540, 980), (1.0, 1.08, 540, 900), (2.4, 1.1, 540, 900)],
        fx=[('flash', 1.0, 0.12, 0.6), ('punch', 1.0, 0.06, 0.25)],
        ov=[lt('lt_araba', 1.0, 2.4, TOP)],
        sfx=[('whoosh', 0.2, 0.5), ('win', 1.0), ('cheer', 1.05, 0.8), ('applause', 1.3, 0.6)]))
    whip(sh); sh.append(endcard('end_dodge'))
    return sh


# ---------------------------------------------------------------- 2) Kriz kartları
def kart():
    sh = []
    cards = [('card_parrot', 'c_papagan', 'b_b', 'lt_papagan', 'trombone'),
             ('card_fountain', 'c_cesme', 'b_a', 'lt_cesme', 'applause'),
             ('card_mom_call', 'c_anne', 'b_b', 'lt_anne', 'heart')]
    for i, (src, c, b, l, s2) in enumerate(cards):
        s = V(src); first = i == 0
        by = 1150 if b == 'b_a' else 1290
        ov = [cap(c, 0.0, 1.9, y=430)]
        if first: ov = [cap('h_kart', 0.0, 0.9, y=430), cap(c, 0.9, 1.9, y=430)]
        ov.append(dict(img=g(b), u0=1.45, u1=1.9, x=W - 150, y=by, anim='pop', out='cut', rot=-8, scale=0.6))
        sh.append(dict(src=s, dur=1.9, time=[(0, 0.75), (1.4, 2.0), (1.9, 2.15)], cam=[(0, 1.0, 540, 840), (1.9, 1.04, 540, 860)],
            fx=[('flash', 0, 0.1, 0.4), ('punch', 1.45, 0.05, 0.2)], ov=ov,
            sfx=[('pop2', 0.0, 0.6), ('tick', 0.6), ('tick', 1.0), ('select', 1.45)]))
        sh.append(dict(src=s, dur=1.9, time=[(0, 2.2), (1.9, 4.6)], cam=[(0, 1.04, 540, 860), (1.9, 1.0, 540, 840)],
            fx=[('flash', 0.3, 0.1, 0.4)], ov=[lt(l, 0.3, 1.9, TOP)],
            sfx=[('ding', 0.3, 0.5), (s2, 0.45, 0.8)]))
    whip(sh); sh.append(endcard('end_kart'))
    return sh


# ---------------------------------------------------------------- 3) Otobüs: simit / saksı
def bus():
    s = V('bus_0'); sh = []
    sh.append(dict(src=s, dur=1.9, time=[(0, 5.9), (0.9, 6.4), (1.9, 7.2)],
        cam=[(0, 1.2, 450, 1300), (0.9, 1.45, C['pot_x'], C['pot_y']), (1.9, 1.35, C['pot_x'], C['pot_y'])],
        fx=[('shake', 0.75, 24, 0.4), ('flash', 0.75, 0.12, 0.7)],
        ov=[cap('h_bus', 0.0, 0.85), lt('lt_saksi', 0.85, 1.9, TOP)],
        sfx=[('whoosh', 0.1, 0.6), ('impact', 0.75, 0.9), ('error', 0.78, 0.6), ('trombone', 1.0, 0.6)]))
    sh.append(dict(src=s, dur=1.8, time=[(0, 9.2), (0.9, 9.85), (1.8, 10.6)], cam=[(0, 1.05, 540, 1200), (1.8, 1.15, 540, 1150)],
        fx=[('flash', 0.85, 0.1, 0.5)], ov=[lt('lt_teyze', 0.85, 1.8, TOP)],
        sfx=[('whoosh', 0.2, 0.5), ('good', 0.85), ('applause', 0.9, 0.6)]))
    sh.append(dict(src=s, dur=1.5, time=[(0, 12.7), (0.4, 13.2), (1.5, 20.5)], cam=[(0, 1.05, 540, 1150), (1.5, 1.0, 540, 1000)],
        fx=[('shake', 0.4, 18, 0.3), ('flash', 0.4, 0.1, 0.5)],
        ov=[stamp('st_yine', 0.4, 1.5, y=700)],
        sfx=[('impact', 0.4, 0.8), ('scratch', 0.5, 0.6), ('whoosh', 0.9, 0.4)]))
    st, sc = C['simit_throw'], C['simit_catch']
    sh.append(dict(src=s, dur=2.2, time=[(0, st - 0.3), (1.0, sc), (2.2, sc + 0.9)],
        cam=[(0, 1.25, 420, 1380), (1.0, 1.5, C['catch_x'], C['catch_y']), (2.2, 1.55, C['catch_x'], C['catch_y'])],
        fx=[('punch', 1.0, 0.08, 0.25), ('flash', 1.0, 0.1, 0.4)],
        ov=[lt('lt_otobus', 1.0, 2.2, TOP)],
        sfx=[('whoosh', 0.3), ('good', 1.0), ('cheer', 1.05, 0.8), ('applause', 1.2, 0.7)]))
    whip(sh); sh.append(endcard('end_bus'))
    return sh


# ---------------------------------------------------------------- 4) Seçim gecesi kıl payı
def secim():
    e = str(SCR / 'sess3_1'); n0, v = C['night_start'], C['verdict']; sh = []
    sh.append(dict(src=e, dur=1.6, time=[(0, n0), (1.6, 2.4)], cam=[(0, 1.15, 540, 1000), (1.6, 1.1, 540, 1000)],
        fx=[('flash', 0, 0.12, 0.6)], ov=[cap('h_secim', 0.0, 1.6, y=430)], sfx=[('swoosh', 0, 0.6), ('heart', 0.6, 0.7), ('heart', 1.1, 0.7)]))
    sh.append(dict(src=e, dur=1.8, time=[(0, 2.4), (1.8, 7.4)], cam=[(0, 1.1, 540, 1000), (1.8, 1.3, 540, 1060)],
        fx=[('tint', 0, 1.8, (40, 40, 200), 0.10)], ov=[stamp('st_basabas', 0.3, 1.8, y=480, rot=-4, sc=0.85)],
        sfx=[('impact', 0.3, 0.7), ('heart', 0.6), ('heart', 0.95), ('heart', 1.3), ('heart', 1.6)]))
    sh.append(dict(src=e, dur=1.6, time=[(0, 7.4), (1.6, v - 0.05)], cam=[(0, 1.3, 540, 1060), (1.6, 1.45, 540, 1060)],
        fx=[('chroma', 1.2, 0.4, 4)], sfx=[('tick', 0.2), ('tick', 0.6), ('heart', 1.0, 0.9), ('heart', 1.3, 1.0)]))
    sh.append(dict(src=e, dur=2.1, time=[(0, v), (2.1, v + 1.6)], cam=[(0, 1.2, 540, 1050), (2.1, 1.1, 540, 1050)],
        fx=[('shake', 0.0, 24, 0.4), ('flash', 0.0, 0.14, 0.9)],
        ov=[stamp('st_kazandi', 0.02, 2.1, y=480, sc=0.85), lt('lt_secim', 0.5, 2.1, BOT)],
        sfx=[('win', 0.0), ('impact', 0.02, 0.8), ('cheer', 0.1, 0.9), ('fanfare', 0.2, 0.6)]))
    whip(sh); sh.append(endcard('end_secim'))
    return sh


# ---------------------------------------------------------------- 5) 8 mini oyun
def mg():
    clips = [('bus', 2.0, 4.2), ('dodge', 2.6, 4.0), ('debate', 3.0, 5.0), ('delegate', 2.5, 4.7),
             ('poster', 2.5, 5.0), ('stack', 3.0, 5.4), ('trend', 3.8, 5.6), ('frame', 2.8, 4.5)]
    sh = []
    for i, (m, a, b) in enumerate(clips):
        d = 1.35 if i == 0 else 1.15
        ov = [cap(f'm{i + 1}', 0.0, d, y=570 if i == 0 else 430)]
        if i == 0: ov.insert(0, cap('h_mg', 0.0, d, y=420, rot=0))
        sh.append(dict(src=str(SCR / f'mg_{m}'), dur=d, time=[(0, a), (d, b)], cam=[(0, 1.0, 540, 960), (d, 1.06, 540, 980)],
            fx=[('flash', 0, 0.08, 0.4)], ov=ov, sfx=[('pop2', 0.0, 0.6), ('ding', 0.05, 0.3)]))
    whip(sh); sh.append(endcard('end_mg'))
    return sh


# ---------------------------------------------------------------- 6) Kedi A/B
def kedi():
    s = V('card_town_cat'); sh = []
    sh.append(dict(src=s, dur=1.8, time=[(0, 0.75), (1.8, 2.0)], cam=[(0, 1.0, 540, 840), (1.8, 1.03, 540, 850)],
        fx=[('flash', 0, 0.1, 0.4)],
        ov=[cap('c_kedi', 0.0, 1.8), dict(img=g('b_a'), u0=1.0, u1=9, x=W - 150, y=1150, anim='pop', out='cut', scale=0.5),
            dict(img=g('b_b'), u0=1.2, u1=9, x=W - 150, y=1290, anim='pop', out='cut', scale=0.5)],
        sfx=[('pop2', 0, 0.6), ('pop2', 1.0, 0.4), ('pop2', 1.2, 0.4)]))
    sh.append(dict(src=s, dur=1.8, time=[(0, 2.0), (1.8, 2.06)], cam=[(0, 1.03, 540, 850), (1.8, 1.05, 540, 860)],
        ov=[cap('cap_ab', 0.0, 1.8, y=430), stamp('n3', 0.0, 0.6, y=600, sc=0.4), stamp('n2', 0.6, 1.2, y=600, sc=0.4), stamp('n1', 1.2, 1.8, y=600, sc=0.4),
            dict(img=g('b_a'), u0=0, u1=1.8, x=W - 150, y=1150, anim='fade', out='cut', scale=0.5),
            dict(img=g('b_b'), u0=0, u1=1.8, x=W - 150, y=1290, anim='fade', out='cut', scale=0.5)],
        sfx=[('tick', 0.0), ('tick', 0.6), ('tick', 1.2), ('heart', 1.5, 0.7)]))
    sh.append(dict(src=s, dur=2.3, time=[(0, 2.1), (2.3, 4.7)], cam=[(0, 1.05, 540, 860), (2.3, 1.0, 540, 840)],
        fx=[('flash', 0.0, 0.12, 0.6), ('punch', 0.0, 0.06, 0.25)],
        ov=[stamp('b_b', 0.0, 0.5, x=W - 150, y=1290, rot=-8, sc=0.7), lt('lt_kedi', 0.4, 2.3, TOP)],
        sfx=[('select', 0.0), ('impact', 0.05, 0.6), ('ding', 0.4, 0.5), ('applause', 0.6, 0.7)]))
    whip(sh); sh.append(endcard('end_q', extra='end_ab', dur=2.8))
    return sh


VIDS = dict(dodge=dodge, kart=kart, bus=bus, secim=secim, mg=mg, kedi=kedi)
if __name__ == '__main__':
    for n in (VIDS if sys.argv[1] == 'all' else sys.argv[1:]):
        sh = VIDS[n](); bw, _ = size('bug')
        glob = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in sh) - sh[-1]['dur'], x=30 + bw / 2, y=262, anim='fade', out='cut')]
        out = OUT / f'h3_{n}.mp4'
        print(out, round(render(sh, out, glob_ov=glob), 2), flush=True)
