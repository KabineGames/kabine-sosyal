import sys, json, time
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME, KLANG, SUF
TAKES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
summary = []
with sync_playwright() as p:
    for t in range(TAKES):
        OUT = SCR / 'rec' / f'sess3_{t}{SUF}'
        b, ctx, page = open_game(p, lang=KLANG)
        page.evaluate(NEWGAME, {})
        page.evaluate("""() => { const {G,Events}=window.__cbs; G.S.week=8; G.S.weeksInTier=8; G.S.money=1200; Events.pick=()=>null; G.startWeek(); }""")
        page.wait_for_timeout(1000*1.0)
        rec = Recorder(page, OUT); rec.start(); page.wait_for_timeout(1000*0.3)
        m = {'night_start': rec.mark()}
        page.evaluate("""() => { const {G,UI,L,Career}=window.__cbs; const S=G.S;
          window.__vals=[]; const t0=performance.now();
          const iv=setInterval(()=>{const e=document.querySelector('#pcMe'); if(e) window.__vals.push([Math.round(performance.now()-t0), parseFloat(e.textContent)]);},100);
          window.__night = UI.electionNight({ title: L.t('el_local'), share: 50.4, rivalName: S.rival.name, rivalLook: S.rival.look, kind: 'local' }).then(w => { clearInterval(iv); window.__won = w; });
        }""")
        page.wait_for_selector('.verdict-big', timeout=30000)
        m['verdict'] = rec.mark(); page.wait_for_timeout(1000*3.5)
        m['verdict_end'] = rec.mark()
        page.locator('#fast').click(); page.wait_for_timeout(1000*0.6)
        m['promo_start'] = rec.mark()
        page.evaluate("() => { window.__cbs.Career.promote(); }")
        page.wait_for_function("() => document.querySelectorAll('.ov').length && /TERF|PROMOT/i.test(document.body.innerText)", timeout=15000)
        m['promo_shown'] = rec.mark()
        page.wait_for_timeout(1000*3.5)
        m['promo_end'] = rec.mark()
        rec.stop()
        vals = page.evaluate("() => window.__vals")
        b.close()
        (OUT / 'marks.json').write_text(json.dumps(m, indent=1)); (OUT / 'vals.json').write_text(json.dumps(vals))
        v = [x[1] for x in vals]
        flips = sum(1 for i in range(1, len(v)) if (v[i] - 50) * (v[i-1] - 50) < 0)
        late_trail = any(x < 50 for x in v[int(len(v)*0.6):-3])
        summary.append({'take': t, 'flips': flips, 'min': min(v), 'max': max(v), 'late_trail': late_trail, 'marks': m})
for s in summary: print(json.dumps(s))
