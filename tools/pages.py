#!/usr/bin/env python3
"""Convert between the single-file page (samples embedded as base64) and the
GitHub Pages layout (index.html + samples/<inst>/<key>.mp3, loaded on demand).

  python3 tools/pages.py split SINGLE.html     # -> index.html, samples/
  python3 tools/pages.py embed OUT.html        # index.html + samples/ -> single file
Run from the repository root.
"""
import sys, os, json, base64, re, shutil

HEAD = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="クラシックの抑揚、ジャズとロックのアーティキュレーションを練習するドリル / A drill for phrasing and articulation in classical, jazz and rock.">
<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}img{max-width:100%}[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
'''
TAG = 'const SAMPLE_DATA='

def find_data(s):
    i = s.index(TAG); j = s.index(';\n', i)
    return i, j, json.loads(s[i + len(TAG):j])

def split(src):
    s = open(src, encoding='utf-8').read()
    i, j, data = find_data(s)
    if os.path.isdir('samples'): shutil.rmtree('samples')
    for inst, ents in data.items():
        os.makedirs(f'samples/{inst}', exist_ok=True)
        for key, e in ents.items():
            open(f'samples/{inst}/{key}.mp3', 'wb').write(base64.b64decode(e.pop('d')))
    s = s[:i] + "const SAMPLE_URL='samples/';\n" + TAG + json.dumps(data, separators=(',', ':')) + s[j:]
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    w = s.index('<div class="wrap">')
    out = HEAD + s[:w].rstrip('\n') + '\n\n</head>\n<body>\n' + s[w:].rstrip('\n') + '\n\n</body>\n</html>\n'
    open('index.html', 'w', encoding='utf-8').write(out)

def embed(dst):
    s = open('index.html', encoding='utf-8').read()
    i, j, data = find_data(s)
    for inst, ents in data.items():
        for key, e in ents.items():
            e['d'] = base64.b64encode(open(f'samples/{inst}/{key}.mp3', 'rb').read()).decode()
    s = s[:i] + TAG + json.dumps(data, separators=(',', ':')) + s[j:]
    s = s.replace("const SAMPLE_URL='samples/';\n", '')
    a = s.index('<title>'); b = s.index('</head>')
    w = s.index('<div class="wrap">')
    body = s[w:s.rindex('</body>')].rstrip('\n') + '\n'
    out = s[a:b].rstrip('\n').replace('<title>フレージング道場</title>\n', '<title>フレージング道場</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n', 1) + '\n\n' + body
    open(dst, 'w', encoding='utf-8').write(out)

if __name__ == '__main__':
    {'split': split, 'embed': embed}[sys.argv[1]](sys.argv[2])
