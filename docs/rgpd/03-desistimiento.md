# Desistimiento en contenido digital de acceso inmediato — análisis (NO implementado)

> El checkout se toca en una sesión aparte. Este documento explica **qué hace
> falta y dónde**, sin cambiar código.

## El marco legal (resumen)

Vendes contenido digital no suministrado en soporte material con acceso inmediato.
Por defecto el consumidor tiene **14 días de desistimiento** (art. 102 TRLGDCU).
Ese derecho **se pierde** si, y solo si (art. 103.m TRLGDCU / Directiva 2011/83):

1. La ejecución **comienza con el consentimiento previo y expreso** del consumidor, y
2. El consumidor **reconoce que, al empezar la ejecución, pierde el derecho de desistimiento**.

Además, debes **conservar prueba** de ese consentimiento y entregar **confirmación
en soporte duradero** (email) de que aceptó.

## Qué hace falta (a implementar en la sesión del checkout)

1. **Casilla en el paso previo al pago** (no pre-marcada, obligatoria) con un
   literal tipo:
   > «Solicito el acceso inmediato al contenido y reconozco que, al comenzar la
   > ejecución, pierdo mi derecho de desistimiento de 14 días.»
   Con enlace a las Condiciones de contratación.

2. **Fuente única del literal + versión** (como `lib/consent.js`): p.ej.
   `lib/desistimiento.js` con `WITHDRAWAL_TEXT` y `WITHDRAWAL_VERSION`.

3. **Bloqueo en servidor**: `POST /api/checkout` debe **rechazar (400)** si no
   llega `withdrawal_ack === true`. No basta con el bloqueo en el front.

4. **Prueba**: añadir a la sesión de Stripe
   `metadata.withdrawal_ack = 'true'` y `metadata.withdrawal_ack_version`. El
   webhook ya persiste `session.metadata` en `purchases.raw_event_json`, así que
   la prueba queda guardada junto a la compra.

5. **Confirmación en soporte duradero**: incluir el literal aceptado en el email
   de bienvenida (`lib/mail.js` → `sendWelcomeEmail`).

## Dónde va, en el código actual

| Paso | Fichero | Punto exacto |
|---|---|---|
| Casilla en el front | `public/index.html` | junto al botón que llama a `POST /api/checkout` |
| Literal + versión | `lib/desistimiento.js` (nuevo) | constante única, como `lib/consent.js` |
| Rechazo en servidor | `routes/checkout.js` | al inicio del handler `POST /` (validar `req.body.withdrawal_ack`) |
| Prueba en Stripe | `routes/checkout.js` | objeto `metadata:` (≈ línea 89) → añadir `withdrawal_ack` y versión |
| Persistencia | `routes/webhook.js` | ya guarda `session.metadata` en `purchases.raw_event_json` (sin cambios) |
| Confirmación duradera | `lib/mail.js` | `sendWelcomeEmail` → añadir el literal aceptado |

## Nota sobre Stripe Checkout

El checkout es una página **alojada por Stripe** (redirección). No conviene
depender de sus `custom_fields` para esto: la casilla legal debe estar en **tu**
paso previo (donde controlas el literal, el bloqueo y la prueba) antes de crear
la sesión. Stripe solo recibe la confirmación vía `metadata`.
