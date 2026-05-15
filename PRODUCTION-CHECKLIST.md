# PRODUCTION CHECKLIST — Claude 101

> Plan de lanzamiento de esta semana. Marca cada caja `[x]` cuando termines.
> Cada paso tiene comandos exactos, variables exactas y validación. Sigue en orden.

**Tiempo total estimado:** 90-120 minutos repartidos en 9 fases.

---

## FASE 0 · Pre-flight (5 min)

```bash
cd ~/Downloads/claude-101-platform
nvm install                          # lee .nvmrc → 22.11.0
nvm use
node --version                       # debe imprimir v22.11.0
rm -rf node_modules package-lock.json
npm install                          # 1-2 min, compila better-sqlite3
npm run setup-demo                   # smoke local
npm start                            # http://localhost:3000
```

- [ ] Servidor arranca sin errores (logs JSON con `Claude 101 listening`).
- [ ] `http://localhost:3000` carga la landing.
- [ ] Magic link de `setup-demo` te lleva a `/app`.

---

## FASE 1 · Stripe LIVE (15 min)

### 1.1 Activar modo LIVE
- [ ] [dashboard.stripe.com](https://dashboard.stripe.com) → toggle **LIVE** (arriba a la derecha)
- [ ] Completa **datos de empresa** (necesario para retirar dinero)

### 1.2 API keys LIVE
- [ ] Developers → API keys → copia:
  - `STRIPE_SECRET_KEY=sk_live_...`
  - `STRIPE_PUBLISHABLE_KEY=pk_live_...`

### 1.3 Webhook en producción
Lo configurarás en la Fase 4 cuando tengas el dominio. Por ahora guarda el endpoint:
```
https://tu-dominio.com/api/stripe/webhook
```
Eventos a escuchar:
- `checkout.session.completed`
- `charge.refunded`
- `charge.dispute.created`

### 1.4 Producto (opcional, ya creamos uno on-the-fly por checkout)
Si quieres aparecer en el dashboard:
- [ ] Products → Add product → "Claude 101 — Acceso vitalicio" → 49 EUR

---

## FASE 2 · Email transaccional con Resend (15 min)

### 2.1 Cuenta
- [ ] [resend.com](https://resend.com) → Sign up

### 2.2 Verificar tu dominio (CRÍTICO)
- [ ] Domains → Add Domain → `tudominio.com`
- [ ] Copia los 3 registros DNS (SPF, DKIM, DMARC) que te dan
- [ ] Pégalos en tu proveedor DNS (Cloudflare, Namecheap…)
- [ ] Espera la propagación (5-30 min)
- [ ] Pulsa **Verify** en Resend hasta que los 3 estén ✓

Si no verificas, solo podrás enviar a tu propio email — no sirve para producción.

### 2.3 API key
- [ ] API Keys → Create API Key → "Production"
- [ ] Guarda `RESEND_API_KEY=re_...`

---

## FASE 3 · Google OAuth (opcional, 10 min)

Solo si quieres login con Google además del magic link.

- [ ] [console.cloud.google.com](https://console.cloud.google.com) → New Project → "Claude 101"
- [ ] APIs & Services → OAuth consent screen → External
  - App name: Claude 101
  - User support email: tu email
  - Authorized domain: `tudominio.com`
  - Scopes: `openid`, `email`, `profile`
- [ ] Credentials → Create Credentials → OAuth client ID → Web application
  - Authorized redirect URIs: `https://tudominio.com/api/auth/google/callback`
- [ ] Guarda `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`

Si tu app está en modo **Testing**, añade los emails que pueden hacer login bajo "Test users". Para abrir a todo el mundo: Publish → External (te pedirá verificación si scopes sensibles, no es el caso).

---

## FASE 4 · Dominio + DNS (5 min)

Recomendación: **Cloudflare Registrar** (al coste).

- [ ] Compra tu dominio (ej. `claude101.com`)
- [ ] Mientras tanto, puedes desplegar primero a Railway/Fly y usar el subdominio de ellos
- [ ] DNS records: los configurarás después del deploy (Fase 5.5)

---

## FASE 5 · Deploy en Railway (15 min)

### 5.1 Repo en GitHub
```bash
cd ~/Downloads/claude-101-platform
git init
git add .
git commit -m "init"
# crea el repo en github.com/new → "claude-101-platform" → private
git remote add origin git@github.com:TU_USUARIO/claude-101-platform.git
git push -u origin main
```

### 5.2 Proyecto Railway
- [ ] [railway.app](https://railway.app) → New Project → Deploy from GitHub
- [ ] Selecciona el repo (Railway detecta `Dockerfile` y `railway.json`)
- [ ] Settings → Build → confirma `Dockerfile` como builder

### 5.3 Postgres
- [ ] **+ New** → Database → **PostgreSQL**
- [ ] Te crea `DATABASE_URL` automáticamente como variable del servicio app

### 5.4 Variables de entorno
En el servicio **app** → Variables → pega:

```bash
NODE_ENV=production
DB_DRIVER=postgres
# DATABASE_URL ya está, Railway la enlaza automáticamente

# Secretos: GENÉRALOS NUEVOS (no uses los de tu .env local)
JWT_SECRET=             # openssl rand -hex 32 → pega aquí
ADMIN_TOKEN=            # openssl rand -hex 32 → pega aquí

# Stripe LIVE
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=  # → se configura en 5.6, déjalo vacío de momento

# Producto
COURSE_PRICE_CENTS=4900
COURSE_CURRENCY=eur
COURSE_PUBLIC_NAME=Claude 101
COURSE_NAME=Claude 101 — Acceso vitalicio

# Email
MAIL_PROVIDER=resend
RESEND_API_KEY=re_...
MAIL_FROM="Claude 101 <hola@tudominio.com>"
SUPPORT_EMAIL=hola@tudominio.com
COMPANY_NAME=Claude 101
COMMUNITY_URL=https://discord.gg/tu-discord   # opcional

# Google OAuth (si la Fase 3)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Monitoring (opcional)
SENTRY_DSN=
RELEASE_VERSION=claude-101@1.0.0

# URL pública — se actualiza tras Generate Domain
PUBLIC_URL=https://tu-app.up.railway.app
```

### 5.5 Generar dominio
- [ ] Settings → Networking → **Generate Domain** → anota la URL `tu-app.up.railway.app`
- [ ] **Actualiza `PUBLIC_URL`** con esa URL → Redeploy

Para usar tu dominio propio:
- [ ] Add Custom Domain → `claude101.com` y `www.claude101.com`
- [ ] Railway te da un CNAME → ponlo en tu DNS (Cloudflare → DNS → Add record)
- [ ] Espera SSL (5-15 min)
- [ ] Actualiza `PUBLIC_URL=https://claude101.com` y redeploy
- [ ] En Google Cloud OAuth: actualiza el redirect URI con tu dominio real
- [ ] En Resend: ya está verificado el dominio en Fase 2

### 5.6 Configurar webhook de Stripe ahora
- [ ] Stripe Dashboard (modo LIVE) → Developers → Webhooks → Add endpoint
- [ ] URL: `https://tu-dominio/api/stripe/webhook`
- [ ] Eventos: `checkout.session.completed`, `charge.refunded`, `charge.dispute.created`
- [ ] Copia el **Signing secret** `whsec_...`
- [ ] Railway → Variables → `STRIPE_WEBHOOK_SECRET=whsec_...` → Redeploy

### 5.7 Verifica /healthz
```bash
curl https://tu-dominio/healthz
# → {"status":"ok",...}
curl https://tu-dominio/api/status
# → "ready_for_production": true, "blockers": []
```

---

## FASE 6 · Migración de datos (solo si tenías SQLite con clientes reales)

Si vienes desde local con clientes ya creados:

```bash
# En tu Mac, con tu .env local apuntando a SQLite y DATABASE_URL al pg de Railway
DATABASE_URL=$(railway variables get DATABASE_URL) \
SOURCE_SQLITE=./db/claude101.db \
npm run migrate:sqlite-to-pg
```

- [ ] Output: `✓ Migración OK. Total: N filas.`
- [ ] En `/admin` de producción: aparecen tus users y purchases.

Si empiezas desde cero, salta esta fase.

---

## FASE 7 · Compra de prueba real (5 min)

⚠ Vas a cobrar con tarjeta real. Usa un cupón temporal para que cueste céntimos.

- [ ] Abre `https://tu-dominio/admin` → entra con tu `ADMIN_TOKEN`
- [ ] Cupones → Crear: `TESTLAUNCH` con `99%` descuento, máx usos `1`
- [ ] Modo incógnito → `https://tu-dominio/?coupon=TESTLAUNCH`
- [ ] Compra con tu tarjeta real → pagas 0.49 €
- [ ] Verifica:
  - [ ] Email con magic link recibido
  - [ ] Magic link te lleva a `/app` con el curso
  - [ ] `/admin → Compras` muestra la transacción
  - [ ] `/admin → Usuarios` te muestra como pagado
- [ ] Stripe Dashboard → refunda la compra
- [ ] Verifica que tu acceso se revoca automáticamente (vuelve `/app` y te lleva a paywall)
- [ ] **Borra el cupón `TESTLAUNCH`**

Si todo va bien aquí, **estás en producción**.

---

## FASE 8 · Monitoring + backups (10 min)

### 8.1 Uptime monitor
- [ ] [uptimerobot.com](https://uptimerobot.com) → New Monitor → HTTPS → `https://tu-dominio/healthz` → cada 5 min
- [ ] Alerta a tu email

### 8.2 Sentry (opcional pero recomendado)
- [ ] [sentry.io](https://sentry.io) → New Project → Node.js → "claude-101"
- [ ] Copia el DSN → Railway → `SENTRY_DSN=...` → Redeploy

### 8.3 Backup automático Postgres
Railway hace snapshots diarios por defecto en su Postgres. Para backup independiente:

```bash
# En tu Mac, una vez al día:
DATABASE_URL=$(railway variables get DATABASE_URL) ./scripts/backup-pg.sh
# Backup local en ./backups/, rotación 14 días
```

Para automatizarlo en un servidor:
```bash
# crontab -e
0 3 * * * cd /app && DATABASE_URL=... bash scripts/backup-pg.sh
```

O con S3:
```bash
S3_BUCKET=mi-bucket-backups DATABASE_URL=... ./scripts/backup-pg.sh
```

---

## FASE 9 · Verificación final E2E (10 min)

Checklist completa **en producción** (modo incógnito, paso a paso):

### Visitante anónimo
- [ ] `https://tu-dominio/` carga la landing en <2 s
- [ ] Footer enlaza correctamente a `/terminos`, `/privacidad`, `/reembolsos`
- [ ] `/api/status` → `ready_for_production: true, blockers: []`
- [ ] `/sitemap.xml` lista todas las URLs con tu dominio
- [ ] `/robots.txt` apunta al sitemap correcto
- [ ] HTTPS forzado (acceder con `http://` redirige a `https://`)

### Compra
- [ ] Cupón fake (`NOEXISTE`) muestra error
- [ ] Cupón válido aplica descuento visible
- [ ] Form de compra → Stripe Checkout → tarjeta de prueba `4242 4242 4242 4242` (en modo TEST si quieres no cobrar de verdad)
- [ ] Página `/success` carga tras pagar
- [ ] Email con magic link llega en <1 min

### Auth
- [ ] Magic link redirige a `/app` y muestra el curso
- [ ] Sesión persiste tras refrescar
- [ ] `/account` muestra email, estado "Activo", fecha de compra
- [ ] "Cerrar sesión" elimina cookie y vuelve a `/`
- [ ] Volver a `/app` redirige a `/login`
- [ ] Nuevo magic link desde `/login` funciona
- [ ] (Si configuraste Google) Botón "Continuar con Google" aparece y funciona

### Admin
- [ ] `/admin` con `ADMIN_TOKEN` correcto entra
- [ ] Stats muestran datos reales
- [ ] Refund desde Stripe revoca acceso automáticamente
- [ ] Concede acceso manual a un email → recibe magic link

### Rutas protegidas
- [ ] `/app` sin sesión → redirect `/login`
- [ ] `/account` sin sesión → redirect `/login`
- [ ] `/api/admin/stats` sin token → 302 (rechaza)
- [ ] `/claude-101-videos/M1-video-animado.html` sin pago → redirect

### Mobile
- [ ] Landing legible en iPhone (Safari)
- [ ] Login + compra funcionan
- [ ] Curso reproducible en mobile

### Operacional
- [ ] Logs en Railway: estructura JSON, sin errores recurrentes
- [ ] Restart del servicio (Railway → Restart) → arranca en <30s
- [ ] `/healthz` responde durante todo el redeploy

---

## QUÉ HACER SI ALGO SE ROMPE

| Síntoma | Causa probable | Acción |
|---|---|---|
| Healthz 502 al deployar | Migración fallando | `railway logs` y revisa stack |
| Webhook 400 | Secret incorrecto | Re-copia `whsec_...` de Stripe |
| Emails no llegan | DNS Resend no verificado | Resend → Domains → re-verify |
| Google OAuth redirect_uri_mismatch | URL en Google Cloud no coincide | Console → Credentials → edita redirect URI |
| Magic link "expirado" inmediato | `JWT_SECRET` distinto entre boots | Verifica que está en Railway variables y no cambia |
| 500 en compras | Stripe key falsa o webhook mal | `/api/status` → blockers |
| Postgres "max connections" | Demasiados workers | Reduce `PG_POOL_MAX` |

---

## VARIABLES ENV — RESUMEN

| Variable | Crítica | Ejemplo |
|---|---|---|
| `NODE_ENV` | sí | `production` |
| `JWT_SECRET` | sí | `<openssl rand -hex 32>` |
| `ADMIN_TOKEN` | sí | `<openssl rand -hex 32>` |
| `PUBLIC_URL` | sí | `https://claude101.com` |
| `DB_DRIVER` | sí | `postgres` |
| `DATABASE_URL` | sí (si pg) | auto-inyectada por Railway |
| `STRIPE_SECRET_KEY` | sí | `sk_live_...` |
| `STRIPE_PUBLISHABLE_KEY` | sí | `pk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | sí | `whsec_...` |
| `MAIL_PROVIDER` | sí | `resend` |
| `RESEND_API_KEY` | sí | `re_...` |
| `MAIL_FROM` | sí | `"Claude 101 <hola@dominio>"` |
| `SUPPORT_EMAIL` | sí | `hola@dominio` |
| `COURSE_PRICE_CENTS` | sí | `4900` |
| `COURSE_CURRENCY` | sí | `eur` |
| `GOOGLE_CLIENT_ID` | no | si quieres OAuth |
| `GOOGLE_CLIENT_SECRET` | no | si quieres OAuth |
| `SENTRY_DSN` | no | recomendado |
| `COMMUNITY_URL` | no | URL Discord |

---

## DESPUÉS DEL LANZAMIENTO

- **Soporte:** revisa `/admin → Compras` diariamente la primera semana
- **Backups:** verifica que `backup-pg.sh` corre OK la primera vez
- **Reembolsos:** hazlos desde Stripe; el webhook revoca automáticamente
- **Conceder acceso manual** (Bizum, transferencia): `/admin → Conceder acceso manualmente`
- **Cupones promo:** créalos desde `/admin → Cupones`. El usuario los aplica con `?coupon=X` en la URL

---

**Fecha de este checklist:** mayo 2026.
**Versión:** 1.0
**Mantenido por:** tú a partir de ahora 💪
