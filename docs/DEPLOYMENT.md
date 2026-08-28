# Deployment Guide

## Production Topology

```text
Vercel
  -> Vite frontend at /
  -> FastAPI backend at /api and /health
  -> PostgreSQL
```

## Vercel Layout

- Project config: `vercel.json`
- Frontend service root: `frontend/`
- Backend service root: `backend/`
- Backend ASGI app: `backend/src/moneybuddy/api/main.py`
- Database migrations: `.github/workflows/migrate.yml`

Top-level Vercel rewrites send `/api/*`, `/health`, and `/health/db` to the
FastAPI service, and everything else to the frontend service. The frontend then
uses an SPA rewrite to serve `index.html` for deep links such as `/dashboard`
and `/transactions`.

## One-click import

Use the repository import flow in Vercel or the deploy button:

```text
https://vercel.com/new/clone?repository-url=https://github.com/Samik123Mit/MoneyBuddy
```

During import, Vercel reads the root `vercel.json` and creates a single project
with two services on one shared domain.

## Required Backend Configuration

- `MONEYBUDDY_DATABASE_URL`
- `MONEYBUDDY_JWT_SECRET_KEY`
- `MONEYBUDDY_ENCRYPTION_KEY`
- `MONEYBUDDY_ENVIRONMENT=production`
- `MONEYBUDDY_FRONTEND_URL`
- `MONEYBUDDY_CORS_ORIGINS`

At least one OAuth provider pair is also required:

- `MONEYBUDDY_GOOGLE_CLIENT_ID`
- `MONEYBUDDY_GOOGLE_CLIENT_SECRET`
- `MONEYBUDDY_GITHUB_CLIENT_ID`
- `MONEYBUDDY_GITHUB_CLIENT_SECRET`

## Optional Frontend Configuration

Leave `VITE_API_BASE_URL` unset for the default Vercel setup so the frontend
calls the same-origin `/api` routes. Set it only if you intentionally split the
frontend and backend across different hosts.

## Release Flow

1. Push changes to a branch.
2. Merge to `main`.
3. Vercel builds both services from the same repository.
4. The migration workflow runs when schema files change.

## Verification

Production checks:

```bash
curl --fail https://<project>.vercel.app/health
curl --fail https://<project>.vercel.app/health/db
curl --fail https://<project>.vercel.app/api/auth/oauth/providers
```

Frontend checks:

1. Open `https://<project>.vercel.app/`.
2. Verify OAuth bootstrap loads.
3. Load a protected route directly.
4. Verify upload, transactions, and analytics pages render.
