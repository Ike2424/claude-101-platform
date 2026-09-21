// Avisa a IndexNow (Bing, Yandex, etc.) de las URLs del sitemap.
// Uso: node scripts/indexnow.mjs [url1 url2 ...]   (sin args: todas las del sitemap público)
const HOST = 'academia101.com';
const KEY = 'fdc1d713279ed95af23c8780fb8404d6';
const SITE = 'https://' + HOST;

let urls = process.argv.slice(2);
if (!urls.length) {
  const xml = await (await fetch(SITE + '/sitemap.xml')).text();
  urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
}
const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: SITE + '/' + KEY + '.txt', urlList: urls }),
});
console.log('IndexNow', res.status, res.statusText, '· URLs enviadas:', urls.length);
