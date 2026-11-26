"""Brezilya (PT-BR) Shorts. Kullanım: python3 make_br.py dodge kart -> cikti/br/br_<isim>.mp4"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import make_hafta3 as M
from engine import render, W
HERE = pathlib.Path(__file__).parent
M.G = HERE / 'gfx' / 'pt'
M.V = lambda n: str(M.REC / 'v2' / (n + '_pt'))
OUT = M.REC.parent / 'cikti' / 'br'; OUT.mkdir(parents=True, exist_ok=True)
cap, lt, stamp, endcard, whip, TOP, BOT = M.cap, M.lt, M.stamp, M.endcard, M.whip, M.TOP, M.BOT


def dodge():
    s = M.V('dodge_3'); sh = []
    sh.append(dict(src=s, dur=2.4, time=[(0, 5.05), (1.3, 5.6), (1.8, 6.0), (2.4, 6.5)], cam=[(0, 1.3, 540, 1330), (1.3, 1.4, 535, 1380), (1.8, 1.5, 530, 1420), (2.4, 1.48, 530, 1420)],
        fx=[('flash', 0, 0.1, 0.4), ('shake', 1.8, 24, 0.4), ('flash', 1.8, 0.12, 0.7)],
        ov=[cap('h_dodge', 0.0, 1.75), lt('lt_yak1', 1.8, 2.4, TOP)],
        sfx=[('swoosh', 0, 0.6), ('tap', 0.5, 0.5), ('camera', 1.8), ('camera', 1.92), ('error', 1.82), ('impact', 1.8, 0.7)]))
    sh.append(dict(src=s, dur=1.6, time=[(0, 6.6), (1.6, 10.9)], cam=[(0, 1.0, 540, 1000), (1.5, 1.05, 540, 1000)],
        fx=[('flash', 1.4, 0.08, 0.4)], sfx=[('whoosh', 0.0, 0.5), ('tap', 0.5, 0.4), ('tap', 0.9, 0.4)]))
    sh.append(dict(src=s, dur=1.2, time=[(0, 12.1), (1.2, 12.9)], cam=[(0, 1.1, 540, 900), (1.2, 1.15, 540, 880)],
        fx=[('flash', 0.3, 0.1, 0.5), ('tint', 0, 0.3, (40, 40, 200), 0.12)],
        ov=[lt('lt_gozluk', 0.05, 1.2, TOP)], sfx=[('ding', 0.3, 0.6), ('perfect', 0.32, 0.6)]))
    sh.append(dict(src=s, dur=2.0, time=[(0, 12.9), (1.2, 14.05), (2.0, 14.5)], cam=[(0, 1.15, 540, 880), (1.2, 1.18, 540, 760), (2.0, 1.22, 540, 760)],
        fx=[('flash', 1.2, 0.12, 0.6), ('punch', 1.2, 0.06, 0.25)],
        ov=[lt('lt_araba', 1.2, 2.0, TOP)],
        sfx=[('whoosh', 0.2, 0.5), ('win', 1.2), ('cheer', 1.25, 0.8), ('applause', 1.5, 0.6)]))
    whip(sh); sh.append(endcard('end_dodge', dur=2.2))
    return sh


def fix_lt(sh):
    for x in sh:
        for o in x.get('ov', []):
            if o.pop('keep', 0):  # oyunun kesik altyazısını ört
                o['y'] = 845; o['scale'] = 1.08; w, _ = M.size(pathlib.Path(o['img']).stem); o['x'] = W / 2; o['rot'] = 0
            elif '/lt_' in o.get('img', ''):
                o['y'] = 440; o['scale'] = 0.62; w, _ = M.size(pathlib.Path(o['img']).stem); o['x'] = 20 + w * 0.62 / 2
    return sh


def big_sub(sh):
    for o in sh[0].get('ov', []):
        if '/h_' in o.get('img', ''): o['anim'] = 'cut'
    for o in sh[-1].get('ov', []):
        o['u0'] = min(o['u0'], 0.15)
        if o.get('img', '').endswith('end_sub.png'): o['scale'] = 1.05
    return sh


def kart():
    sh = M.kart()
    for x in sh:
        if 'cam' in x and 'card' not in x: x['cam'] = [(t, z * 1.06, cx, cy + 40) for t, z, cx, cy in x['cam']]
    sh[-1] = endcard('end_kart', extra='end_ab', dur=2.4)
    return fix_lt(sh)


VIDS = dict(dodge=lambda: big_sub(fix_lt(dodge())), kart=lambda: big_sub(kart()))
# ---------------------------------------------------------------- TRAILER (reklam montajı)
B = 60 / 128
def mg(n): return str(M.REC / f'mg_{n}_pt')
def pill(n, u0, u1): w, _ = M.size(n); return dict(img=M.g(n), u0=u0, u1=u1, x=30 + w * 1.0 / 2, y=372, anim='slam', out='cut', scale=1.0)
CLIPS = [('konvoy', mg('konvoy'), 5.6, 8.6, (1.08, 540, 900)), ('stack', mg('stack'), 3.0, 5.8, (1.0, 540, 900)),
         ('frame', mg('frame'), 3.8, 6.4, (1.25, 540, 1150)),
         None,
         ('dodge', M.V('dodge_3'), 5.2, 6.6, (1.55, 532, 1420)), ('summit', mg('summit'), 3.0, 6.0, (1.2, 540, 1000)),
         ('trend', mg('trend'), 5.6, 7.4, (1.1, 540, 1150)), ('debate', mg('debate'), 4.2, 6.0, (1.2, 540, 820)),
         ('bus', M.V('bus_0'), 9.0, 10.6, (1.15, 540, 1000))]
LADDER = {0: 'lad1', 4: 'lad2', 6: 'lad3'}
CAPY = {'trend': 1250}
MORE = [('parliament', 4.0, 6.0), ('poster', 5.0, 7.5), ('bus', 5.6, 7.4), ('gala', 2.4, 3.4)]


def trailer(hook):
    sh = []
    band = dict(img=str(M.G / 'band.png'), u0=0, u1=B, x=540, y=520, anim='cut', out='cut')
    hk = [('rally', mg('rally'), 4.0, 4.8, (1.3, 540, 1180)), ('konvoy', mg('konvoy'), 6.2, 7.2, (1.08, 540, 900)),
          ('stack', mg('stack'), 4.6, 5.8, (1.0, 540, 900)), ('rally', mg('rally'), 4.9, 5.6, (1.35, 540, 1200))]
    for k, (n, src, a, b, (z, cx, cy)) in enumerate(hk):
        ov = [band, dict(M.cap(hook, 0.0, B, y=520, rot=-2), anim='cut')]
        if k >= 2: ov.append(dict(pill('lad1', 0, B), anim='slam' if k == 2 else 'cut'))
        sh.append(dict(src=src, dur=B, time=[(0, a), (B, b)], cam=[(0, z, cx, cy), (B, z * 1.05, cx, cy)],
            fx=[('flash', 0, 0.05, 0.4)], ov=ov, sfx=[('impact', 0.0, 0.5 if k else 0.8)] + ([('gaffe', 0.05, 0.6)] if k == 3 else [])))
    lad = 'lad1'
    for i, c in enumerate(CLIPS):
        if c is None:
            for j, (n, a, b) in enumerate(MORE):
                ov = [dict(M.stamp('v_more', 0.0, B, y=900, sc=0.82), anim='slam' if j == 0 else 'cut'), dict(pill(lad, 0, B), anim='cut')]
                sh.append(dict(src=mg(n), dur=B, time=[(0, a), (B, b)], cam=[(0, 1.0, 540, 960), (B, 1.05, 540, 960)],
                    fx=[('flash', 0, 0.05, 0.5)], ov=ov, sfx=[('tick', 0.0, 0.6)] + ([('impact', 0.0, 0.6)] if j == 0 else [])))
            continue
        n, src, a, b, (z, cx, cy) = c
        d = 2 * B; up = i in LADDER and i > 0
        if i in LADDER: lad = LADDER[i]
        ov = [M.cap('v_' + n, 0.0, d, y=CAPY.get(n, 560), rot=-2), dict(pill(lad, 0.0, d), anim='slam' if up else 'cut')]
        sh.append(dict(src=src, dur=d, time=[(0, a), (d, b)], cam=[(0, z, cx, cy), (d, z * 1.06, cx, cy)],
            fx=[('flash', 0, 0.06, 0.35)] + ([('punch', 0, 0.06, 0.2)] if up else []), ov=ov,
            sfx=[('whoosh', 0.0, 0.35)] + ([('level', 0.0, 0.7)] if up else [])))
    e = str(M.REC / 'sess3_0_pt')
    sh.append(dict(src=e, dur=4 * B, time=[(0, 8.2), (B, 8.75), (4 * B, 10.4)], cam=[(0, 1.25, 540, 900), (4 * B, 1.25, 540, 900)],
        fx=[('flash', B, 0.14, 0.9), ('shake', B, 26, 0.45)],
        ov=[dict(pill(lad, 0, B), anim='cut'), pill('lad4', B, 4 * B), M.stamp('st_pres', B, 4 * B, y=800, rot=-4, sc=0.78),
            dict(img=str(M.G / 'patch504.png'), u0=0.0, u1=4 * B, x=190, y=1172, anim='cut', out='cut'),
            dict(img=M.g('end_store'), u0=B + 0.35, u1=4 * B, x=540, y=1330, anim='pop', out='cut')],
        sfx=[('heart', 0.0, 0.8), ('win', B), ('cheer', B + 0.05, 0.9), ('fanfare', B + 0.1, 0.6)]))
    M.whip(sh); sh.append(endcard('end_tr', extra='end_18', dur=2.0))
    return big_sub(sh)


def drop_time(sh):
    return sum(x['dur'] for x in sh[:-2]) + B
VIDS['trA'] = lambda: trailer('hA')
VIDS['trB'] = lambda: trailer('hB')


if __name__ == '__main__':
    for n in sys.argv[1:]:
        sh = VIDS[n](); bw, _ = M.size('bug')
        glob = [dict(img=M.g('bug'), u0=0.0, u1=sum(x['dur'] for x in sh) - sh[-1]['dur'], x=30 + bw / 2, y=262, anim='fade', out='cut')]
        out = OUT / f'br_{n}.mp4'
        print(out, round(render(sh, out, glob_ov=glob), 2), flush=True)
        if n.startswith('tr'):
            import subprocess
            tot = sum(x['dur'] for x in sh); mus = OUT / 'music.wav'
            subprocess.run(['python3', str(HERE / 'music_synth.py'), str(mus), str(tot), str(drop_time(sh))], check=True)
            fin = OUT / f'br_{n}_m.mp4'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(out), '-i', str(mus), '-filter_complex',
                '[1:a]volume=0.55[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', str(fin)], check=True)
            print(fin)


