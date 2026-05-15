// Tracker minimalista — sin cookies de terceros, sin scripts externos.
// Visitor ID anónimo en localStorage (no es PII).
(function () {
  if (window.__c101_track) return;
  window.__c101_track = true;

  function vid() {
    try {
      let v = localStorage.getItem('c101_vid');
      if (!v) {
        v = (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36));
        localStorage.setItem('c101_vid', v);
      }
      return v;
    } catch { return null; }
  }

  function send(url, payload) {
    try {
      const data = JSON.stringify({ ...payload, visitor_id: vid() });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(url, new Blob([data], { type: 'application/json' }));
      } else {
        fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: data, keepalive: true });
      }
    } catch {}
  }

  function trackPage() {
    send('/api/track/page', {
      path: location.pathname + location.search,
      referrer: document.referrer || null,
    });
  }

  // API pública: window.track('event_name', { meta })
  window.track = function (type, meta) {
    send('/api/track/event', { type, meta: meta || null });
  };

  // Auto-track al cargar
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', trackPage);
  } else {
    trackPage();
  }

  // SPA-friendly: trackea cambios de URL si los hubiera
  let lastPath = location.pathname;
  setInterval(() => {
    if (location.pathname !== lastPath) {
      lastPath = location.pathname;
      trackPage();
    }
  }, 1000);
})();
