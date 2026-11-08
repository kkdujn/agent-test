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

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


if "messages" not in st.session_state :
    st.session_state.messages = []

st.title("영어 학원 평가 도우미")

# 채점 결과 저장 공간
if "report" not in st.session_state:
    st.session_state.report = None

if "excel_data" not in st.session_state:
    st.session_state.excel_data = None

with st.sidebar:
    st.header("데이터 업로드")

    # 1. 파일 업로드
    question_file = st.file_uploader("문제지 PDF", type=["pdf"])
    answer_file = st.file_uploader("정답지 PDF", type=["pdf"])
    student_file = st.file_uploader("학생 답안 엑셀",type=["xlsx"])

    st.divider()
    
    # 세 파일이 모두 업로드되었는지 확인
    files_ready = all([
        question_file is not None,
        answer_file is not None,
        student_file is not None
    ])
    

    # 분석 시작
    if st.button(
        "분석 시작",
        use_container_width=True,
        disabled=not files_ready
    ):

        with st.spinner("자동 채점 중입니다..."):

            try:
                # 자동 채점
                report = analyze_files(
                    question_file.getvalue(),
                    student_file.getvalue(),
                    answer_file.getvalue()
                )

                # 채점 결과 저장
                st.session_state.report = report

                # 다운로드할 엑셀 생성
                st.session_state.excel_data = make_excel(report)

                st.success("자동 채점 완료!")

            except Exception as e:
                st.session_state.report = None
                st.session_state.excel_data = None
                st.error(f"채점 오류: {e}")

    # 엑셀 추출 버튼
    st.download_button(
        label="엑셀 추출",
        data=st.session_state.excel_data or b"",
        file_name="채점결과.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        disabled=st.session_state.excel_data is None,
        use_container_width=True
    )


# 메인 화면
st.title("영어 모의고사 평가 도우미")

report = st.session_state.report

if report is not None:

    st.subheader("채점 결과")

    col1, col2, col3 = st.columns(3)

    col1.metric("평균", f"{report.mean:.2f}점")
    col2.metric("중앙값", f"{report.median:.2f}점")
    col3.metric("학생 수", f"{report.count}명")

    st.dataframe(
        report.scores,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("문항별 정답 여부")

    st.dataframe(
        report.correctness,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("왼쪽에서 파일을 업로드하고 분석을 시작해주세요.")
    

prompt = st.chat_input("여기에 입력하시오.", disabled=not st.session_state.analyzed)

if prompt:
    response = agent.invoke(
        {"messages" : [{"role" : "user", "content" : prompt}]}
    )
    st.session_state.messages.append({'role' : "user", 'content' : prompt})
    st.session_state.messages.append({'role' : "ai", 'content' : response['messages'][-1].content})

for message in st.session_state.messages :
    with st.chat_message(message['role']) :
        st.write(message['content'])

