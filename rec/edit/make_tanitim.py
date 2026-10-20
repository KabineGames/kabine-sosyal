"""'Bir siyasetçinin bir haftası' — Kabine tanıtım reel'i, KABİNE HABER kurgusu."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cv2
from engine import render, W, H

REC = pathlib.Path(__file__).resolve().parent.parent
LANG = sys.argv[1] if len(sys.argv) > 1 else 'tr'
SUF = '' if LANG == 'tr' else '_en'
G = pathlib.Path(__file__).parent / 'gfx' / LANG
OUT = REC.parent / 'cikti' / 'v2'
OUT.mkdir(parents=True, exist_ok=True)
cfg = json.loads((pathlib.Path(__file__).parent / f'tanitim_{LANG}.json').read_text())


def g(name): return str(G / f'{name}.png')


def size(name):
    im = cv2.imread(g(name), cv2.IMREAD_UNCHANGED); return im.shape[1], im.shape[0]


TOP, BOT = 548, 1345


def lt(name, u0, u1, y=TOP, sc=0.9):
    w, h = size(name)
    return dict(img=g(name), u0=u0, u1=u1, x=20 + w * sc / 2, y=y, anim='slide', out='slideL', rot=-1.5, scale=sc)


def day(name, u0=0.0, u1=9):
    w, h = size(name)
    return dict(img=g(name), u0=u0, u1=u1, x=W - 36 - w / 2, y=262, anim='pop', out='cut', rot=3)


def V(name): return str(REC / 'v2' / f'{name}{SUF}') if (REC / 'v2' / f'{name}{SUF}').exists() else str(REC / 'v2' / name)


C = cfg
shots = []

# 1) COLD OPEN — the prompter gaffe, live
r = V('rally_fail'); t_trap = C['trap']
shots.append(dict(src=r, dur=1.6,
    time=[(0, t_trap - 0.45), (0.5, t_trap + 0.05), (1.6, t_trap + 0.05)],
    cam=[(0, 1.0, 540, 960), (0.44, 1.06, 540, 900), (0.5, 1.72, 540, 700), (1.6, 1.82, 540, 700)],
    fx=[('shake', 0.47, 34, 0.5), ('flash', 0.46, 0.16, 0.9), ('tint', 0.48, 1.6, (40, 30, 200), 0.22), ('chroma', 0.46, 0.64, 10)],
    ov=[dict(img=g('cap_live'), u0=0.0, u1=0.46, x=W / 2, y=360, anim='pop', out='cut'),
        dict(img=g('gaf'), u0=0.5, u1=1.6, x=W / 2, y=420, anim='slam', rot=-8, out='cut'),
        dict(img=g('q_asfalt'), u0=0.66, u1=1.6, x=W / 2, y=1260, anim='slam', rot=-3, out='cut')],
    sfx=[('tap', 0.05, 0.7), ('tap', 0.42, 0.7), ('error', 0.46), ('scratch', 0.46, 0.9), ('impact', 0.5, 0.8), ('impact', 0.66, 0.6), ('boo', 0.7, 0.9)]))

# 2) REWIND — VHS back to Monday
shots.append(dict(src=r, dur=0.75,
    time=[(0, t_trap + 0.05), (0.75, 1.4)],
    cam=[(0, 1.82, 540, 700), (0.75, 1.0, 540, 960)],
    fx=[('vhs', 0, 0.75, 0.9)],
    ov=[dict(img=g('rew_pzt'), u0=0.0, u1=0.75, x=W / 2, y=760, anim='fade', out='cut')],
    sfx=[('rewind', 0.0, 0.8)]))


def card_beat(name, click, dname, ltname, dur=1.95, lead=0.7):
    s = V(name)
    a = click - lead
    return dict(src=s, dur=dur,
        time=[(0, a), (dur, a + dur)],
        cam=[(0, 1.0, 540, 840), (lead, 1.03, 540, 840), (dur, 1.05, 540, 840)],
        fx=[('punch', lead, 0.05, 0.2), ('flash', lead + 0.02, 0.1, 0.35)],
        ov=[day(dname), lt(ltname, lead + 0.12, dur)],
        sfx=[('pop2', 0.0, 0.5), ('select', lead), ('swoosh', lead + 0.1, 0.6), ('ding', lead + 0.2, 0.35)])


# 3) PAZARTESİ — cat joins the council
shots.append(card_beat('card_town_cat', C['cat_click'], 'd_pzt', 'lt_kedi'))
shots[-1]['whip_out'] = 0.12
# 4) SALI — mom calls
sh = card_beat('card_mom_call', C['mom_click'], 'd_sal', 'lt_anne'); sh['whip_in'] = 0.12; shots.append(sh)

# 5) ÇARŞAMBA — the rally goes wild
h1 = C['hit1']
shots.append(dict(src=r, dur=1.9,
    time=[(0, h1 - 0.75), (1.9, h1 + 1.15)],
    cam=[(0, 1.0, 540, 960), (0.72, 1.12, 540, 900), (0.8, 1.6, 540, 720), (1.9, 1.5, 540, 740)],
    fx=[('shake', 0.75, 26, 0.45), ('flash', 0.75, 0.12, 0.7), ('chroma', 0.75, 0.86, 8)],
    ov=[day('d_car'), lt('lt_miting', 0.95, 1.9, y=BOT)],
    sfx=[('pop2', 0.0, 0.5), ('perfect', 0.75), ('impact', 0.75, 0.7), ('cheer', 0.8), ('applause', 1.0, 0.8)]))
shots[-1]['whip_out'] = 0.12

# 6) PERŞEMBE — ...and then it happened (wide replay of the gaffe)
shots.append(dict(src=r, dur=1.75, whip_in=0.12,
    time=[(0, t_trap - 0.7), (0.75, t_trap + 0.05), (1.75, t_trap + 0.6)],
    cam=[(0, 1.0, 540, 960), (0.7, 1.05, 540, 900), (0.78, 1.45, 540, 720), (1.75, 1.5, 540, 720)],
    fx=[('shake', 0.72, 20, 0.35), ('tint', 0.74, 1.5, (40, 30, 200), 0.15)],
    ov=[day('d_per'), dict(img=g('cap_ohal'), u0=0.0, u1=0.7, x=W / 2, y=420, anim='pop', out='shrink'), lt('lt_gaf', 0.75, 1.75, y=BOT)],
    sfx=[('pop2', 0.0, 0.5), ('heart', 0.1, 0.6), ('error', 0.72), ('trombone', 0.78, 0.55)]))

# 7) CUMA — bus tour: simit lands with auntie, then a flower pot pays the price
b = V(C['bus_src'])
st, sc = C['simit_throw'], C['simit_catch']
shots.append(dict(src=b, dur=2.05,
    time=[(0, st - 0.55), (2.05, st + 1.5)],
    cam=[(0, 1.3, 380, 1420), (0.55, 1.3, 420, 1380), (sc - st + 0.55, 1.5, C['catch_x'], C['catch_y']), (2.05, 1.55, C['catch_x'], C['catch_y'])],
    fx=[('punch', sc - st + 0.55, 0.08, 0.25), ('flash', sc - st + 0.55, 0.1, 0.3)],
    ov=[day('d_cum'), lt('lt_otobus', sc - st + 0.6, 2.05)],
    sfx=[('pop2', 0.0, 0.5), ('whoosh', 0.55), ('good', sc - st + 0.55), ('applause', sc - st + 0.6), ('ding', sc - st + 0.62, 0.35)]))
shots[-1]['whip_out'] = 0.1
pt, pb = C['pot_throw'], C['pot_break']
shots.append(dict(src=b, dur=1.45, whip_in=0.1,
    time=[(0, pt - 0.2), (1.45, pt + 1.25)],
    cam=[(0, 1.25, 500, 1300), (pb - pt + 0.2, 1.45, C['pot_x'], C['pot_y']), (1.45, 1.5, C['pot_x'], C['pot_y'])],
    fx=[('shake', pb - pt + 0.2, 30, 0.4), ('tint', pb - pt + 0.22, 0.9, (40, 30, 210), 0.18)],
    ov=[day('d_cum'), lt('lt_saksi', pb - pt + 0.25, 1.45)],
    sfx=[('whoosh', 0.15), ('splat', pb - pt + 0.2), ('impact', pb - pt + 0.2, 0.6), ('gaffe', pb - pt + 0.3, 0.7)]))

# 8) CUMARTESİ — dodge the press (caught)
d = V(C['dodge_src']); ct = C['caught']
shots.append(dict(src=d, dur=1.85, whip_in=0.1,
    time=[(0, ct - 0.75), (1.85, ct + 1.1)],
    cam=[(0, 1.2, 540, C['caught_y'] + 120), (0.75, 1.42, C['caught_x'], C['caught_y']), (1.85, 1.45, C['caught_x'], C['caught_y'])],
    fx=[('shake', 0.75, 28, 0.4), ('flash', 0.75, 0.12, 0.8)],
    ov=[day('d_cmt'), dict(img=g('st_yorum'), u0=0.78, u1=1.85, x=W / 2, y=1080, anim='slam', rot=-7, out='cut', scale=0.85), lt('lt_basin', 0.82, 1.85)],
    sfx=[('pop2', 0.0, 0.5), ('tap', 0.2, 0.5), ('tap', 0.45, 0.5), ('camera', 0.75), ('camera', 0.85), ('error', 0.78), ('impact', 0.78, 0.6)]))
shots[-1]['whip_out'] = 0.1

# 9) PAZAR — election night, fast-forward to a photo finish
e = V('../sess3_1') if LANG == 'tr' else str(REC / 'sess3_0_en')
e0, ev = C['night_start'], C['verdict']
shots.append(dict(src=e, dur=3.0, whip_in=0.1,
    time=[(0, e0), (1.5, ev - 0.9), (1.9, ev), (3.0, ev + 1.1)],
    cam=[(0, 1.05, 540, 980), (1.5, 1.1, 540, 1000), (1.9, 1.25, 540, 1050), (3.0, 1.3, 540, 1040)],
    fx=[('shake', 1.9, 22, 0.4), ('flash', 1.9, 0.14, 0.8)],
    ov=[day('d_paz'), dict(img=g('st_kazandi'), u0=1.92, u1=3.0, x=W / 2, y=560, anim='slam', rot=-6, out='cut'), lt('lt_secim', 2.0, 3.0, y=BOT)],
    sfx=[('pop2', 0.0, 0.5), ('drum', 0.2, 0.7), ('heart', 0.9, 0.8), ('heart', 1.25, 0.9), ('heart', 1.55, 1.0), ('win', 1.9), ('impact', 1.92, 0.8), ('fanfare', 2.0, 0.8)]))

# 10) END CARD
cx = W / 2
shots.append(dict(card=g('end_bg'), dur=2.4,
    ov=[dict(img=g('end_icon'), u0=0.0, u1=9, x=cx, y=560, anim='drop', scale=0.86),
        dict(img=g('end_logo'), u0=0.28, u1=9, x=cx, y=930, anim='slam'),
        dict(img=g('end_sub'), u0=0.5, u1=9, x=cx, y=1080, anim='fade'),
        dict(img=g('end_tag'), u0=0.75, u1=9, x=cx, y=1290, anim='rise'),
        dict(img=g('end_soon'), u0=1.1, u1=9, x=cx, y=1500, anim='pop', rot=-3, pulse=True),
        dict(img=g('end_handle'), u0=1.25, u1=9, x=cx, y=1640, anim='fade')],
    fx=[('flash', 0.28, 0.12, 0.6)],
    sfx=[('swoosh', 0.0, 0.7), ('thud', 0.3), ('impact', 0.28, 0.9), ('sting', 0.3, 0.7), ('pop2', 1.1, 0.6), ('ding', 1.12, 0.4)]))

bug = g('bug'); bw, bh = size('bug')
glob_ov = [dict(img=bug, u0=0.0, u1=sum(s['dur'] for s in shots) - 2.4, x=30 + bw / 2, y=262, anim='fade', out='cut')]
out = OUT / f'kabine_tanitim_v2_{LANG.upper()}.mp4'
total = render(shots, out, glob_ov=glob_ov)
print(out, round(total, 2))
