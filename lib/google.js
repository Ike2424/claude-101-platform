// Google OAuth 2.0 — Authorization Code Flow.
// Sin dependencias extra; usa fetch nativo de Node 18+.
//
// Flujo:
//   1) buildAuthUrl()  → URL a la que redirigimos al usuario.
//   2) Google llama a /api/auth/google/callback?code=...&state=...
//   3) exchangeCodeForTokens(code) → { id_token, access_token }
//   4) verifyIdToken(id_token) → { email, email_verified, name }
//
// El id_token de Google es un JWT firmado con RS256.
// Para verificarlo necesitamos las claves públicas de Google.
// Las cacheamos en memoria con su expiración.
import crypto from 'node:crypto';

const GOOGLE_DISCOVERY = 'https://accounts.google.com/.well-known/openid-configuration';
const GOOGLE_CERTS = 'https://www.googleapis.com/oauth2/v3/certs';

let _certsCache = { keys: null, expiresAt: 0 };

export function isConfigured() {
  return Boolean(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET);
}

export function buildAuthUrl({ redirectUri, state }) {
  const params = new URLSearchParams({
    client_id: process.env.GOOGLE_CLIENT_ID,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'openid email profile',
    state,
    access_type: 'online',
    prompt: 'select_account',
  });
  return `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
}

export async function exchangeCodeForTokens({ code, redirectUri }) {
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      redirect_uri: redirectUri,
      grant_type: 'authorization_code',
    }),
  });
  if (!r.ok) {
    const txt = await r.text();
    throw new Error(`Google token exchange failed: ${r.status} ${txt}`);
  }
  return r.json();
}

async function getGoogleCerts() {
  const now = Date.now();
  if (_certsCache.keys && _certsCache.expiresAt > now + 60_000) return _certsCache.keys;
  const r = await fetch(GOOGLE_CERTS);
  if (!r.ok) throw new Error('No se pudieron obtener las claves públicas de Google');
  const ttl = parseInt((r.headers.get('cache-control') || '').match(/max-age=(\d+)/)?.[1] || '3600', 10);
  const { keys } = await r.json();
  _certsCache = { keys, expiresAt: now + ttl * 1000 };
  return keys;
}

function base64UrlDecode(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/');
  while (s.length % 4) s += '=';
  return Buffer.from(s, 'base64');
}

// Verifica un id_token de Google (JWT firmado con RS256).
// Devuelve el payload si es válido, lanza si no.
export async function verifyIdToken(idToken) {
  const [headerB64, payloadB64, sigB64] = idToken.split('.');
  if (!headerB64 || !payloadB64 || !sigB64) throw new Error('id_token mal formado');

  const header = JSON.parse(base64UrlDecode(headerB64).toString('utf8'));
  const payload = JSON.parse(base64UrlDecode(payloadB64).toString('utf8'));

  // 1) Buscar la clave que firmó
  const certs = await getGoogleCerts();
  const key = certs.find(k => k.kid === header.kid);
  if (!key) throw new Error('Clave de firma no encontrada');

  // 2) Verificar firma RS256
  const pubKey = crypto.createPublicKey({ key, format: 'jwk' });
  const verifier = crypto.createVerify('RSA-SHA256');
  verifier.update(`${headerB64}.${payloadB64}`);
  const ok = verifier.verify(pubKey, base64UrlDecode(sigB64));
  if (!ok) throw new Error('Firma inválida del id_token');

  // 3) Validar claims
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp < now) throw new Error('id_token caducado');
  if (payload.iss !== 'https://accounts.google.com' && payload.iss !== 'accounts.google.com')
    throw new Error('Issuer inválido');
  if (payload.aud !== process.env.GOOGLE_CLIENT_ID) throw new Error('Audience inválida');
  if (!payload.email) throw new Error('Sin email en el id_token');
  if (payload.email_verified !== true) throw new Error('Email no verificado por Google');

  return payload;
}

// Genera un state firmado simple (HMAC) — evita Redis para CSRF
export function makeState() {
  const nonce = crypto.randomBytes(16).toString('base64url');
  const mac = crypto.createHmac('sha256', process.env.JWT_SECRET || 'fallback').update(nonce).digest('base64url');
  return `${nonce}.${mac}`;
}

export function verifyState(state) {
  if (!state || !state.includes('.')) return false;
  const [nonce, mac] = state.split('.');
  const expected = crypto.createHmac('sha256', process.env.JWT_SECRET || 'fallback').update(nonce).digest('base64url');
  return expected === mac;
}
