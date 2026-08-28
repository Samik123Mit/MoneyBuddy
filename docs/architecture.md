# Architecture

## System Overview

```mermaid
flowchart TD
    FE[React + TypeScript Frontend<br/>Pages, charts, upload flows]
    API[FastAPI Backend<br/>Auth, validation, services]
    DB[(PostgreSQL<br/>SQLAlchemy + Alembic)]
    AN[Analytics Layer<br/>calculations, rollups, reporting]

    FE -->|REST API| API
    API --> DB
    API --> AN
    AN --> DB
```

## Repository Layout

```text
MoneyBuddy/
  frontend/
  backend/
  docs/
  .github/workflows/
```

## Request Flow

```mermaid
sequenceDiagram
    participant UI as React Page
    participant Client as API Client
    participant Route as FastAPI Route
    participant Service as Service / Query Logic
    participant DB as PostgreSQL

    UI->>Client: Request data
    Client->>Route: HTTP request
    Route->>Service: Validate + authorize
    Service->>DB: Query / persist
    DB-->>Service: Rows / status
    Service-->>Route: Response payload
    Route-->>Client: JSON response
    Client-->>UI: Render state
```

## Ingestion Flow

```mermaid
flowchart TD
    A[CSV / Excel] --> B[Browser parse]
    B --> C[Row validation]
    C --> D[Normalization]
    D --> E[Deterministic SHA-256 ID]
    E --> F[Idempotent reconciliation]
    F --> G[Persistence]
    G --> H[Analytics refresh]
```

## Backend Layers

- API layer: routing, auth, validation, error mapping
- Service layer: reconciliation, calculations, report logic
- Persistence layer: SQLAlchemy models and Alembic migrations
- Analytics layer: rollups, trends, anomaly detection, reporting helpers

## Frontend Layers

- Routed pages for dashboard, upload, transactions, analytics, planning, and settings
- Shared API client and TanStack Query cache
- Zustand stores for auth, preferences, and local UI state
- Reusable chart and table components
