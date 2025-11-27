import os
from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

# Define State
class AgentState(BaseModel):
    repo_path: str
    files: List[str] = []
    file_docs: Dict[str, str] = {}
    final_docs: Dict[str, str] = {}

# Initialize LLM - try Gemini first, then OpenAI
llm = None
gemini_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if gemini_key:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    print("Using Google Gemini 2.5 Flash")
elif openai_key:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    print("Using OpenAI GPT-4o-mini")
else:
    raise ValueError("No LLM API key found. Please set GOOGLE_API_KEY or OPENAI_API_KEY")

def list_files_node(state: AgentState):
    """Walks the repo and lists all relevant files."""
    repo_path = state.repo_path
    file_list = []
    for root, _, files in os.walk(repo_path):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.h', '.md')):
                full_path = os.path.join(root, file)
                file_list.append(full_path)
    
    return {"files": file_list}

def analyze_file_node(state: AgentState):
    """
    Analyzes files. In a real graph, this would be a map/reduce or batch operation.
    For simplicity in this MVP, we will iterate sequentially or just do the top 5 files 
    to save tokens/time during the demo.
    """
    files = state.files[:5] # LIMIT for demo purposes
    docs = {}
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            rel_path = os.path.relpath(file_path, state.repo_path)
            
            prompt = f"""
            You are an expert senior engineer.
            Explain this file as if onboarding a new developer.
            
            File: {rel_path}
            
            Code:
            ```
            {content[:2000]} 
            ```
            (Truncated if too long)
            
            Output Markdown with:
            1. Summary of purpose
            2. Key functions/classes
            """
            
            response = llm.invoke([SystemMessage(content="You are a documentation generator."), HumanMessage(content=prompt)])
            docs[rel_path] = response.content
        except Exception as e:
            docs[rel_path] = f"Error analyzing file: {str(e)}"
            
    return {"file_docs": docs}

def generate_readme_node(state: AgentState):
    """Generates a main README based on the file summaries."""
    if not state.file_docs:
        return {"final_docs": {"README.md": "# Project Documentation\n\nNo files were analyzed."}}
    
    # Create a detailed file listing
    file_details = []
    for filename, doc in state.file_docs.items():
        file_details.append(f"### {filename}\n\n{doc}\n")
    
    files_content = "\n".join(file_details)
    
    prompt = f"""Based on the following analyzed files from a codebase, write a comprehensive README.md.

ANALYZED FILES:
{files_content}

Write a complete README.md that includes:
1. Project title and brief description
2. Project Overview - what the project does
3. Key Components - list the main files/modules and their purposes
4. Architecture - how the components work together
5. How to use/run the project (if evident from the code)

Write ONLY the README content in Markdown format. Do not ask for more information."""
    
    response = llm.invoke([SystemMessage(content="You are a technical writer creating documentation from code analysis."), HumanMessage(content=prompt)])
    
    final_docs = state.file_docs.copy()
    final_docs["README.md"] = response.content
    
    return {"final_docs": final_docs}

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("list_files", list_files_node)
workflow.add_node("analyze_files", analyze_file_node)
workflow.add_node("generate_readme", generate_readme_node)

workflow.set_entry_point("list_files")
workflow.add_edge("list_files", "analyze_files")
workflow.add_edge("analyze_files", "generate_readme")
workflow.add_edge("generate_readme", END)

app = workflow.compile()
