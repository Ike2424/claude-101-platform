// Google Analytics 4 (gtag.js) — Claude 101
// Cargador self-hosted: una sola fuente para todas las páginas.
(function () {
  var GA_ID = 'G-1CMXBW0F9R';
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', GA_ID);
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
})();
