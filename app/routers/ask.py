from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.schema_store import get_relevant_schema
from app.services.sql_generator import generate_sql
from app.services.query_executor import execute_read_query
from app.utils.validator import is_safe_read_query
# --> 1. ADD THIS IMPORT
from app.services.llm_judge import evaluate_sql 

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_finops_assistant(payload: QuestionRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # 1. Fetch schema context
        schema_context = get_relevant_schema(payload.question)
        
        # 2. Call Gemini to generate SQL
        generated_sql = generate_sql(payload.question, schema_context)
        
        # 3. VALIDATE (Stage 1: Static Parsing for Security)
        if not is_safe_read_query(generated_sql):
            raise HTTPException(
                status_code=403, 
                detail=f"Security alert: Generated SQL blocked (mutative command). Query: {generated_sql}"
            )
            
        # --> 4. VALIDATE (Stage 2: LLM-as-a-Judge for Semantic Accuracy)
        judge_evaluation = evaluate_sql(payload.question, generated_sql, schema_context)
        if not judge_evaluation.get("is_valid"):
            raise HTTPException(
                status_code=422, # 422 Unprocessable Entity
                detail=f"AI Validation Failed: {judge_evaluation.get('reason')} (Query: {generated_sql})"
            )
        
        # 5. Execute the safe, validated SQL query
        query_results = execute_read_query(generated_sql)
        
        return {
            "question": payload.question,
            "generated_sql": generated_sql,
            "results": query_results
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except RuntimeError as db_err:
        raise HTTPException(status_code=500, detail=f"Database execution error: {db_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")