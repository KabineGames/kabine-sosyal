"""Editor sound effects synthesized with numpy (no downloads): impact, whoosh, scratch, rewind, sad trombone, sting, riser."""
import numpy as np
from scipy import signal

SR = 44100


def _t(d):
    return np.arange(int(d * SR)) / SR


def _env(n, a=0.005, r=None, curve=4.0):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    dec = np.exp(-curve * t / (r if r else n / SR))
    return att * dec


def _bp(x, lo, hi):
    b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return signal.lfilter(b, a, x)


def _lp(x, f):
    b, a = signal.butter(2, f / (SR / 2), 'low')
    return signal.lfilter(b, a, x)


def norm(x, peak=0.9):
    m = np.abs(x).max() or 1
    return x / m * peak


def impact(d=0.55):
    t = _t(d)
    f = 110 * np.exp(-t * 7) + 38
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 6.5)
    click = _bp(np.random.randn(len(t)), 900, 6000) * np.exp(-t * 60) * 0.6
    rumble = _lp(np.random.randn(len(t)), 220) * np.exp(-t * 5) * 1.4
    return norm(body * 1.2 + click + rumble)


def whoosh(d=0.32, lo=400, hi=4200):
    n = int(d * SR); x = np.random.randn(n)
    out = np.zeros(n); seg = 512
    for i in range(0, n, seg):
        p = i / n; fc = lo + (hi - lo) * np.sin(np.pi * p) ** 1.5
        out[i:i + seg] = _bp(x[i:i + seg + 0], max(80, fc * 0.6), min(SR / 2 - 100, fc * 1.4))[:len(out[i:i + seg])]
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return norm(out * env)


def scratch(d=0.42):
    t = _t(d)
    f = 520 + 420 * np.sin(2 * np.pi * 7.5 * t) * np.exp(-t * 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = signal.sawtooth(ph) * 0.5
    nz = _bp(np.random.randn(len(t)), 700, 3500)
    mod = np.abs(np.sin(2 * np.pi * 7.5 * t)) ** 0.5
    return norm((saw + nz * 0.8) * mod * np.exp(-t * 3))


def rewind(d=0.7):
    t = _t(d)
    f = 300 + 2400 * (t / d) ** 1.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = signal.sawtooth(ph) * 0.35
    chirp = np.sin(2 * np.pi * 18 * t) > 0.2
    nz = _bp(np.random.randn(len(t)), 1500, 7000) * 0.4
    env = np.clip(t / 0.05, 0, 1) * np.clip((d - t) / 0.08, 0, 1)
    return norm(_lp((tone * chirp + nz) * env, 7000))


def trombone(base=196.0):
    notes = [(base, 0.32), (base * 0.944, 0.32), (base * 0.891, 0.32), (base * 0.841, 1.05)]
    out = []
    for i, (f0, d) in enumerate(notes):
        t = _t(d)
        vib = 1 + (0.025 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.3, 0, 1) if i == 3 else 0)
        f = f0 * vib * (1 - 0.06 * t / d if i == 3 else 1)
        ph = 2 * np.pi * np.cumsum(f) / SR
        x = signal.sawtooth(ph) * 0.6 + np.sin(ph * 2) * 0.25
        x = _lp(x, 1400)
        env = np.clip(t / 0.03, 0, 1) * np.clip((d - t) / 0.06, 0, 1)
        out.append(x * env)
    return norm(np.concatenate(out), 0.75)


def sting(d=0.9):
    t = _t(d); out = np.zeros(len(t))
    for f in (523.25, 659.25, 783.99, 1046.5):
        out += signal.square(2 * np.pi * f * t) * 0.18 * np.exp(-t * 3.2)
    out = _lp(out, 5000)
    tim = np.sin(2 * np.pi * (90 * np.exp(-t * 3) + 50) * t) * np.exp(-t * 5) * 0.8
    return norm(out + tim)


def riser(d=0.8):
    t = _t(d)
    nz = np.random.randn(len(t))
    out = np.zeros(len(t)); seg = 1024
    for i in range(0, len(t), seg):
        fc = 300 + 6000 * (i / len(t)) ** 2
        out[i:i + seg] = _bp(nz[i:i + seg], max(80, fc * 0.7), min(SR / 2 - 100, fc * 1.3))[:len(out[i:i + seg])]
    return norm(out * (t / d) ** 1.5)


def pop():
    t = _t(0.09)
    f = 900 * np.exp(-t * 30) + 300
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40))


def ding():
    t = _t(0.8)
    x = np.sin(2 * np.pi * 1760 * t) + 0.5 * np.sin(2 * np.pi * 2640 * t) + 0.25 * np.sin(2 * np.pi * 3520 * t)
    return norm(x * np.exp(-t * 5), 0.6)


def tick_tock(n=3, gap=0.5):
    out = np.zeros(int(n * gap * SR) + 2000)
    for i in range(n):
        t = _t(0.05); f = 1800 if i % 2 == 0 else 1300
        s = np.sin(2 * np.pi * f * t) * np.exp(-t * 90)
        k = int(i * gap * SR); out[k:k + len(s)] += s
    return norm(out, 0.6)


SYNTH = dict(impact=impact, swoosh=whoosh, scratch=scratch, rewind=rewind, trombone=trombone, sting=sting, riser=riser, pop2=pop, ding=ding, ticktock=tick_tock)
