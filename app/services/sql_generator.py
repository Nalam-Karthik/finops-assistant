"""
services/sql_generator.py

WHY THIS FILE EXISTS:
This file translates a natural language question and a schema string into 
a valid SQL query using Google's Gemini models.
"""
from google import genai
from google.genai import types
from app.config import settings

# Initialize the Gemini client using the unified SDK
client = genai.Client(api_key=settings.gemini_api_key)

def generate_sql(question: str, schema_context: str) -> str:
    """
    Calls Gemini to translate the user's question into SQL based on the provided schema.
    """
    system_prompt = f"""
    You are an expert Data Analyst and FinOps assistant.
    Your job is to write a valid SQLite SQL query to answer the user's question.
    
    Use the following database schema context to write the query:
    {schema_context}
    
    Rules:
    1. Return ONLY the raw SQL query.
    2. Do not include markdown formatting like ```sql or ```.
    3. Do not include explanations or conversational text.
    4. Ensure the query is compatible with SQLite syntax.
    """
    
    # Temperature 0.0 ensures deterministic, predictable code generation
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0 
        )
    )
    
    # Extract the text
    raw_sql = response.text.strip()
    
    # Safety cleanup: Strip out markdown block formatting if the model includes it
    if raw_sql.startswith("```sql"):
        raw_sql = raw_sql[6:]
    elif raw_sql.startswith("```"):
        raw_sql = raw_sql[3:]
        
    if raw_sql.endswith("```"):
        raw_sql = raw_sql[:-3]
        
    return raw_sql.strip()

# --- STANDALONE TEST BLOCK ---
if __name__ == "__main__":
    from app.services.schema_store import get_relevant_schema
    
    test_question = "Which project had the highest compute cost?"
    print(f"User Question: {test_question}\n")
    
    print("1. Fetching relevant schema from ChromaDB...")
    context = get_relevant_schema(test_question)
    
    print("2. Calling Gemini to generate SQL...\n")
    try:
        generated_sql = generate_sql(test_question, context)
        print("=== GENERATED SQL ===")
        print(generated_sql)
        print("=====================")
    except Exception as e:
        print(f"Failed to generate SQL: {e}")