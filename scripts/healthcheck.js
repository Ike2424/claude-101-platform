// Script para HEALTHCHECK de Docker. Exit 0 si OK, 1 si no.
const port = process.env.PORT || 3000;
const url = `http://127.0.0.1:${port}/healthz`;

(async () => {
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(4000) });
    if (!r.ok) throw new Error(`status ${r.status}`);
    process.exit(0);
  } catch (err) {
    console.error(`healthcheck failed: ${err.message}`);
    process.exit(1);
  }
})();
