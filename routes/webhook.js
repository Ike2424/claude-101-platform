import { Router } from 'express';
import { logger } from '../lib/logger.js';
import express from 'express';
import { stripe, WEBHOOK_SECRET } from '../lib/stripe.js';
import { one, exec, isUniqueViolation } from '../lib/db.js';
import { sendMagicLink } from '../lib/mail.js';
import { makeMagicToken } from '../lib/token.js';

const router = Router();

const PUBLIC_URL = process.env.PUBLIC_URL || 'http://localhost:3000';
const MINUTES = parseInt(process.env.MAGIC_LINK_LIFETIME_MIN || '20', 10);

// CRÍTICO: Stripe necesita el body RAW para verificar la firma.
// El router se monta en server.js con express.raw() ANTES de express.json().
router.post('/', express.raw({ type: 'application/json' }), async (req, res) => {
  if (!WEBHOOK_SECRET) {
    logger.error('STRIPE_WEBHOOK_SECRET no configurado.');
    return res.status(500).send('Webhook secret missing');
  }

  let event;
  try {
    const sig = req.headers['stripe-signature'];
    event = stripe.webhooks.constructEvent(req.body, sig, WEBHOOK_SECRET);
  } catch (err) {
    logger.error({ err: err.message }, 'Webhook signature inválida:');
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Idempotencia: si ya procesamos este evento, devolvemos 200 sin hacer nada
  const already = await one('SELECT id FROM webhook_events WHERE stripe_id = ?', [event.id]);
  if (already) {
    return res.json({ received: true, idempotent: true });
  }

  try {
    if (event.type === 'checkout.session.completed') {
      const session = event.data.object;
      const email = (session.customer_details?.email || session.customer_email || '').toLowerCase();
      if (!email) {
        logger.error({ err: session.id }, 'Checkout completado sin email:');
        return res.status(200).json({ received: true, skipped: true });
      }

      // Upsert user
      let user = await one('SELECT id FROM users WHERE email = ?', [email]);
      if (!user) {
        await exec(
          'INSERT INTO users (email, has_paid, paid_at, stripe_customer) VALUES (?, 1, CURRENT_TIMESTAMP, ?)',
          [email, session.customer || null]
        );
        user = await one('SELECT id FROM users WHERE email = ?', [email]);
      } else {
        await exec(
          'UPDATE users SET has_paid = 1, paid_at = COALESCE(paid_at, CURRENT_TIMESTAMP), stripe_customer = COALESCE(stripe_customer, ?), updated_at = CURRENT_TIMESTAMP WHERE id = ?',
          [session.customer || null, user.id]
        );
      }

      // Registrar la compra
      try {
        await exec(
          `INSERT INTO purchases (user_id, email, stripe_session_id, stripe_payment_intent_id, amount_cents, currency, status, raw_event_json)
           VALUES (?, ?, ?, ?, ?, ?, 'completed', ?)`,
          [
            user.id,
            email,
            session.id,
            session.payment_intent || null,
            session.amount_total || 0,
            session.currency || 'eur',
            JSON.stringify(event).slice(0, 100000), // protección contra payloads gigantes
          ]
        );
      } catch (err) {
        // Idempotencia: si la purchase ya existía (UNIQUE en stripe_session_id), continuamos
        if (!isUniqueViolation(err)) throw err;
      }

      // Enviar magic link inmediato para que pueda entrar sin esperar al success page
      try {
        const { raw, hash } = makeMagicToken();
        const expires = new Date(Date.now() + MINUTES * 60 * 1000).toISOString();
        await exec(
          'INSERT INTO magic_tokens (user_id, token_hash, expires_at, ip, user_agent) VALUES (?, ?, ?, ?, ?)',
          [user.id, hash, expires, null, 'stripe-webhook']
        );
        const link = `${PUBLIC_URL}/api/auth/verify?token=${encodeURIComponent(raw)}`;
        await sendMagicLink({ to: email, link });
        logger.info(`[webhook] Acceso concedido y magic link enviado a ${email}`);
      } catch (err) {
        logger.error({ err: err }, 'Error enviando magic link tras pago:');
      }
    }

    if (event.type === 'charge.refunded' || event.type === 'charge.dispute.created') {
      // Política: revocar acceso ante refund completo o disputa
      const charge = event.data.object;
      const email = (charge.billing_details?.email || '').toLowerCase();
      if (email) {
        await exec('UPDATE users SET has_paid = 0, updated_at = CURRENT_TIMESTAMP WHERE email = ?', [email]);
        await exec(
          `UPDATE purchases SET status = 'refunded' WHERE email = ? AND status = 'completed'`,
          [email]
        );
        logger.info(`[webhook] Acceso revocado para ${email} (motivo: ${event.type})`);
      }
    }

    // Marcar como procesado (idempotencia)
    await exec('INSERT INTO webhook_events (stripe_id, type) VALUES (?, ?)', [event.id, event.type]);
    res.json({ received: true });
  } catch (err) {
    logger.error({ err: err }, 'Error procesando webhook:');
    res.status(500).send('Error procesando evento');
  }
});

export default router;
