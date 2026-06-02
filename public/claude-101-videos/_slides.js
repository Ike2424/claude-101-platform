// Slides engine — usa window.MODULE_DATA definido por cada Mx-slides.html
(function () {
  const D = window.MODULE_DATA;
  if (!D) { document.body.innerHTML = '<div style="padding:40px;text-align:center;font-family:system-ui;">Error: MODULE_DATA no definido</div>'; return; }

  // === ESTADO ===
  const slides = D.slides;
  const TOTAL = slides.length;
  const state = {
    current: 0,
    completed: new Set(),
    score: { correct: 0, total: 0 },
    sub: {}, // sub-state per slide
  };

  // === SCAFFOLD ===
  document.title = `Claude 101 · Módulo ${D.module} · Slides`;
  document.body.innerHTML = `
    <div class="header">
      <div class="header-left">
        <button class="exit-btn" id="exitBtn" type="button" aria-label="Volver a los módulos">
          <span class="exit-btn-arrow">←</span><span class="exit-btn-label">Salir</span>
        </button>
        <div class="brand">Claude<em>·101</em> <span class="brand-tag">Módulo ${D.module} · Slides</span></div>
      </div>
      <div class="slide-counter"><strong id="slideNum">1</strong> <span style="opacity:.5;">/</span> <span id="slideTotal">${TOTAL}</span></div>
    </div>
    <div class="stage" id="stage"></div>
    <div class="controls">
      <button class="nav-btn" id="btnPrev">← <span class="nav-btn-label">Anterior</span></button>
      <div class="dots" id="dots"></div>
      <button class="nav-btn primary" id="btnNext"><span class="nav-btn-label">Siguiente</span> →</button>
    </div>
  `;

  const stage = document.getElementById('stage');
  const dotsEl = document.getElementById('dots');
  const btnPrev = document.getElementById('btnPrev');
  const btnNext = document.getElementById('btnNext');
  const slideNum = document.getElementById('slideNum');

  // Render placeholders
  slides.forEach((s, i) => {
    const el = document.createElement('div');
    el.className = 'slide' + (i === 0 ? ' active' : '');
    el.dataset.idx = i;
    el.innerHTML = '<div class="slide-inner"></div>';
    stage.appendChild(el);

    const dot = document.createElement('button');
    dot.className = 'dot' + (i === 0 ? ' active' : '');
    dot.dataset.idx = i;
    dot.setAttribute('aria-label', 'Ir a slide ' + (i+1));
    dot.addEventListener('click', () => goTo(i));
    dotsEl.appendChild(dot);
  });

  // === HELPERS ===
  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function scoreQ(ok){ state.score.total += 1; if (ok) state.score.correct += 1; }
  function markCompleted(i){ state.completed.add(i); updateNav(); updateDots(); }

  function updateDots(){
    dotsEl.querySelectorAll('.dot').forEach((d, i) => {
      d.classList.toggle('active', i === state.current);
      d.classList.toggle('done', state.completed.has(i));
    });
  }
  function canAdvance(i){ return i === 0 || state.completed.has(i); }
  function updateNav(){
    btnPrev.disabled = state.current === 0;
    btnNext.innerHTML = state.current === TOTAL - 1
      ? 'Finalizar <span class="nav-btn-label">→</span>'
      : '<span class="nav-btn-label">Siguiente</span> →';
    btnNext.disabled = !canAdvance(state.current) || state.current === TOTAL - 1;
  }
  function goTo(i){
    if (i < 0 || i >= TOTAL) return;
    document.querySelectorAll('.slide').forEach(s => s.classList.toggle('active', parseInt(s.dataset.idx,10) === i));
    state.current = i;
    slideNum.textContent = i + 1;
    updateDots();
    updateNav();
    // Render the slide content lazily on first visit
    const inner = document.querySelectorAll('.slide')[i].querySelector('.slide-inner');
    if (!inner.dataset.rendered) {
      renderSlide(i, inner);
      inner.dataset.rendered = '1';
    }
  }

  // Debounced tap helper for nav
  let lastTap = 0;
  function debounced(fn){ return (e) => { const n = Date.now(); if (n - lastTap < 300) return; lastTap = n; if (e && e.preventDefault) e.preventDefault(); fn(); }; }
  btnPrev.addEventListener('click', debounced(() => goTo(state.current - 1)));
  btnNext.addEventListener('click', debounced(() => { if (state.current !== TOTAL - 1) goTo(state.current + 1); }));
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' && !btnNext.disabled) goTo(state.current + 1);
    else if (e.key === 'ArrowLeft' && !btnPrev.disabled) goTo(state.current - 1);
  });

  // === EXIT BUTTON ===
  function exitToModules(){
    try { if (window.parent && window.parent !== window) window.parent.postMessage({ type: 'slides-exit' }, '*'); } catch(e){}
    try { if (window.top && window.top !== window) { window.top.location.href = '/app'; return; } } catch(e){}
    try { window.location.href = '/app'; } catch(e){ history.back(); }
  }
  document.getElementById('exitBtn').addEventListener('click', exitToModules);

  // === SLIDE RENDERERS ===
  const RENDERERS = {
    intro(i, inner, d){
      const id = `intro_${i}`;
      inner.innerHTML = `
        <div class="eyebrow">${escapeHtml(d.eyebrow || 'Antes de empezar')}</div>
        <h1 class="title">${d.title}</h1>
        <p class="subtitle">${escapeHtml(d.subtitle || 'Toca lo que apliques. Esto solo nos ayuda a personalizar tu camino.')}</p>
        <div class="chips" id="${id}"></div>
        <p style="font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:14px;letter-spacing:.08em;text-transform:uppercase;">Pulsa <strong style="color:var(--ink);">Siguiente</strong> cuando termines</p>
      `;
      const wrap = document.getElementById(id);
      (d.chips || []).forEach(label => {
        const b = document.createElement('button');
        b.className = 'chip';
        b.textContent = label;
        b.addEventListener('click', () => b.classList.toggle('selected'));
        wrap.appendChild(b);
      });
      markCompleted(i);
    },

    choice(i, inner, d){
      const id = `choice_${i}`;
      const fbId = `fb_${i}`;
      const letters = ['A','B','C','D','E'];
      inner.innerHTML = `
        <div class="eyebrow">${escapeHtml(d.eyebrow || 'Pregunta')}</div>
        <h2 class="title">${d.title}</h2>
        ${d.prompt ? `<p class="prompt-text">${d.prompt}</p>` : ''}
        <div class="choices" id="${id}"></div>
        <div class="feedback" id="${fbId}"></div>
      `;
      const wrap = document.getElementById(id);
      d.options.forEach((opt, k) => {
        const b = document.createElement('button');
        b.className = 'choice';
        b.innerHTML = `<span class="choice-letter">${letters[k]}</span><span>${opt}</span>`;
        b.addEventListener('click', () => {
          const all = wrap.querySelectorAll('.choice');
          const isRight = k === d.correct;
          all.forEach((x, j) => { x.classList.add('disabled'); if (j === d.correct) x.classList.add('correct'); });
          if (!isRight) b.classList.add('wrong');
          const fb = document.getElementById(fbId);
          fb.innerHTML = `<strong>${isRight ? '¡Bien!' : 'No exactamente.'}</strong> ${d.feedback}`;
          fb.classList.add('show');
          if (!isRight) fb.classList.add('wrong');
          scoreQ(isRight);
          markCompleted(i);
        });
        wrap.appendChild(b);
      });
    },

    reveal(i, inner, d){
      const id = `reveal_${i}`;
      const fbId = `fb_${i}`;
      inner.innerHTML = `
        <div class="eyebrow">Explora</div>
        <h2 class="title">${d.title}</h2>
        ${d.prompt ? `<p class="prompt-text">${d.prompt}</p>` : '<p class="prompt-text">Toca cada tarjeta para abrirla.</p>'}
        <div class="reveal-grid" id="${id}"></div>
        <div class="feedback" id="${fbId}"></div>
      `;
      const wrap = document.getElementById(id);
      const opened = new Set();
      d.items.forEach((item, k) => {
        const card = document.createElement('div');
        card.className = 'reveal-card';
        card.innerHTML = `
          <div class="reveal-icon">${item.icon}</div>
          <div class="reveal-name">${escapeHtml(item.name)}</div>
          <div class="reveal-tag">${escapeHtml(item.tag || '')}</div>
          <div class="reveal-body">${item.body}</div>
        `;
        card.addEventListener('click', () => {
          card.classList.toggle('open');
          opened.add(k);
          if (opened.size === d.items.length){
            const fb = document.getElementById(fbId);
            fb.innerHTML = `<strong>${d.feedbackHead || 'Bien.'}</strong> ${d.feedback || ''}`;
            fb.classList.add('show');
            markCompleted(i);
          }
        });
        wrap.appendChild(card);
      });
    },

    tf(i, inner, d){
      const id = `tf_${i}`;
      const fbId = `fb_${i}`;
      inner.innerHTML = `
        <div class="eyebrow">¿Verdadero o falso?</div>
        <h2 class="title">${d.title}</h2>
        <p class="prompt-text">${d.statement}</p>
        <div class="tf-row" id="${id}">
          <button class="tf-btn" data-val="true">Verdadero</button>
          <button class="tf-btn" data-val="false">Falso</button>
        </div>
        <div class="feedback" id="${fbId}"></div>
      `;
      const wrap = document.getElementById(id);
      const correctVal = d.correct ? 'true' : 'false';
      wrap.querySelectorAll('.tf-btn').forEach(b => b.addEventListener('click', () => {
        const isRight = b.dataset.val === correctVal;
        wrap.querySelectorAll('.tf-btn').forEach(x => { x.classList.add('disabled'); if (x.dataset.val === correctVal) x.classList.add('correct'); });
        if (!isRight) b.classList.add('wrong');
        const fb = document.getElementById(fbId);
        fb.innerHTML = `<strong>${isRight ? 'Correcto.' : 'Casi.'}</strong> ${d.feedback}`;
        fb.classList.add('show');
        if (!isRight) fb.classList.add('wrong');
        scoreQ(isRight);
        markCompleted(i);
      }));
    },

    scenarios(i, inner, d){
      const fbId = `fb_${i}`;
      inner.innerHTML = `
        <div class="eyebrow">Práctica · <span id="scc_${i}">1 de ${d.list.length}</span></div>
        <h2 class="title">${d.title}</h2>
        <div class="scenario-card">
          <div class="scenario-q">Caso</div>
          <div class="scenario-text" id="sct_${i}">${d.list[0].text}</div>
        </div>
        <div class="choices" id="sch_${i}"></div>
        <div class="scenario-progress" id="scp_${i}">${d.list.map((_, k) => `<div class="scenario-dot ${k === 0 ? 'current' : ''}"></div>`).join('')}</div>
        <div class="feedback" id="${fbId}"></div>
      `;
      let idx = 0;
      const letters = ['A','B','C','D'];
      function render(){
        const item = d.list[idx];
        document.getElementById(`sct_${i}`).textContent = item.text;
        document.getElementById(`scc_${i}`).textContent = (idx + 1) + ' de ' + d.list.length;
        const dots = document.querySelectorAll(`#scp_${i} .scenario-dot`);
        dots.forEach((dot, k) => { dot.classList.remove('done','current'); if (k < idx) dot.classList.add('done'); else if (k === idx) dot.classList.add('current'); });
        const fb = document.getElementById(fbId); fb.classList.remove('show','wrong');
        const wrap = document.getElementById(`sch_${i}`);
        wrap.innerHTML = '';
        item.options.forEach((opt, k) => {
          const b = document.createElement('button');
          b.className = 'choice';
          b.innerHTML = `<span class="choice-letter">${letters[k]}</span><span>${opt}</span>`;
          b.addEventListener('click', () => {
            const isRight = k === item.correct;
            wrap.querySelectorAll('.choice').forEach((x, j) => { x.classList.add('disabled'); if (j === item.correct) x.classList.add('correct'); });
            if (!isRight) b.classList.add('wrong');
            fb.innerHTML = `<strong>${isRight ? '¡Bien!' : 'Casi.'}</strong> ${item.feedback}`;
            fb.classList.add('show');
            if (!isRight) fb.classList.add('wrong');
            scoreQ(isRight);
            setTimeout(() => {
              idx += 1;
              if (idx >= d.list.length) markCompleted(i);
              else render();
            }, 1800);
          });
          wrap.appendChild(b);
        });
      }
      render();
    },

    recap(i, inner, d){
      const fbId = `fb_${i}`;
      inner.innerHTML = `
        <div class="eyebrow">Recap rápido · <span id="rcc_${i}">1 de ${d.list.length}</span></div>
        <h2 class="title" id="rcq_${i}">${d.list[0].q}</h2>
        <div class="choices" id="rch_${i}"></div>
        <div class="feedback" id="${fbId}"></div>
      `;
      let idx = 0;
      const letters = ['A','B','C','D'];
      function render(){
        const item = d.list[idx];
        document.getElementById(`rcq_${i}`).textContent = item.q;
        document.getElementById(`rcc_${i}`).textContent = (idx + 1) + ' de ' + d.list.length;
        const fb = document.getElementById(fbId); fb.classList.remove('show','wrong');
        const wrap = document.getElementById(`rch_${i}`);
        wrap.innerHTML = '';
        item.options.forEach((opt, k) => {
          const b = document.createElement('button');
          b.className = 'choice';
          b.innerHTML = `<span class="choice-letter">${letters[k]}</span><span>${opt}</span>`;
          b.addEventListener('click', () => {
            const isRight = k === item.correct;
            wrap.querySelectorAll('.choice').forEach((x, j) => { x.classList.add('disabled'); if (j === item.correct) x.classList.add('correct'); });
            if (!isRight) b.classList.add('wrong');
            fb.innerHTML = `<strong>${isRight ? 'Eso es.' : 'No exactamente.'}</strong> ${item.explain}`;
            fb.classList.add('show');
            if (!isRight) fb.classList.add('wrong');
            scoreQ(isRight);
            setTimeout(() => {
              idx += 1;
              if (idx >= d.list.length) markCompleted(i);
              else render();
            }, 1600);
          });
          wrap.appendChild(b);
        });
      }
      render();
    },

    final(i, inner, d){
      inner.innerHTML = `
        <div class="eyebrow">${escapeHtml(d.eyebrow || `Has terminado el módulo ${D.module}`)}</div>
        <h1 class="title">${d.title}</h1>
        <p class="subtitle">${d.subtitle}</p>
        <div class="final-stats">
          <div class="final-stat"><div class="final-stat-num" id="fc_${i}">${state.score.correct}</div><div class="final-stat-label">Aciertos</div></div>
          <div class="final-stat"><div class="final-stat-num" id="ft_${i}">${state.score.total}</div><div class="final-stat-label">Preguntas</div></div>
          <div class="final-stat"><div class="final-stat-num" id="fp_${i}">${state.score.total ? Math.round(100 * state.score.correct / state.score.total) : 0}%</div><div class="final-stat-label">Score</div></div>
        </div>
        <button class="final-cta" id="finishBtn_${i}">${escapeHtml(d.ctaLabel || `Marcar M${D.module} como completado →`)}</button>
      `;
      // Refresh stats on first show
      document.getElementById(`fc_${i}`).textContent = state.score.correct;
      document.getElementById(`ft_${i}`).textContent = state.score.total;
      document.getElementById(`fp_${i}`).textContent = (state.score.total ? Math.round(100 * state.score.correct / state.score.total) : 0) + '%';
      markCompleted(i);
      document.getElementById(`finishBtn_${i}`).addEventListener('click', () => {
        try {
          if (window.parent && window.parent !== window){
            window.parent.postMessage({ type: 'slides-complete', module: D.module, score: state.score.correct, total: state.score.total }, '*');
          }
        } catch(e){}
        try {
          fetch('/api/quiz/attempt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify({ module: D.module, score: state.score.correct, total: state.score.total })
          }).catch(() => {});
        } catch {}
        const btn = document.getElementById(`finishBtn_${i}`);
        btn.textContent = `✓ M${D.module} completado`;
        btn.style.background = 'var(--olive)';
      });
    }
  };

  function renderSlide(i, inner){
    const s = slides[i];
    const fn = RENDERERS[s.type];
    if (!fn) { inner.innerHTML = `<p>Tipo de slide desconocido: ${s.type}</p>`; markCompleted(i); return; }
    fn(i, inner, s);
  }

  // Render first slide eagerly
  const firstInner = document.querySelectorAll('.slide')[0].querySelector('.slide-inner');
  renderSlide(0, firstInner);
  firstInner.dataset.rendered = '1';

  updateDots();
  updateNav();
})();
