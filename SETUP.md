# SETUP — Puesta en producción de Claude 101

Guía operativa para pasar de "todo funciona en mi Mac" a **un producto vivo en Internet** que cobra de verdad. Tiempo estimado: **45-60 minutos** si lo haces todo seguido.

---

## ⚡ Resumen visual

```
1. Instalar local + arrancar          (5 min)
2. Stripe (modo TEST)                  (10 min)
3. Email transaccional (Resend)        (10 min)
4. Google OAuth (opcional)             (10 min)
5. Comprar dominio + DNS               (5 min)
6. Desplegar (Railway/Fly)             (10 min)
7. Stripe modo LIVE                    (5 min)
8. Validación final                    (5 min)
```

Hay un comando que te dice **qué te falta**:
```bash
npm run check:prod
```
Ejecútalo cuantas veces quieras durante el proceso.

---

## 1. Instalar local (5 min)

```bash
cd ~/Downloads/claude-101-platform
npm install
cp .env.example .env       # si no existe
npm run migrate
npm run setup-demo
npm start
```

Abre `http://localhost:3000`. Pulsa el magic link impreso en consola para entrar al curso.

Genera secretos fuertes y pégalos en `.env`:
```bash
openssl rand -hex 32     # → JWT_SECRET
openssl rand -hex 32     # → ADMIN_TOKEN
```

---

## 2. Stripe en modo TEST (10 min)

### 2.1 Cuenta
Crea cuenta en [dashboard.stripe.com/register](https://dashboard.stripe.com/register). Asegúrate de que el **toggle TEST** está activo arriba a la derecha.

### 2.2 API keys
**Developers → API keys** → copia:
```
sk_test_...   → STRIPE_SECRET_KEY
pk_test_...   → STRIPE_PUBLISHABLE_KEY
```

### 2.3 Webhook local con Stripe CLI
```bash
brew install stripe/stripe-cli/stripe
stripe login
stripe listen --forward-to localhost:3000/api/stripe/webhook
```
Copia el `whsec_...` que imprime → `STRIPE_WEBHOOK_SECRET` en `.env`. Reinicia el server.

### 2.4 Prueba de compra
1. `http://localhost:3000` → Comprar acceso
2. Tarjeta de test: `4242 4242 4242 4242` · cualquier fecha futura · cualquier CVC
3. Verás el magic link en la consola del server (porque `MAIL_PROVIDER=console`)
4. Cópialo, pégalo en el navegador → entras a `/app`

✓ Si llegas aquí, todo el flujo de pago funciona en local.

---

## 3. Email transaccional con Resend (10 min)

Mientras desarrollas vale `MAIL_PROVIDER=console`. Para que los magic links lleguen a tus clientes en producción necesitas envío real.

### 3.1 Cuenta
[resend.com](https://resend.com) → registrate.

### 3.2 Verificar dominio (si ya tienes uno)
**Domains → Add Domain** → sigue las instrucciones DNS (SPF, DKIM, DMARC).

Mientras no lo verifiques puedes mandar desde `onboarding@resend.dev` pero **solo a tu propio email** — no sirve para producción real.

### 3.3 API key
**API Keys → Create API Key** → copia.

### 3.4 Configurar `.env`
```
MAIL_PROVIDER=resend
RESEND_API_KEY=re_...
MAIL_FROM="Claude 101 <hola@tudominio.com>"
SUPPORT_EMAIL=hola@tudominio.com
```
Reinicia y prueba: `/login` → mete tu email → debe llegarte un email real.

---

## 4. Google OAuth (opcional, 10 min)

Permite que los usuarios entren con su cuenta de Google además del magic link.

### 4.1 Crear proyecto en Google Cloud
1. [console.cloud.google.com](https://console.cloud.google.com) → crea proyecto "Claude 101"
2. **APIs & Services → OAuth consent screen** → External → rellena nombre app, email, dominio
3. Añade scopes: `openid`, `email`, `profile`
4. **Test users** → añade tu email si está en modo testing

### 4.2 Credenciales
**Credentials → Create Credentials → OAuth client ID**
- Application type: **Web application**
- Authorized redirect URIs: `https://TU-DOMINIO/api/auth/google/callback`
  - Para local también: `http://localhost:3000/api/auth/google/callback`

Copia client_id y secret → `.env`:
```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

Reinicia. En `/login` aparecerá el botón "Continuar con Google".

> **Importante:** el login con Google solo da acceso si el usuario **ya ha pagado** (tiene `has_paid=1` en la DB). Si no, redirige al paywall. Esto evita que se den de alta sin comprar.

---

## 5. Dominio + DNS (5 min)

### 5.1 Comprar
Recomendación: **Cloudflare Registrar** (precios al coste, sin renovaciones abusivas). Alternativas: Namecheap, Porkbun.

### 5.2 Apuntar al hosting
Cuando despliegues a Railway/Fly te darán un CNAME tipo `xyz.up.railway.app` o `claude-101.fly.dev`. En tu proveedor DNS añade:
```
A    @                    → IP del hosting (o "ALIAS" si soporta)
CNAME www                 → tu-app.railway.app
CNAME app (opcional)      → tu-app.railway.app
CNAME blog (opcional)     → tu-app.railway.app
CNAME admin (opcional)    → tu-app.railway.app
```

Si activas los subdominios (`app.`, `blog.`, etc.) pon en `.env`:
```
ENABLE_VHOST=true
ROOT_DOMAIN=tudominio.com
```

---

## 6. Desplegar (10 min)

### Opción A — Railway (recomendado para empezar)

1. Sube el repo a GitHub
2. [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Selecciona el repo
4. **+ New → Database → PostgreSQL** (te da `DATABASE_URL` automática)
5. **Variables**: pega todas las de tu `.env` salvo `PORT` y `DATABASE_URL`. Cambia:
   - `DB_DRIVER=postgres`
   - `PUBLIC_URL=https://tu-app.up.railway.app` (o tu dominio si ya está DNS)
   - `NODE_ENV=production`
6. **Settings → Networking → Generate Domain** → anota la URL
7. Conecta dominio custom (Add Custom Domain)
8. Después del primer deploy, abre el shell: `npm run migrate`
9. **Configura el webhook en Stripe**: Dashboard → Developers → Webhooks → **Add endpoint**
   - URL: `https://tu-dominio/api/stripe/webhook`
   - Eventos: `checkout.session.completed`, `charge.refunded`, `charge.dispute.created`
   - Copia el `whsec_...` → variable `STRIPE_WEBHOOK_SECRET` en Railway
10. Redeploy

### Opción B — Fly.io (Docker)

```bash
brew install flyctl && fly auth login
fly launch --no-deploy --copy-config
fly volumes create claude101_data --size 1 --region mad     # solo si DB_DRIVER=sqlite
fly secrets set \
  JWT_SECRET=$(openssl rand -hex 32) \
  ADMIN_TOKEN=$(openssl rand -hex 32) \
  PUBLIC_URL=https://tu-app.fly.dev \
  STRIPE_SECRET_KEY=sk_live_... \
  STRIPE_PUBLISHABLE_KEY=pk_live_... \
  STRIPE_WEBHOOK_SECRET=whsec_... \
  MAIL_PROVIDER=resend \
  RESEND_API_KEY=re_... \
  MAIL_FROM="Claude 101 <hola@tudominio.com>" \
  SUPPORT_EMAIL=hola@tudominio.com
fly deploy
```

---

## 7. Activar modo LIVE de Stripe (5 min)

Cuando estés listo para cobrar de verdad:

1. Stripe Dashboard → activa **LIVE** (toggle arriba a la derecha)
2. **Developers → API keys** → copia las claves LIVE (`sk_live_...`, `pk_live_...`)
3. Configura un **webhook NUEVO en modo LIVE** apuntando al mismo endpoint — el secret es diferente del de TEST
4. Actualiza las env vars de producción con las claves LIVE + nuevo `STRIPE_WEBHOOK_SECRET`
5. Redeploy

---

## 8. Validación final (5 min)

Ejecuta el check de producción desde tu Mac apuntando a las env vars de prod:
```bash
npm run check:prod
```
Debe imprimir `✓ READY FOR PRODUCTION · 0 blocker(s)`.

Adicional, en el navegador:

| URL | Esperado |
|---|---|
| `https://tu-dominio/` | Landing renderiza, JSON-LD OK |
| `https://tu-dominio/healthz` | `{"status":"ok"}` |
| `https://tu-dominio/api/status` | `"ready_for_production": true` |
| `https://tu-dominio/sitemap.xml` | XML con tus URLs reales |
| `https://tu-dominio/robots.txt` | Sitemap apuntando a HTTPS |
| `https://tu-dominio/admin` | Pide token; con tu `ADMIN_TOKEN` entras |

Después haz una **compra de prueba REAL** con una tarjeta tuya por el precio mínimo (puedes usar un cupón de 99% para no gastar 49 €):

1. Crea en `/admin` un cupón temporal `TEST99` con `discount_pct=99`
2. Compra con `?coupon=TEST99` → pagas 0,49 €
3. Verifica que llega el magic link a tu email real
4. Entras a `/app` y ves el curso
5. En `/admin` → Compras debe aparecer
6. Devuelve el pago desde Stripe Dashboard
7. Verifica que tu acceso queda revocado automáticamente
8. **Borra el cupón TEST99**

Si todo OK, **estás en producción** ✓.

---

## 9. Después del lanzamiento

### Monitoring
- Uptime: configura un check externo (UptimeRobot, BetterStack) apuntando a `/healthz`
- Logs: Railway/Fly tienen logs nativos en el dashboard
- Errores: considera Sentry (variable de env `SENTRY_DSN` si lo integras)

### Backups (SQLite)
Si usas SQLite en VPS/Fly, programa backup periódico del volumen. Para Postgres, los hostings buenos hacen backup automático.

### Operativa diaria
- `/admin` → estadísticas y compras
- `npm run setup-demo` solo en local, **NO en producción**
- Reembolsos: hazlos desde Stripe Dashboard, el webhook revoca acceso automáticamente

### Cambios habituales
| Cosa | Dónde |
|---|---|
| Precio | env `COURSE_PRICE_CENTS` |
| Moneda | env `COURSE_CURRENCY` |
| Nombre visible | env `COURSE_PUBLIC_NAME` |
| Email soporte | env `SUPPORT_EMAIL` |
| Discord | env `COMMUNITY_URL` |
| Cupón temporal | `/admin → Cupones` |
| Suscripción en vez de one-time | `routes/checkout.js` → `mode: 'subscription'` |

---

## Problemas comunes

**"STRIPE_WEBHOOK_SECRET inválido"** → secrets de TEST y LIVE son distintos; revisa que coincida con el modo.

**Emails no llegan** → 1) `MAIL_PROVIDER` no está en `console`; 2) DNS de Resend está verificado; 3) `MAIL_FROM` está verificado en Resend.

**Google OAuth devuelve "redirect_uri_mismatch"** → la URI configurada en Google Cloud debe coincidir EXACTAMENTE con `${PUBLIC_URL}/api/auth/google/callback`.

**"Database is locked" en producción** → estás usando SQLite en un host efímero (Railway sin volumen). Cambia a Postgres.

**El cliente paga pero no recibe email** → verifica logs del server; el webhook debe haber recibido `checkout.session.completed`. Si Stripe muestra el evento como "failed" delivery, hay problema de URL/secret.

---

## Coste estimado mensual

| Servicio | Plan recomendado | €/mes aprox |
|---|---|---|
| Dominio | Cloudflare Registrar | 1 € |
| Hosting (Railway Hobby) | 5 $/mes incluye DB | ~5 € |
| Email (Resend Free) | 3.000 emails/mes gratis | 0 € |
| Stripe | 1.4% + 0.25 € por venta | variable |
| Google OAuth | Gratis | 0 € |
| **Total fijo** | | **~6 €/mes** |

Con 5-10 ventas al mes ya cubres costes 10x. El producto se sostiene desde la primera venta.
