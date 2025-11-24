import streamlit as st
from streamlit.navigation import page
from langchain_groq import ChatGroq
import os
import dotenv

dotenv.load_dotenv(override=True)
groq_api_key = os.environ.get("GROQ_API_KEY")

st.set_page_config(
    layout="centered",
    page_title="AI chatbot"
)
st.title("chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.6
)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("You: ")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
try:
    response = llm.invoke(input=[{"role": "system", "content": "you are a helpful chat assistant"}, *st.session_state.chat_history])
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
except Exception as e:
    st.markdown(f"I ran into an error! \n\n{e}")
    # st.session_state.chat_history = []


