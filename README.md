# Claude 101 — Plataforma

Curso completo de Claude en español, con landing pública, paywall de Stripe y autenticación passwordless.

## Estructura

```
claude-101-platform/
├── server.js                  Entry point Express
├── package.json
├── .env.example               Copia a .env y rellena
├── db/
│   ├── schema.sql             Esquema (SQLite/Postgres)
│   ├── migrate.js             Script de migración
│   └── claude101.db           (generado, ignorado en git)
├── lib/
│   ├── db.js                  Abstracción SQLite/Postgres
│   ├── stripe.js              Stripe SDK
│   ├── mail.js                Resend/SMTP/console
│   └── token.js               JWT + magic link tokens
├── middleware/
│   ├── requireAuth.js         Verifica JWT en cookie
│   └── requirePaid.js         Verifica has_paid
├── routes/
│   ├── auth.js                Magic link + verify + logout
│   ├── checkout.js            Crea Stripe Checkout Session
│   ├── webhook.js             Procesa eventos de Stripe
│   └── course.js              Progreso del usuario
├── public/                    Servido como estático
│   ├── index.html             Landing pública con pricing
│   ├── login.html             Formulario de magic link
│   ├── verify-pending.html    Pantalla "revisa tu email"
│   ├── success.html           Post-pago
│   ├── app.html               Wrapper logueado (carga course.html en iframe)
│   ├── account.html           Perfil del usuario (gated)
│   ├── admin.html             Panel administrativo (protegido por token)
│   ├── course.html            El curso completo (gated)
│   ├── styles-shared.css      Tema compartido
│   └── claude-101-videos/     Videos animados + assets (gated)
├── Dockerfile                 Imagen para producción
├── .dockerignore
├── fly.toml                   Config para Fly.io
└── docs/production/           Guiones de producción de los videos
```

## Quick start (5 minutos)

```bash
# 1. Instalar dependencias
npm install

# 2. Configurar entorno
cp .env.example .env
# Editar .env: como mínimo JWT_SECRET (openssl rand -hex 32)

# 3. Crear la base de datos
npm run migrate

# 4. Arrancar
npm start
```

Abre `http://localhost:3000`.

**Por defecto** los emails se imprimen en consola (`MAIL_PROVIDER=console`), así que puedes probar el flujo end-to-end sin configurar nada de email todavía.

Para conectar Stripe (y aceptar pagos reales) sigue **[SETUP.md](./SETUP.md)** paso a paso.

## Flujo de usuario

1. Visitante llega a `/` → ve landing con precio.
2. Introduce email y pulsa "Comprar acceso" → `POST /api/checkout` → redirección a Stripe.
3. Paga en Stripe → Stripe redirige a `/success`.
4. En paralelo, Stripe envía webhook `checkout.session.completed` → backend marca al usuario como pagado y envía email con magic link.
5. Usuario hace clic en el email → `GET /api/auth/verify` → cookie de sesión + redirect a `/app`.
6. `/app` carga `course.html` en iframe (ambos gated por auth + paywall).
7. Si pierde el enlace, va a `/login`, mete su email y recibe uno nuevo.

## Seguridad — qué se ha implementado

- **JWT en cookie HTTP-only** (no accesible desde JS, evita XSS-stealing).
- **Magic tokens hasheados** con SHA-256 antes de guardarlos. Si la DB se filtra, los tokens no son utilizables.
- **Single-use + expiración** en los magic tokens (20 min por defecto).
- **Verificación de firma del webhook** de Stripe (`stripe.webhooks.constructEvent`).
- **Idempotencia** de eventos de Stripe (no procesar el mismo `evt_xxx` dos veces).
- **Rate limiting** agresivo en endpoints de auth (6 req/min).
- **Body raw** del webhook se preserva — montaje correcto antes de `express.json()`.
- **Cabeceras de seguridad** básicas (`X-Content-Type-Options`, `X-Frame-Options`, etc).
- **Enumeration-safe**: `/auth/magic-link` responde igual exista el email o no.
- **Revocación automática** ante refunds y disputas de chargeback.

## Panel de administración

Visita `/admin`. Introduce el `ADMIN_TOKEN` de tu `.env`. Tiene 6 pestañas:

- **Visión:** stats principales · curvas de visitas e ingresos por día · embudo de conversión visual (visitas → checkouts → compras).
- **Web:** páginas más visitadas, referrers externos, eventos capturados (checkout_started, cta_click, etc).
- **Curso:** usuarios activos, lecciones más completadas, distribución de progreso.
- **Usuarios:** buscable. Concede / revoca acceso con un clic. Concede acceso por email (con magic link automático).
- **Compras:** últimas transacciones con su estado y session ID de Stripe.
- **Cupones:** crea cupones de descuento (`-20%`, etc), pausa, borra. Se aplican en checkout y en Stripe a la vez.

Selector de rango temporal (7d / 30d / 90d / 1a) en la parte superior.

Genera un token fuerte para producción:
```bash
openssl rand -hex 32
```
y ponlo en `ADMIN_TOKEN` del `.env` de producción.

## Tracking y métricas

La plataforma trae su propio sistema de analytics (no necesitas Google Analytics):

- **Page views** se trackean automáticamente vía `/track.js` (sin cookies, ID anónimo en localStorage).
- **Eventos personalizados** desde el frontend: `window.track('event_name', { ... })`.
- **IP hasheada** con SHA-256, sin guardar IPs en claro (privacy-friendly).
- **Rate-limited** a 60 hits/min por IP.

El admin agrega todo en charts SVG inline (sin libs externas) y un embudo de conversión.

## Cupones de descuento

Crea cupones desde la pestaña "Cupones" del admin. Se aplican de dos formas:

- **En la URL:** `https://tudominio.com/?coupon=VERANO20` autocompleta el campo en la landing.
- **Manual:** el usuario introduce el código en el campo de cupón antes de comprar.

El sistema valida internamente (existe, activo, no caducado, no agotado) y luego pasa un Coupon temporal a Stripe Checkout con el `percent_off` correspondiente. La factura sale con el descuento correctamente reflejado.

## Páginas legales

Incluidas como plantillas mínimas (RGPD-friendly):

- `/terminos` — términos y condiciones
- `/privacidad` — política de privacidad
- `/reembolsos` — política de devolución

**⚠ Plantillas genéricas: adáptalas a tu jurisdicción real y consulta con un abogado antes de producción.**

## Cambiar el precio

En `.env`:
```
COURSE_PRICE_CENTS=4900   # 49,00 €
```

## Cambiar a subscription

Edita `routes/checkout.js` y cambia `mode: 'payment'` por `mode: 'subscription'` + define un precio recurrente en Stripe Dashboard. Tendrás que escuchar también `customer.subscription.deleted` en el webhook para revocar accesos.

## Deploy

Cualquier host que soporte Node.js + variables de entorno:

- **Railway** (recomendado, $5/mes): conecta el repo, define las env vars, ya. Ver `SETUP.md`.
- **Render**: similar.
- **Fly.io**: `fly.toml` y `Dockerfile` ya incluidos. Ver `SETUP.md` sección 4.
- **Docker propio**: `docker build -t claude-101 . && docker run -p 3000:3000 --env-file .env -v $(pwd)/db:/app/db claude-101`
- **VPS clásico**: con PM2 o systemd.

## Licencia y créditos

Contenido del curso © tú. Stack open-source. Anthropic y Claude son marcas de Anthropic, PBC (no afiliada).
