"""
utils/validator.py

WHY THIS FILE EXISTS:
This is your first line of defense. LLMs can be tricked (prompt injection) 
into generating destructive commands (DROP, DELETE, UPDATE, INSERT). 
This file statically parses the SQL string BEFORE it ever touches the database,
ensuring it is strictly a read-only SELECT statement.
"""
import sqlglot
from sqlglot import exp

def is_safe_read_query(sql_query: str) -> bool:
    """
    Parses a SQL string and returns True ONLY if it is a safe SELECT statement.
    Blocks all mutative commands (DROP, DELETE, UPDATE, INSERT, etc.).
    """
    try:
        # Parse the query using the SQLite dialect
        parsed_expressions = sqlglot.parse(sql_query, read="sqlite")
        
        # An empty query is not safe
        if not parsed_expressions:
            return False
            
        # Check every statement in the parsed query (in case of multiple statements separated by ';')
        for expression in parsed_expressions:
            # If any expression is NOT a Select statement, block the whole query
            if not isinstance(expression, exp.Select):
                return False
                
        return True
        
    except Exception as e:
        # If sqlglot can't even parse it, it's malformed or dangerous. Block it.
        print(f"Validation parsing error: {e}")
        return False