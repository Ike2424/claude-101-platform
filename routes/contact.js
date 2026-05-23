import { Router } from 'express';
import { logger } from '../lib/logger.js';
import rateLimit from 'express-rate-limit';

const router = Router();

const limit = rateLimit({ windowMs: 60 * 1000, max: 5, standardHeaders: true, legacyHeaders: false });

// POST /api/contact { name, email, message, topic? }
router.post('/', limit, async (req, res) => {
  const name = String(req.body?.name || '').trim().slice(0, 120);
  const email = String(req.body?.email || '').trim().toLowerCase().slice(0, 200);
  const topicRaw = String(req.body?.topic || '').trim().slice(0, 80);
  // Whitelist anti-injection: solo aceptamos tópicos predefinidos
  const ALLOWED_TOPICS = ['general', 'soporte', 'facturacion', 'bug', 'sugerencia', 'newsletter', 'partnership'];
  const topic = ALLOWED_TOPICS.includes(topicRaw) ? topicRaw : 'general';
  const message = String(req.body?.message || '').trim().slice(0, 4000);

  if (!name || !email || !message || !email.includes('@')) {
    return res.status(400).json({ error: 'Faltan datos' });
  }
  if (message.length < 10) {
    return res.status(400).json({ error: 'El mensaje es demasiado corto' });
  }

  const to = process.env.SUPPORT_EMAIL || 'hola@claude101.com';
  const provider = (process.env.MAIL_PROVIDER || 'console').toLowerCase();

  const subject = `[Claude 101] Contacto · ${topic || 'general'} · ${name}`;
  const text = `De: ${name} <${email}>\nTema: ${topic || '—'}\n\n${message}`;

  // En modo console: solo log. En prod (resend/smtp): envío real.
  if (provider === 'console') {
    logger.info('\n──── ✉️  CONTACTO (modo console) ────');
    logger.info(`A: ${to}`);
    logger.info(`Asunto: ${subject}`);
    logger.info(text);
    logger.info('───────────────────────────────────\n');
  } else {
    try {
      if (provider === 'resend') {
        const { Resend } = await import('resend');
        const r = new Resend(process.env.RESEND_API_KEY);
        await r.emails.send({
          from: process.env.MAIL_FROM || 'Claude 101 <onboarding@resend.dev>',
          to,
          reply_to: email,
          subject,
          text,
        });
      } else if (provider === 'smtp') {
        const nodemailer = (await import('nodemailer')).default;
        const t = nodemailer.createTransport({
          host: process.env.SMTP_HOST,
          port: parseInt(process.env.SMTP_PORT || '587', 10),
          secure: process.env.SMTP_PORT === '465',
          auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
        });
        await t.sendMail({
          from: process.env.MAIL_FROM || `Claude 101 <${to}>`,
          to,
          replyTo: email,
          subject,
          text,
        });
      }
    } catch (err) {
      logger.error({ err: err.message }, 'Contact email error:');
      return res.status(500).json({ error: 'No se pudo enviar. Inténtalo más tarde.' });
    }
  }

  res.json({ ok: true });
});

export default router;
