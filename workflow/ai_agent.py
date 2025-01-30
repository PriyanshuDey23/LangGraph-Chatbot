# Setup Api keys

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv('GROQ_API_KEY')
TAVILY_API_KEY=os.getenv('TAVILY_API_KEY')
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')


# Setup LLm and Tools

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

google_llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=GOOGLE_API_KEY)
groq_llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=GROQ_API_KEY)

search_tool=TavilySearchResults(max_results=3,api_key=TAVILY_API_KEY)


# Setup AI Agent with Search tool functionality

from langgraph.prebuilt import create_react_agent

from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"

agent=create_react_agent(
    model=groq_llm,
    tools=[search_tool],
    state_modifier=system_prompt # Role 
)


# Combining everything in a function
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="Google":
        llm=ChatGoogleGenerativeAI(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search else [] # Allow search from front end

    agent=create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]

# Testing
# query="Tell me about how to make a cake"
# state={"messages": query}
# response=agent.invoke(state)
# messages=response.get("messages")
# ai_messages=[message.content for message in messages if isinstance(message, AIMessage)] # only ai message 
# print (ai_messages[-1]) # Last AI message





