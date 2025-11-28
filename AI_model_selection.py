import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(override=True)
groq_api_key = os.getenv("GROQ_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
genai_api_key = os.getenv("GEMINI_API_KEY")
llm = ""
st.set_page_config(
    page_title = "Choose your own model",
)
# st.title("Select your AI Model")
st.header("Select AI Model")
provider = st.selectbox(
    "AI Models",
    options=["-select a provider-","Deepseek", "Gemini", "Groq"]
)

if provider == "Deepseek":
    model = st.selectbox(
        "choose model",
        options=["-select a model-","deepseek-chat", "deepseek-reasoner"]
    )
    llm = ChatDeepSeek(api_key=deepseek_api_key, model=model, temperature=0.5)
elif provider == "Gemini":
    model = st.selectbox(
        "choose model",
        options=["-select a model-", "gemini-2.5-pro", "gemini-2.5-flash"]
    )
    llm = ChatGoogleGenerativeAI(api_key=genai_api_key, model=model, temperature=0.5)
else:
    model = st.selectbox(
        "choose model",
        options=["-select a model-", "llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    )
    llm = ChatGroq(model=model, api_key=groq_api_key, temperature=0.1)
if provider not in ["-select a provider-"] and  model not in ["-select a model-"]:
    st.write(f"Good choice! You've selected {provider} -> {model}. Fire your query now")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input("You:")
if user_prompt:
    st.chat_message("user").write(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    try:
        response = llm.invoke(input=[{"role": "system", "content":"You are a helpful chat assistant"},
                    *st.session_state.chat_history])
        assistant_response = getattr(response, "content", None) or getattr(response, "text", "")
        assistant_response = f"[{provider} | {model}]\n\n{assistant_response}"
        st.session_state.chat_history.append({"role": "system", "content": assistant_response})
        with st.chat_message("assistant"):
            st.write(assistant_response)
    except Exception as e:
        st.write(e)
