"""Hafta 4 kayıtları (rec/v2/<isim>_<dil>/). Kullanım: KLANG=en|pt|tr python3 rec4.py <dodge|strike|frame|night|rally|scandal>...
Reklam kayıtlarında (dodge, strike, frame) parti adı "Team Kettle"/"Time Chaleira" verilir (oyuncunun seçtiği ad; ekranda "party" kelimesi çıkmasın).
Botlar sadece gerçek girdi verir (tuş/tık); oyun kodu değişmez. Şans sonuçları (kart B'nin kötü dalı) Math.random ile seçilir."""
import sys, json, time, random
sys.path.insert(0, '.')
from harness import *
from setup_js import NEWGAME, KLANG
from bots import RALLY_BOT, PROMPTER_FORCE
V2 = SCR / 'rec' / 'v2'
SUF = '_' + KLANG
AD_PARTY = {'en': 'Team Kettle', 'pt': 'Time Chaleira', 'tr': 'Demlik Ekibi'}[KLANG]
LOGGER = """() => { window.__ev = []; const seen = new WeakSet();
  new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) { if (!(n instanceof HTMLElement) || seen.has(n)) continue; seen.add(n);
    const cls = String(n.className || ''); if (/float-txt|banner|verdict-big|prompter|slogan|res|ev-|toast|countdown|tw-card/.test(cls) || n.querySelector?.('.prompter,.res,.choice')) window.__ev.push([Date.now()/1000, cls.slice(0,30), (n.textContent||'').trim().slice(0,90)]); } })
  .observe(document.body, {childList: true, subtree: true}); }"""


def session(name, fn, ad=False, toasts=False, opts=None):
    name = name + SUF
    with sync_playwright() as p:
        b, ctx, page = open_game(p, lang=KLANG)
        o = dict(opts or {})
        if ad: o['party'] = AD_PARTY
        page.evaluate(NEWGAME, o)
        if toasts: page.add_style_tag(content='#toasts{display:block!important}')
        page.evaluate(LOGGER)
        out = V2 / name
        rec = Recorder(page, out)
        marks = fn(page, rec)
        rec.stop()
        ev = page.evaluate("() => window.__ev")
        b.close()
    t0 = rec.t0
    (out / 'marks.json').write_text(json.dumps(marks, ensure_ascii=False, indent=1))
    evs = [[round(e[0] - t0, 2), e[1], e[2]] for e in ev]
    (out / 'events.json').write_text(json.dumps(evs, ensure_ascii=False, indent=0))
    print(name, json.dumps(marks, ensure_ascii=False)[:600])
    for e in evs: print('  ', e)


# ---------------------------------------------------------------- Muhabirden Kaç botu (kanvas piksellerini okur)
DODGE_BOT = """(cfg) => {
  const st = window.__dg = { pc: 3, pr: 0, caught: 0, mode: cfg.mode, ram: cfg.ram || 0, rams: 0, done: false, log: [] };
  const SAFE = new Set([0, 4, 8, 12]), CS = 16, ROWS = 13;
  const cv = document.querySelector('.mg-stage canvas'); const g = cv.getContext('2d', { willReadFrequently: true });
  const H = cv.height, W = cv.width;
  const rowY = r => H - (r + 1) * CS;
  const BG = new Set(['86,93,110', '78,85,102', '98,106,124']);
  new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.classList && n.classList.contains('float-txt')) {
      st.caught++; let back = st.pr - 1; while (back > 0 && !SAFE.has(back)) back--; st.pr = Math.max(0, back); st.log.push(['caught', performance.now()]); } })
    .observe(document.querySelector('.mg-stage'), { childList: true, subtree: true });
  const lanePix = (r) => { const d = g.getImageData(0, rowY(r) + 6, W, 1).data; const occ = []; for (let x = 0; x < W; x++) { const k = d[4*x] + ',' + d[4*x+1] + ',' + d[4*x+2]; occ.push(!BG.has(k)); } return occ; };
  const shadesAt = () => { for (let r = 1; r < ROWS - 1; r++) { if (SAFE.has(r)) continue; const d = g.getImageData(0, rowY(r) + 8, W, 1).data; for (let x = 0; x < W; x++) if (d[4*x] === 20 && d[4*x+1] === 22 && d[4*x+2] === 31) return { r, c: Math.floor(x / CS) }; } return null; };
  const clear = (r, c, ahead) => { if (SAFE.has(r) || r >= ROWS - 1) return true; const dir = r % 2 ? 1 : -1; const occ = lanePix(r); const cx = c * CS + 8;
    const up = 7 + 44 * ahead, down = 7; const lo = dir > 0 ? cx - up : cx - down, hi = dir > 0 ? cx + down : cx + up;
    for (let x = Math.max(0, Math.floor(lo)); x <= Math.min(W - 1, Math.ceil(hi)); x++) if (occ[x]) return false; return true; };
  const incoming = (r, c) => { const dir = r % 2 ? 1 : -1; const occ = lanePix(r); const cx = c * CS + 8; // reporter 1-2 cells upstream, about to arrive
    let hit = false; for (let x = 0; x < W; x++) if (occ[x]) { const dx = (cx - x) * dir; if (dx > 14 && dx < 30) hit = true; if (dx >= -6 && dx <= 14) return false; } return hit; };
  const key = k => window.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
  const move = (dc, dr) => { st.pc = Math.max(0, Math.min(6, st.pc + dc)); st.pr = Math.max(0, Math.min(12, st.pr + dr)); key(dc < 0 ? 'ArrowLeft' : dc > 0 ? 'ArrowRight' : dr < 0 ? 'ArrowDown' : 'ArrowUp'); st.last = performance.now(); st.log.push([dc ? 'side' : dr < 0 ? 'down' : 'up', performance.now(), st.pr, st.pc]); };
  st.last = 0; st.invUntil = 0; st.clear = clear; st.lanePix = lanePix; st.ticks = 0;
  const tick = () => {
    if (st.done || !document.querySelector('.mg-stage canvas')) { st.done = true; return; }
    setTimeout(tick, 45); st.ticks++;
    if (document.querySelector('.howto, .countdown')) return;
    const now = performance.now(); if (now - st.last < 120) return;
    if (st.caughtSeen !== st.caught) { st.caughtSeen = st.caught; st.last = now + 700; return; } // yakalanınca kısa bekle
    const { pr, pc } = st;
    if (pr >= 12) { st.done = true; return; }
    // kasıtlı çarpma: güvenli şeritteyken üstteki şeride gelen muhabire doğru yürü
    if (st.mode === 'ram' && st.rams < st.ram && pr >= cfg.ramFrom && SAFE.has(pr)) {
      if (incoming(pr + 1, pc)) { st.rams++; move(0, 1); }
      return;
    }
    if (st.mode === 'ram' && st.rams >= st.ram) return; // sonra bekle: süre dolsun
    // gözlük: aynı segmentteyse sütununa git
    if (st.mode === 'clean' && now < st.invUntil) { move(0, 1); return; }
    const sh = shadesAt();
    if (st.mode === 'clean' && sh && SAFE.has(pr) && sh.r > pr && sh.r < pr + 4 && pc !== sh.c) { move(sh.c > pc ? 1 : -1, 0); return; }
    if (sh && pr + 1 === sh.r && pc === sh.c && clear(pr + 1, pc, 0.25)) { move(0, 1); st.invUntil = performance.now() + 2300; return; }
    const danger = (r, c) => { if (SAFE.has(r)) return false; const dir = r % 2 ? 1 : -1; const occ = lanePix(r); const cx = c * CS + 8;
      for (let x = 0; x < W; x++) if (occ[x]) { const dx = (cx - x) * dir; if (dx > -6 && dx < 24) return true; } return false; };
    if (SAFE.has(pr)) {
      if (clear(pr + 1, pc, 0.35) && clear(pr + 2, pc, 0.45)) { move(0, 1); return; }
      for (const dc of [1, -1]) { const c = pc + dc; if (c < 0 || c > 6) continue; if (clear(pr + 1, c, 0.5) && clear(pr + 2, c, 0.6)) { move(dc, 0); return; } }
      return;
    }
    if (clear(pr + 1, pc, 0.3)) { move(0, 1); return; }
    if (danger(pr, pc)) {
      if (clear(pr - 1, pc, 0.2)) { move(0, -1); return; }
      for (const dc of [1, -1]) { const c = pc + dc; if (c >= 0 && c <= 6 && clear(pr, c, 0.15)) { move(dc, 0); return; } }
    }
  };
  tick();
}"""


def start_mission(page, mid, band='local', ti=0, mode='mission'):
    """Haftalık görevi (sonuç ekranı + yarın manşeti dahil) oyunun kendi akışıyla başlatır."""
    page.evaluate("""([mid, band, ti]) => { const {G} = window.__cbs; const m = G.missionInfo(mid); m.band = band; m.ti = ti; G.S.wk.mission = m; G.S.wk.done = false; G.busy = false; window.__pm = G.playMission(); }""", [mid, band, ti])


def skip_howto(page):
    page.wait_for_selector('.howto', state='visible', timeout=15000); page.wait_for_timeout(500)
    page.locator('.howto').click()


def dodge_ad(page, rec):
    page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; G.S.tier=1; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(900)
    rec.start(); page.wait_for_timeout(200); m = {'start': rec.mark()}
    # 1. tur: ilk segmenti koş, sonra muhabirlere bilerek çarp (3 kez), süre dolsun -> kötü manşet
    start_mission(page, 'dodge'); skip_howto(page); m['go1'] = rec.mark()
    page.evaluate(DODGE_BOT, {'mode': 'ram', 'ram': 3, 'ramFrom': 4})
    page.wait_for_selector('.res', state='visible', timeout=40000); m['res1'] = rec.mark()
    m['log1'] = page.evaluate("() => window.__dg.log.map(x => [x[0], x[2], x[3]])")
    page.wait_for_timeout(3200); m['res1_end'] = rec.mark()
    page.locator('.res [data-act=ok]').click(); page.wait_for_timeout(500)
    # 2. tur: temiz koşu, gözlük + araba
    start_mission(page, 'dodge'); skip_howto(page); m['go2'] = rec.mark()
    page.evaluate(DODGE_BOT, {'mode': 'clean'})
    page.wait_for_selector('.res', state='visible', timeout=40000); m['res2'] = rec.mark()
    m['log2'] = page.evaluate("() => window.__dg.log.map(x => [x[0], x[2], x[3]])"); m['caught2'] = page.evaluate("() => window.__dg.caught")
    page.wait_for_timeout(3200); m['end'] = rec.mark()
    return m


# ---------------------------------------------------------------- kriz kartı
def card_force(evid, pick, force=None, pre=None):
    """force: 'lose' -> şanslı seçeneğin kötü dalı, 'win' -> iyi dalı."""
    def fn(page, rec):
        page.evaluate("([id, pre]) => { const {G,Events,C}=window.__cbs; G.S.week=3; G.S.tier=1; if (pre) Object.assign(G.S, pre); Events.pick=()=>C.eventById[id]; }", [evid, pre])
        rec.start(); page.wait_for_timeout(300); m = {'start': rec.mark()}
        page.evaluate("() => { window.__cbs.G.startWeek(); }")
        page.wait_for_selector('.choice', state='visible'); m['shown'] = rec.mark(); page.wait_for_timeout(2600)
        if force: page.evaluate("(f) => { const o = Math.random; Math.random = () => f === 'lose' ? 0.995 : 0.001; setTimeout(() => { Math.random = o; }, 400); }", force)
        m['click'] = rec.mark(); page.locator('.choice').nth(pick).click(); page.wait_for_timeout(4200); m['end'] = rec.mark()
        return m
    return fn


# ---------------------------------------------------------------- Kadrajda Kal botu
FRAME_BOT = """(cfg) => {
  const st = window.__fr = { mode: cfg.mode, nods: 0, log: [], done: false };
  const cv = document.querySelector('.mg-stage canvas'); const g = cv.getContext('2d', { willReadFrequently: true });
  const W = cv.width, H = cv.height, floor = H - 30, LC = 60.5;
  const key = (k, up) => window.dispatchEvent(new KeyboardEvent(up ? 'keyup' : 'keydown', { key: k, bubbles: true }));
  let dir = 0, lastBub = false;
  const setDir = d => { if (d === dir) return; if (dir < 0) key('ArrowLeft', true); if (dir > 0) key('ArrowRight', true); if (d < 0) key('ArrowLeft'); if (d > 0) key('ArrowRight'); dir = d; };
  const tick = () => {
    if (!document.querySelector('.mg-stage canvas')) { st.done = true; setDir(0); return; }
    setTimeout(tick, 40);
    if (document.querySelector('.howto, .countdown')) return;
    const d = g.getImageData(0, 0, W, H).data;
    let gx0 = 1e9, gx1 = -1, wx0 = 1e9, wx1 = -1, bub = false;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = 4 * (y * W + x), r = d[i], gg = d[i+1], b = d[i+2];
      if (((r === 245 && gg === 184 && b === 61) || (Math.abs(r - 113) < 4 && Math.abs(gg - 88) < 4 && Math.abs(b - 37) < 4)) && y > floor - 95 && y < floor - 58) { gx0 = Math.min(gx0, x); gx1 = Math.max(gx1, x); }
      if (r === 255 && gg === 255 && b === 255) { wx0 = Math.min(wx0, x); wx1 = Math.max(wx1, x); }
      if (r === 244 && gg === 241 && b === 232 && y > floor - 62 && y < floor - 44) bub = true; }
    if (gx1 < 0) return;
    const hx = (gx0 + gx1) / 2 + 0.5, cx = wx1 > 0 ? (wx0 + wx1) / 2 : LC;
    let tgt;
    if (st.mode === 'rush') tgt = LC;               // lidere yapış -> koruma / dirsek
    else tgt = Math.max(30, Math.min(48, cx - 10));                                // kadrajda, dirsek mesafesinin dışında
    st.hx = hx; st.gx = [gx0, gx1]; st.cx = cx; st.H = H;
    const e = tgt - hx; setDir(Math.abs(e) < 2.5 ? 0 : e > 0 ? 1 : -1);
    if (bub && !lastBub && st.mode !== 'rush') { key(' '); st.nods++; st.log.push(['nod', performance.now()]); }
    lastBub = bub;
  };
  tick();
}"""


def frame_ad(page, rec):
    page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; G.S.tier=1; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(900)
    rec.start(); page.wait_for_timeout(200); m = {'start': rec.mark()}
    start_mission(page, 'frame'); skip_howto(page); m['go1'] = rec.mark()
    page.evaluate(FRAME_BOT, {'mode': 'rush'})
    page.wait_for_selector('.res', state='visible', timeout=40000); m['res1'] = rec.mark()
    page.wait_for_timeout(2500); page.locator('.res [data-act=ok]').click(); page.wait_for_timeout(500)
    start_mission(page, 'frame'); skip_howto(page); m['go2'] = rec.mark()
    page.evaluate(FRAME_BOT, {'mode': 'clean'})
    page.wait_for_selector('.res', state='visible', timeout=40000); m['res2'] = rec.mark(); m['nods'] = page.evaluate("() => window.__fr.nods")
    page.wait_for_timeout(3200); m['end'] = rec.mark()
    return m


# ---------------------------------------------------------------- Seçim gecesi (harita + son bölge)
def night(page, rec):
    page.evaluate("""() => { const {G,Events}=window.__cbs; G.S.week=8; G.S.weeksInTier=8; G.S.money=1200; Events.pick=()=>null; G.startWeek(); }""")
    page.wait_for_timeout(1000)
    rec.start(); page.wait_for_timeout(300); m = {'night_start': rec.mark()}
    page.evaluate("""() => { const {G,UI,L}=window.__cbs; const S=G.S; window.__vals=[]; const t0=performance.now();
      const iv=setInterval(()=>{const e=document.querySelector('#pcMe'), t=document.querySelector('#mtally'), c=document.querySelector('#cnt'); if(e) window.__vals.push([Math.round(performance.now()-t0), parseFloat(e.textContent), t?t.textContent:'', c?c.textContent:''])},50);
      window.__t0 = t0; window.__night = UI.electionNight({ title: L.t('el_local'), share: 50.6, rivalName: S.rival.name, rivalLook: S.rival.look, kind: 'local' }).then(w => { clearInterval(iv); window.__won = w; }); }""")
    page.wait_for_selector('.verdict-big', timeout=40000); m['verdict'] = rec.mark(); page.wait_for_timeout(4500); m['end'] = rec.mark()
    vals = page.evaluate("() => window.__vals"); t0n = m['night_start']
    m['vals'] = [[round(v[0] / 1000 + t0n, 2), v[1], v[2], v[3]] for v in vals[::2]]
    return m


# ---------------------------------------------------------------- Miting: bilerek kötü zamanlama + prompter, sonra kusursuz
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


def rally(page, rec):
    page.evaluate("() => { const {G,Events}=window.__cbs; G.S.week=2; Events.pick=()=>null; G.startWeek(); }"); page.wait_for_timeout(900)
    rec.start(); page.wait_for_timeout(200); m = {'start': rec.mark()}
    start_mission(page, 'rally', 'local', 0)
    page.wait_for_selector('#tap', state='visible'); page.wait_for_timeout(600); m['go1'] = rec.mark()
    page.evaluate("() => { window.__gaf = []; setInterval(() => { const e = document.querySelector('#slg.gaf'); if (e && !window.__gaf.includes(e.textContent)) window.__gaf.push(e.textContent); }, 50); }")
    page.evaluate(PROMPTER_FORCE)
    page.evaluate(RALLY_BOT, {'plan': ['x', 'x', 'p', 'x', 'x']})
    page.wait_for_selector('.prompter', state='visible', timeout=25000); m['prompter'] = rec.mark()
    page.evaluate(PROMPTER_FAIL, 800); m['failed'] = rec.mark()
    page.wait_for_selector('.res', state='visible', timeout=60000); m['res1'] = rec.mark(); page.wait_for_timeout(3000)
    page.locator('.res [data-act=ok]').click(); page.wait_for_timeout(500)
    page.evaluate("() => { if (window.__origRand) { Math.random = window.__origRand; window.__origRand = null; window.__forceWin = null; } }")
    start_mission(page, 'rally', 'local', 0)
    page.wait_for_selector('#tap', state='visible'); page.wait_for_timeout(600); m['go2'] = rec.mark()
    page.evaluate(RALLY_BOT, {'plan': ['p'] * 12})
    page.wait_for_selector('.res', state='visible', timeout=60000); m['res2'] = rec.mark(); page.wait_for_timeout(3500); m['end'] = rec.mark()
    m['gaffes'] = page.evaluate("() => window.__gaf")
    # kurgusal ülkenin şehir adları Türkçe: İngilizce kayıtta "Hello, Yeni Şehir!" gafı çıkarsa kaydı tekrarla (dil tutarlılığı)
    if KLANG != 'tr' and any(ch in g for g in m['gaffes'] for ch in 'ŞşİıĞğÇçÖöÜü'): raise RuntimeError('Türkçe şehir adlı gaf: ' + str(m['gaffes']))
    return m


# ---------------------------------------------------------------- Skandal zinciri: fenomen kartı -> sızan kayıt -> Etiket Savaşı
TREND_BOT = """() => { const st = window.__tw = { taps: 0 };
  const tick = () => { if (!document.querySelector('.tw')) return; setTimeout(tick, 230);
    const fh = document.querySelector('#twf'); if (!fh) return; const fr = fh.getBoundingClientRect();
    const c = [...document.querySelectorAll('.tw-card.fan:not(.hit), .tw-card.meme:not(.hit)')].filter(e => { const r = e.getBoundingClientRect(); return r.top > fr.top + fr.height * 0.25 && r.bottom < fr.bottom - 4; })
      .sort((a, b) => (b.classList.contains('meme') - a.classList.contains('meme')) || (a.getBoundingClientRect().top - b.getBoundingClientRect().top))[0];
    if (c) { c.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, cancelable: true})); st.taps++; } };
  tick(); }"""


def scandal(page, rec):
    page.evaluate("() => { const {G,Events,C}=window.__cbs; G.S.week=4; G.S.tier=1; G.S.scandal=38; G.S.bars.medya=55; Events.pick=()=>C.eventById.influencer; }")
    rec.start(); page.wait_for_timeout(300); m = {'start': rec.mark()}
    page.evaluate("() => { window.__cbs.G.startWeek(); }")
    page.wait_for_selector('.choice', state='visible'); m['card1'] = rec.mark(); page.wait_for_timeout(2600)
    page.evaluate("() => { const o = Math.random; Math.random = () => 0.995; setTimeout(() => { Math.random = o; }, 400); }")
    m['click1'] = rec.mark(); page.locator('.choice').nth(0).click(); page.wait_for_timeout(3800); m['out1'] = rec.mark()
    page.locator('.ov [data-act], .ov .btn').last.click(); page.wait_for_timeout(700)
    # dosya kabardı: bir sonraki hafta sızan ses kaydı (oyunun kendi ifşa olayı)
    page.evaluate("() => { const {G,Events,C}=window.__cbs; G.S.scandal = Math.max(G.S.scandal, 44); G.S.wk.done = true; Events.pick=()=>C.eventById.exp_audio; G.busy=false; G.startWeek(); }")
    page.wait_for_selector('.choice', state='visible'); m['card2'] = rec.mark(); page.wait_for_timeout(2800)
    n = page.locator('.choice').count(); m['n_choices'] = n
    m['click2'] = rec.mark(); page.locator('.choice').nth(n - 1).click()
    page.wait_for_selector('.tw', state='visible', timeout=15000); m['trend_shown'] = rec.mark()
    try: skip_howto(page)
    except Exception: pass
    m['trend_go'] = rec.mark(); page.evaluate(TREND_BOT)
    page.wait_for_selector('.tw', state='detached', timeout=40000); m['trend_end'] = rec.mark()
    page.wait_for_timeout(4500); m['end'] = rec.mark(); m['scandal'] = page.evaluate("() => window.__cbs.G.S.scandal")
    return m


which = sys.argv[1:]
if 'dodge' in which: session('h4_dodge', dodge_ad, ad=True)
if 'strike' in which: session('h4_strike', card_force('strike', 1, 'lose'), ad=True)
if 'strikeA' in which: session('h4_strikeA', card_force('strike', 0), ad=True)
if 'frame' in which: session('h4_frame', frame_ad, ad=True)
if 'night' in which: session('h4_night', night)
# miting kalabalığındaki renkli bayrakçıklar gerçek ülke renkleri olmasın: oyunun kurgusal "Yeni Cumhuriyet" ülkesi
if 'rally' in which: session('h4_rally', rally, opts={'country': 'XX', 'city': 'Yeni Şehir' if KLANG == 'tr' else 'New Town'})
if 'scandal' in which: session('h4_scandal', scandal, toasts=True)
