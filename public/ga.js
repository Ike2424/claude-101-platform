// Gestor de consentimiento de cookies/analítica — Claude 101 (RGPD/LSSI art. 22).
// NADA de analítica se carga antes del clic de aceptar. Rechazar es tan visible
// como aceptar. La decisión se guarda en localStorage (c101_consent).
// Cubre: Google Analytics 4, Microsoft Clarity y la analítica propia (track.js).
(function () {
  var GA_ID = 'G-1CMXBW0F9R';
  var CLARITY_ID = 'x3hq8bcs7a';
  var KEY = 'c101_consent';

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadGA() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  function loadClarity() {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
  }
  function startAnalytics() {
    loadGA();
    loadClarity();
    if (window.__c101_startTracking) window.__c101_startTracking(); // analítica propia
  }

  // Permite reabrir la decisión desde la web (p.ej. un enlace en /cookies).
  window.c101SetConsent = function (granted) {
    set(granted ? 'granted' : 'denied');
    if (granted) startAnalytics();
  };

  var decision = get();
  if (decision === 'granted') { startAnalytics(); return; }
  if (decision === 'denied') { return; }

  function showBanner() {
    if (document.getElementById('c101-cookie-banner')) return;
    var style = document.createElement('style');
    style.textContent = '#c101-cookie-banner{position:fixed;left:12px;right:12px;bottom:12px;z-index:99999;max-width:560px;margin:0 auto;background:#FBF8F0;border:1px solid #E1D8C2;border-radius:14px;padding:16px 18px;box-shadow:0 8px 30px rgba(0,0,0,.16);font-family:-apple-system,BlinkMacSystemFont,sans-serif}#c101-cookie-banner p{margin:0 0 12px;font-size:13px;line-height:1.55;color:#3A352D}#c101-cookie-banner a{color:#C8542B}#c101-cookie-banner .cc-row{display:flex;gap:8px;flex-wrap:wrap}#c101-cookie-banner button{flex:1;min-width:120px;padding:10px 14px;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid #1C1A16}#c101-cookie-banner .cc-accept{background:#1C1A16;color:#F4EFE3}#c101-cookie-banner .cc-reject{background:transparent;color:#1C1A16}';
    document.head.appendChild(style);
    var b = document.createElement('div');
    b.id = 'c101-cookie-banner'; b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', 'Aviso de cookies');
    b.innerHTML = '<p>Usamos cookies de analítica (Google Analytics y Microsoft Clarity) <strong>solo si las aceptas</strong>. Puedes rechazarlas y navegar igual. <a href="/cookies">Más información</a>.</p><div class="cc-row"><button class="cc-reject" type="button">Rechazar</button><button class="cc-accept" type="button">Aceptar</button></div>';
    document.body.appendChild(b);
    b.querySelector('.cc-accept').addEventListener('click', function () { set('granted'); b.remove(); startAnalytics(); });
    b.querySelector('.cc-reject').addEventListener('click', function () { set('denied'); b.remove(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showBanner);
  else showBanner();
})();
