# API Reference

Human-readable reference for the MoneyBuddy API.

## Base URLs

- Local: `http://localhost:8000`
- Built frontend: relative `/api/...` paths through the frontend API client

## Authentication

MoneyBuddy uses OAuth sign-in and JWT bearer tokens for protected API access.

Public endpoints:

- `GET /health`
- `GET /health/db`
- `GET /api/auth/oauth/providers`
- `POST /api/auth/oauth/google/callback`
- `POST /api/auth/oauth/github/callback`
- `POST /api/auth/refresh`

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

## Core Endpoint Groups

| Area | Prefix | Purpose |
| --- | --- | --- |
| Auth | `/api/auth` | Profile, logout, refresh, reset |
| OAuth | `/api/auth/oauth` | Provider bootstrap and callbacks |
| Transactions | `/api/transactions` | Ledger queries, filters, tags, export |
| Upload | `/api/upload` | Statement-row ingestion and import history |
| Analytics | `/api/analytics` | KPI and chart endpoints |
| Analytics v2 | `/api/analytics/v2` | Persisted rollups, budgets, goals, anomalies |
| Calculations | `/api/calculations` | On-demand financial calculations |
| Preferences | `/api/preferences` | User financial settings |
| Classifications | `/api/account-classifications` | Account type mapping |
| Rules | `/api/categorization-rules` | Categorization rule CRUD and apply |
| Saved views | `/api/saved-views` | Transaction filter presets |
| Reports | `/api/reports` | Exportable report generation |
| Rates | `/api/exchange-rates`, `/api/rates`, `/api/stock-price` | Market and instrument reference data |

## Ingestion Contract

`POST /api/upload` accepts validated transaction rows, not raw files.

```json
{
  "file_name": "statement.xlsx",
  "file_hash": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "force": false,
  "rows": [
    {
      "date": "2026-07-01",
      "amount": 85000,
      "currency": "INR",
      "type": "Income",
      "account": "HDFC Bank",
      "category": "Salary",
      "subcategory": "Monthly",
      "note": "July salary"
    }
  ]
}
```

The ingestion pipeline validates, normalizes, reconciles, persists, and then refreshes analytics.

## Response Conventions

- Validation errors: HTTP `422`
- Auth errors: HTTP `401`
- Missing resources: HTTP `404`
- Rate limiting: HTTP `429`
- Database outage: HTTP `503`
- Unexpected server errors: HTTP `500` with a correlation ID

## Local Inspection

```bash
cd backend
uv run uvicorn moneybuddy.api.main:app --reload --port 8000
```

Useful URLs:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
