"""
WHY THIS TABLE EXISTS:
This is your "fact table" — the actual dollars spent. Departments, projects,
and services are all descriptive context; billing is where the numbers live.
Every cost question ultimately becomes a query that starts here.

Design choice: month and year as separate integers, not a single date
column. For a project this size, (month=6, year=2026) is simpler for the
LLM to generate correct SQL against than parsing date ranges — a deliberate
simplification worth being able to explain if asked about it.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    cloud_service_id = Column(Integer, ForeignKey("cloud_services.id"), nullable=False)
    month = Column(Integer, nullable=False)   # 1-12
    year = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)    # USD spent on this service, this month

    project = relationship("Project", back_populates="billing_records")
    cloud_service = relationship("CloudService", back_populates="billing_records")