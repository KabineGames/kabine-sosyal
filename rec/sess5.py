import sys, json, time
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME, KLANG, SUF
IDS = sys.argv[1:]
with sync_playwright() as p:
    for mid in IDS:
        OUT = SCR / 'rec' / f'mg_{mid}{SUF}'
        b, ctx, page = open_game(p, lang=KLANG)
        page.evaluate(NEWGAME, {})
        page.evaluate("""() => { const {G,Events}=window.__cbs; G.S.week=2; G.S.tier=2; Events.pick=()=>null; G.startWeek(); }""")
        time.sleep(0.8)
        rec = Recorder(page, OUT); rec.start(); time.sleep(0.2)
        page.evaluate("""(id) => { const {G,MG,L,MGMETA}=window.__cbs; const m=G.missionInfo(id);
           MG.run(id, G.mgCtx(id, 'mission', { title: G.missionTitle(m), mission: m, vars: G.mVars(m) })); }""", mid)
        # light random input so the screen moves
        for k in range(18):
            time.sleep(0.45)
            try:
                page.mouse.move(150 + 20 * k, 500 - 10 * k)
                if mid in ('bus',): 
                    if k == 3: page.mouse.move(240, 650); page.mouse.down(); page.mouse.move(200, 760, steps=8)
                    if k == 5: page.mouse.up()
                elif mid in ('dodge', 'delegate'):
                    page.mouse.click(120 + 40 * (k % 6), 430 + 30 * (k % 4))
                elif True:
                    page.mouse.click(240 + (k % 3 - 1) * 90, 420 + (k % 4) * 60)
            except Exception as e: print('input', e)
        rec.stop()
        b.close()
        print(mid, len(rec.frames))
