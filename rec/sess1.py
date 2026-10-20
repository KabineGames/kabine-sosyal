import sys, json, time
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME, KLANG, SUF
from bots import RALLY_BOT
PICK = int(sys.argv[1]) if len(sys.argv) > 1 else 0
OUT = SCR / 'rec' / f'sess1_{PICK}{SUF}'
marks = {}
with sync_playwright() as p:
    b, ctx, page = open_game(p, lang=KLANG)
    page.evaluate(NEWGAME, {})
    info = page.evaluate("""() => { const {G,Events,C,Screens}=window.__cbs; G.S.week=2; G.S.money=1200; Events.pick=()=>C.eventById['giraffe']; return G.S.rival.name }""")
    print('rival', info)
    rec = Recorder(page, OUT); rec.start(); page.wait_for_timeout(1000*0.4)
    marks['ev_start'] = rec.mark()
    page.evaluate("() => { window.__cbs.G.startWeek(); }")
    page.wait_for_selector('.choice', state='visible'); page.wait_for_timeout(1000*3.2)
    marks['ev_click'] = rec.mark()
    page.locator('.choice').nth(PICK).click(); page.wait_for_timeout(1000*3.5)
    marks['ev_done'] = rec.mark()
    # hub briefly
    rec.stop()
    b.close()
(OUT / 'marks.json').write_text(json.dumps(marks, indent=1))
print(json.dumps(marks))
