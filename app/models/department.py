"""
WHY THIS TABLE EXISTS:
The top of your org hierarchy. Without a real Department table, "which
department spent the most" has nothing to group by except a repeated
text field — this makes it a first-class, joinable entity instead.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.session import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)   # "Engineering"
    code = Column(String, nullable=False, unique=True)    # "ENG"

    # This is NOT a database column — it's a Python-side convenience.
    # department.employees gives you a list of Employee objects without
    # writing a JOIN by hand. SQLAlchemy builds the JOIN when you access it.
    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")