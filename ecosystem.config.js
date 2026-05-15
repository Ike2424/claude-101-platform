// PM2 config para VPS clásico (Hetzner, DigitalOcean, etc.)
// Uso: pm2 start ecosystem.config.js
//      pm2 save && pm2 startup
//      pm2 logs claude-101
//      pm2 reload claude-101
module.exports = {
  apps: [{
    name: 'claude-101',
    script: 'server.js',
    exec_mode: 'cluster',           // Aprovecha varios cores
    instances: process.env.PM2_INSTANCES || 'max',
    autorestart: true,
    watch: false,
    max_memory_restart: '512M',
    kill_timeout: 25_000,            // Coincide con shutdown timeout del server
    listen_timeout: 30_000,
    wait_ready: false,
    env: {
      NODE_ENV: 'production',
    },
    env_production: {
      NODE_ENV: 'production',
    },
    error_file: 'logs/err.log',
    out_file: 'logs/out.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
  }],
};
