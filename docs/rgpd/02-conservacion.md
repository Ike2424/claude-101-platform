# Plazos de conservación y ejercicio de derechos

> **Propuesta — pendiente de confirmación por el responsable (TACTO Digital SLU).**
> Los plazos marcados como «propuesto» son valores por defecto razonables; el
> responsable debe validarlos. El script `scripts/purge.mjs` aplica estos plazos
> (configurables por variables de entorno).

## 1. Plazos de conservación por tratamiento

| Tratamiento | Datos | Plazo (propuesto) | Base del plazo | Automatizado en |
|---|---|---|---|---|
| Facturación / compras | `purchases` (email, importe, IDs Stripe) | **6 años** | Art. 30 Código de Comercio + obligaciones fiscales | **NO se purga** (conservación legal) |
| Cuenta y acceso al curso | `users` | Mientras dure el acceso (curso "de por vida"); se borra a petición de supresión | Ejecución de contrato | `scripts/gdpr.mjs delete` |
| Certificados | `certificates` (nombre) | Igual que la cuenta / hasta supresión | Ejecución de contrato | `gdpr.mjs delete` |
| Progreso y quizzes | `progress`, `quiz_attempts` | Igual que la cuenta / hasta supresión | Ejecución de contrato | `gdpr.mjs delete` |
| Acceso passwordless | `magic_tokens` (IP, UA) | **30 días** (`MAGIC_TOKEN_RETENTION_DAYS`) | Sin valor tras uso/caducidad | `scripts/purge.mjs` |
| Lista de correo (activos) | `book_leads` | Mientras haya consentimiento | Consentimiento | baja del usuario |
| Lista de correo (bajas) | `book_leads` con `unsubscribed_at` | **12 meses** tras la baja (`LEADS_BAJA_RETENTION_MONTHS`), luego se borra | Prueba de la baja | `scripts/purge.mjs` |
| Analítica propia | `page_views`, `events` | **14 meses** (`ANALYTICS_RETENTION_MONTHS`) | Minimización | `scripts/purge.mjs` |
| Logs de aplicación | stdout en Railway | Según retención de Railway | Operación/seguridad | (gestionado por Railway) |

## 2. Ejercicio de derechos (acceso, portabilidad, supresión)

Herramienta de administración por email:

```bash
# Acceso + portabilidad: exporta todo lo asociado a un email
node scripts/gdpr.mjs export cliente@ejemplo.com salida.json

# Supresión (dry-run: muestra qué borraría)
node scripts/gdpr.mjs delete cliente@ejemplo.com
# Supresión real
node scripts/gdpr.mjs delete cliente@ejemplo.com --commit
```

La supresión borra cuenta, leads, tokens, certificados, progreso y desvincula la
analítica; **conserva las facturas** (`purchases`) por obligación legal.

## 3. Canal de ejercicio de derechos (visible en la web)

- El usuario puede ejercer sus derechos escribiendo a la dirección de protección
  de datos (ver política de privacidad). El formulario de contacto incluye el
  asunto **«Protección de datos»** para canalizar estas solicitudes.
- La dirección concreta se fija en la política de privacidad (bloque 5, requiere
  el email de contacto del responsable).

## 4. Purga periódica

`scripts/purge.mjs` aplica los plazos de arriba. Ejecutar de forma recurrente
(p. ej. tarea programada mensual). Por defecto es *dry-run*; usar `--commit`
para ejecutar. Nunca toca `purchases`.
