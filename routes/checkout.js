import { Router } from 'express';
import { logger } from '../lib/logger.js';
import { stripe, PRICE_CENTS, CURRENCY, PRODUCT_NAME } from '../lib/stripe.js';
import { one, exec } from '../lib/db.js';

const router = Router();

const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';

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
router.post('/', async (req, res) => {
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

    // Marcamos uso del cupón (optimista; si la sesión expira, lo descontamos en cron — por ahora suficiente)
    if (couponId) {
      try { await exec('UPDATE coupons SET uses = uses + 1 WHERE id = ?', [couponId]); } catch {}
    }

    res.json({ url: session.url, id: session.id, applied_discount_pct: discountPct, final_amount: finalAmount });
  } catch (err) {
    logger.error({ err: err }, 'Error creando checkout:');
    res.status(500).json({ error: 'No se pudo iniciar el pago. Revisa la configuración de Stripe.' });
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

export default router;
