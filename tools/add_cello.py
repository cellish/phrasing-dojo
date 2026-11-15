#!/usr/bin/env python3
"""Add the cello samples (Freesound pack 12408 by flcellogrl, CC BY 3.0, as
collected in nbrosowsky/tonejs-instruments) to samples/cello/ and register them
in index.html's SAMPLE_DATA.

  python3 tools/add_cello.py PATH/TO/tonejs-instruments/samples/cello

For each note it trims to the onset, writes a 3 s mono MP3, and stores:
  o  where the steady part of the bow stroke starts (playback starts here)
  g  gain that matches the piano's loudness over that steady part
  ls/le  a loop inside the steady part, so held notes can last any length
Needs ffmpeg and numpy. Run from the repository root.
"""
import sys, os, re, glob, json, math, subprocess
import numpy as np

SR = 44100
NAMES = {'C': 0, 'Cs': 1, 'D': 2, 'Ds': 3, 'E': 4, 'F': 5, 'Fs': 6, 'G': 7, 'Gs': 8, 'A': 9, 'As': 10, 'B': 11}


def pcm(path, extra=()):
    raw = subprocess.run(['ffmpeg', '-v', 'error', *extra, '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def loudness(path, secs=1.0):
    out = subprocess.run(['ffmpeg', '-v', 'info', '-t', str(secs), '-i', path, '-af', 'ebur128', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float([l for l in out.split('\n') if l.strip().startswith('I:')][-1].split()[1])


def onset(x):
    pk = np.abs(x).max() or 1
    return int(np.argmax(np.abs(x) > pk * 0.03)), float(pk)


def loop_points(x, o, end):
    """Pick a loop [ls, le) inside the steady part so the seam matches: compare 25 ms windows."""
    w = int(.025 * SR)
    a0, a1 = o + int(.05 * SR), o + int(.3 * SR)
    b0, b1 = max(a1 + int(.25 * SR), end - int(.4 * SR)), end - w
    best = None
    for ls in range(a0, a1, 32):
        a = x[ls:ls + w]
        for le in range(b0, max(b0 + 1, b1), 8):
            b = x[le:le + w]
            d = np.sum((a - b) ** 2) / (np.sum(a * a) + 1e-9)
            if best is None or d < best[0]:
                best = (d, ls, le)
    return best[1], best[2]


def main(src):
    os.makedirs('samples/cello', exist_ok=True)
    html = open('index.html', encoding='utf-8').read()
    i = html.index('const SAMPLE_DATA='); j = html.index(';\n', i)
    data = json.loads(html[i + len('const SAMPLE_DATA='):j])
    # loudness target: the piano's (its stored gain already levels it)
    p = data['piano']['60_1']
    target = loudness('samples/piano/60_1.mp3') + 20 * math.log10(p['g'])
    out = {}
    for f in sorted(glob.glob(os.path.join(src, '*.wav'))):
        b = os.path.basename(f)[:-4]
        mm = re.fullmatch(r'([A-G]s?)(\d)', b)
        if not mm:
            continue  # skip alternate takes such as "F2 v2"
        midi = 12 * (int(mm.group(2)) + 1) + NAMES[mm.group(1)]
        if not 45 <= midi <= 73:
            continue
        x = pcm(f); o0, _ = onset(x)
        dst = f'samples/cello/{midi}.mp3'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, o0 / SR - .004):.4f}', '-i', f, '-t', '3.0',
                        '-af', 'afade=t=out:st=2.85:d=0.15', '-ac', '1', '-ar', str(SR), '-b:a', '96k', dst], check=True)
        y = pcm(dst); _, pk = onset(y)
        # play from the steady part of the bow stroke (the recordings swell in slowly)
        w = int(.05 * SR); env = np.sqrt(np.convolve(y * y, np.ones(w) / w, 'same'))
        top = env.max(); idx = np.nonzero(env >= .7 * top)[0]
        o, end = int(idx[0]), int(idx[-1])
        ls, le = loop_points(y, o, end)
        seg = f'/tmp/cello_seg_{midi}.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(o / SR), '-t', str((end - o) / SR), '-i', dst, seg], check=True)
        g = 10 ** ((target - loudness(seg, 5)) / 20); os.remove(seg)
        out[str(midi)] = {'m': midi, 'o': round(o / SR, 4), 'p': round(float(pk), 3), 'g': round(float(g), 4),
                          'a': 0, 'ls': round(ls / SR, 4), 'le': round(le / SR, 4)}
        print(midi, out[str(midi)])
    data['cello'] = out
    html = html[:i] + 'const SAMPLE_DATA=' + json.dumps(data, separators=(',', ':')) + html[j:]
    open('index.html', 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main(sys.argv[1])
