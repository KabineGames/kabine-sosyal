"""Reklam videoları (mini oyunlar). Siyaset kelimesi/bayrak/parti adı yok, TikTok-Meta reklam incelemesine uygun.
Kullanım: python3 make_reklam.py a|b   → cikti/v2/reklam_mg_<a|b>.mp4
A ve B sadece ilk saniyedeki kanca yazısıyla ayrılır (A/B testi)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_hafta3 import g, size, cap, stamp, whip, SCR, OUT, W
from engine import render

# (klip, başlangıç, bitiş) — en hareketli anlar; 'frame' (bayrak + parti adı) reklamda yok
CLIPS = [('stack', 3.0, 5.4), ('dodge', 2.6, 4.0), ('bus', 2.0, 4.2), ('trend', 3.8, 5.6),
         ('debate', 3.0, 5.0), ('delegate', 3.3, 5.3), ('poster', 2.5, 5.0)]
NAME = dict(bus='r1', dodge='r2', debate='r3', delegate='r4', poster='r5', stack='r6', trend='r7')


def build(v):
    sh = []
    for i, (m, a, b) in enumerate(CLIPS):
        d = 1.5 if i == 0 else 1.0
        ov = [cap(NAME[m], 0.0, d, y=560 if i == 0 else 430)]
        if i == 0: ov.insert(0, cap('ra_hook' if v == 'a' else 'rb_hook', 0.0, d, y=410, rot=0))
        fx = [('flash', 0, 0.08, 0.4)] + ([('shake', 0.05, 16, 0.25)] if i == 0 else [])
        sh.append(dict(src=str(SCR / f'mg_{m}'), dur=d, time=[(0, a), (d, b)],
                       cam=[(0, 1.1 if i == 0 else 1.08, 540, 1040), (d, 1.14, 540, 1050)],
                       fx=fx, ov=ov, sfx=[('impact' if i == 0 else 'pop2', 0.0, 0.6), ('ding', 0.05, 0.3)]))
    # 've dahası' son mini oyun üstünde
    sh[-1]['ov'].append(stamp('r_more', 0.45, 1.0, y=760, rot=-5, sc=0.8))
    whip(sh)
    cx = W / 2
    sh.append(dict(card=g('end_bg'), dur=2.8, fx=[('flash', 0.35, 0.1, 0.5)],
        ov=[dict(img=g('end_icon'), u0=0.0, u1=9, x=cx, y=430, anim='drop', scale=0.6),
            dict(img=g('end_logo'), u0=0.2, u1=9, x=cx, y=700, anim='slam', scale=0.8),
            dict(img=g('r_end'), u0=0.4, u1=9, x=cx, y=930, anim='slam'),
            dict(img=g('r_ara'), u0=0.3, u1=9, x=cx, y=1170, anim='pop', rot=-3, pulse=True, scale=1.15),
            dict(img=g('end_handle'), u0=0.5, u1=9, x=cx, y=1310, anim='fade')],
        sfx=[('impact', 0.0, 0.8), ('thud', 0.2), ('sting', 0.42, 0.6), ('pop2', 0.7, 0.6), ('ding', 0.75, 0.4)]))
    return sh


if __name__ == '__main__':
    for v in sys.argv[1:]:
        sh = build(v); bw, _ = size('bug')
        glob = [dict(img=g('bug'), u0=0.0, u1=sum(s['dur'] for s in sh) - 2.8, x=30 + bw / 2, y=262, anim='fade', out='cut')]
        out = OUT / f'reklam_mg_{v}.mp4'
        print(out, round(render(sh, out, glob_ov=glob), 2), flush=True)
