"""
WHY THIS TABLE EXISTS:
So a project can have an accountable owner. Without this, "who do I email
about this project going over budget" has no answer in your data model.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)   # "Engineer", "FinOps Analyst", etc.

    # ForeignKey means: this column's value MUST exist as an id in
    # departments. The database itself enforces this — you cannot insert
    # an employee with department_id=999 if no department 999 exists.
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    department = relationship("Department", back_populates="employees")
    projects_owned = relationship("Project", back_populates="owner")