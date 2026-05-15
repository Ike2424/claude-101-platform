# DEMO — Claude 101 en 3 minutos

Esta guía te lleva de **0 a probando la plataforma con URL pública** en menos de 3 minutos.

---

## ⚡ Quick start local (sin Stripe, sin pagos reales)

```bash
cd ~/Downloads/claude-101-platform
npm install              # ~30 segundos
npm run migrate          # crea db/claude101.db
npm run setup-demo       # crea super usuario + cupones + datos seed
npm start                # arranca en http://localhost:3000
```

`npm run setup-demo` imprime en consola:

```
🔑 Super usuario (acceso al curso):
   Email:       demo@claude101.local
   Magic link:  http://localhost:3000/api/auth/verify?token=...

👤 Admin panel:
   URL:    http://localhost:3000/admin
   Token:  dev_admin_token_change_in_prod_...

🏷️  Cupones de prueba:
   BIENVENIDO20 → -20%
   LANZAMIENTO  → -30% (máx 50 usos)
   FRIENDS10    → -10%
```

### Lo que puedes hacer ya:

| Acción | URL |
|---|---|
| Ver la landing | http://localhost:3000/ |
| Probar un cupón en checkout | Escribe `BIENVENIDO20` en la landing |
| Entrar al curso como usuario pagado | Clica el magic link impreso por setup-demo |
| Ver tu cuenta | http://localhost:3000/account |
| Entrar al admin | http://localhost:3000/admin (pega el ADMIN_TOKEN) |
| Healthcheck | http://localhost:3000/healthz |
| SEO | http://localhost:3000/sitemap.xml · /robots.txt |

---

## 🌍 Darle URL pública en 60 segundos (sin comprar dominio)

Para que puedas mandarle el link a alguien y que pruebe la plataforma sin que tenga acceso a tu Mac.

### Opción A — Cloudflare Tunnel (recomendado, gratis, sin cuenta)

```bash
# 1. Instala cloudflared una vez
brew install cloudflared

# 2. Arranca tu servidor (en una terminal)
npm start

# 3. Abre OTRA terminal y arranca el tunnel
npm run tunnel
```

Cloudflared te dará una URL tipo `https://abc-xyz.trycloudflare.com` — esa es **pública en Internet**, sin que tengas que tocar DNS ni comprar nada. Es temporal (se cae si paras el comando) pero perfecta para demos.

**Importante:** edita tu `.env` y pon esa URL en `PUBLIC_URL`:
```
PUBLIC_URL=https://abc-xyz.trycloudflare.com
```
Reinicia el servidor. Ahora los emails y enlaces de Stripe apuntan correctamente.

### Opción B — ngrok (alternativa)

```bash
brew install ngrok
ngrok http 3000
```

Te da una URL similar. Misma idea — necesita cuenta gratis ngrok.com.

### Opción C — Despliegue real (Railway / Fly / Render)

Sigue `SETUP.md`. Te da un dominio `*.up.railway.app` o `*.fly.dev` gratis y permanente.

---

## 🧪 Flujo completo de prueba (paso a paso)

### 1. Prueba como visitante

1. Ve a `/` (landing).
2. Lee el hero. Haz scroll: features, casos de uso, comparativa, programa, testimonios.
3. En pricing, escribe el cupón `BIENVENIDO20` — verás el descuento aplicarse en verde.
4. Si tienes Stripe configurado, dale a "Comprar acceso" para probar el flujo real con tarjeta de test `4242 4242 4242 4242`.
5. Si NO tienes Stripe, salta al paso siguiente con el magic link.

### 2. Prueba como usuario pagado

Pega el magic link de `setup-demo` en el navegador. Te lleva a `/app`:

- Verás el curso completo embebido en iframe.
- Navega entre módulos en el sidebar izquierdo.
- Al entrar a las lecciones 1.1, 2.1, 3.1, etc verás reproducirse el video animado correspondiente.
- Marca una lección como completada — eso registra `progress` en la DB.

Visita `/account`:
- Ves tu email, estado y fecha de "compra".
- Botón para pedir un nuevo magic link.
- Botón de logout.

### 3. Prueba como administrador

Ve a `/admin` y pega el `ADMIN_TOKEN`. Tendrás 6 pestañas:

- **Visión:** ya verás métricas (porque setup-demo metió page views, eventos y compras seed).
- **Web:** páginas más vistas, referrers, eventos.
- **Curso:** las lecciones que has marcado como completadas aparecen como "top".
- **Usuarios:** veras al `demo@claude101.local`. Puedes revocarle el acceso y volver a concedérselo.
- **Compras:** las 4 ventas seed.
- **Cupones:** los 3 cupones que sembraste. Pausa, edita, borra. Crea uno nuevo.

### 4. Prueba el tracking en vivo

1. Abre dos pestañas: una en `/admin` (pestaña Web) y otra en `/`.
2. En la landing, haz clic en "Comprar acceso" sin completar el form — solo el botón.
3. En `/admin` refresca (botón ↻) — verás el evento `checkout_started` capturado.

---

## 🎁 Datos del super usuario (resumen)

| Cosa | Valor por defecto |
|---|---|
| Email demo | `demo@claude101.local` |
| Acceso | Vitalicio (`has_paid=1`) |
| Magic link | Generado en cada `npm run setup-demo` (válido 1h) |
| Admin token | Definido en `.env` (`ADMIN_TOKEN`) |
| Cupones | `BIENVENIDO20`, `LANZAMIENTO`, `FRIENDS10` |

---

## 🔄 Resetear todo

Si quieres empezar limpio:

```bash
rm db/claude101.db                # Borra la DB
npm run migrate                   # Recrea el esquema
npm run setup-demo                # Re-crea todo desde cero
```

---

## ❓ Problemas comunes

**"Cannot find module 'better-sqlite3'"**
→ `npm install` no terminó. Vuelve a correrlo.

**"command not found: cloudflared"**
→ `brew install cloudflared` (Mac). Para Linux/Windows ver [docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-and-setup/installation/).

**"Stripe checkout falla"**
→ Pon claves reales de Stripe TEST en `.env`. Sigue `SETUP.md` sección 2.

**El magic link impreso por setup-demo no funciona**
→ Solo es válido 1 hora. Vuelve a correr `npm run setup-demo` para uno nuevo. O ve a `/login`, mete el email demo, y se imprimirá otro en consola (porque `MAIL_PROVIDER=console`).
