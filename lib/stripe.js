import 'dotenv/config';
import { logger } from './logger.js';
import Stripe from 'stripe';

const key = process.env.STRIPE_SECRET_KEY;
if (!key || key.includes('xxxxxxxx')) {
  logger.warn('⚠ STRIPE_SECRET_KEY no configurado. Las rutas de checkout devolverán error.');
}

export const stripe = new Stripe(key || 'sk_test_placeholder', {
  // Sin apiVersion fija: usa la default del SDK
  timeout: 30000,
  maxNetworkRetries: 3,
  // CRITICAL: forzar el cliente HTTP a usar fetch nativo en lugar del node-http
  // interno del SDK. En Railway, el cliente por defecto tiene problemas de
  // conexión (StripeConnectionError) pero fetch funciona perfectamente.
  httpClient: Stripe.createFetchHttpClient(),
});

export const PRICE_CENTS = parseInt(process.env.COURSE_PRICE_CENTS || '4900', 10);
export const CURRENCY = (process.env.COURSE_CURRENCY || 'eur').toLowerCase();
export const PRODUCT_NAME = process.env.COURSE_NAME || 'Claude 101 — Acceso vitalicio';

export const WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET || '';
