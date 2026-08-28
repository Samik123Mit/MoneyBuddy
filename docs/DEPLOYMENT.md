# Deployment Guide

## Production Topology

```text
GitHub Pages
  -> FastAPI on Vercel
  -> PostgreSQL
```

## Deployment Sources

- Frontend build: `.github/workflows/deploy-frontend.yml`
- Backend entry point: `backend/api/index.py`
- Backend routing: `backend/vercel.json`
- Database migrations: `.github/workflows/migrate.yml`
- Health ping: `.github/workflows/keepalive.yml`

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

## Frontend Build Configuration

Set the GitHub Actions repository variable:

- `VITE_API_BASE_URL`

`GITHUB_PAGES=true` is supplied by the workflow and switches the Vite base path to `/MoneyBuddy/`.

## Release Flow

1. Push changes to a branch.
2. Merge to `main`.
3. GitHub Actions deploys the frontend.
4. Vercel deploys the backend from the connected repository.
5. The migration workflow runs when schema files change.

## Verification

Backend:

```bash
curl --fail <backend-url>/health
curl --fail <backend-url>/health/db
curl --fail <backend-url>/api/auth/oauth/providers
```

Frontend:

1. Open the GitHub Pages site.
2. Verify OAuth bootstrap loads.
3. Load a protected route directly.
4. Verify upload, transactions, and analytics pages render.
