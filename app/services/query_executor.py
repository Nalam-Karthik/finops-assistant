"""
services/query_executor.py

WHY THIS FILE EXISTS:
Gemini gives us a raw SQL string. This file takes that string, safely executes 
it against our SQLite database using a raw database connection, and returns 
the rows as readable dictionaries.
"""
from sqlalchemy import text
from app.database.session import SessionLocal

def execute_read_query(sql_query: str):
    """
    Executes a raw SELECT query and returns the results as a list of dictionaries.
    """
    db = SessionLocal()
    try:
        # Wrap the raw string query in SQLAlchemy's safety text() construct
        result = db.execute(text(sql_query))
        
        # Extract column names so we can map them to values
        columns = result.keys()
        
        # Convert rows into clean, JSON-serializable dictionaries
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows
    except Exception as e:
        # If the LLM generated bad SQL syntax, catch it gracefully here
        raise RuntimeError(f"Database execution failed: {str(e)}")
    finally:
        db.close()