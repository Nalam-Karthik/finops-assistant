"""
services/schema_store.py

WHY THIS FILE EXISTS (THE MOCK RAG PIVOT):
In a massive enterprise system, this file would connect to a Vector Database 
like ChromaDB or Pinecone to fetch only relevant tables. 

However, since we only have 6 tables and are using Gemini (which has a huge 
context window), we can safely pass the entire schema. This file mocks the 
RAG (Retrieval-Augmented Generation) pattern so the architecture remains 
enterprise-grade, without the dependency overhead of a local vector DB.
"""

# Highly detailed descriptions of our 6 database tables
TABLE_SCHEMAS = {
    "departments": (
        "Table: departments. Contains organizational departments. "
        "Columns: id (INTEGER, PK), name (VARCHAR, unique, e.g., 'Engineering'), code (VARCHAR, unique, e.g., 'ENG')."
    ),
    "employees": (
        "Table: employees. Contains company employees, their roles, and departmental alignments. "
        "Columns: id (INTEGER, PK), name (VARCHAR), email (VARCHAR, unique), role (VARCHAR, e.g., 'Engineering Manager'), "
        "department_id (INTEGER, FK matching departments.id)."
    ),
    "projects": (
        "Table: projects. Represents specific corporate projects or cloud environments where infrastructure runs. "
        "Columns: id (INTEGER, PK), name (VARCHAR, e.g., 'checkout-service-prod'), department_id (INTEGER, FK matching departments.id), "
        "owner_id (INTEGER, FK matching employees.id)."
    ),
    "cloud_services": (
        "Table: cloud_services. A lookup reference catalog of available cloud products and their broad billing families. "
        "Columns: id (INTEGER, PK), name (VARCHAR, unique, e.g., 'Compute Engine', 'BigQuery'), category (VARCHAR, e.g., 'Compute', 'Storage', 'Analytics')."
    ),
    "billing": (
        "Table: billing. The main fact table recording raw infrastructure expenditures. "
        "Columns: id (INTEGER, PK), project_id (INTEGER, FK matching projects.id), cloud_service_id (INTEGER, FK matching cloud_services.id), "
        "month (INTEGER, 1-12), year (INTEGER), amount (FLOAT, actual dollar cost spent in USD)."
    ),
    "budgets": (
        "Table: budgets. Contains forward-looking target financial limits set for projects. "
        "Columns: id (INTEGER, PK), project_id (INTEGER, FK matching projects.id), month (INTEGER), year (INTEGER), "
        "budgeted_amount (FLOAT, financial limit allocated in USD)."
    )
}

def get_relevant_schema(question: str, limit: int = 6) -> str:
    """
    Returns the database schema context. 
    (Mocks semantic retrieval by just returning the full dictionary).
    """
    documents = list(TABLE_SCHEMAS.values())
    return "\n\n".join(documents)

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    test_q = "Show me the budget limits for checkout service"
    print(f"Testing Schema Retrieval for: '{test_q}'\n")
    context = get_relevant_schema(test_q)
    print("=== SCHEMA CONTEXT ===")
    print(context[:200] + "...")
    print("=================================")