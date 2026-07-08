"""
WHY THIS TABLE EXISTS:
Kept separate from billing on purpose — see the note at the top of this
message. A budget is a target set in advance; billing is what actually
happened. Comparing the two tables is what "exceeded budget" means.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    budgeted_amount = Column(Float, nullable=False)

    project = relationship("Project", back_populates="budgets")