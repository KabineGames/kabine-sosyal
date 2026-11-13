"""Reklam v3 — kedi kancası + anlaşılır mini oyunlar (her birinde ne yapıldığı yazar) + CTA.
python3 make_reklam3.py [tr|en] → cikti/v2/reklam_kabine.mp4 / reklam_cabinet_en.mp4. Bayraklı (basın, zirve) ve durağan (bütçe, meclis) mini oyunlar yok."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_hafta3 import g, cap, stamp, whip, size, V, lt, SCR, OUT, W, TOP, C
from engine import render
import make_hafta3
LANG = (sys.argv[1:] or ['tr'])[0]
if LANG == 'en':  # İngilizce kayıtlar (rec2.py/sess5.py KLANG=en) ve zaman kodları
    make_hafta3.G = make_hafta3.G.parent / 'en'
    C = dict(C, bus_src='bus_0_en', simit_throw=18.7, simit_catch=19.15, catch_x=680, catch_y=1200,
             dodge_src='dodge_0_en', caught=2.85, caught_x=640, caught_y=1520)
SUF = '_en' if LANG == 'en' else ''


def build():
    sh = []
    # 1) KANCA: kedi meclis üyesi oldu
    sh.append(dict(src=V('card_town_cat' + SUF), dur=2.3, time=[(0, 1.95), (0.4, 2.1), (2.3, 4.3)],
        cam=[(0, 1.05, 540, 860), (2.3, 1.0, 540, 840)],
        fx=[('flash', 0.0, 0.1, 0.5), ('flash', 0.4, 0.12, 0.6), ('punch', 0.4, 0.06, 0.25)],
        ov=[cap('c_kedi', 0.0, 0.5, y=430), lt('lt_kedi', 0.45, 2.3, TOP)],
        sfx=[('pop2', 0.0, 0.6), ('select', 0.4), ('impact', 0.45, 0.7), ('applause', 0.7, 0.7), ('ding', 1.0, 0.4)]))
    # 2) mini oyunlar
    st, sc = C['simit_throw'], C['simit_catch']
    sh.append(dict(src=V(C['bus_src']), dur=1.8, time=[(0, st - 0.3), (1.0, sc), (1.8, sc + 0.6)],
        cam=[(0, 1.25, 420, 1300), (1.0, 1.45, C['catch_x'], C['catch_y']), (1.8, 1.5, C['catch_x'], C['catch_y'])],
        fx=[('flash', 0, 0.08, 0.4), ('punch', 1.0, 0.08, 0.25)],
        ov=[cap('ad2_15', 0.0, 1.8, y=430, rot=0), cap('i_bus', 0.1, 1.8, y=600)],
        sfx=[('impact', 0.0, 0.7), ('whoosh', 0.3), ('good', 1.0), ('applause', 1.05, 0.6)]))
    ct = C['caught']
    sh.append(dict(src=V(C['dodge_src']), dur=1.6, time=[(0, ct - 1.2), (1.6, ct + 0.4)],
        cam=[(0, 1.1, 540, 1250), (1.6, 1.3, C['caught_x'], C['caught_y'])],
        fx=[('flash', 0, 0.08, 0.4), ('shake', 1.2, 18, 0.3)], ov=[cap('i_dodge', 0.0, 1.6, y=430)],
        sfx=[('pop2', 0.0, 0.6), ('tap', 0.4, 0.5), ('tap', 0.8, 0.5), ('camera', 1.2), ('error', 1.22, 0.6)]))
    for m, a, b, n, d in [('stack', 2.0 if LANG == 'en' else 3.0, 4.4 if LANG == 'en' else 5.4, 'i_stack', 1.6), ('market', 2.0, 4.6, 'i_market', 1.5),
                          ('gala', 1.8, 4.4, 'i_gala', 1.5), ('trend', 3.8, 5.6, 'i_trend', 1.4)]:
        sh.append(dict(src=str(SCR / f'mg_{m}{SUF}'), dur=d, time=[(0, a), (d, b)],
            cam=[(0, 1.08, 540, 1040), (d, 1.14, 540, 1050)], fx=[('flash', 0, 0.08, 0.4)],
            ov=[cap(n, 0.0, d, y=430)], sfx=[('pop2', 0.0, 0.6), ('ding', 0.08, 0.3)]))
    sh[-1]['ov'].append(stamp('r_more', 0.6, 1.4, y=760, rot=-5, sc=0.8))
    whip(sh)
    cx = W / 2
    sh.append(dict(card=g('end_bg'), dur=3.0, fx=[('flash', 0.3, 0.1, 0.5)],
        ov=[dict(img=g('end_icon'), u0=0.0, u1=9, x=cx, y=380, anim='drop', scale=0.55),
            dict(img=g('end_logo'), u0=0.15, u1=9, x=cx, y=620, anim='slam', scale=0.75),
            dict(img=g('ad2_end'), u0=0.3, u1=9, x=cx, y=830, anim='slam', scale=0.85),
            dict(img=g('ad_free'), u0=0.45, u1=9, x=cx, y=1040, anim='pop', rot=-3, pulse=True, scale=1.2),
            dict(img=g('r_ara'), u0=0.6, u1=9, x=cx, y=1180, anim='fade', scale=min(0.95, 820 / size('r_ara')[0])),
            dict(img=g('end_handle'), u0=0.75, u1=9, x=cx, y=1300, anim='fade')],
        sfx=[('impact', 0.0, 0.8), ('thud', 0.15), ('sting', 0.32, 0.6), ('pop2', 0.45, 0.6), ('ding', 0.5, 0.4)]))
    return sh


if __name__ == '__main__':
    sh = build(); bw, _ = size('bug')
    glob = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in sh) - 3.0, x=30 + bw / 2, y=262, anim='fade', out='cut')]
    out = OUT / ('reklam_kabine.mp4' if LANG == 'tr' else 'reklam_cabinet_en.mp4')
    print(out, round(render(sh, out, glob_ov=glob), 2), flush=True)
