from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    # SQLite-specific: by default SQLite only allows the thread that opened
    # a connection to use it. FastAPI can handle a request on a different
    # thread than the one that created the engine, so we relax this.
    # (This flag doesn't apply to Postgres/MySQL — it's a SQLite quirk.)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    A FastAPI dependency. Every request that touches the DB will call this,
    get a fresh session, and FastAPI guarantees it's closed afterward —
    even if the request raises an exception halfway through. This 'yield'
    pattern is FastAPI's way of doing setup/teardown around a request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()