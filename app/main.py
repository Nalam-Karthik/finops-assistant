from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
# 1. Import the router you just created in app/routers/ask.py
from app.routers.ask import router as ask_router

app = FastAPI(
    title="FinOps Assistant",
    description="Ask natural-language questions about cloud costs.",
    version="0.1.0",
)

# Without this, your frontend/index.html (Part 7) making a fetch() call to
# this API would get silently blocked by the browser's same-origin policy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Register your new router here
app.include_router(ask_router, tags=["FinOps Core"])


@app.get("/")
def health_check():
    """
    Zero dependencies on purpose — no DB, no LLM. This is your first line
    of debugging: "is the server even alive", independent of everything else.
    """
    return {"status": "ok", "service": "finops-assistant"}