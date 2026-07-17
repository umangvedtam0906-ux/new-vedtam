
# Hostinger + CERT Feed Setup

This project is prepared to show live CERT-In advisory updates on:

- `index.html` homepage CERT section
- `cert-advisory.html` CERT landing page

Both pages read from the same `cert-data.json` feed.

## What is already prepared

- `update-cert-data.mjs`
  Fetches the latest CERT-In entries and writes `cert-data.json`.
- `.github/workflows/refresh-cert-feed.yml`
  Runs every 6 hours and updates the feed automatically.
- `.github/workflows/deploy-hostinger.yml`
  Uploads the project to Hostinger on each push to `main` or `master`.
- `package.json`
  Adds `npm run update:cert`.

## Recommended production setup

For a static Hostinger site, the simplest setup is:

1. Push this project to GitHub.
2. Add the Hostinger GitHub secrets listed below.
3. Enable the GitHub Actions workflows.
4. Let `refresh-cert-feed.yml` refresh `cert-data.json` on a schedule.
5. Let `deploy-hostinger.yml` publish each pushed update to Hostinger.

This avoids needing cron or a persistent Node process inside shared hosting.

## GitHub secrets required for Hostinger deploy

Add these in your GitHub repository:

- `HOSTINGER_HOST`
  Your FTP/SFTP hostname.
- `HOSTINGER_USERNAME`
  Your Hostinger FTP/SFTP username.
- `HOSTINGER_PASSWORD`
  Your Hostinger FTP/SFTP password.
- `HOSTINGER_PORT`
  Optional. Default `21`.
- `HOSTINGER_PROTOCOL`
  Optional. Example: `ftp`, `ftps`, or `sftp`.
- `HOSTINGER_REMOTE_DIR`
  Optional. Default `/public_html`.

## Workflow behavior

- `refresh-cert-feed.yml`
  Updates `cert-data.json` every 6 hours and commits it back to the repo.
- `deploy-hostinger.yml`
  Deploys the repo to Hostinger whenever `main` or `master` changes.

Together, this gives you an automated CERT refresh + live deployment pipeline.

## If your Hostinger plan supports cron / scheduled jobs

You can also run the updater directly on the server:

```bash
npm run update:cert
```

Useful environment variables:

- `CERT_YEAR`
  Override the target year if needed.
- `CERT_OUTPUT_FILE`
  Change output file path.
- `CERT_MAX_ENTRIES`
  Limit advisory count.

Example:

```bash
CERT_YEAR=2026 CERT_OUTPUT_FILE=public_html/cert-data.json npm run update:cert
```

## Homepage and landing page behavior

- Homepage uses `window.VEDTAM_CERT_DATA_URL` from `index.html`.
- CERT landing page now also respects `window.VEDTAM_CERT_DATA_URL`.
- Default fallback is `cert-data.json` in the site root.

## Hostinger checklist

- Upload all website files to `public_html/`.
- Confirm `cert-data.json` is publicly reachable:
  `https://yourdomain.com/cert-data.json`
- Confirm the CERT landing page loads the feed.
- Confirm the homepage CERT chart/summary updates from the same file.
- If using Git deployment, verify each GitHub update redeploys automatically.

## Recommended next step

1. Push this repo to GitHub.
2. Add the Hostinger secrets.
3. Run `Deploy To Hostinger` once manually from GitHub Actions.
4. Verify:
   - homepage CERT section
   - `cert-advisory.html`
   - `cert-data.json`
