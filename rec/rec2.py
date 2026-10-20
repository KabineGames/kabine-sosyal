import sys, json, time, random, math
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME
from bots import RALLY_BOT, PROMPTER_FORCE
V2 = SCR / 'rec' / 'v2'
LOGGER = """() => { window.__ev = []; const seen = new WeakSet();
  new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) { if (!(n instanceof HTMLElement) || seen.has(n)) continue; seen.add(n);
    const cls = n.className || ''; if (/float-txt|banner|verdict-big|prompter|slogan/.test(cls) || n.querySelector?.('.prompter')) window.__ev.push([Date.now()/1000, String(cls).slice(0,30), (n.textContent||'').trim().slice(0,80)]); } })
  .observe(document.body, {childList: true, subtree: true}); }"""

def session(name, fn, lang='tr'):
    with sync_playwright() as p:
        b, ctx, page = open_game(p, lang=lang)
        page.evaluate(NEWGAME, {})
        page.evaluate(LOGGER)
        out = V2 / name
        rec = Recorder(page, out)
        marks = fn(page, rec)
        rec.stop()
        ev = page.evaluate("() => window.__ev")
        b.close()
    t0 = rec.t0
    (out / 'marks.json').write_text(json.dumps(marks, ensure_ascii=False, indent=1))
    (out / 'events.json').write_text(json.dumps([[round(e[0] - t0, 2), e[1], e[2]] for e in ev], ensure_ascii=False, indent=0))
    frames_to_mp4(out, V2 / f'{name}.mp4')
    print(name, marks, [[round(e[0] - t0, 2), e[2][:30]] for e in ev][:14])

def card(evid, pick):
    def fn(page, rec):
        page.evaluate("(id) => { const {G,Events,C}=window.__cbs; G.S.week=2; Events.pick=()=>C.eventById[id]; }", evid)
        rec.start(); page.wait_for_timeout(300); m = {'start': rec.mark()}
        page.evaluate("() => { window.__cbs.G.startWeek(); }")
        page.wait_for_selector('.choice', state='visible'); m['shown'] = rec.mark(); page.wait_for_timeout(1500)
        m['click'] = rec.mark(); page.locator('.choice').nth(pick).click(); page.wait_for_timeout(2600); m['end'] = rec.mark()
        return m
    return fn

PROMPTER_FAIL = """(delay) => new Promise(res => {
  const {C, L} = window.__cbs;
  const iv = setInterval(() => {
    const pr = document.querySelector('.prompter'); if (!pr) return;
    const btns = [...pr.querySelectorAll('[data-o]')]; if (!btns.length) return;
    clearInterval(iv);
    const texts = btns.map(b => b.textContent.trim());
    const set = L.arr(C.prompter).find(s => texts.every(t => s.map(x => x.trim()).includes(t)));
    const seq = [set[0].trim(), set[3].trim()];
    let i = 0;
    const step = () => { if (i >= seq.length) return res(seq); const b = btns[texts.indexOf(seq[i])]; b.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, cancelable:true})); i++; setTimeout(step, delay); };
    setTimeout(step, delay + 350);
  }, 30);
})"""

def rally_fail(page, rec):
    page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(900)
    page.evaluate("() => { const {G}=window.__cbs; G.S.wk.mission = G.missionInfo('rally'); window.__cbs.Screens.hub(); }"); page.wait_for_timeout(600)
    rec.start(); page.wait_for_timeout(300); m = {'start': rec.mark()}
    page.evaluate("() => { window.__cbs.G.playMission(); }")
    page.wait_for_selector('#tap', state='visible'); page.wait_for_timeout(600); m['go'] = rec.mark()
    page.evaluate(PROMPTER_FORCE)
    page.evaluate(RALLY_BOT, {'plan': ['p', 'x', 'p', 'p', 'p']})
    page.wait_for_selector('.prompter', state='visible', timeout=20000); m['prompter'] = rec.mark()
    page.evaluate(PROMPTER_FAIL, 800); m['failed'] = rec.mark()
    page.wait_for_selector('.res', state='visible', timeout=60000); m['result'] = rec.mark(); page.wait_for_timeout(2500)
    return m

def bus(seed):
    def fn(page, rec):
        random.seed(seed)
        page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; G.S.tier=1; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(800)
        rec.start(); page.wait_for_timeout(200); m = {'start': rec.mark()}
        page.evaluate("""() => { const {G,MG}=window.__cbs; const m=G.missionInfo('bus'); MG.run('bus', G.mgCtx('bus','mission',{title:G.missionTitle(m), mission:m, vars:G.mVars(m)})); }""")
        page.wait_for_selector('.mg-stage canvas', state='visible'); page.wait_for_timeout(900)
        bb = page.locator('.mg-stage canvas').bounding_box(); sc = bb['width'] / 160
        m['go'] = rec.mark(); m['throws'] = []
        for k in range(8):
            ang = math.radians(random.uniform(30, 68)); pw = random.uniform(0.55, 0.98)
            L = pw * 55 * sc
            sx, sy = bb['x'] + bb['width'] * 0.45, bb['y'] + bb['height'] * 0.55
            ex, ey = sx - math.cos(ang) * L, sy + math.sin(ang) * L
            page.mouse.move(sx, sy); page.mouse.down()
            for s in range(1, 9): page.mouse.move(sx + (ex - sx) * s / 8, sy + (ey - sy) * s / 8); page.wait_for_timeout(28)
            page.wait_for_timeout(180); m['throws'].append(rec.mark()); page.mouse.up()
            page.wait_for_timeout(random.randint(1400, 1900))
        page.wait_for_timeout(800); m['end'] = rec.mark()
        return m
    return fn

def dodge(seed):
    def fn(page, rec):
        random.seed(seed)
        page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; G.S.tier=2; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(800)
        rec.start(); page.wait_for_timeout(200); m = {'start': rec.mark()}
        page.evaluate("""() => { const {G,MG}=window.__cbs; const m=G.missionInfo('dodge'); MG.run('dodge', G.mgCtx('dodge','mission',{title:G.missionTitle(m), mission:m, vars:G.mVars(m)})); }""")
        page.wait_for_selector('.mg-stage canvas', state='visible'); page.wait_for_timeout(900); m['go'] = rec.mark()
        t_end = time.time() + 17
        while time.time() < t_end:
            r = random.random()
            if r < 0.78: page.keyboard.press('ArrowUp')
            elif r < 0.89: page.keyboard.press('ArrowLeft')
            else: page.keyboard.press('ArrowRight')
            page.wait_for_timeout(random.randint(260, 520))
            if page.evaluate("() => !!document.querySelector('.banner') && /Arabaya|car/i.test(document.querySelector('.banner').textContent)"): break
        page.wait_for_timeout(1400); m['end'] = rec.mark()
        return m
    return fn

which = sys.argv[1:] or ['cards', 'rally', 'bus', 'dodge']
if 'cards' in which:
    for evid, pick in [('town_cat', 1), ('parrot', 1), ('fountain', 0), ('mom_call', 1)]: session(f'card_{evid}', card(evid, pick))
if 'rally' in which: session('rally_fail', rally_fail)
if 'bus' in which:
    for s in range(4): session(f'bus_{s}', bus(100 + s))
if 'dodge' in which:
    for s in range(4): session(f'dodge_{s}', dodge(200 + s))
