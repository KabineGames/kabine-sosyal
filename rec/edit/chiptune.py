"""Telifsiz, koddan üretilen chiptune altlık müzik (piksel oyuna uygun).
Kullanım: python3 chiptune.py <süre_sn> <çıktı.wav> [bpm] [seed]"""
import sys, numpy as np
from scipy.io import wavfile
SR = 44100
def note_hz(n): return 440.0 * 2 ** ((n - 69) / 12)
def env(n, a=0.005, r=0.08):
    t = np.arange(n) / SR; e = np.minimum(1, t / a)
    tail = np.clip((n / SR - t) / r, 0, 1); return e * tail
def square(f, n, duty=0.25):
    ph = (np.arange(n) * f / SR) % 1.0; return np.where(ph < duty, 1.0, -1.0)
def tri(f, n):
    ph = (np.arange(n) * f / SR) % 1.0; return 4 * np.abs(ph - 0.5) - 1
def kick(n):
    t = np.arange(n) / SR; f = 150 * np.exp(-t * 30) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)
def hat(n, rng):
    t = np.arange(n) / SR; return rng.uniform(-1, 1, n) * np.exp(-t * 60)
def song(dur, bpm=132, seed=1):
    rng = np.random.default_rng(seed)
    beat = 60 / bpm; step = beat / 2; N = int(dur * SR) + SR
    out = np.zeros((N, 2))
    prog = [(48, [0, 4, 7]), (45, [0, 3, 7]), (41, [0, 4, 7]), (43, [0, 4, 7])]  # C Am F G
    scale = [0, 2, 4, 7, 9, 12, 14, 16]
    nsteps = int(dur / step) + 2
    def add(sig, i, pan=0.0, g=1.0):
        s = int(i * step * SR); e = min(N, s + len(sig))
        out[s:e, 0] += sig[:e - s] * g * (1 - pan); out[s:e, 1] += sig[:e - s] * g * (1 + pan)
    lead = [rng.choice(scale) for _ in range(16)]
    for i in range(nsteps):
        bar = (i // 8) % 4; root, ch = prog[bar]; L = int(step * SR)
        # bas: oktav zıplayan üçgen
        f = note_hz(root - 12 + (12 if i % 2 else 0)); add(tri(f, L) * env(L, r=0.05), i, g=0.32)
        # arpej
        a = root + 24 + ch[i % 3]; add(square(note_hz(a), L // 2, 0.125) * env(L // 2, r=0.04), i, pan=-0.3, g=0.07)
        # melodi (2 adımda bir, 4 barlık motif tekrar)
        if i % 2 == 0:
            m = root + 36 + lead[(i // 2) % 16] - (root - 48)
            if (i // 2) % 8 != 7:
                add(square(note_hz(m), 2 * L, 0.25) * env(2 * L, r=0.12), i, pan=0.25, g=0.075)
        if i % 4 == 0: add(kick(L * 2), i, g=0.55)
        if i % 4 == 2: add(hat(L, rng) * 0.6 + kick(L) * 0.0, i, g=0.18)  # snare yerine gürültü
        add(hat(L // 3, rng), i, pan=0.4, g=0.06)
    out = out[:int(dur * SR)]
    fade = int(0.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    out /= max(1e-9, np.abs(out).max()); return out * 0.9
if __name__ == '__main__':
    dur = float(sys.argv[1]); bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 132
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    wavfile.write(sys.argv[2], SR, (song(dur, bpm, seed) * 32767).astype(np.int16))
