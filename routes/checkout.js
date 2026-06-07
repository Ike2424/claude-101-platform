import { Router } from 'express';
import rateLimit from 'express-rate-limit';
import { logger } from '../lib/logger.js';
import { stripe, PRICE_CENTS, CURRENCY, PRODUCT_NAME } from '../lib/stripe.js';
import { one, exec } from '../lib/db.js';

const router = Router();

const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';


// Rate limiter para checkout (anti-abuse de creación de sessions)
const checkoutLimiter = rateLimit({
  windowMs: 60_000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Demasiados intentos. Espera 1 minuto.' },
});

// Valida cupón interno y devuelve el descuento aplicable (%)
async function validateCoupon(code) {
  if (!code) return null;
  const c = await one(
    `SELECT id, code, discount_pct, max_uses, uses, expires_at, active FROM coupons WHERE code = ?`,
    [code.toUpperCase()]
  );
  if (!c) return { error: 'Cupón inválido' };
  if (!c.active) return { error: 'Cupón desactivado' };
  if (c.max_uses != null && c.uses >= c.max_uses) return { error: 'Cupón agotado' };
  if (c.expires_at && new Date(c.expires_at) < new Date()) return { error: 'Cupón caducado' };
  return { coupon: c };
}

// POST /api/checkout  { email?, coupon? }
router.post('/', checkoutLimiter, async (req, res) => {
  try {
    const email = (req.body?.email || '').trim().toLowerCase() || undefined;
    const couponCode = (req.body?.coupon || '').trim().toUpperCase() || null;

    let discountPct = 0;
    let couponId = null;
    if (couponCode) {
      const v = await validateCoupon(couponCode);
      if (v?.error) return res.status(400).json({ error: v.error });
      discountPct = v.coupon.discount_pct;
      couponId = v.coupon.id;
    }

    const finalAmount = Math.round(PRICE_CENTS * (100 - discountPct) / 100);

    // Crear o reutilizar Stripe Coupon si hay descuento
    let stripeCoupon = null;
    if (discountPct > 0) {
      try {
        stripeCoupon = await stripe.coupons.create({
          percent_off: discountPct,
          duration: 'once',
          name: `Claude 101 ${couponCode} -${discountPct}%`,
        });
      } catch (err) {
        logger.error({ err: err.message }, 'Stripe coupon error:');
      }
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      payment_method_types: ['card'],
      // Recuperación de carrito abandonado: Stripe envía un email con enlace
      // para terminar el pago si la sesión caduca sin completarse.
      after_expiration: { recovery: { enabled: true, allow_promotion_codes: false } },
      customer_email: email,
      line_items: [{
        price_data: {
          currency: CURRENCY,
          product_data: {
            name: PRODUCT_NAME,
            description: 'Curso Claude 101 — 8 módulos · acceso vitalicio · actualizaciones incluidas',
          },
          unit_amount: PRICE_CENTS,
        },
        quantity: 1,
      }],
      discounts: stripeCoupon ? [{ coupon: stripeCoupon.id }] : undefined,
      allow_promotion_codes: !stripeCoupon, // si ya aplicamos uno, no permitimos otro
      success_url: `${PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${PUBLIC_URL}/?canceled=1`,
      metadata: {
        product: 'claude-101',
        internal_coupon_id: couponId ? String(couponId) : '',
        internal_coupon_code: couponCode || '',
      },
    });

    // NO incrementamos coupons.uses aquí — se hace en el webhook tras pago confirmado
    // (evita que abandonos / sessions expiradas agoten cupones gratis)

    res.json({ url: session.url, id: session.id, applied_discount_pct: discountPct, final_amount: finalAmount });
  } catch (err) {
    // Log detallado para diagnosticar
    logger.error({
      err: err?.message,
      type: err?.type,
      code: err?.code,
      param: err?.param,
      statusCode: err?.statusCode,
      raw: err?.raw?.message,
    }, 'Error creando checkout:');
    // Devolver detalle del error para diagnosticar (sin filtrar secrets)
    res.status(500).json({
      error: 'No se pudo iniciar el pago.',
      stripe_error: err?.message || 'sin mensaje',
      stripe_type: err?.type || null,
      stripe_code: err?.code || null,
      stripe_status: err?.statusCode || null,
    });
  }
});

// GET /api/checkout/validate-coupon?code=XXX
// Para previsualizar en la landing antes de pulsar comprar
router.get('/validate-coupon', async (req, res) => {
  const code = String(req.query.code || '').trim().toUpperCase();
  if (!code) return res.status(400).json({ error: 'code requerido' });
  const v = await validateCoupon(code);
  if (v?.error) return res.status(400).json({ error: v.error });
  res.json({ ok: true, discount_pct: v.coupon.discount_pct, code: v.coupon.code });
});

// GET /api/checkout/session-summary?session_id=cs_...
router.get('/session-summary', async (req, res) => {
  try {
    const id = String(req.query.session_id || '').trim();
    if (!id.startsWith('cs_')) return res.status(400).json({ error: 'session_id inválido' });
    const s = await stripe.checkout.sessions.retrieve(id);
    if (s.payment_status !== 'paid') return res.json({ paid: false });
    return res.json({
      paid: true,
      transaction_id: s.payment_intent || s.id,
      value: (s.amount_total || 0) / 100,
      currency: (s.currency || 'eur').toUpperCase(),
    });
  } catch (err) {
    logger.error({ err: err?.message }, 'session-summary error');
    return res.status(500).json({ error: 'No se pudo recuperar la sesión' });
  }
});

export default router;
