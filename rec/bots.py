# In-page helpers injected before recording
RALLY_BOT = """(cfg) => {
  window.__rallyBot && cancelAnimationFrame(window.__rallyBot.raf);
  const st = { raf: 0, n: 0, plan: cfg.plan || ['p','p','p','p','p'], lastHit: 0 };
  window.__rallyBot = st;
  const tick = () => {
    st.raf = requestAnimationFrame(tick);
    const cur = document.querySelector('#cur'), zp = document.querySelector('#zp'), zo = document.querySelector('#zo'), tap = document.querySelector('#tap');
    if (!cur || !zp || !tap || tap.offsetParent === null) return;
    if (performance.now() - st.lastHit < 1000) return;
    const p = parseFloat(cur.style.left), l = parseFloat(zp.style.left), w = parseFloat(zp.style.width);
    if (isNaN(p) || isNaN(l)) return;
    const want = st.plan[st.n] || 'p';
    let ok = false;
    if (want === 'p') ok = Math.abs(p - (l + w / 2)) < w * 0.22;
    else { const ol = parseFloat(zo.style.left), ow = parseFloat(zo.style.width); ok = (p < ol - 6 || p > ol + ow + 6); }
    if (ok) { st.lastHit = performance.now(); st.n++; tap.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, cancelable:true})); }
  };
  tick();
}"""

# Force the teleprompter surprise right after hit #2, then solve it like a skilled player
PROMPTER_FORCE = """() => {
  if (window.__origRand) return;
  const orig = Math.random; window.__origRand = orig; window.__forceWin = null;
  Math.random = function () { const w = window.__forceWin; const t = performance.now(); if (w && t >= w[0] && t <= w[1]) return 0.01; return orig(); };
  const prevBot = window.__rallyBot;
  const watch = setInterval(() => { const b = window.__rallyBot; if (b && b.n === 2 && !window.__forceWin) { window.__forceWin = [b.lastHit + 780, b.lastHit + 1400]; clearInterval(watch); } }, 10);
}"""
PROMPTER_SOLVE = """(delay) => new Promise(res => {
  const {C, L} = window.__cbs;
  const iv = setInterval(() => {
    const pr = document.querySelector('.prompter'); if (!pr) return;
    const btns = [...pr.querySelectorAll('[data-o]')]; if (!btns.length) return;
    clearInterval(iv);
    const texts = btns.map(b => b.textContent.trim());
    const set = L.arr(C.prompter).find(s => texts.every(t => s.map(x => x.trim()).includes(t)));
    const order = set.slice(0, 3).map(x => x.trim());
    let i = 0;
    const step = () => { if (i >= 3) return res(order); const b = btns[texts.indexOf(order[i])]; b.dispatchEvent(new PointerEvent('pointerdown', {bubbles:true, cancelable:true})); i++; setTimeout(step, delay); };
    setTimeout(step, delay + 300);
  }, 30);
})"""
