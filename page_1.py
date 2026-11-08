import streamlit as st
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5.4-mini")

tavily_tool = TavilySearch(
    max_results=5,
    topic="general",
)

agent = create_agent(model, tools=[tavily_tool])


if "messages" not in st.session_state :
    st.session_state.messages = []

st.title("영어 학원 평가 도우미")
