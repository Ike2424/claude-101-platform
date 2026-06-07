// Google Analytics 4 + Consent Mode v2 + banner de cookies — Claude 101
(function () {
  var GA_ID = 'G-1CMXBW0F9R';
  var KEY = 'c101_consent';
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var granted = stored === 'granted';
  gtag('consent', 'default', {
    ad_storage: granted ? 'granted' : 'denied',
    ad_user_data: granted ? 'granted' : 'denied',
    ad_personalization: granted ? 'granted' : 'denied',
    analytics_storage: granted ? 'granted' : 'denied',
    wait_for_update: 500
  });
  gtag('js', new Date());
  gtag('config', GA_ID);
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  function setConsent(value) {
    try { localStorage.setItem(KEY, value); } catch (e) {}
    var g = value === 'granted' ? 'granted' : 'denied';
    gtag('consent', 'update', { ad_storage: g, ad_user_data: g, ad_personalization: g, analytics_storage: g });
  }
  if (stored === 'granted' || stored === 'denied') return;
  function showBanner() {
    if (document.getElementById('c101-cookie-banner')) return;
    var style = document.createElement('style');
    style.textContent = '#c101-cookie-banner{position:fixed;left:12px;right:12px;bottom:12px;z-index:99999;max-width:560px;margin:0 auto;background:#FBF8F0;border:1px solid #E1D8C2;border-radius:14px;padding:16px 18px;box-shadow:0 8px 30px rgba(0,0,0,.16);font-family:-apple-system,BlinkMacSystemFont,sans-serif}#c101-cookie-banner p{margin:0 0 12px;font-size:13px;line-height:1.55;color:#3A352D}#c101-cookie-banner a{color:#C8542B}#c101-cookie-banner .cc-row{display:flex;gap:8px;flex-wrap:wrap}#c101-cookie-banner button{flex:1;min-width:120px;padding:10px 14px;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid #1C1A16}#c101-cookie-banner .cc-accept{background:#1C1A16;color:#F4EFE3}#c101-cookie-banner .cc-reject{background:transparent;color:#1C1A16}';
    document.head.appendChild(style);
    var b = document.createElement('div');
    b.id = 'c101-cookie-banner'; b.setAttribute('role','dialog'); b.setAttribute('aria-label','Aviso de cookies');
    b.innerHTML = '<p>Usamos cookies de analítica para entender cómo se usa la web y mejorarla. Puedes aceptarlas o rechazarlas. <a href="/privacidad">Más información</a>.</p><div class="cc-row"><button class="cc-reject" type="button">Rechazar</button><button class="cc-accept" type="button">Aceptar</button></div>';
    document.body.appendChild(b);
    b.querySelector('.cc-accept').addEventListener('click', function () { setConsent('granted'); b.remove(); });
    b.querySelector('.cc-reject').addEventListener('click', function () { setConsent('denied'); b.remove(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showBanner);
  else showBanner();
})();
