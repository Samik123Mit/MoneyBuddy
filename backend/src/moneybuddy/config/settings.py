"""Application settings and configuration."""

import secrets
import warnings
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Maximum upload file size (50 MB)
MAX_UPLOAD_SIZE_BYTES: int = 50 * 1024 * 1024


class Settings(BaseSettings):
    """Application settings.

    Configuration is loaded from environment variables with MONEYBUDDY_ prefix.
    A .env file in the project root can also be used for local development.

    Critical settings for production:
    - MONEYBUDDY_JWT_SECRET_KEY: Must be a strong random string (min 32 chars)
    - MONEYBUDDY_DATABASE_URL: Production database connection string

    """

    model_config = SettingsConfigDict(
        env_prefix="MONEYBUDDY_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    environment: str = "development"  # development, staging, production

    # Database settings
    database_url: str = "sqlite:///./moneybuddy.db"
    database_echo: bool = False

    # Application settings
    log_level: str = "INFO"
    data_dir: Path = Path("./data")

    # JWT Authentication settings
    # SECURITY: Set MONEYBUDDY_JWT_SECRET_KEY in production!
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30  # 30 minutes (industry standard)
    jwt_refresh_token_expire_days: int = 7

    # Dedicated at-rest encryption key for sensitive user configuration.
    # If unset, encryption.py falls back to jwt_secret_key (legacy behavior).
    # Must be >= 32 chars in production when explicitly configured.
    encryption_key: str = ""

    # JWT strict token_version mode.
    # During rollout, tokens issued before token_version was baked into JWTs
    # still work (treated as tv=0). Flipping this to true on/after day 8 makes
    # `verify_token` reject any token that lacks a `tv` claim. Refresh TTL is
    # 7 days, so day 8 guarantees any surviving pre-migration refresh token
    # is already expired.
    jwt_strict_tv: bool = False

    # Upload limits
    max_upload_size_bytes: int = MAX_UPLOAD_SIZE_BYTES

    # Database pool settings (PostgreSQL only; SQLite uses defaults).
    # Defaults are sized for Neon free tier (limited concurrent connections).
    # Override via env vars to scale up on paid Postgres.
    db_pool_size: int = 5
    db_max_overflow: int = 3
    db_pool_recycle_seconds: int = 300  # Neon idles connections after 5m
    db_connect_timeout_seconds: int = 10
    db_statement_timeout_seconds: int = 30
    db_idle_transaction_timeout_seconds: int = 60

    # OAuth settings — set client ID and secret for each provider to enable.
    # Google: https://console.cloud.google.com/apis/credentials
    google_client_id: str = ""
    google_client_secret: str = ""
    # GitHub: https://github.com/settings/developers
    github_client_id: str = ""
    github_client_secret: str = ""

    # Frontend URL for OAuth redirect callbacks.
    # Dev: http://localhost:5173 | Prod: your actual frontend URL.
    frontend_url: str = "http://localhost:5173"

    # CORS settings — override with MONEYBUDDY_CORS_ORIGINS env var (JSON array).
    # Defaults include localhost origins for development only.
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    # Column name mappings (for normalization)
    date_column_names: list[str] = ["Period", "Date", "date", "period"]
    account_column_names: list[str] = ["Accounts", "Account", "account", "accounts"]
    category_column_names: list[str] = ["Category", "category"]
    subcategory_column_names: list[str] = ["Subcategory", "subcategory", "Sub Category"]
    note_column_names: list[str] = ["Note", "note", "Notes", "notes", "Description"]
    amount_column_names: list[str] = ["Amount / INR", "Amount", "amount", "Amount/INR"]
    type_column_names: list[str] = [
        "Income/Expense",
        "Type",
        "type",
        "Transaction Type",
    ]
    currency_column_names: list[str] = ["Currency", "currency"]

    def get_data_dir(self) -> Path:
        """Get data directory, creating it if necessary."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir

    def validate_production_settings(self) -> list[str]:
        """Validate critical settings for non-development deployment.

        Returns:
            List of warning/error messages (empty if all OK)

        """
        issues: list[str] = []

        # JWT secret must be explicitly configured in ANY non-development environment
        if not self.jwt_secret_key:
            if self.environment != "development":
                issues.append(
                    "CRITICAL: jwt_secret_key is not configured. "
                    "Set MONEYBUDDY_JWT_SECRET_KEY environment variable!"
                )

        # JWT secret should be sufficiently long
        if self.jwt_secret_key and len(self.jwt_secret_key) < 32:
            issues.append("CRITICAL: jwt_secret_key must be at least 32 characters")

        # Encryption key length check (only enforce if user opted in by setting one)
        if self.encryption_key and len(self.encryption_key) < 32:
            issues.append("CRITICAL: encryption_key must be at least 32 characters")

        if self.environment in ("staging", "production"):
            # SQLite not suitable for multi-user production
            if self.database_url.startswith("sqlite"):
                issues.append(
                    "CRITICAL: SQLite is not suitable for production. "
                    "Use PostgreSQL: set MONEYBUDDY_DATABASE_URL."
                )

        return issues

    def warn_if_development_secrets(self) -> None:
        """Emit warnings if using development secrets.

        Called during startup to alert developers.
        """
        if not self.jwt_secret_key:
            warnings.warn(
                "Using auto-generated JWT secret! Set MONEYBUDDY_JWT_SECRET_KEY "
                "environment variable for production.",
                UserWarning,
                stacklevel=2,
            )


# Global settings instance
settings = Settings()

# In development, auto-generate a random secret so tokens work without config.
# This is NOT used in production — the startup validator blocks non-dev
# environments that haven't set MONEYBUDDY_JWT_SECRET_KEY.
if settings.environment == "development" and not settings.jwt_secret_key:
    settings.jwt_secret_key = secrets.token_urlsafe(48)

# Validate settings on import for any non-development environment
if settings.environment != "development":
    _issues = settings.validate_production_settings()
    for _issue in _issues:
        if _issue.startswith("CRITICAL"):
            raise RuntimeError(_issue)
        warnings.warn(_issue, UserWarning, stacklevel=1)
