// Envío de emails — Resend, SMTP o console (dev)
import 'dotenv/config';
import { logger } from './logger.js';

const PROVIDER = (process.env.MAIL_PROVIDER || 'console').toLowerCase();
const FROM = process.env.MAIL_FROM || 'Claude 101 <onboarding@resend.dev>';

let _resend, _smtp;

async function getResend() {
  if (_resend) return _resend;
  const { Resend } = await import('resend');
  _resend = new Resend(process.env.RESEND_API_KEY);
  return _resend;
}

async function getSmtp() {
  if (_smtp) return _smtp;
  const nodemailer = (await import('nodemailer')).default;
  _smtp = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587', 10),
    secure: process.env.SMTP_PORT === '465',
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  });
  return _smtp;
}

export async function sendMagicLink({ to, link }) {
  const subject = 'Tu enlace de acceso a Claude 101';
  const text = `Hola,\n\nEste es tu enlace de acceso a Claude 101 (válido durante ${process.env.MAGIC_LINK_LIFETIME_MIN || 20} minutos):\n\n${link}\n\nSi no has solicitado este email, puedes ignorarlo sin problema.\n\nUn saludo,\nClaude 101`;
  const html = `
<!doctype html>
<html><body style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #F4EFE3; padding: 32px;">
  <div style="max-width: 480px; margin: 0 auto; background: #FBF8F0; border: 1px solid #E1D8C2; border-radius: 16px; padding: 36px;">
    <h1 style="font-family: Georgia, serif; color: #1C1A16; font-size: 26px; margin: 0 0 12px;">Tu acceso a <em style="color: #C8542B;">Claude 101</em></h1>
    <p style="color: #3A352D; line-height: 1.6; font-size: 15px; margin: 0 0 22px;">Haz clic en el botón para entrar. El enlace caduca en ${process.env.MAGIC_LINK_LIFETIME_MIN || 20} minutos y solo se puede usar una vez.</p>
    <p style="margin: 0 0 24px;">
      <a href="${link}" style="display:inline-block; background: #1C1A16; color: #F4EFE3; padding: 14px 24px; border-radius: 100px; text-decoration: none; font-weight: 600; font-size: 14px;">Entrar a Claude 101 →</a>
    </p>
    <p style="color: #756B5B; font-size: 12px; line-height: 1.55; margin: 0;">O copia este enlace:<br><a href="${link}" style="color: #C8542B; word-break: break-all;">${link}</a></p>
    <hr style="border: 0; border-top: 1px solid #E1D8C2; margin: 28px 0;">
    <p style="color: #A39782; font-size: 11px; margin: 0;">Si no has solicitado este email, ignóralo. Nadie podrá entrar a tu cuenta solo con este mensaje sin acceso a tu bandeja de entrada.</p>
  </div>
</body></html>`;

  if (PROVIDER === 'console') {
    logger.info('\n──────── ✉️  MAGIC LINK (modo console) ────────');
    logger.info(`Para: ${to}`);
    logger.info(`Enlace: ${link}`);
    logger.info('─────────────────────────────────────────────\n');
    return { ok: true, provider: 'console' };
  }

  if (PROVIDER === 'resend') {
    const r = await getResend();
    const { data, error } = await r.emails.send({ from: FROM, to, subject, html, text });
    if (error) throw new Error(`Resend error: ${error.message || JSON.stringify(error)}`);
    return { ok: true, provider: 'resend', id: data?.id };
  }

  if (PROVIDER === 'smtp') {
    const t = await getSmtp();
    const info = await t.sendMail({ from: FROM, to, subject, text, html });
    return { ok: true, provider: 'smtp', id: info.messageId };
  }

  throw new Error(`MAIL_PROVIDER desconocido: ${PROVIDER}`);
}
