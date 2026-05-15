// Wraps async route handlers para capturar rejections en el error middleware.
// Uso: router.get('/x', asyncHandler(async (req, res) => { ... }))
export const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
