# Setup pydantic tool (Scheme validation)
from pydantic import BaseModel # How communication between frontend and backend is done(standardized)
from typing import List
from ai_agent import get_response_from_ai_agent

# If from fromtend this format of data should  come to prcess in the backend
# We will receive in this format from frontend
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search:bool

# Setup Ai Agent From Frontend Request( End point from which the request is coming)

from fastapi import FastAPI

app = FastAPI(title="LangGraph AI Agent")


ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gemini-2.0-flash-exp"]

@app.post("/chat")

def chat_endpoint(request: RequestState): # Format will be of RequestState
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    # Check the model name
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    # This all will come from frontend
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response from it! 
    response=get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response # To front end

# Run app 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080) # Run the app

    # http://127.0.0.1:8080/docs

