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

// Email de bienvenida post-compra
export async function sendWelcomeEmail({ to }) {
  const subject = '¡Bienvenido a Claude 101! Acceso inmediato 🎉';
  const loginUrl = process.env.PUBLIC_URL || 'https://academia101.com';
  const text = `¡Hola!

Tu compra en Claude 101 ha sido confirmada. Ya tienes acceso inmediato.

🚀 Por dónde empezar:
1. Inicia sesión aquí: ${loginUrl}/login
2. Abre el módulo 1 ("Bienvenida y fundamentos") — toma 30 minutos
3. Haz el primer prompt del ejercicio práctico

📚 Recursos recomendados:
- Guía completa de Claude: ${loginUrl}/blog/como-usar-claude-ai-guia-completa
- Cómo escribir prompts: ${loginUrl}/blog/como-escribir-prompts-claude

¿Dudas? Responde este email. Leemos cada mensaje.

Un saludo,
Claude 101`;

  const html = `
<!doctype html>
<html><body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; padding: 20px;">
  <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    
    <h1 style="margin: 0 0 20px; color: #1a1a1a; font-size: 28px; font-weight: 700;">¡Hola!</h1>
    
    <p style="font-size: 16px; line-height: 1.6; color: #333; margin: 0 0 24px;">
      Tu compra en Claude 101 ha sido confirmada. <strong>Ya tienes acceso inmediato</strong> — entra con el email que acabas de usar en el checkout.
    </p>
    
    <div style="background: #f9f9f9; border-left: 4px solid #ff6b35; padding: 20px; margin: 24px 0;">
      <h2 style="margin: 0 0 16px; color: #1a1a1a; font-size: 18px;">🚀 Por dónde empezar</h2>
      <ol style="margin: 0; padding-left: 20px; color: #555;">
        <li style="margin-bottom: 10px;"><strong>Inicia sesión</strong> aquí: <a href="${loginUrl}/login" style="color: #ff6b35; text-decoration: none; font-weight: 600;">${loginUrl}/login</a></li>
        <li style="margin-bottom: 10px;"><strong>Abre el módulo 1</strong> ("Bienvenida y fundamentos") — toma 30 minutos</li>
        <li><strong>Haz el primer prompt</strong> del ejercicio práctico</li>
      </ol>
    </div>
    
    <h3 style="color: #1a1a1a; margin: 24px 0 12px; font-size: 16px;">📚 Recursos recomendados</h3>
    <p style="font-size: 14px; line-height: 1.6; color: #555; margin: 0 0 12px;">
      Mientras avanzas en el curso, estos posts te irán bien:
    </p>
    <ul style="margin: 0; padding-left: 20px; color: #555; font-size: 14px;">
      <li style="margin-bottom: 8px;"><a href="${loginUrl}/blog/como-usar-claude-ai-guia-completa" style="color: #ff6b35; text-decoration: none;">Guía completa de Claude</a> — referencia general</li>
      <li><a href="${loginUrl}/blog/como-escribir-prompts-claude" style="color: #ff6b35; text-decoration: none;">Cómo escribir prompts</a> — técnicas que usaremos</li>
    </ul>
    
    <hr style="margin: 28px 0; border: none; border-top: 1px solid #e0e0e0;">
    
    <h3 style="color: #1a1a1a; margin: 20px 0 10px; font-size: 16px;">¿Dudas o problemas?</h3>
    <p style="font-size: 14px; line-height: 1.6; color: #555; margin: 0;">
      Responde este email. Leemos cada mensaje y respondemos dentro de 24 horas.
    </p>
    
    <hr style="margin: 28px 0; border: none; border-top: 1px solid #e0e0e0;">
    
    <div style="text-align: center; font-size: 12px; color: #999;">
      <p style="margin: 0;">© 2026 Claude 101 · Acceso de por vida</p>
      <p style="margin: 8px 0 0 0;">Hecho por <a href="https://tactoagencia.com" style="color: #ff6b35; text-decoration: none;">Tacto Agencia</a></p>
    </div>
    
  </div>
</body></html>`;

  if (PROVIDER === 'console') {
    logger.info('\n──────── ✉️  WELCOME EMAIL (modo console) ────────');
    logger.info(`Para: ${to}`);
    logger.info(`Asunto: ${subject}`);
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
