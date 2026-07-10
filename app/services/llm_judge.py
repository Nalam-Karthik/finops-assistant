"""
services/llm_judge.py

WHY THIS FILE EXISTS:
This is Stage 2 of your validation pipeline. The first LLM generates the SQL. 
This second LLM call looks at the Question, the Schema, and the Generated SQL, 
and determines if the SQL accurately answers the question without hallucinating.
"""
from google import genai
from google.genai import types
import json
from app.config import settings

# Initialize the Gemini client
client = genai.Client(api_key=settings.gemini_api_key)

def evaluate_sql(question: str, generated_sql: str, schema_context: str) -> dict:
    """
    Evaluates if the generated SQL semantically matches the user's intent.
    Returns a dictionary with 'is_valid' (boolean) and 'reason' (string).
    """
    system_prompt = """
    You are a strict SQL Database Auditor. 
    Your job is to evaluate if a generated SQL query accurately and logically answers the user's question based on the provided schema.
    
    Rules:
    1. Check for hallucinations (e.g., querying columns that don't exist in the schema).
    2. Check for logic errors (e.g., using the wrong table to answer the question).
    3. Return ONLY a raw JSON object. Do not include markdown formatting like ```json.
    
    Required JSON Format:
    {
        "is_valid": true or false,
        "reason": "Brief explanation of your decision"
    }
    """
    
    # We feed the judge all three pieces of context
    evaluation_prompt = f"""
    User Question: {question}
    Database Schema: {schema_context}
    Generated SQL: {generated_sql}
    """
    
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=evaluation_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0 # Strict and deterministic grading
        )
    )
    
    try:
        # Clean up the response to ensure it's pure JSON
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
        
    except Exception as e:
        # Fail closed: if the judge hallucinates or returns bad JSON, block the query
        return {"is_valid": False, "reason": "The LLM Judge failed to output valid JSON."}