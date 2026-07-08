"""
WHY THIS TABLE EXISTS:
Cloud costs are almost always attributed at the project level — this maps
directly to how GCP organizes billing (a "project" is the natural unit of
cost attribution). Every billing row and budget row hangs off a project.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)   # "checkout-service-prod"

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    department = relationship("Department", back_populates="projects")
    owner = relationship("Employee", back_populates="projects_owned")
    billing_records = relationship("Billing", back_populates="project")
    budgets = relationship("Budget", back_populates="project")