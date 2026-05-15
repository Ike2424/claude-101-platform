// Asume que requireAuth ya corrió y dejó req.user
export function requirePaid(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: 'No autenticado' });
  }
  if (!req.user.has_paid) {
    const wantsJson = req.path.startsWith('/api/') || req.accepts(['html', 'json']) === 'json';
    if (wantsJson) {
      return res.status(402).json({ error: 'Pago requerido', checkout: '/api/checkout' });
    }
    return res.redirect('/?error=paywall');
  }
  next();
}
