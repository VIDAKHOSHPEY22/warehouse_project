"""
پکیج models - همه مدل‌ها اینجا import می‌شوند تا Alembic و
Base.metadata.create_all() همه جدول‌ها را بشناسند.
"""
from app.models.user import User          # noqa
from app.models.location import Location  # noqa
from app.models.item import Item          # noqa
from app.models.batch import Batch        # noqa
from app.models.mission import Mission    # noqa
from app.models.transaction import Transaction  # noqa
from app.models.audit import AuditLog     # noqa
