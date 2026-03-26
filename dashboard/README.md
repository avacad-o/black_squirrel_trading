# Dashboard — private website

Web UI for Black Squirrel Trading. Password-protected; run on your server behind HTTPS.

## Run locally

From the **repo root** (`black_squirrel_trading/`):

```bash
export DASHBOARD_PASSWORD=your-secret-password
export SECRET_KEY=your-flask-secret-key   # long random string for sessions

# Option A: Flask dev server
python -m flask --app dashboard.app run --host 0.0.0.0 --port 5000

# Option B: Gunicorn (production-style)
gunicorn -w 1 -b 0.0.0.0:5000 "dashboard.app:app"
```

Open **http://localhost:5000** (or http://your-server-ip:5000). Log in with `DASHBOARD_PASSWORD`.

## Run on Hetzner (private website)

1. **HTTPS**: Put the app behind a reverse proxy (nginx or Caddy) with TLS. Use Let’s Encrypt for a free certificate.
2. **Env**: Set `DASHBOARD_PASSWORD`, `SECRET_KEY`, and any Tardigrade/Stardust env vars (Doppler or `.env`) on the server.
3. **Systemd** (example):

   ```ini
   [Unit]
   Description=Black Squirrel Dashboard
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/black_squirrel_trading
   Environment="DASHBOARD_PASSWORD=..."
   Environment="SECRET_KEY=..."
   ExecStart=/path/to/venv/bin/gunicorn -w 1 -b 127.0.0.1:5000 "dashboard.app:app"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then point nginx/Caddy at `127.0.0.1:5000` and enable HTTPS.

## Pages

- **/** — Overview and links to Tardigrade / Stardust
- **/tardigrade** — Bracket clock, entry allowed, risk state, recent trades
- **/stardust** — Four quadrants (REMNANT, STASIS, SMOLDER, ROGUE), scores, refresh

All routes require login except `/login`.
