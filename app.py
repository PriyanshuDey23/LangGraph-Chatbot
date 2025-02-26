import streamlit as st
from dotenv import load_dotenv
load_dotenv()


# Set page configuration
st.set_page_config(page_title="LangGraph Agent UI", page_icon="🤖", layout="wide")

# Add a background image
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.example.com/background.jpg");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# Title and description
st.title("LangGraph Agent 🤖")
st.write("Create and Interact with the AI Agents!")

# Model Provider
MODEL_NAMES_GROQ = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"]
MODEL_NAMES_GOOGLE = ["gemini-2.0-flash"]



# Sidebar for agent configuration
with st.sidebar:
    st.header("Agent Configuration")
    
    # Input for defining the AI Agent
    system_prompt = st.text_area("📝 Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

    # Model Provider and Model selection
    provider = st.radio("🌐 Select Provider:", ("Groq", "Google"))
    
    # Model selection based on provider
    if provider == "Groq":
        selected_model = st.selectbox("🤖 Select Groq Model:", ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"])
    else:
        selected_model = st.selectbox("🤖 Select Google Model:", ["gemini-2.0-flash"])

    # Web search option
    allow_web_search = st.checkbox("🔍 Allow Web Search") # Boolean



# User query
user_query = st.text_area("💬 Enter your query:", height=150, placeholder="Ask Anything!")

API_URL="http://127.0.0.1:8080/chat" # run  Backend.py


# Submit button
if st.button("🚀 Ask Agent!"):
    # Check if either user query or system prompt is empty
    if not user_query.strip() and not system_prompt.strip():
        st.warning("Both the query and the system prompt are required.")
    elif not user_query.strip():
        st.warning("Please enter a query!")
    elif not system_prompt.strip():
        st.warning("Please define your AI Agent (system prompt)!")
    else:
        with st.spinner("Processing your request..."):
            # Proceed with processing the request if both fields are filled



            #Step2: Connect with backend via URL
            import requests

            # Send post request to swagger  along with data from the user
            payload={
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }

            response=requests.post(API_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json() # Collect the response from 200 code, successful response
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {response_data}")








