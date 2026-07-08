"""
WHY THIS TABLE EXISTS:
A lookup table for what's actually being paid for. Separate from billing
so you can GROUP BY category ("Compute", "Storage", "Analytics") without
string-matching, and so a typo can't silently split one service into two
different groups in a report.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.session import Base


class CloudService(Base):
    __tablename__ = "cloud_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)   # "Compute Engine"
    category = Column(String, nullable=False)              # "Compute"

    billing_records = relationship("Billing", back_populates="cloud_service")