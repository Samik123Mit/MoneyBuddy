"""Internal model package.

Models are split into domain modules for maintainability.
The public import path remains ``moneybuddy.db.models`` — see ``db/models.py``
for the facade.

IMPORTANT: every model module must be imported here so SQLAlchemy's
``Base.metadata`` registers all tables before Alembic or ``init_db`` run.
"""

from moneybuddy.db._models._constants import CASCADE_ALL_DELETE_ORPHAN, USER_FK
from moneybuddy.db._models.analytics import (
    CategoryTrend,
    CohortSpending,
    DailySummary,
    FYSummary,
    MerchantIntelligence,
    MonthlySummary,
    TransferFlow,
)
from moneybuddy.db._models.enums import (
    AccountType,
    AnomalyType,
    GoalStatus,
    RecurrenceFrequency,
    TransactionType,
)
from moneybuddy.db._models.investments import (
    InvestmentHolding,
    NetWorthSnapshot,
    TaxRecord,
)
from moneybuddy.db._models.organization import (
    CategorizationRule,
    SavedFilterView,
    TransactionTag,
)
from moneybuddy.db._models.provider_usage import ProviderUsageLog
from moneybuddy.db._models.planning import (
    Anomaly,
    Budget,
    FinancialGoal,
    RecurringTransaction,
    ScheduledTransaction,
)
from moneybuddy.db._models.transactions import (
    AccountClassification,
    ColumnMappingLog,
    ImportLog,
    Transaction,
)
from moneybuddy.db._models.user import AuditLog, User, UserPreferences

__all__ = [
    "CASCADE_ALL_DELETE_ORPHAN",
    "USER_FK",
    "AccountClassification",
    "AccountType",
    "Anomaly",
    "AnomalyType",
    "AuditLog",
    "Budget",
    "CategorizationRule",
    "CategoryTrend",
    "CohortSpending",
    "ColumnMappingLog",
    "DailySummary",
    "FYSummary",
    "FinancialGoal",
    "GoalStatus",
    "ImportLog",
    "InvestmentHolding",
    "MerchantIntelligence",
    "MonthlySummary",
    "NetWorthSnapshot",
    "ProviderUsageLog",
    "RecurrenceFrequency",
    "RecurringTransaction",
    "SavedFilterView",
    "ScheduledTransaction",
    "TaxRecord",
    "Transaction",
    "TransactionTag",
    "TransactionType",
    "TransferFlow",
    "User",
    "UserPreferences",
]
