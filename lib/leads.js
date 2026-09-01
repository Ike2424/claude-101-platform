// Consultas sobre book_leads. La regla "no enviar a bajas" vive AQUÍ, en la
// consulta, para que ningún código que envíe marketing pueda saltársela.
import { q } from './db.js';

// Leads a los que SÍ se puede enviar marketing: con consentimiento y sin baja.
export function mailableLeads() {
  return q(
    `SELECT id, email FROM book_leads
     WHERE consent = 1 AND unsubscribed_at IS NULL
     ORDER BY created_at ASC`
  );
}
