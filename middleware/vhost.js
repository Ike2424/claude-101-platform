// vhost — mapea subdominios al path interno equivalente.
// Activable con ENABLE_VHOST=true.
//
// Ejemplos:
//   app.claude101.com/    → req.url = /app
//   admin.claude101.com/  → req.url = /admin
//   blog.claude101.com/X  → req.url = /blog/X
//   www.claude101.com/    → req.url = /
//   claude101.com/        → req.url = / (sin cambio)
//
// Si DNS no está configurado y el host viene directo, este middleware
// no afecta. Es seguro tenerlo activo siempre que ENABLE_VHOST=true.

const SUBDOMAIN_TO_PATH = {
  app: '/app',
  admin: '/admin',
  blog: '/blog',
  recursos: '/recursos',
  docs: '/docs',
  contacto: '/contacto',
  comunidad: '/comunidad',
  sobre: '/sobre',
};

export function vhost(req, _res, next) {
  if (process.env.ENABLE_VHOST !== 'true') return next();
  const root = (process.env.ROOT_DOMAIN || '').toLowerCase();
  if (!root) return next();

  const host = String(req.headers.host || '').toLowerCase().split(':')[0];
  if (!host.endsWith(root)) return next();

  // Extraer subdominio (todo lo que está antes del root)
  let sub = host.slice(0, host.length - root.length).replace(/\.$/, '');
  if (!sub || sub === 'www') return next();

  const target = SUBDOMAIN_TO_PATH[sub];
  if (!target) return next();

  // Si la url interna ya empieza por el target, no la duplicamos
  if (req.url.startsWith(target)) return next();

  // Reescribir: '/' → target, '/algo' → target + '/algo'
  if (req.url === '/' || req.url === '') {
    req.url = target;
  } else {
    req.url = target + req.url;
  }
  next();
}
