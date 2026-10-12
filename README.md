# ezlcal — EZLine CRM calendar (ezlcal.alamark.com)

Installable web app (PWA) for E-Z Line's sales team: team agenda, calendar, accounts with
company families, contacts, staff history, and appointments with any number of staff,
account and contact invitees. Works offline; changes sync when the phone reconnects.

```
backend/
  app/main.py        FastAPI API (/api/*), bound to 127.0.0.1 only
  app/manage.py      migrate | seed | create-users | reset-password
  app/schema.sql     Postgres tables (re-runnable)
  seed/seed.json     snapshot from Dev FileMaker (accounts, contacts, staff, To Dos)
  requirements.txt
web/                 static app served by IIS (index.html, sw.js, manifest, icons)
  web.config.template  IIS rewrite: /api/* -> 127.0.0.1:PORT, SPA fallback
scripts/             Windows PowerShell 5.1 deploy scripts
```

## First install on fms26 (Windows PowerShell 5.1, elevated)

Run every script with `powershell.exe -ExecutionPolicy Bypass -File <script>`; not pwsh 7.

1. `git clone https://github.com/<org>/ezlcal.git C:\Apps\ezlcal` and `cd C:\Apps\ezlcal`
2. `.\scripts\create-database.ps1 -ApiPort <free port>`
   creates role and database `ezlcal` and writes `backend\.env`. Pick the port from the
   discovery report.
3. `.\scripts\deploy.ps1 -NoPull -Seed -CreateUsers`
   builds the venv, creates tables, loads the snapshot, and prints each person's
   temporary password **once**.
4. `.\scripts\install-service.ps1` registers the API as Windows service `ezlcal` (NSSM).
5. `.\scripts\iis-site.ps1` creates IIS site `ezlcal` on `ezlcal.alamark.com` (HTTP),
   then tests it through loopback. It does not touch FileMaker Server's IIS site.
6. DNS + HTTPS for `ezlcal.alamark.com` (separate step, depends on the certificate source).

## Updating

```
cd C:\Apps\ezlcal
.\scripts\deploy.ps1
```
Pulls, updates dependencies, migrates, republishes `backend\dist`, restarts the
service, and checks `/api/health`. After changing anything in `web\`, bump `VERSION`
in `web\sw.js` so installed phones pick up the new version.

## People

* Logins are `first.last`. New staff: add them to the `staff` table (or re-seed),
  then `deploy.ps1 -CreateUsers -NoPull`.
* Forgotten password: `backend\.venv\Scripts\python.exe -m app.manage reset-password first.last`
  (run from `backend\`). They pick a new one at next sign-in.

## iPhone install

Open https://ezlcal.alamark.com in **Safari**, sign in, tap **Share**, then
**Add to Home Screen**. It launches full screen and opens without signal; anything saved
offline syncs when the phone reconnects.

## Data notes

* Reference tables use FileMaker keys (`z_Kp_CRMaccounts_txt`, `__Kp_Buyer`, `ID_staff`),
  so the later FileMaker Data API sync is a straight upsert.
* Migrated To Dos keep their `TODxxx` id in `events.id` and `legacy_fm_id`; re-seeding
  never overwrites an event that already exists.
* `backend\.env` holds the database password and JWT secret. It is git-ignored; never commit it.
* `seed.json` contains client account and contact names; keep this repo **private**.
