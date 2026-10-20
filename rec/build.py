"""Builds finished 1080x1920 reels from recorded sessions + rendered text cards."""
import json, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cards import render

REC = pathlib.Path(__file__).parent
FPS = 30


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); raise SystemExit(1)


def seg_clip(seg, cards_dir, out):
    ins, pre = [], ''
    if 'src' in seg:
        ins += ['-i', str(REC / seg['src'])]
        pre = f"[0:v]trim=start={seg['a']}:end={seg['b']},setpts=PTS-STARTPTS,fps={FPS}[b0]"
        dur = seg['b'] - seg['a']
    elif 'freeze' in seg:
        ins += ['-ss', str(seg['at']), '-i', str(REC / seg['freeze'])]
        dur = seg['dur']
        pre = f"[0:v]trim=end_frame=1,loop=loop={int(dur * FPS)}:size=1:start=0,setpts=N/{FPS}/TB,fps={FPS}[b0]"
    elif 'still' in seg:
        ins += ['-loop', '1', '-t', str(seg['dur']), '-i', str(REC / seg['still'])]
        dur = seg['dur']
        n = int(dur * FPS)
        pre = (f"[0:v]scale=1080:1920,zoompan=z='1+0.05*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
               f"trim=end_frame={n},setpts=N/{FPS}/TB[b0]")
    elif 'card' in seg:
        ins += ['-loop', '1', '-t', str(seg['dur']), '-i', str(cards_dir / f"{seg['card']}.png")]
        dur = seg['dur']
        pre = f"[0:v]scale=1080:1920,fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS[b0]"
    chain = [pre]
    last = 'b0'
    for i, (name, t0, t1) in enumerate(seg.get('ov', [])):
        ins += ['-i', str(cards_dir / f'{name}.png')]
        t1 = dur if t1 is None else t1
        nxt = f'b{i + 1}'
        chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{t0},{t1})'[{nxt}]")
        last = nxt
    chain.append(f"[{last}]scale=1080:1920,format=yuv420p[v]")
    run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(chain), '-map', '[v]',
         '-t', f'{dur:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(out)])
    return dur


def build(name, segs, cards, out_dir):
    out_dir = pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    cards_dir = REC / 'cards' / name
    render(cards, cards_dir)
    tmp = REC / 'tmp' / name; tmp.mkdir(parents=True, exist_ok=True)
    parts, total, timeline = [], 0.0, []
    for i, s in enumerate(segs):
        p = tmp / f'p{i:02d}.mp4'
        d = seg_clip(s, cards_dir, p)
        parts.append(p); timeline.append((round(total, 2), round(total + d, 2), s.get('label', ''))); total += d
    lst = tmp / 'list.txt'; lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    final = out_dir / f'{name}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
         '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS),
         '-c:a', 'aac', '-b:a', '96k', '-shortest', '-movflags', '+faststart', str(final)])
    (tmp / 'timeline.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=1))
    return final, total, timeline
