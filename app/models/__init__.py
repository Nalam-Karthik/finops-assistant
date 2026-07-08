"""
WHY THIS FILE MATTERS:
SQLAlchemy's Base.metadata only knows about a model once Python has
actually imported that file. If you forget to import a model anywhere,
create_all() will silently skip that table — no error, just a missing
table you discover confusingly later when a query fails.

Importing every model here means one `from app.models import ...`
elsewhere guarantees all six tables get registered.
"""

from app.models.department import Department
from app.models.employee import Employee
from app.models.project import Project
from app.models.cloud_service import CloudService
from app.models.billing import Billing
from app.models.budget import Budget