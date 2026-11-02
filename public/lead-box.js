// Caja de captura de emails para los artículos del blog.
// Usa el endpoint y el literal de consentimiento que ya existen (/api/lead, lib/consent.js):
// el texto se pide al servidor y es el mismo que se guarda como prueba.
// Uso: <div id="lead-box" data-source="blog-mi-articulo"></div><script src="/lead-box.js" defer></script>
(function () {
  var host = document.getElementById('lead-box');
  if (!host) return;
  var PACK = '/pack-prompts-juridicos';
  var source = (host.getAttribute('data-source') || 'blog').slice(0, 40);

  var css = document.createElement('style');
  css.textContent =
    '#lead-box .lb{background:#0A1A33;color:#fff;border-radius:10px;padding:28px;margin:40px 0;border-top:3px solid #C99A3B;font-family:inherit}' +
    '#lead-box .lb h3{color:#fff;font-size:22px;line-height:1.2;margin:0 0 8px;font-style:normal;font-weight:700;letter-spacing:-.02em}' +
    '#lead-box .lb h3 em{color:#C99A3B;font-style:normal}' +
    '#lead-box .lb p{color:rgba(255,255,255,.78);font-size:14px;line-height:1.55;margin:0 0 14px}' +
    '#lead-box .lb-row{display:flex;gap:8px;flex-wrap:wrap}' +
    '#lead-box .lb input[type=email]{flex:1;min-width:220px;padding:12px 14px;border-radius:6px;border:1px solid rgba(255,255,255,.25);background:#fff;color:#0A1A33;font-size:15px}' +
    '#lead-box .lb button{padding:12px 20px;border-radius:6px;border:0;background:#C99A3B;color:#0A1A33;font-weight:700;font-size:15px;cursor:pointer}' +
    '#lead-box .lb button:disabled{opacity:.6;cursor:wait}' +
    '#lead-box .lb label{display:flex;gap:9px;align-items:flex-start;margin-top:12px;font-size:12px;line-height:1.5;color:rgba(255,255,255,.7);cursor:pointer}' +
    '#lead-box .lb label input{margin-top:2px;flex-shrink:0;width:16px;height:16px;accent-color:#C99A3B}' +
    '#lead-box .lb label a{color:#E9C77F}' +
    '#lead-box .lb-msg{margin-top:12px;min-height:18px;font-size:14px;color:#fff}' +
    '#lead-box .lb-msg a{color:#C99A3B;font-weight:700}';
  document.head.appendChild(css);

  host.innerHTML =
    '<div class="lb">' +
      '<h3>Pack gratis: <em>12 prompts jurídicos</em> y checklist de confidencialidad</h3>' +
      '<p>Plantillas listas para copiar (contratos, cartas de despido, resúmenes de sentencias, clientes) y la lista de comprobación antes de usar IA con un asunto. Sin tarjeta.</p>' +
      '<form novalidate>' +
        '<div class="lb-row"><input type="email" name="email" placeholder="tu@despacho.com" required autocomplete="email" aria-label="Tu email">' +
        '<button type="submit">Quiero el pack</button></div>' +
        '<label><input type="checkbox" name="consent" required><span class="lb-consent">Acepto recibir emails y la política de privacidad.</span></label>' +
        '<div class="lb-msg" role="status" aria-live="polite"></div>' +
      '</form>' +
    '</div>';

  var form = host.querySelector('form');
  var msg = host.querySelector('.lb-msg');
  var btn = host.querySelector('button');

  fetch('/api/lead/consent').then(function (r) { return r.json(); }).then(function (c) {
    if (c && c.text) host.querySelector('.lb-consent').textContent = c.text;
  }).catch(function () {});

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = form.email.value.trim();
    if (!email || email.indexOf('@') < 1) { msg.textContent = 'Escribe un email válido.'; return; }
    if (!form.consent.checked) { msg.textContent = 'Marca la casilla de consentimiento para recibir el pack.'; return; }
    btn.disabled = true;
    fetch('/api/lead', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, consent: true, source: source })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; });
    }).then(function (res) {
      if (res.ok) {
        msg.innerHTML = '✓ Listo. <a href="' + PACK + '">Abre tu pack de prompts</a>.';
        form.reset();
        if (window.track) window.track('lead_blog', { src: source });
        if (window.gtag) window.gtag('event', 'generate_lead', { source: source });
      } else {
        msg.textContent = (res.j && res.j.error) || 'No se pudo. Inténtalo de nuevo.';
      }
      btn.disabled = false;
    }).catch(function () { msg.textContent = 'Error de red. Inténtalo de nuevo.'; btn.disabled = false; });
  });
})();
