import { Router } from 'express';
import { exec, q } from '../lib/db.js';

const router = Router();

// POST /api/course/progress  { lessonId, completed }
router.post('/progress', async (req, res) => {
  const lessonId = String(req.body?.lessonId || '').trim();
  const completed = !!req.body?.completed;
  if (!lessonId) return res.status(400).json({ error: 'lessonId requerido' });
  if (completed) {
    try {
      await exec(
        'INSERT INTO progress (user_id, lesson_id) VALUES (?, ?)',
        [req.user.id, lessonId]
      );
    } catch (err) {
      // SQLite usa 'UNIQUE', Postgres usa código '23505'
      if (!String(err.message).includes('UNIQUE') && err.code !== '23505') throw err;
    }
  } else {
    await exec('DELETE FROM progress WHERE user_id = ? AND lesson_id = ?', [req.user.id, lessonId]);
  }
  res.json({ ok: true });
});

// GET /api/course/progress
router.get('/progress', async (req, res) => {
  const rows = await q('SELECT lesson_id, completed_at FROM progress WHERE user_id = ?', [req.user.id]);
  res.json({ completed: rows.map(r => r.lesson_id) });
});

export default router;
