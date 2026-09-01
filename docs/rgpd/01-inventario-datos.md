# Inventario de datos personales — borrador del Registro de Actividades de Tratamiento (RAT)

**Responsable:** TACTO Digital SLU (datos registrales pendientes de completar).
**Producto:** curso digital «Claude 101 / academia101.com» (60 €, pago único con Stripe) + captación de emails desde el libro.
**Fecha de la auditoría:** generado por revisión del código del repo `claude-101-platform` (rama `rgpd-compliance`).

> Este documento se ha construido leyendo el código, no una plantilla. Cada fila
> cita dónde vive el tratamiento. Sirve de borrador; las bases legales y los plazos
> deben confirmarse por el responsable (ver `docs/rgpd/decisiones-pendientes`).

## 1. Tratamientos

| # | Tratamiento | Datos | Base legal (probable) | Destinatarios / encargados | Ubicación en el código |
|---|---|---|---|---|---|
| 1 | Cuenta y acceso al curso | email, has_paid, paid_at, stripe_customer | Ejecución de contrato (art. 6.1.b) | Stripe, Resend, Railway | `routes/webhook.js`, `routes/auth.js` → tabla `users` |
| 2 | Cobro y facturación | email, importe, IDs de Stripe, payload reducido del evento | Contrato + obligación legal (facturación/fiscal) | Stripe, Railway | `routes/webhook.js` → tabla `purchases` |
| 3 | Acceso passwordless (magic link) | user_id, hash del token, **IP en claro**, user-agent | Contrato / interés legítimo (seguridad) | Railway | `routes/auth.js`, `routes/webhook.js` → tabla `magic_tokens` |
| 4 | Inicio de sesión con Google (OAuth) | email, nombre (de Google) | Consentimiento / contrato | Google | `routes/auth.js`, `lib/google.js` |
| 5 | Certificados de finalización | **nombre completo**, user_id, código | Ejecución de contrato | Railway | `routes/certificates.js` → tabla `certificates` |
| 6 | Progreso y evaluaciones | user_id, lecciones completadas, puntuaciones | Ejecución de contrato | Railway | `routes/course.js`, `routes/quiz.js` → `progress`, `quiz_attempts` |
| 7 | Analítica propia (first-party) | `c101_vid` (localStorage), ip_hash, user-agent, referrer, ruta, meta | Consentimiento (art. 22 LSSI) | Railway | `public/track.js`, `routes/track.js` → `page_views`, `events` |
| 8 | Analítica de terceros | GA4 (`_ga`, `_ga_*`), Microsoft Clarity (`_clck`, `_clsk`) + grabación de sesión | Consentimiento (art. 22 LSSI) | Google, Microsoft | `public/ga.js`, `public/index.html`, `public/checkout-clarity.html` |
| 9 | Contacto y newsletter | name, email, message, topic | Consentimiento (newsletter) / interés legítimo (soporte) | Resend o SMTP (se **envía a la bandeja**, **no se guarda en BD**) | `routes/contact.js` |
| 10 | Recuperación de carrito abandonado | email | Interés legítimo (a valorar) | Stripe, Resend | `routes/checkout.js`, `routes/webhook.js`, `lib/mail.js` |
| 11 | Carga de fuentes tipográficas | IP del visitante | Consentimiento (transferencia a tercero) | Google Fonts CDN | Todas las HTML de `public/` + `routes/libro.js` |
| 12 | Logs de aplicación | **email en claro** (varias líneas), tokens/códigos en `req.url` | Interés legítimo (operación/seguridad) | Railway (stdout) | `lib/logger.js`, `routes/auth.js`, `routes/webhook.js` |
| 13 | Monitorización de errores | eventos de error (posible PII) | Interés legítimo | Sentry (configurable; actualmente OFF) | `lib/sentry.js` |

## 2. Datos almacenados en el navegador del visitante

| Clave | Tipo | Para qué | ¿Exento de consentimiento? |
|---|---|---|---|
| `session` | cookie (HttpOnly) | sesión de usuario autenticado (JWT) | Sí (técnica necesaria) |
| `oauth_state` | cookie (HttpOnly, 10 min) | anti-CSRF del login con Google | Sí (técnica necesaria) |
| `admin_token` | cookie (HttpOnly) | sesión de administración | Sí (técnica necesaria) |
| `c101_consent` | localStorage | recuerda la decisión de cookies de GA | Sí (registro del consentimiento) |
| `c101_vid` | localStorage | **identificador persistente de analítica propia** | **No** — requiere consentimiento |
| `web-checklist-c9`, `explorer-c11` | localStorage | estado de UI de los widgets del libro (sin PII) | Sí (funcional) |
| `_ga`, `_ga_*`, `_gid` | cookie (Google) | Google Analytics | **No** — requiere consentimiento |
| `_clck`, `_clsk` | cookie (Microsoft) | Microsoft Clarity + grabación de sesión | **No** — requiere consentimiento |

**Fuentes tipográficas:** se cargan desde `fonts.googleapis.com` / `fonts.gstatic.com` (CDN). No hay fuentes autoalojadas en `public/`. Efecto: la IP del visitante se transfiere a Google en cada visita, sin consentimiento.

## 3. Hallazgos de cumplimiento (a corregir en los bloques siguientes)

- **A. Analítica sin consentimiento previo.** `track.js` crea `c101_vid` al cargar; Clarity se carga sin puerta de consentimiento (y graba sesión); GA carga su script (IP a Google) pese a Consent Mode. → art. 22 LSSI.
- **B. Google Fonts por CDN.** IP del visitante a Google sin consentimiento. Recomendación: autoalojar las fuentes (elimina la transferencia y la necesidad de consentimiento por este motivo).
- **C. PII en logs.** Email en claro en varias líneas de `auth.js`/`webhook.js`; tokens de magic link y `code` de OAuth quedan en `req.url` (log de accesos). El `redact` de `logger.js` solo cubre `req.body.email`.
- **D. IP en claro** en `magic_tokens` (el resto del sistema hashea la IP).
- **E. No hay almacenamiento de leads.** No existe `book_leads`; los emails captados solo se reenvían por email. Sin almacenamiento no hay prueba de consentimiento ni gestión de baja (bloques 2 y 3 dependen de crearlo).
- **F. El banner actual solo gobierna GA;** no cubre Clarity, `c101_vid` ni las fuentes.
- **G. Textos legales:** existen `public/privacidad.html` y `public/terminos.html`; hay que revisarlos y regenerarlos a partir de este inventario (bloque 5).

## 4. Recipientes/encargados detectados (para el RAT y la política de privacidad)

- **Stripe** — pasarela de pago (email de compra, importe, datos de tarjeta que trata Stripe directamente). Encargado/responsable según su DPA.
- **Resend** (o SMTP configurado) — envío de emails transaccionales y de la newsletter reenviada.
- **Railway** — hosting de la app, base de datos (Postgres) y logs. *(Pendiente: confirmar región de alojamiento para transferencias.)*
- **Google** — Analytics 4, Google Fonts (CDN) y, si está activo, login con Google (OAuth).
- **Microsoft** — Clarity (analítica + grabación de sesión).
- **Cloudflare (cdnjs)** — librerías JS (jsPDF) en la página de certificado.
- **Sentry** — sólo si `SENTRY_DSN` está configurado (actualmente no).
