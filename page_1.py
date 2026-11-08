
import streamlit as st

# 화면 중앙에 배치하기 위한 여백
st.markdown("<div style='height: 100px;'></div>",
            unsafe_allow_html=True)

# 가천대학교 로고 중앙 정렬
left, center, right = st.columns([2,2,2])

with center:
    st.image("gachon_logo.jpg", use_container_width=True)

# 로고와 제목 사이 간격
st.markdown("<div style='height: 50px;'></div>",
            unsafe_allow_html=True)

# 학원 이름
st.markdown(
    """
    <h2 style='text-align: center;'>
        영어 학원 평가 도우미
    </h2>
    """,
    unsafe_allow_html=True
)
