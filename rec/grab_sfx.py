import sys, json, base64, wave, struct
sys.path.insert(0, '.')
import numpy as np
from harness import *
NAMES = ['click','tap','select','perfect','good','ok','gaffe','cheer','applause','boo','camera','coin','fanfare','whoosh','thud','snip','heart','pop','splat','error','paper','type','ring','win','lose','level','drum','tick','achieve','drums']
with sync_playwright() as p:
    b, ctx, page = open_game(p, settings={'sound': True})
    for n in NAMES:
        data = page.evaluate("""async (n) => {
          const off = new OfflineAudioContext(2, 44100 * 3, 44100);
          A.build(off); A.on = true; A.held = true;
          try { SFX[n](); } catch (e) { return 'ERR ' + e; }
          const buf = await off.startRendering();
          const l = buf.getChannelData(0), r = buf.getChannelData(1);
          const out = new Int16Array(l.length * 2);
          for (let i = 0; i < l.length; i++) { out[2*i] = Math.max(-1, Math.min(1, l[i])) * 32767; out[2*i+1] = Math.max(-1, Math.min(1, r[i])) * 32767; }
          let s = ''; const u8 = new Uint8Array(out.buffer); for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
          return btoa(s); }""", n)
        if isinstance(data, str) and data.startswith('ERR'): print(n, data); continue
        a = np.frombuffer(base64.b64decode(data), dtype=np.int16).reshape(-1, 2)
        nz = np.where(np.abs(a).max(axis=1) > 30)[0]
        end = (nz[-1] + 2205) if len(nz) else 4410
        a = a[:min(end, len(a))]
        with wave.open(f'sfx/{n}.wav', 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes(a.tobytes())
        print(n, round(len(a) / 44100, 2), 's peak', int(np.abs(a).max()))
    b.close()
