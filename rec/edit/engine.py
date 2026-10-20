"""Tiny motion-graphics compositor for Kabine reels.

A reel is a list of shots. Each shot pulls frames from a recorded screencast (timestamped jpgs),
remaps time (speed ramps, freezes, rewinds), moves a virtual camera (zoom/pan with easing),
applies effects (shake, flash, chroma split, VHS, red tint, whip transitions) and composites
animated overlay graphics. Audio is mixed from game SFX + synthesized SFX on the same timeline.
"""
import json, math, pathlib, subprocess, wave, random
import numpy as np
import cv2

W, H, FPS, SR = 1080, 1920, 30, 44100
REC = pathlib.Path(__file__).resolve().parent.parent
SFX_DIR = REC / 'sfx'


# ---------------------------------------------------------------- sources
class Source:
    def __init__(self, d):
        self.dir = pathlib.Path(d)
        meta = json.loads((self.dir / 'frames.json').read_text())
        t0 = meta['t0']
        self.ts = np.array([f[0] - t0 for f in meta['frames']])
        self.names = [f[1] for f in meta['frames']]
        self.cache = {}

    def frame(self, t):
        i = int(np.searchsorted(self.ts, t, side='right') - 1)
        i = max(0, min(i, len(self.names) - 1))
        if i not in self.cache:
            if len(self.cache) > 90:
                self.cache.pop(next(iter(self.cache)))
            im = cv2.imread(str(self.dir / self.names[i]), cv2.IMREAD_COLOR)
            if im.shape[1] != W or im.shape[0] != H:
                im = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
            self.cache[i] = im
        return self.cache[i]


_SOURCES = {}


def src(d):
    d = str(d)
    if d not in _SOURCES:
        _SOURCES[d] = Source(d)
    return _SOURCES[d]


# ---------------------------------------------------------------- easing / interpolation
def smooth(x):
    x = min(1, max(0, x)); return x * x * (3 - 2 * x)


def ease_out_cubic(x):
    x = min(1, max(0, x)); return 1 - (1 - x) ** 3


def ease_out_back(x, k=1.9):
    x = min(1, max(0, x)); return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2


def interp(keys, u, ease=smooth):
    """keys: [(u, v...)] -> tuple v at u with eased segments."""
    if u <= keys[0][0]: return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= u <= b[0]:
            f = ease((u - a[0]) / max(1e-6, b[0] - a[0]))
            return tuple(x + (y - x) * f for x, y in zip(a[1:], b[1:]))
    return keys[-1][1:]


def lin(keys, u):
    return interp(keys, u, ease=lambda x: min(1, max(0, x)))[0]


# ---------------------------------------------------------------- overlays
_IMG = {}


def load_rgba(p):
    p = str(p)
    if p not in _IMG:
        im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        if im.shape[2] == 3:
            im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
        _IMG[p] = im
    return _IMG[p]


def paste(frame, img, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.003 or scale <= 0.01: return
    h, w = img.shape[:2]
    if abs(scale - 1) > 1e-3 or abs(rot) > 1e-3:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
        cos, sin = abs(M[0, 0]), abs(M[0, 1])
        nw, nh = int(h * sin + w * cos) + 2, int(h * cos + w * sin) + 2
        M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
        img = cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        h, w = nh, nw
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if fx1 <= fx0 or fy1 <= fy0: return
    sub = img[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
    a = sub[:, :, 3:4].astype(np.float32) / 255.0 * alpha
    reg = frame[fy0:fy1, fx0:fx1].astype(np.float32)
    frame[fy0:fy1, fx0:fx1] = (reg * (1 - a) + sub[:, :, :3].astype(np.float32) * a).astype(np.uint8)


def overlay_state(o, u):
    """o: dict(img, u0, u1, x, y, rot, anim, out, scale). returns (cx, cy, scale, rot, alpha) or None."""
    u0, u1 = o['u0'], o.get('u1', 1e9)
    if u < u0 or u > u1: return None
    k = u - u0; x, y, s, r, a = o['x'], o['y'], o.get('scale', 1.0), o.get('rot', 0.0), 1.0
    anim = o.get('anim', 'pop')
    if anim == 'slam':
        d = 0.17
        if k < d: s *= 2.3 - 1.36 * ease_out_cubic(k / d); a = min(1, k / 0.05)
        elif k < d + 0.09: s *= 0.94 + 0.06 * smooth((k - d) / 0.09)
    elif anim == 'pop':
        if k < 0.22: s *= 0.35 + 0.65 * ease_out_back(k / 0.22, 2.6); a = min(1, k / 0.06)
    elif anim == 'slide':
        if k < 0.24: x = x - 1250 * (1 - ease_out_back(k / 0.24, 1.2))
    elif anim == 'slideR':
        if k < 0.24: x = x + 1250 * (1 - ease_out_back(k / 0.24, 1.2))
    elif anim == 'drop':
        if k < 0.32: y = y - 900 * (1 - ease_out_back(k / 0.32, 1.6))
    elif anim == 'rise':
        if k < 0.26: y = y + 500 * (1 - ease_out_cubic(k / 0.26)); a = min(1, k / 0.12)
    elif anim == 'fade':
        a = min(1, k / 0.15)
    if o.get('wobble'):
        r += math.sin(u * 9) * o['wobble']
    if o.get('pulse'):
        s *= 1 + 0.04 * math.sin(u * 10)
    out = o.get('out', 'cut'); rem = u1 - u
    if out == 'fade' and rem < 0.12: a *= rem / 0.12
    elif out == 'shrink' and rem < 0.1: s *= max(0.05, rem / 0.1)
    elif out == 'slideL' and rem < 0.14: x -= 1250 * (1 - rem / 0.14) ** 2
    return x, y, s, r, a


# ---------------------------------------------------------------- effects
def camera(frame, zoom, cx, cy, rot=0.0, dx=0.0, dy=0.0):
    if abs(zoom - 1) < 1e-3 and abs(rot) < 1e-3 and abs(dx) < 0.5 and abs(dy) < 0.5 and abs(cx - W / 2) < 0.5 and abs(cy - H / 2) < 0.5:
        return frame
    # clamp so the frame stays covered
    hw, hh = W / 2 / zoom, H / 2 / zoom
    if zoom >= 1:
        cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    M = cv2.getRotationMatrix2D((cx, cy), rot, zoom)
    M[0, 2] += W / 2 - cx + dx; M[1, 2] += H / 2 - cy + dy
    return cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def chroma(frame, px):
    if px < 1: return frame
    b, g, r = cv2.split(frame); px = int(px)
    r = np.roll(r, px, axis=1); b = np.roll(b, -px, axis=1)
    return cv2.merge([b, g, r])


_SCAN = None


def vhs(frame, amt, seed):
    global _SCAN
    if _SCAN is None:
        _SCAN = np.ones((H, 1, 1), np.float32); _SCAN[::4] = 0.72; _SCAN[1::4] = 0.86
    f = frame.astype(np.float32) * (1 - 0.25 * amt + 0.25 * amt * _SCAN)
    rng = np.random.default_rng(seed)
    if amt > 0.3:
        for _ in range(3):
            y = int(rng.integers(0, H - 40)); h = int(rng.integers(6, 30)); s = int(rng.integers(-40, 40))
            f[y:y + h] = np.roll(f[y:y + h], s, axis=1)
    f += rng.normal(0, 10 * amt, (H // 4, W // 4, 1)).repeat(4, 0).repeat(4, 1)
    out = np.clip(f, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV); hsv[:, :, 1] = (hsv[:, :, 1] * (1 - 0.35 * amt)).astype(np.uint8)
    return chroma(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), 6 * amt)


def tint(frame, color, amt):
    if amt <= 0: return frame
    c = np.array(color, np.float32).reshape(1, 1, 3)
    return np.clip(frame.astype(np.float32) * (1 - amt) + c * amt, 0, 255).astype(np.uint8)


def whip(frame, p, direction=-1):
    """p in [0,1]: 0 = untouched, 1 = fully pushed off screen with heavy blur."""
    if p <= 0: return frame
    k = int(4 + 120 * p)
    bl = cv2.blur(frame, (k, 1))
    M = np.float32([[1, 0, direction * W * 0.9 * p ** 1.6], [0, 1, 0]])
    return cv2.warpAffine(bl, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def grade(frame, contrast=1.08, sat=1.12):
    f = frame.astype(np.float32)
    f = (f - 128) * contrast + 128
    hsv = cv2.cvtColor(np.clip(f, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * sat, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def vignette():
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1 - 0.28 * np.clip(d - 0.55, 0, 1) ** 1.4 * 2, 0.6, 1).astype(np.float32)[:, :, None]


# ---------------------------------------------------------------- render
def render(shots, out_path, glob_ov=(), sfx=(), music_gain=0.0, grade_on=True):
    total = sum(s['dur'] for s in shots)
    n = int(round(total * FPS))
    vig = vignette()
    starts = np.cumsum([0] + [s['dur'] for s in shots])
    tmp = pathlib.Path(out_path).with_suffix('.v.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(tmp)], stdin=subprocess.PIPE)
    all_sfx = list(sfx)
    for si, s in enumerate(shots):
        for e in s.get('sfx', []):
            all_sfx.append((e[0], starts[si] + e[1]) + tuple(e[2:]))
    rnd = random.Random(7)
    for i in range(n):
        T = i / FPS
        si = int(np.searchsorted(starts, T, side='right') - 1); si = min(si, len(shots) - 1)
        s = shots[si]; u = T - starts[si]
        if 'card' in s:
            frame = load_rgba(s['card'])[:, :, :3].copy()
        else:
            tsrc = lin(s['time'], u)
            frame = src(s['src']).frame(tsrc).copy()
        # camera
        z, cx, cy = interp(s.get('cam', [(0, 1.0, W / 2, H / 2)]), u)
        dx = dy = rot = 0.0
        for e in s.get('fx', []):
            if e[0] == 'shake' and e[1] <= u <= e[1] + e[3]:
                k = 1 - (u - e[1]) / e[3]
                dx += rnd.uniform(-1, 1) * e[2] * k; dy += rnd.uniform(-1, 1) * e[2] * k; rot += rnd.uniform(-1, 1) * e[2] * 0.02 * k
            if e[0] == 'punch' and e[1] <= u <= e[1] + e[3]:
                k = (u - e[1]) / e[3]; z *= 1 + e[2] * math.sin(math.pi * min(1, k * 1.0)) * (1 - k) ** 0.3
        frame = camera(frame, z, cx, cy, rot, dx, dy)
        for e in s.get('fx', []):
            name = e[0]
            if name == 'chroma' and e[1] <= u <= e[2]: frame = chroma(frame, e[3])
            elif name == 'vhs' and e[1] <= u <= e[2]: frame = vhs(frame, e[3], i)
            elif name == 'tint' and e[1] <= u <= e[2]:
                k = min(1, (u - e[1]) / 0.08) * min(1, (e[2] - u) / 0.08 + 0.001)
                frame = tint(frame, e[3], e[4] * k)
            elif name == 'bw' and e[1] <= u <= e[2]:
                g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); frame = cv2.merge([g, g, g])
        if grade_on and 'card' not in s:
            frame = grade(frame)
        # transitions
        if s.get('whip_out'):
            d = s['whip_out']; rem = s['dur'] - u
            if rem < d: frame = whip(frame, 1 - rem / d, -1)
        if s.get('whip_in'):
            d = s['whip_in']
            if u < d: frame = whip(frame, 1 - u / d, +1)
        frame = (frame.astype(np.float32) * vig).astype(np.uint8)
        # overlays
        for o in s.get('ov', []):
            stt = overlay_state(o, u)
            if stt: paste(frame, load_rgba(o['img']), stt[0], stt[1], stt[2], stt[3], stt[4])
        for o in glob_ov:
            stt = overlay_state(o, T)
            if stt: paste(frame, load_rgba(o['img']), stt[0], stt[1], stt[2], stt[3], stt[4])
        # flashes (after overlays so they read as camera flashes)
        for e in s.get('fx', []):
            if e[0] == 'flash' and e[1] <= u <= e[1] + e[2]:
                a = (1 - (u - e[1]) / e[2]) ** 1.5 * (e[3] if len(e) > 3 else 0.85)
                frame = np.clip(frame.astype(np.float32) * (1 - a) + 255 * a, 0, 255).astype(np.uint8)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close(); ff.wait()
    wav = pathlib.Path(out_path).with_suffix('.wav')
    mix_audio(all_sfx, total, wav)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(tmp), '-i', str(wav), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', str(out_path)], check=True)
    tmp.unlink(); return total


# ---------------------------------------------------------------- audio
_SND = {}


def snd(name):
    if name in _SND: return _SND[name]
    p = SFX_DIR / f'{name}.wav'
    if p.exists():
        with wave.open(str(p)) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).astype(np.float32) / 32768
        if a.shape[1] == 1: a = np.repeat(a, 2, 1)
        m = np.abs(a).max() or 1; a = a / m * 0.8
    else:
        from sfx_synth import SYNTH
        x = SYNTH[name]().astype(np.float32); a = np.stack([x, x], 1) * 0.85
    _SND[name] = a; return a


def mix_audio(events, total, out):
    n = int((total + 0.05) * SR); buf = np.zeros((n, 2), np.float32)
    for e in events:
        name, t = e[0], e[1]; g = e[2] if len(e) > 2 else 1.0
        a = snd(name) * g; k = int(t * SR)
        if k >= n: continue
        m = min(len(a), n - k); buf[k:k + m] += a[:m]
    fade = int(0.04 * SR); buf[-fade:] *= np.linspace(1, 0, fade)[:, None]
    buf = np.tanh(buf * 1.1) / np.tanh(1.1)
    peak = np.abs(buf).max() or 1; buf = buf / peak * 0.89
    with wave.open(str(out), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())
