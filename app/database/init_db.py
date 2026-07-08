"""
database/init_db.py

WHY THIS IS A SEPARATE FILE FROM session.py:
Base.metadata.create_all() actually issues CREATE TABLE statements. If this
lived inside session.py, you'd risk re-running CREATE TABLE every time you
just wanted a session for a normal request. Keeping it separate means it
only runs when you explicitly ask it to.
"""

from app.database.session import engine, Base
from app.models import Department, Employee, Project, CloudService, Billing, Budget  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


if __name__ == "__main__":
    init_db()