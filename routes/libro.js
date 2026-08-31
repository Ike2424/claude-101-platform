// ============================================================
// /libro — Ampliaciones del libro "IA para Abogados" (José Salto Masáts)
// Páginas PÚBLICAS de "teaser" enlazadas desde los QR del libro.
// Contenido gratuito + hueco para vídeo de YouTube + CTA al curso.
// El material completo vive tras requirePaid; aquí NO se gatea nada.
// Datos en content/libro.json (edita ahí para añadir vídeos/capítulos).
// ============================================================
import { Router } from 'express';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_PATH = path.join(__dirname, '..', 'content', 'libro.json');

// En producción cacheamos; en dev recargamos en cada request para iterar cómodo.
const isProd = process.env.NODE_ENV === 'production';
let _cache = null;
function loadData() {
  if (isProd && _cache) return _cache;
  const data = JSON.parse(readFileSync(DATA_PATH, 'utf-8'));
  _cache = data;
  return data;
}

const esc = (s = '') =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// YouTube id válido: 11 chars [A-Za-z0-9_-]
const isYouTubeId = (id) => typeof id === 'string' && /^[A-Za-z0-9_-]{11}$/.test(id);

const num = (v, def) => (Number.isFinite(Number(v)) ? Number(v) : def);

// Calculadora de ROI del capítulo 1 (valor/hora × horas recuperadas vs. cuota).
function calculatorHTML(c) {
  const cfg = c.calculator && typeof c.calculator === 'object' ? c.calculator : {};
  const d = cfg.defaults || {};
  const rate = num(d.rate, 60);
  const hours = num(d.hours, 20);
  const tool = num(d.toolCost, 20);
  const bench = cfg.benchmark ||
    'El sector estima entre 40 y 100 h/mes en tareas mecánicas; estudios independientes apuntan a ~5 h/semana (≈ 20 h/mes).';
  return `
    <section class="calc" aria-labelledby="calcTitle">
      <div class="calc-head">
        <div class="calc-kicker">Calculadora</div>
        <h2 id="calcTitle">¿Cuánto te ahorra la IA al mes?</h2>
        <p>Pon lo que vale tu hora y las horas que recuperas al mes. Ese número —y no la cuota de la herramienta— es la cuenta que importa.</p>
      </div>
      <div class="calc-grid">
        <div class="calc-controls">
          <div class="calc-field">
            <label class="l" for="cRate">¿Cuánto vale tu hora?</label>
            <span class="v"><input id="cRate" type="number" min="0" max="1000" step="5" value="${rate}" inputmode="numeric"> €/h</span>
            <input id="cRateR" class="range" type="range" min="20" max="300" step="5" value="${rate}" aria-label="Valor de tu hora en euros">
          </div>
          <div class="calc-field">
            <label class="l" for="cHours">¿Cuántas horas recuperas al mes?</label>
            <span class="v"><input id="cHours" type="number" min="0" max="300" step="1" value="${hours}" inputmode="numeric"> h/mes</span>
            <input id="cHoursR" class="range" type="range" min="0" max="100" step="1" value="${hours}" aria-label="Horas recuperadas al mes">
            <span class="hint">${esc(bench)}</span>
          </div>
          <div class="calc-field">
            <label class="l" for="cTool">Cuota mensual de tus herramientas de IA</label>
            <span class="v"><input id="cTool" type="number" min="0" max="1000" step="5" value="${tool}" inputmode="numeric"> €/mes</span>
            <input id="cToolR" class="range" type="range" min="0" max="200" step="5" value="${tool}" aria-label="Cuota mensual de las herramientas">
          </div>
        </div>
        <div class="calc-out" aria-live="polite">
          <div class="calc-big"><span id="oMonth">—</span><small>al mes recuperados</small></div>
          <div class="calc-year"><span id="oYear">—</span> al año</div>
          <div class="calc-net">Descontando la cuota: <strong id="oNet">—</strong> netos al mes</div>
          <div class="calc-ratio" id="oRatio"></div>
        </div>
      </div>
      <p class="calc-foot">Cálculo orientativo. El rango de horas procede de estimaciones del sector y de estudios independientes citados en el libro.</p>
    </section>
    <script>
    (function(){
      var f=new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0,useGrouping:true});
      function g(id){return document.getElementById(id);}
      var pairs=[['cRate','cRateR'],['cHours','cHoursR'],['cTool','cToolR']];
      function calc(){
        var r=Math.max(0,+g('cRate').value||0), h=Math.max(0,+g('cHours').value||0), t=Math.max(0,+g('cTool').value||0);
        var month=r*h, year=month*12, net=month-t;
        g('oMonth').textContent=f.format(month);
        g('oYear').textContent=f.format(year);
        g('oNet').textContent=f.format(net);
        g('oRatio').textContent=(t>0&&month>0)?('Por cada 1 € en la herramienta, recuperas '+Math.round(month/t)+' €.'):'';
      }
      pairs.forEach(function(p){
        var a=g(p[0]), b=g(p[1]);
        a.addEventListener('input',function(){b.value=a.value;calc();});
        b.addEventListener('input',function(){a.value=b.value;calc();});
      });
      calc();
      if(window.track) window.track('libro_calc_view',{n:1});
    })();
    </script>`;
}

// Checklist interactivo (capítulo 9): marcable y persistente en el navegador.
function checklistHTML(c) {
  const cl = c.checklist;
  if (!cl || !Array.isArray(cl.items) || !cl.items.length) return '';
  const key = `web-checklist-c${c.n}`;
  const items = cl.items.map((it, i) => `
      <label class="check-item"><input type="checkbox" data-i="${i}"><span>${esc(it)}</span></label>`).join('');
  const dl = cl.download && cl.download.href ? `
      <a class="doc check-dl" style="max-width:340px;" href="${esc(cl.download.href)}" download onclick="track&&track('libro_textos_base',{n:${c.n}})">
        <div class="dtype">${esc(cl.download.type || 'Descarga')}</div>
        <div class="dname">${esc(cl.download.label)}</div>
        <div class="dgo">⬇ Descargar${cl.download.size ? ` · ${esc(cl.download.size)}` : ''}</div>
      </a>` : '';
  return `
    <section class="check">
      <h2>${esc(cl.title || 'Checklist')}</h2>
      ${cl.intro ? `<p>${esc(cl.intro)}</p>` : ''}
      <div class="check-progress" id="checkProg"></div>
      <div class="check-list">${items}</div>
      ${dl}
    </section>
    <script>
    (function(){
      var KEY=${JSON.stringify(key)}, N=${cl.items.length};
      var boxes=[].slice.call(document.querySelectorAll('.check-item input[data-i]'));
      var prog=document.getElementById('checkProg');
      var saved=[];
      try{ saved=JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){}
      function render(){
        var done=boxes.filter(function(b){return b.checked;}).length;
        var msg = done===0?'empieza a marcar' : (done>=N?'¡lista para captar!':'vas bien');
        prog.innerHTML = done+' / '+N+' — <b>'+msg+'</b>';
      }
      boxes.forEach(function(b){
        var i=+b.getAttribute('data-i');
        if(saved.indexOf(i)!==-1) b.checked=true;
        b.addEventListener('change',function(){
          var on=boxes.filter(function(x){return x.checked;}).map(function(x){return +x.getAttribute('data-i');});
          try{ localStorage.setItem(KEY, JSON.stringify(on)); }catch(e){}
          render();
        });
      });
      render();
    })();
    </script>`;
}

// Biblioteca de prompts (capítulo 4): buscador + filtros + copiar.
function promptLibraryHTML(c) {
  const pl = c.promptLibrary;
  if (!pl || !Array.isArray(pl.prompts) || !pl.prompts.length) return '';
  const chips = (pl.categories || []).map((cat) =>
    `<button class="plib-chip" type="button" data-cat="${esc(cat)}" aria-pressed="false">${esc(cat)}</button>`).join('');
  const cards = pl.prompts.map((p, i) => {
    const text = (p.lines || []).join('\n');
    const hay = ((p.title || '') + ' ' + (p.cat || '') + ' ' + text).toLowerCase();
    return `<article class="pcard" data-cat="${esc(p.cat || '')}" data-search="${esc(hay)}">
        <div class="pcard-head"><span class="t">${esc(p.title || '')}</span><span class="tag">${esc(p.cat || '')}</span></div>
        <pre id="pl${c.n}-${i}">${esc(text)}</pre>
        <button class="pcopy" type="button" data-copy="pl${c.n}-${i}">Copiar</button>
      </article>`;
  }).join('');
  return `
    <section class="plib">
      <h2>${esc(pl.title || 'Biblioteca de prompts')}</h2>
      ${pl.intro ? `<p>${esc(pl.intro)}</p>` : ''}
      <div class="plib-controls">
        <input class="plib-search" type="search" placeholder="Buscar prompt…" aria-label="Buscar prompt">
        <div class="plib-chips">${chips}</div>
      </div>
      <div class="plib-count" id="plibCount"></div>
      <div class="plib-list">${cards}</div>
      <div class="plib-empty" id="plibEmpty" style="display:none;">No hay prompts para ese filtro.</div>
    </section>
    <script>
    (function(){
      var search=document.querySelector('.plib-search');
      var chips=[].slice.call(document.querySelectorAll('.plib-chip'));
      var cards=[].slice.call(document.querySelectorAll('.pcard'));
      var count=document.getElementById('plibCount');
      var empty=document.getElementById('plibEmpty');
      var activeCat=null;
      function apply(){
        var q=(search.value||'').trim().toLowerCase(); var vis=0;
        cards.forEach(function(card){
          var okCat=!activeCat || card.getAttribute('data-cat')===activeCat;
          var okQ=!q || card.getAttribute('data-search').indexOf(q)!==-1;
          var show=okCat&&okQ; card.classList.toggle('hidden',!show); if(show)vis++;
        });
        count.textContent=vis+' prompt'+(vis===1?'':'s');
        empty.style.display=vis?'none':'block';
      }
      search.addEventListener('input',apply);
      chips.forEach(function(ch){ ch.addEventListener('click',function(){
        var cat=ch.getAttribute('data-cat'); activeCat=(activeCat===cat)?null:cat;
        chips.forEach(function(x){x.setAttribute('aria-pressed', x.getAttribute('data-cat')===activeCat?'true':'false');});
        apply();
      });});
      function fallback(txt,cb){ var t=document.createElement('textarea'); t.value=txt; document.body.appendChild(t); t.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(t); cb(); }
      document.querySelectorAll('.pcopy').forEach(function(btn){ btn.addEventListener('click',function(){
        var el=document.getElementById(btn.getAttribute('data-copy')); var txt=el.textContent;
        function done(){ btn.textContent='¡Copiado!'; btn.classList.add('ok'); setTimeout(function(){btn.textContent='Copiar';btn.classList.remove('ok');},1500); if(window.track)window.track('libro_prompt_copy'); }
        if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(txt).then(done).catch(function(){fallback(txt,done);}); } else { fallback(txt,done); }
      });});
      apply();
    })();
    </script>`;
}

// Explorador Tareas → herramientas + ROI (capítulo 11).
function explorerHTML(c) {
  const ex = c.explorer;
  if (!ex || !Array.isArray(ex.tasks) || !ex.tasks.length) return '';
  const rate = num((ex.defaults || {}).rate, 60);
  const rows = ex.tasks.map((t, i) => `
      <label class="etask">
        <input type="checkbox" data-h="${Number(t.hours) || 0}" data-i="${i}">
        <span class="info">
          <span class="lab">${esc(t.label)}</span>
          <span class="combo">${esc(t.combo || '')}${t.chapterSlug ? ` · <a href="/libro/${esc(t.chapterSlug)}">cap. ${esc(String(t.chapter))} →</a>` : ''}</span>
        </span>
        <span class="hrs">${Number(t.hours) || 0} h/mes</span>
      </label>`).join('');
  return `
    <section class="expl">
      <h2>${esc(ex.title || 'Tu plan de IA')}</h2>
      ${ex.intro ? `<p>${esc(ex.intro)}</p>` : ''}
      <div class="expl-rate"><label for="exRate">¿Cuánto vale tu hora?</label><input id="exRate" type="number" min="0" max="1000" step="5" value="${rate}"> €/h</div>
      <div class="expl-grid">${rows}</div>
      <div class="expl-out" aria-live="polite">
        <div><div class="n" id="exHours">0 h</div><div class="l">al mes recuperadas</div></div>
        <div><div class="n" id="exMonth">0 €</div><div class="l">al mes</div></div>
        <div><div class="n" id="exYear">0 €</div><div class="l">al año</div></div>
      </div>
      <p class="expl-note">Estimación orientativa: las horas son una referencia para un despacho pequeño. El ahorro real depende de tu volumen y de cómo implementes cada combinación.</p>
    </section>
    <script>
    (function(){
      var KEY='explorer-c${c.n}';
      var f=new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0,useGrouping:true});
      var boxes=[].slice.call(document.querySelectorAll('.etask input[data-i]'));
      var rate=document.getElementById('exRate');
      var saved=[]; try{saved=JSON.parse(localStorage.getItem(KEY)||'[]');}catch(e){}
      function calc(){
        var hrs=0; boxes.forEach(function(b){ if(b.checked) hrs+=(+b.getAttribute('data-h')||0); });
        var r=Math.max(0,+rate.value||0); var month=hrs*r;
        document.getElementById('exHours').textContent=hrs+' h';
        document.getElementById('exMonth').textContent=f.format(month);
        document.getElementById('exYear').textContent=f.format(month*12);
      }
      function save(){ var on=boxes.filter(function(b){return b.checked;}).map(function(b){return +b.getAttribute('data-i');}); try{localStorage.setItem(KEY,JSON.stringify(on));}catch(e){} }
      boxes.forEach(function(b){ var i=+b.getAttribute('data-i'); if(saved.indexOf(i)!==-1)b.checked=true; b.addEventListener('change',function(){save();calc();}); });
      rate.addEventListener('input',calc);
      calc();
    })();
    </script>`;
}

function layout({ title, description, canonical, body }) {
  return `<!DOCTYPE html>
<html lang="es">
<head>
<script src="/ga.js"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${esc(canonical)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,0..100;1,9..144,300..900,0..100&family=Geist:wght@300..700&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles-shared.css">
<style>
.libro-hero { padding: 60px 0 24px; text-align: center; }
.libro-kicker { font-family: var(--mono); font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
.libro-hero h1 { font-family: var(--display); font-style: italic; font-size: clamp(32px, 4.5vw, 54px); line-height: 1.05; margin-bottom: 14px; }
.libro-hero h1 em { font-style: normal; color: var(--accent); }
.libro-hero .lead { color: var(--ink-2); max-width: 60ch; margin: 0 auto; font-size: 17px; line-height: 1.6; }

.chapters { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 20px 0 40px; }
.chapter-card { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 26px; display: flex; flex-direction: column; gap: 10px; text-decoration: none; color: inherit; transition: all .25s var(--ease); }
.chapter-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); border-color: var(--accent); }
.chapter-card .num { font-family: var(--mono); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.chapter-card h3 { font-family: var(--display); font-size: 21px; line-height: 1.2; }
.chapter-card .tag { font-size: 14px; color: var(--ink-2); line-height: 1.55; }
.chapter-card .go { margin-top: auto; padding-top: 6px; font-family: var(--mono); font-size: 12px; color: var(--accent); }

.wrap-narrow { max-width: 760px; margin: 0 auto; }
.crumbs { font-family: var(--mono); font-size: 12px; color: var(--muted); padding-top: 28px; }
.crumbs a { color: var(--muted); }
.teaser-card { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px, 4vw, 38px); margin: 8px 0 22px; }
.teaser-card .tagline { font-family: var(--mono); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin-bottom: 14px; }
.teaser-card p.body { font-size: 17px; line-height: 1.7; color: var(--ink-1); }
.teaser-card h2.inside { font-family: var(--display); font-size: 19px; margin: 24px 0 12px; }
.inside-list { list-style: none; display: grid; gap: 10px; }
.inside-list li { position: relative; padding-left: 26px; color: var(--ink-2); line-height: 1.55; }
.inside-list li::before { content: "✓"; position: absolute; left: 0; top: 0; color: var(--accent); font-weight: 700; }

.video-frame { position: relative; width: 100%; aspect-ratio: 16 / 9; border-radius: var(--r-md); overflow: hidden; border: 1px solid var(--line); margin: 6px 0 4px; background: #000; }
.video-frame iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.video-soon { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; height: 100%; background: linear-gradient(135deg, var(--ink), #2a2a2a); color: rgba(244,239,227,.85); text-align: center; padding: 20px; }
.video-soon .em { font-size: 30px; }
.video-soon .t { font-family: var(--display); font-style: italic; font-size: 20px; }
.video-soon .s { font-size: 13px; color: rgba(244,239,227,.6); max-width: 40ch; }
.video-cap { font-family: var(--mono); font-size: 11px; color: var(--muted); text-align: center; margin-top: 6px; }

.cta-book { background: var(--ink); color: var(--bg); border-radius: var(--r-xl); padding: clamp(26px, 4vw, 40px); text-align: center; margin: 26px 0; }
.cta-book h2 { color: var(--bg); font-family: var(--display); font-style: italic; font-size: 26px; margin-bottom: 10px; }
.cta-book h2 em { color: var(--accent); font-style: normal; }
.cta-book p { color: rgba(244,239,227,.72); margin: 0 auto 20px; max-width: 52ch; line-height: 1.6; }
.cta-actions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
/* El .btn-ghost global usa texto oscuro; sobre el fondo oscuro del CTA hay que aclararlo */
.cta-book .btn-ghost { color: var(--bg); border-color: rgba(244,239,227,.4); }
.cta-book .btn-ghost:hover { color: var(--ink); background: var(--bg); border-color: var(--bg); }

.chap-nav { display: flex; justify-content: space-between; gap: 12px; margin: 10px 0 60px; font-family: var(--mono); font-size: 13px; }
.chap-nav a { color: var(--accent); }
.chap-nav span { color: var(--muted); }

/* Calculadora de ROI (capítulo 1) */
.calc { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px,4vw,34px); margin: 8px 0 22px; }
.calc-kicker { font-family: var(--mono); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.calc-head h2 { font-family: var(--display); font-size: clamp(22px,3vw,30px); line-height: 1.1; margin-bottom: 8px; }
.calc-head p { color: var(--ink-2); line-height: 1.6; max-width: 62ch; font-size: 15px; }
.calc-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: 24px; margin-top: 24px; align-items: stretch; }
.calc-controls { display: grid; gap: 20px; align-content: start; }
.calc-field { display: grid; gap: 8px; }
.calc-field .l { font-weight: 600; font-size: 15px; color: var(--ink); }
.calc-field .v { font-family: var(--mono); font-size: 13px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
.calc-field .v input { width: 90px; font-family: var(--mono); font-size: 15px; padding: 6px 8px; border: 1px solid var(--line-2); border-radius: 8px; background: var(--bg); color: var(--ink); }
.calc-field .range { width: 100%; accent-color: var(--accent); cursor: pointer; }
.calc-field .hint { font-size: 12px; color: var(--muted); line-height: 1.5; }
.calc-out { background: var(--ink); color: var(--bg); border-radius: var(--r-md); padding: 26px 24px; text-align: center; display: flex; flex-direction: column; justify-content: center; }
.calc-big { display: flex; flex-direction: column; gap: 2px; }
.calc-big span { font-family: var(--display); font-size: clamp(36px,6vw,50px); color: var(--accent); font-weight: 600; line-height: 1; }
.calc-big small { color: rgba(244,239,227,.7); font-size: 13px; }
.calc-year { margin-top: 14px; font-size: 15px; color: rgba(244,239,227,.9); }
.calc-year span { font-weight: 600; }
.calc-net { margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(244,239,227,.15); font-size: 14px; color: rgba(244,239,227,.85); }
.calc-net strong { color: var(--bg); }
.calc-ratio { margin-top: 10px; font-size: 13px; color: rgba(244,239,227,.7); min-height: 18px; }
.calc-foot { font-size: 12px; color: var(--muted); margin-top: 16px; line-height: 1.5; }

/* Caso práctico (García) */
.caso-card { grid-column: 1 / -1; background: linear-gradient(135deg, var(--ink), #2b2620); color: var(--bg); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 30px; display: flex; flex-direction: column; gap: 10px; text-decoration: none; transition: all .25s var(--ease); }
.caso-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.caso-card .badge { align-self: flex-start; font-family: var(--mono); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--ink); background: var(--accent); padding: 4px 11px; border-radius: 100px; }
.caso-card h3 { font-family: var(--display); font-style: italic; font-size: 26px; color: var(--bg); line-height: 1.1; }
.caso-card .tag { color: rgba(244,239,227,.75); font-size: 15px; line-height: 1.55; max-width: 66ch; }
.caso-card .go { font-family: var(--mono); font-size: 12px; color: var(--accent); margin-top: 4px; }

.caso-proto { font-family: var(--mono); font-size: 13px; color: var(--ink-2); background: var(--bg-3); border-radius: var(--r-md); padding: 14px 16px; margin: 0 0 28px; text-align: center; line-height: 1.5; }

.timeline { margin: 6px 0 30px; }
.tl-item { display: grid; grid-template-columns: 44px 1fr; gap: 16px; }
.tl-rail { display: flex; flex-direction: column; align-items: center; }
.tl-badge { width: 40px; height: 40px; border-radius: 50%; background: var(--accent); color: var(--bg); font-family: var(--display); font-weight: 600; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
.tl-line { width: 2px; flex: 1; background: var(--line-2); margin: 6px 0; }
.tl-item:last-child .tl-line { display: none; }
.tl-body { padding-bottom: 26px; }
.tl-cap { font-family: var(--mono); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.tl-body h3 { font-family: var(--display); font-size: 20px; margin: 2px 0 6px; }
.tl-body p { color: var(--ink-2); line-height: 1.6; font-size: 15px; margin-bottom: 8px; }
.tl-body a { font-family: var(--mono); font-size: 12px; }

.demo { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px,4vw,30px); margin: 0 0 26px; }
.demo h2 { font-family: var(--display); font-size: clamp(20px,3vw,26px); margin-bottom: 6px; }
.demo > p { color: var(--ink-2); font-size: 15px; margin-bottom: 16px; }
.demo-tabs { display: inline-flex; background: var(--bg-3); border-radius: 100px; padding: 4px; gap: 4px; margin-bottom: 18px; }
.demo-tab { font-family: var(--mono); font-size: 12px; padding: 8px 16px; border-radius: 100px; border: 0; background: transparent; color: var(--ink-2); cursor: pointer; transition: all .15s var(--ease); }
.demo-tab[aria-selected="true"] { background: var(--card); color: var(--ink); box-shadow: var(--shadow-sm); }
.demo-panel { display: none; }
.demo-panel[data-active="true"] { display: block; }
.demo-block { margin-bottom: 14px; }
.demo-block .lbl { font-family: var(--mono); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.demo-prompt { font-family: var(--mono); font-size: 13px; line-height: 1.6; white-space: pre-wrap; background: var(--ink); color: var(--bg); padding: 16px; border-radius: var(--r-md); }
.demo-result { font-size: 15px; line-height: 1.6; color: var(--ink-1); border-left: 3px solid var(--accent); padding: 4px 0 4px 14px; }

.docs { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin: 0 0 10px; }
.doc { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-md); padding: 18px; display: flex; flex-direction: column; gap: 8px; text-decoration: none; color: inherit; transition: all .2s var(--ease); }
.doc:hover { border-color: var(--accent); transform: translateY(-2px); }
.doc .dtype { font-family: var(--mono); font-size: 10px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.doc .dname { font-weight: 600; font-size: 15px; }
.doc .dgo { font-family: var(--mono); font-size: 12px; color: var(--accent); margin-top: auto; }
.docs-note { font-size: 12px; color: var(--muted); text-align: center; margin: 8px 0 28px; }

/* Checklist interactivo (capítulo 9) */
.check { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px,4vw,30px); margin: 0 0 26px; }
.check h2 { font-family: var(--display); font-size: clamp(20px,3vw,26px); margin-bottom: 6px; }
.check > p { color: var(--ink-2); font-size: 15px; margin-bottom: 16px; }
.check-progress { font-family: var(--mono); font-size: 13px; color: var(--muted); margin-bottom: 14px; }
.check-progress b { color: var(--accent); }
.check-list { display: grid; gap: 2px; margin-bottom: 18px; }
.check-item { display: flex; gap: 12px; align-items: flex-start; padding: 12px; border-radius: var(--r-md); cursor: pointer; transition: background .15s var(--ease); }
.check-item:hover { background: var(--bg-3); }
.check-item input { width: 20px; height: 20px; margin-top: 1px; accent-color: var(--accent); flex-shrink: 0; cursor: pointer; }
.check-item span { font-size: 15px; line-height: 1.5; color: var(--ink-1); }
.check-item input:checked ~ span { color: var(--muted); text-decoration: line-through; }
.check-dl { display: inline-flex; }

/* Biblioteca de prompts (capítulo 4) */
.plib { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px,4vw,30px); margin: 0 0 26px; }
.plib h2 { font-family: var(--display); font-size: clamp(20px,3vw,26px); margin-bottom: 6px; }
.plib > p { color: var(--ink-2); font-size: 14px; line-height: 1.6; margin-bottom: 16px; }
.plib-controls { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 14px; }
.plib-search { flex: 1; min-width: 200px; padding: 10px 14px; border: 1px solid var(--line-2); border-radius: 100px; background: var(--bg); color: var(--ink); font-size: 14px; }
.plib-chips { display: flex; gap: 6px; flex-wrap: wrap; }
.plib-chip { font-family: var(--mono); font-size: 12px; padding: 7px 13px; border-radius: 100px; border: 1px solid var(--line-2); background: transparent; color: var(--ink-2); cursor: pointer; transition: all .15s var(--ease); }
.plib-chip[aria-pressed="true"] { background: var(--accent); color: #fff; border-color: var(--accent); }
.plib-count { font-family: var(--mono); font-size: 12px; color: var(--muted); margin-bottom: 12px; }
.plib-list { display: grid; gap: 12px; }
.pcard { border: 1px solid var(--line); border-radius: var(--r-md); padding: 16px; background: var(--bg-2); }
.pcard.hidden { display: none; }
.pcard-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 10px; }
.pcard-head .t { font-weight: 600; font-size: 15px; }
.pcard-head .tag { font-family: var(--mono); font-size: 10px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); flex-shrink: 0; }
.pcard pre { font-family: var(--mono); font-size: 12.5px; line-height: 1.6; white-space: pre-wrap; background: var(--ink); color: var(--bg); padding: 14px; border-radius: 8px; margin: 0 0 10px; overflow-x: auto; }
.pcopy { font-family: var(--mono); font-size: 12px; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--line-2); background: var(--card); color: var(--ink); cursor: pointer; transition: all .15s var(--ease); }
.pcopy.ok { background: var(--accent); color: #fff; border-color: var(--accent); }
.plib-empty { color: var(--muted); font-size: 14px; padding: 16px 0; }

/* Explorador Tareas → herramientas + ROI (capítulo 11) */
.expl { background: var(--card); border: 1px solid var(--line); border-radius: var(--r-lg); padding: clamp(22px,4vw,30px); margin: 0 0 26px; }
.expl h2 { font-family: var(--display); font-size: clamp(20px,3vw,26px); margin-bottom: 6px; }
.expl > p { color: var(--ink-2); font-size: 14px; line-height: 1.6; margin-bottom: 16px; }
.expl-rate { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; font-size: 14px; font-weight: 600; }
.expl-rate input { width: 90px; padding: 6px 8px; border: 1px solid var(--line-2); border-radius: 8px; background: var(--bg); color: var(--ink); font-family: var(--mono); font-size: 15px; }
.expl-grid { display: grid; gap: 8px; margin-bottom: 20px; }
.etask { display: flex; gap: 12px; align-items: flex-start; padding: 14px; border: 1px solid var(--line); border-radius: var(--r-md); cursor: pointer; transition: border-color .15s var(--ease); }
.etask:hover { border-color: var(--accent); }
.etask input { width: 20px; height: 20px; margin-top: 2px; accent-color: var(--accent); flex-shrink: 0; cursor: pointer; }
.etask .info { flex: 1; }
.etask .lab { font-weight: 600; font-size: 15px; display: block; }
.etask .combo { font-size: 13px; color: var(--ink-2); margin-top: 2px; }
.etask .hrs { font-family: var(--mono); font-size: 12px; color: var(--muted); white-space: nowrap; }
.expl-out { background: var(--ink); color: var(--bg); border-radius: var(--r-md); padding: 22px; display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; text-align: center; }
.expl-out .n { font-family: var(--display); font-size: clamp(24px,4vw,34px); color: var(--accent); font-weight: 600; line-height: 1; }
.expl-out .l { font-size: 12px; color: rgba(244,239,227,.7); margin-top: 4px; }
.expl-note { font-size: 12px; color: var(--muted); margin-top: 14px; line-height: 1.5; }

@media (max-width: 720px) {
  .chapters { grid-template-columns: 1fr; }
  .calc-grid { grid-template-columns: 1fr; }
  .docs { grid-template-columns: 1fr; }
  .expl-out { grid-template-columns: 1fr; }
}
</style>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/favicon.svg">
</head>
<body>
<a href="#main" class="skip-link">Saltar al contenido</a>
<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="brand">Claude<em>·101</em></a>
    <div class="nav-links">
      <a href="/libro">El libro</a>
      <a href="/blog">Blog</a>
      <a href="/#precio">Curso</a>
      <a href="/login" class="btn btn-ghost btn-sm">Ya tengo acceso</a>
    </div>
  </div>
</nav>
<main id="main" class="container">
${body}
</main>
<footer class="foot">
  <div class="foot-inner">
    <div class="foot-bottom">
      <a href="/" class="brand">Claude<em>·101</em></a>
      <div>
        <a href="/terminos">Términos</a> · <a href="/privacidad">Privacidad</a> · <a href="/contacto">Contacto</a>
      </div>
    </div>
  </div>
</footer>
<script src="/track.js"></script>
</body>
</html>`;
}

// Para el sitemap: lista de slugs de capítulos.
export function getChapterSlugs() {
  try {
    const d = loadData();
    const slugs = d.chapters.map((c) => c.slug);
    if (d.caso && d.caso.slug) slugs.push(d.caso.slug);
    return slugs;
  } catch {
    return [];
  }
}

// Página del caso práctico (recorrido + demo prompt + documentos ficticios).
function casoHTML(caso, book) {
  const stages = (caso.stages || []).map((s) => `
    <div class="tl-item">
      <div class="tl-rail"><div class="tl-badge">${esc(s.n)}</div><div class="tl-line"></div></div>
      <div class="tl-body">
        <div class="tl-cap">Entrega ${esc(s.n)}${s.chapter ? ` · Capítulo ${esc(String(s.chapter))}` : ''}</div>
        <h3>${esc(s.title)}</h3>
        <p>${esc(s.text)}</p>
        ${s.chapterSlug ? `<a href="/libro/${esc(s.chapterSlug)}">Ver el capítulo ${esc(String(s.chapter))} →</a>` : ''}
      </div>
    </div>`).join('');

  const d = caso.demo || {};
  const demo = d.bad && d.good ? `
    <section class="demo">
      <h2>El mismo caso, dos prompts</h2>
      <p>La diferencia no está en la IA, sino en cómo le hablas. Compáralo:</p>
      <div class="demo-tabs" role="tablist">
        <button class="demo-tab" role="tab" aria-selected="true" data-tab="bad">Prompt genérico</button>
        <button class="demo-tab" role="tab" aria-selected="false" data-tab="good">Prompt jurídico</button>
      </div>
      <div class="demo-panel" data-tab="bad" data-active="true">
        <div class="demo-block"><div class="lbl">Lo que escribes</div><div class="demo-prompt">${esc(d.bad.prompt)}</div></div>
        <div class="demo-block"><div class="lbl">Lo que obtienes</div><div class="demo-result">${esc(d.bad.result)}</div></div>
      </div>
      <div class="demo-panel" data-tab="good" data-active="false">
        <div class="demo-block"><div class="lbl">Lo que escribes</div><div class="demo-prompt">${esc(d.good.prompt)}</div></div>
        <div class="demo-block"><div class="lbl">Lo que obtienes</div><div class="demo-result">${esc(d.good.result)}</div></div>
      </div>
    </section>` : '';

  const docs = caso.docs && caso.docs.length ? `
    <h2 class="inside" style="text-align:center;">Documentos del caso <span style="color:var(--muted);font-weight:400;font-style:italic;">(ficticios, para practicar)</span></h2>
    <div class="docs">
      ${caso.docs.map((doc) => `
        <a class="doc" href="${esc(doc.href)}" download onclick="track&&track('caso_doc',{f:'${esc(doc.label)}'})">
          <div class="dtype">${esc(doc.type || 'Descarga')}</div>
          <div class="dname">${esc(doc.label)}</div>
          <div class="dgo">⬇ Descargar${doc.size ? ` · ${esc(doc.size)}` : ''}</div>
        </a>`).join('')}
    </div>
    <p class="docs-note">Documentos de ejemplo, ficticios y anonimizados. No son asesoramiento jurídico.</p>` : '';

  const body = `
  <nav class="crumbs wrap-narrow"><a href="/libro">← Todas las ampliaciones</a></nav>
  <header class="libro-hero wrap-narrow">
    <div class="libro-kicker">${esc(book.title)} · ${esc(caso.kicker || 'Caso práctico')}</div>
    <h1>${esc(caso.title)}</h1>
    ${caso.intro ? `<p class="lead">${esc(caso.intro)}</p>` : ''}
  </header>
  <div class="wrap-narrow">
    ${caso.protagonista ? `<div class="caso-proto">${esc(caso.protagonista)}</div>` : ''}
    <div class="timeline">${stages}</div>
    ${demo}
    ${docs}
    <section class="cta-book">
      <h2>El caso completo, <em>dentro</em></h2>
      <p>El paso a paso de cada entrega —con los prompts, la configuración y el flujo real— está en la plataforma. Acceso completo, un único pago.</p>
      <div class="cta-actions">
        <a class="btn btn-accent btn-lg" href="/#precio" onclick="track&&track('caso_cta_precio')">Ver el curso completo</a>
        <a class="btn btn-ghost btn-lg" href="/login">Ya tengo acceso</a>
      </div>
    </section>
    <nav class="chap-nav"><a href="/libro">← Todas las ampliaciones</a><span></span></nav>
  </div>
  <script>
  (function(){
    var tabs=[].slice.call(document.querySelectorAll('.demo-tab'));
    var panels=[].slice.call(document.querySelectorAll('.demo-panel'));
    tabs.forEach(function(t){
      t.addEventListener('click',function(){
        tabs.forEach(function(x){x.setAttribute('aria-selected', x===t?'true':'false');});
        panels.forEach(function(p){p.setAttribute('data-active', p.getAttribute('data-tab')===t.getAttribute('data-tab')?'true':'false');});
      });
    });
  })();
  </script>`;

  return layout({
    title: `${caso.title} · ${book.title}`,
    description: (caso.intro || caso.title).slice(0, 155),
    canonical: `/libro/${caso.slug}`,
    body,
  });
}

const router = Router();

// GET /libro — índice de capítulos (hub)
router.get('/', (_req, res) => {
  const { book, chapters, caso } = loadData();
  const casoCard = caso ? `
    <a class="caso-card" href="/libro/${esc(caso.slug)}" onclick="track&&track('libro_caso_open')">
      <span class="badge">${esc(caso.kicker || 'Caso práctico')}</span>
      <h3>${esc(caso.title)}</h3>
      <div class="tag">${esc(caso.intro || caso.tagline || '')}</div>
      <div class="go">Abrir el caso →</div>
    </a>` : '';
  const cards = chapters.map((c) => `
    <a class="chapter-card" href="/libro/${esc(c.slug)}" onclick="track&&track('libro_chapter_open',{n:${c.n}})">
      <div class="num">Capítulo ${c.n}</div>
      <h3>${esc(c.title)}</h3>
      <div class="tag">${esc(c.tagline)}</div>
      <div class="go">Abrir ampliación →</div>
    </a>`).join('');

  const body = `
  <header class="libro-hero">
    <div class="libro-kicker">${esc(book.title)} · ${esc(book.author)}</div>
    <h1>Amplía el <em>libro</em></h1>
    <p class="lead">${esc(book.intro)}</p>
  </header>
  <section class="chapters">${casoCard}${cards}</section>`;

  res.set('Cache-Control', 'no-cache');
  res.send(layout({
    title: `Amplía el libro · ${book.title}`,
    description: `Recursos y vídeos que amplían "${book.title}" de ${book.author}. Adelanto gratuito; el material completo, dentro de la plataforma.`,
    canonical: '/libro',
    body,
  }));
});

// GET /libro/:slug — página de un capítulo
router.get('/:slug', (req, res) => {
  const { book, chapters, caso } = loadData();
  // Caso práctico (García): página propia
  if (caso && req.params.slug === caso.slug) {
    res.set('Cache-Control', 'no-cache');
    return res.send(casoHTML(caso, book));
  }
  let idx = chapters.findIndex((c) => c.slug === req.params.slug);
  if (idx === -1) {
    // Alias numérico /libro/cap-N (el libro enlaza así algunos capítulos)
    const m = /^cap-(\d+)$/.exec(req.params.slug);
    if (m) idx = chapters.findIndex((c) => String(c.n) === m[1]);
  }
  if (idx === -1) return res.redirect('/libro'); // QR mal escaneado → al hub del libro
  const c = chapters[idx];
  const prev = chapters[idx - 1];
  const next2 = chapters[idx + 1];

  const bullets = (c.bullets || []).map((b) => `<li>${esc(b)}</li>`).join('');

  const video = isYouTubeId(c.videoId)
    ? `<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/${esc(c.videoId)}?rel=0" title="${esc(c.title)}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
       <div class="video-cap">Vídeo del capítulo ${c.n}</div>`
    : `<div class="video-frame"><div class="video-soon"><div class="em">🎬</div><div class="t">Vídeo en preparación</div><div class="s">El vídeo-tutorial de este capítulo estará disponible muy pronto. Guarda esta página.</div></div></div>`;

  const resource = c.resource && c.resource.href
    ? `<p style="margin-top:18px;"><a class="btn btn-ghost btn-sm" href="${esc(c.resource.href)}" download onclick="track&&track('libro_resource',{n:${c.n}})">⬇ ${esc(c.resource.label || 'Descargar recurso')}</a></p>`
    : '';

  const calculator = c.calculator ? calculatorHTML(c) : '';
  const checklist = checklistHTML(c);
  const promptLibrary = promptLibraryHTML(c);
  const explorer = explorerHTML(c);

  const resources = c.resources && c.resources.length ? `
    <h2 class="inside" style="text-align:center;">${esc(c.resourcesTitle || 'Descargas del capítulo')}</h2>
    <div class="docs">
      ${c.resources.map((r) => `
        <a class="doc" href="${esc(r.href)}" download onclick="track&&track('libro_resource_dl',{n:${c.n}})">
          <div class="dtype">${esc(r.type || 'Descarga')}</div>
          <div class="dname">${esc(r.label)}</div>
          <div class="dgo">⬇ Descargar${r.size ? ` · ${esc(r.size)}` : ''}</div>
        </a>`).join('')}
    </div>
    ${c.resourcesNote ? `<p class="docs-note">${esc(c.resourcesNote)}</p>` : ''}` : '';

  const body = `
  <nav class="crumbs wrap-narrow"><a href="/libro">← Todas las ampliaciones</a></nav>
  <header class="libro-hero wrap-narrow">
    <div class="libro-kicker">${esc(book.title)} · Capítulo ${c.n}</div>
    <h1>${esc(c.title)}</h1>
  </header>

  <div class="wrap-narrow">
    <article class="teaser-card">
      <div class="tagline">${esc(c.tagline)}</div>
      <p class="body">${esc(c.teaser)}</p>
      ${bullets ? `<h2 class="inside">Dentro del curso completo</h2><ul class="inside-list">${bullets}</ul>` : ''}
      ${resource}
    </article>

    ${calculator}

    ${promptLibrary}

    ${resources}

    ${checklist}

    ${explorer}

    ${video}

    <section class="cta-book">
      <h2>Esto es solo <em>el aperitivo</em></h2>
      <p>Las plantillas, los casos reales y los ejercicios paso a paso de este capítulo están dentro de la plataforma. Acceso completo, un único pago.</p>
      <div class="cta-actions">
        <a class="btn btn-accent btn-lg" href="/#precio" onclick="track&&track('libro_cta_precio',{n:${c.n}})">Ver el curso completo</a>
        <a class="btn btn-ghost btn-lg" href="/login">Ya tengo acceso</a>
      </div>
    </section>

    <nav class="chap-nav">
      ${prev ? `<a href="/libro/${esc(prev.slug)}">← Cap. ${prev.n}</a>` : '<span></span>'}
      ${next2 ? `<a href="/libro/${esc(next2.slug)}">Cap. ${next2.n} →</a>` : '<span></span>'}
    </nav>
  </div>`;

  res.set('Cache-Control', 'no-cache');
  res.send(layout({
    title: `${c.title} · ${book.title}`,
    description: c.teaser.slice(0, 155),
    canonical: `/libro/${c.slug}`,
    body,
  }));
});

export default router;
