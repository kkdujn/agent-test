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

st.title("우리 회사 챗봇")

prompt = st.chat_input("여기에 입력하시오.")
if prompt:
    response = agent.invoke(
        {"messages" : [{"role" : "user", "content" : prompt}]}
    )
    st.session_state.messages.append({'role' : "user", 'content' : prompt})
    st.session_state.messages.append({'role' : "ai", 'content' : response['messages'][-1].content})

for message in st.session_state.messages :
    with st.chat_message(message['role']) :
        st.write(message['content'])