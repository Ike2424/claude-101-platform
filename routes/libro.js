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

@media (max-width: 720px) {
  .chapters { grid-template-columns: 1fr; }
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
    return loadData().chapters.map((c) => c.slug);
  } catch {
    return [];
  }
}

const router = Router();

// GET /libro — índice de capítulos (hub)
router.get('/', (_req, res) => {
  const { book, chapters } = loadData();
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
  <section class="chapters">${cards}</section>`;

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
  const { book, chapters } = loadData();
  const idx = chapters.findIndex((c) => c.slug === req.params.slug);
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
