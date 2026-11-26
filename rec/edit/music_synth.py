"""128 BPM sentetik trailer ritmi (telifsiz). python3 music_synth.py out.wav sure_sn drop_sn"""
import sys, wave, numpy as np
SR = 44100
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR; return np.minimum(t / a, 1) * np.exp(-t / d)
def kick(): n = int(.35 * SR); t = np.arange(n) / SR; f = 150 * np.exp(-t * 18) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .22)
def clap(): n = int(.2 * SR); return np.random.RandomState(1).randn(n) * env(n, .001, .06) * .5
def hat(): n = int(.05 * SR); x = np.random.RandomState(2).randn(n); x = np.diff(np.r_[0, x]); return x * env(n, .0005, .012) * .25
def bass(f, dur): n = int(dur * SR); t = np.arange(n) / SR; x = np.sign(np.sin(2 * np.pi * f * t)) * .5 + np.sin(2 * np.pi * f * t) * .5; return x * env(n, .005, dur * .6) * .32
def lead(f, dur): n = int(dur * SR); t = np.arange(n) / SR; x = (2 * ((f * t) % 1) - 1); return x * env(n, .004, dur * .5) * .1
def build(total, drop):
    b = 60 / 128; out = np.zeros(int((total + 1) * SR))
    def add(x, at, g=1.0):
        i = int(at * SR); j = min(len(out), i + len(x)); out[i:j] += x[:j - i] * g
    roots = [55, 55, 65.41, 49]; mel = [440, 523.25, 659.25, 587.33, 523.25, 440, 392, 440]
    k = 0; t = 0.0
    while t < total:
        pre = drop - 1.9 < t < drop  # riser bölümü: sadece hızlanan trampet
        if not pre:
            add(kick(), t)
            if k % 2 == 1: add(clap(), t)
            add(bass(roots[(k // 4) % 4] * (2 if t >= drop else 1), b * .9), t)
            if t >= drop or k >= 4: add(lead(mel[k % 8], b * .45), t); add(lead(mel[(k + 3) % 8] * 1.5, b * .4), t + b / 2, .7)
        else:
            sub = 2 if t < drop - 1 else 4
            for q in range(sub): add(clap() * (.4 + .6 * (t - drop + 1.9) / 1.9), t + q * b / sub)
        add(hat(), t + b / 2); add(hat(), t, .6)
        t += b; k += 1
    # riser gürültü
    n = int(1.9 * SR); add(np.random.RandomState(3).randn(n) * np.linspace(0, .22, n), drop - 1.9)
    out = out[:int(total * SR)]; fade = int(.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)
    out /= np.abs(out).max() + 1e-9; return (out * .85 * 32767).astype(np.int16)
if __name__ == '__main__':
    o, total, drop = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    a = build(total, drop); st = np.stack([a, a], 1)
    with wave.open(o, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
