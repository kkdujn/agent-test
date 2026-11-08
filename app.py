import streamlit as st 
from dotenv import load_dotenv

load_dotenv()

# st.title("우리 회사 챗봇")

page_1 = st.Page("page_1.py", title = '1 페이지', icon = '🌸') # 객체 만들고 할당
page_2 = st.Page("page_2.py", title = '2 페이지') 
page_3 = st.Page("page_3.py", title = '3 페이지') 

pages = st.navigation([page_1, page_2, page_3], position = 'top')

pages.run()