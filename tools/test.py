#!/usr/bin/env python3
"""Walk every exercise in both languages and both modes, answer it, and report
script errors, untranslated Japanese left in the English UI, and horizontal
overflow at phone width.

  python3 tools/test.py            # tests index.html (GitHub Pages layout)
  python3 tools/test.py SINGLE.html  # tests a single-file build

Needs Python Playwright with Chromium. Run from the repository root.
"""
import asyncio, functools, http.server, re, sys, threading
from playwright.async_api import async_playwright

JP = re.compile(r'[぀-ヿ一-鿿]')


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Quiet, directory='.')
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]


async def walk(pg, style, mode, seen, problems):
    await pg.click('#style-' + style)
    await pg.click('#mode-' + mode)
    if await pg.is_disabled('#mode-' + mode):
        return
    n = await pg.evaluate("set().filter(p=>S.mode==='cmp'||!p.cmpOnly).length")
    for _ in range(n):
        pid = await pg.evaluate('cur().id')
        seen.add((style, mode, pid))
        if mode == 'cmp':
            await pg.click('#opt2 .btn.primary')
            await pg.click('#opt2 .pick')
        elif style == 'c':
            await pg.click('#staff .note >> nth=0')
        else:
            await pg.click('#staff .note:not(.fixed) >> nth=0')
            await pg.click('#controls .btn.primary')
        if await pg.is_hidden('#feedback'):
            problems.append(f'{style} {mode} {pid}: no feedback shown')
        await pg.click('#next')


async def main(target):
    port = serve()
    url = f'http://127.0.0.1:{port}/{target}'
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for loc in ['ja-JP', 'en-US']:
            ctx = await b.new_context(locale=loc, viewport={'width': 900, 'height': 1000})
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(url)
            await pg.wait_for_timeout(500)
            seen = set()
            for st in 'cjr':
                for mode in ['peak', 'cmp']:
                    await walk(pg, st, mode, seen, problems)
            if loc == 'en-US':
                txt = await pg.evaluate('document.body.innerText')
                left = sorted(set(JP.findall(txt)))
                if left:
                    problems.append('Japanese left in English UI: ' + ''.join(left[:40]))
            total = await pg.evaluate("['c','j','r'].map(s=>SETS[s].length+SETS[s].filter(p=>!p.cmpOnly).length).reduce((a,b)=>a+b)")
            print(f'{loc}: visited {len(seen)} of {total} exercise views, errors {errs}')
            problems += [f'{loc} script error: {e}' for e in errs]
            await ctx.close()
        # phone width: nothing may stick out sideways (only the Pages build has its own
        # viewport tag; the single-file build gets one from the artifact host)
        if target != 'index.html':
            await b.close(); print('\n'.join(problems) if problems else 'all good'); return 1 if problems else 0
        ctx = await b.new_context(locale='ja-JP', viewport={'width': 360, 'height': 800})
        pg = await ctx.new_page()
        await pg.goto(url)
        for st in 'cjr':
            await pg.click('#style-' + st)
            for mode in ['peak', 'cmp']:
                await pg.click('#mode-' + mode)
                w = await pg.evaluate('document.documentElement.scrollWidth-innerWidth')
                if w > 1:
                    problems.append(f'phone {st} {mode}: page {w}px wider than the screen')
        await b.close()
    print('\n'.join(problems) if problems else 'all good')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else 'index.html')))
