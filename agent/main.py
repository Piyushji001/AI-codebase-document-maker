from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import app as agent_graph, AgentState
import os

app = FastAPI()

class AnalysisRequest(BaseModel):
    repo_path: str

@app.post("/analyze")
def analyze_repo(request: AnalysisRequest):
    repo_path = request.repo_path
    
    if not os.path.exists(repo_path):
        raise HTTPException(status_code=404, detail=f"Repo path not found: {repo_path}")

    try:
        # Invoke LangGraph
        initial_state = AgentState(repo_path=repo_path)
        result = agent_graph.invoke(initial_state)
        
        return result["final_docs"]
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate_limit" in error_msg.lower():
            raise HTTPException(status_code=429, detail="OpenAI API rate limit exceeded. Please check your API key quota or wait a moment.")
        elif "401" in error_msg or "authentication" in error_msg.lower():
            raise HTTPException(status_code=401, detail="OpenAI API authentication failed. Please check your API key.")
        else:
            raise HTTPException(status_code=500, detail=f"Agent analysis failed: {error_msg}")
