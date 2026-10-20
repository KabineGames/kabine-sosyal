import sys, json, time
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME, KLANG, SUF
from bots import RALLY_BOT, PROMPTER_FORCE, PROMPTER_SOLVE
OUT = SCR / 'rec' / f'sess2{SUF}'
marks = {}
with sync_playwright() as p:
    b, ctx, page = open_game(p, lang=KLANG)
    page.evaluate(NEWGAME, {})
    page.evaluate("""() => { const {G,Events,C}=window.__cbs; G.S.week=2; G.S.money=1200; Events.pick=()=>null; G.startWeek(); }""")
    page.wait_for_timeout(1000*1.0)
    page.evaluate("() => { const {G}=window.__cbs; G.S.wk.mission = G.missionInfo('rally'); window.__cbs.Screens.hub(); }"); page.wait_for_timeout(1000*0.8)
    rec = Recorder(page, OUT); rec.start(); page.wait_for_timeout(1000*0.3)
    marks['rally_start'] = rec.mark()
    page.evaluate("() => { window.__cbs.G.playMission(); }")
    page.wait_for_selector('#tap', state='visible'); page.wait_for_timeout(1000*0.6)
    marks['rally_go'] = rec.mark()
    page.evaluate(PROMPTER_FORCE)
    page.evaluate(RALLY_BOT, {'plan': ['p','p','p','p','p']})
    page.wait_for_selector('.prompter', state='visible', timeout=20000)
    marks['prompter'] = rec.mark()
    order = page.evaluate(PROMPTER_SOLVE, 750)
    marks['prompter_solved'] = rec.mark()
    print('order', order)
    page.wait_for_selector('.res', state='visible', timeout=60000)
    marks['result'] = rec.mark(); page.wait_for_timeout(1000*4.0)
    marks['result_end'] = rec.mark()
    page.locator('.res [data-act="ok"]').click(); page.wait_for_timeout(1000*0.8)
    marks['paper_start'] = rec.mark()
    page.evaluate("() => { window.__cbs.G.endWeek(); }")
    page.wait_for_selector('#paper', state='visible'); page.wait_for_timeout(1000*4.5)
    marks['paper_end'] = rec.mark()
    rec.stop()
    print(page.evaluate("() => ({rating: window.__cbs.G.S.hist.heads[0]})"))
    b.close()
(OUT / 'marks.json').write_text(json.dumps(marks, indent=1))
print(json.dumps(marks))
