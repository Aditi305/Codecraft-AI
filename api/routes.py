from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from orchestration.graph import app as agent_app
import json

# API routes
router = APIRouter(prefix="/api/v1", tags=["code-generation"])

class TaskRequest(BaseModel):
    task: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "task": "Create a Python function to calculate fibonacci numbers"
            }
        }

class TaskResponse(BaseModel):
    architecture: str
    code: str
    tests: str
    review: str
    final_decision: str

@router.post("/generate", response_model=TaskResponse, summary="Generate code using multi-agent system")
def generate_code(request: TaskRequest):
    """
    Main endpoint - runs the multi-agent workflow to generate code.
    
    Workflow:
    1. Architect - designs the architecture
    2. Coder - writes the code
    3. Tester - creates tests
    4. Reviewer - reviews everything
    5. Manager - decides approve/rewrite
    
    If manager says rewrite, it loops back to coder.
    """
    try:
        # run the agent workflow
        result = agent_app.invoke({
            "task": request.task
        })

        return TaskResponse(
            architecture=result.get("architecture", ""),
            code=result.get("code", ""),
            tests=result.get("tests", ""),
            review=result.get("review", ""),
            final_decision=result.get("decision", "")
        )
    except Exception as e:
        error_str = str(e)
        
        # handle different error types
        if "insufficient_quota" in error_str or "429" in error_str or "quota" in error_str.lower():
            raise HTTPException(
                status_code=402,  # Payment Required
                detail={
                    "error": "API Quota Exceeded",
                    "message": "You've exceeded your API quota or need to set up billing.",
                    "solutions": [
                        "1. Check your OpenRouter account credits: https://openrouter.ai/credits",
                        "2. Add credits if needed: https://openrouter.ai/credits",
                        "3. Check your usage: https://openrouter.ai/activity",
                        "4. Wait for your quota to reset, or add more credits"
                    ],
                    "help_links": {
                        "credits": "https://openrouter.ai/credits",
                        "activity": "https://openrouter.ai/activity",
                        "keys": "https://openrouter.ai/keys"
                    }
                }
            )
        elif "api_key" in error_str.lower() or "authentication" in error_str.lower() or "unauthorized" in error_str.lower():
            raise HTTPException(
                status_code=401,  # Unauthorized
                detail={
                    "error": "OpenRouter API Key Issue",
                    "message": "There's a problem with your OpenRouter API key.",
                    "solutions": [
                        "1. Verify your API key is correct in the .env file",
                        "2. Check if your API key is active: https://openrouter.ai/settings/keys",
                        "3. Make sure you've set OPENROUTER_API_KEY in your .env file (not OPENAI_API_KEY)",
                        "4. Get your API key from: https://openrouter.ai/settings/keys"
                    ],
                    "help_links": {
                        "keys": "https://openrouter.ai/settings/keys",
                        "credits": "https://openrouter.ai/credits",
                        "activity": "https://openrouter.ai/activity"
                    }
                }
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail={
                    "error": "Processing Error",
                    "message": str(e),
                    "help": "Check the error message above for details. If the issue persists, verify your OpenRouter API key and account status at https://openrouter.ai/settings/keys"
                }
            )

