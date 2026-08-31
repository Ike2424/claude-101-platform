// Analítica propia — SOLO tras consentimiento (c101_consent === 'granted').
// window.track siempre existe (para no romper onclick), pero no envía ni crea
// el identificador c101_vid hasta que hay consentimiento.
(function () {
  if (window.__c101_track_init) return;
  window.__c101_track_init = true;

  function consented() {
    try { return localStorage.getItem('c101_consent') === 'granted'; } catch (e) { return false; }
  }

  function vid() {
    try {
      var v = localStorage.getItem('c101_vid');
      if (!v) {
        v = (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36));
        localStorage.setItem('c101_vid', v);
      }
      return v;
    } catch { return null; }
  }

  function send(url, payload) {
    if (!consented()) return; // sin consentimiento: nada sale ni se crea c101_vid
    try {
      var data = JSON.stringify(Object.assign({}, payload, { visitor_id: vid() }));
      if (navigator.sendBeacon) {
        navigator.sendBeacon(url, new Blob([data], { type: 'application/json' }));
      } else {
        fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: data, keepalive: true });
      }
    } catch {}
  }

  function trackPage() {
    send('/api/track/page', { path: location.pathname + location.search, referrer: document.referrer || null });
  }

  // API pública
  window.track = function (type, meta) { send('/api/track/event', { type: type, meta: meta || null }); };

  var started = false;
  function start() {
    if (started) return;
    started = true;
    trackPage();
    var lastPath = location.pathname;
    setInterval(function () {
      if (location.pathname !== lastPath) { lastPath = location.pathname; trackPage(); }
    }, 1000);
  }
  // El gestor de consentimiento llama a esto al aceptar.
  window.__c101_startTracking = start;

  // Autoarranque solo si ya había consentimiento de una visita anterior.
  if (consented()) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
    else start();
  }
})();
