import { Router } from 'express';
import { one, exec, q } from '../lib/db.js';
import { logger } from '../lib/logger.js';
import { requireAuth } from '../middleware/requireAuth.js';
import { requirePaid } from '../middleware/requirePaid.js';

const router = Router();

// POST /api/quiz/attempt { module: 1..9, score: int, total: int }
router.post('/attempt', requireAuth, requirePaid, async (req, res) => {
  const moduleNum = parseInt(req.body?.module, 10);
  const score = parseInt(req.body?.score, 10);
  const total = parseInt(req.body?.total, 10);

  if (!Number.isFinite(moduleNum) || moduleNum < 1 || moduleNum > 9) {
    return res.status(400).json({ error: 'module inválido (1-9)' });
  }
  if (!Number.isFinite(score) || score < 0 || score > total) {
    return res.status(400).json({ error: 'score inválido' });
  }
  if (!Number.isFinite(total) || total < 1 || total > 50) {
    return res.status(400).json({ error: 'total inválido' });
  }

  try {
    await exec(
      'INSERT INTO quiz_attempts (user_id, module_num, score, total) VALUES (?, ?, ?, ?)',
      [req.user.id, moduleNum, score, total]
    );
    res.json({ ok: true });
  } catch (err) {
    logger.error({ err: err?.message }, 'quiz attempt insert failed');
    res.status(500).json({ error: 'No se pudo guardar' });
  }
});

// GET /api/quiz/me — estadísticas y badges del usuario
router.get('/me', requireAuth, requirePaid, async (req, res) => {
  try {
    // Mejor puntuación por módulo
    const best = await q(
      `SELECT module_num, MAX(score) AS best_score, MAX(total) AS total
       FROM quiz_attempts WHERE user_id = ? GROUP BY module_num ORDER BY module_num`,
      [req.user.id]
    );
    const totalAttempts = (await one('SELECT COUNT(*) AS n FROM quiz_attempts WHERE user_id = ?', [req.user.id]))?.n ?? 0;

    // Calcular badges
    const modulesPassed70 = best.filter(b => b.best_score / b.total >= 0.7).length;
    const modulesPassed80 = best.filter(b => b.best_score / b.total >= 0.8).length;
    const badges = [];
    if (totalAttempts >= 1) badges.push({ id: 'iniciado', name: 'Iniciado', desc: 'Has completado tu primer quiz', emoji: '🌱' });
    if (modulesPassed70 >= 4) badges.push({ id: 'avanzado', name: 'Avanzado', desc: '4+ módulos con 70%+', emoji: '🚀' });
    if (modulesPassed80 >= 9) badges.push({ id: 'maestro', name: 'Maestro', desc: 'Los 9 módulos con 80%+', emoji: '🎖️' });

    res.json({
      total_attempts: totalAttempts,
      best_by_module: best,
      modules_passed_70: modulesPassed70,
      modules_passed_80: modulesPassed80,
      badges,
    });
  } catch (err) {
    logger.error({ err: err?.message }, 'quiz me failed');
    res.status(500).json({ error: 'No se pudo cargar' });
  }
});

export default router;
