# Streamlit 라이브러리 import
import streamlit as st

# langchain 라이브러리에서 필요한 클래스들 import
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# OpenAI API 키 설정
OPENAI_API_KEY = "api-key"

# ChatOpenAI 인스턴스 생성 및 필수 파라미터 설정
chat = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-3.5-turbo",
    api_key=OPENAI_API_KEY
)

# 세션 상태에서 채팅 히스토리 초기화 또는 불러오기
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력 처리 및 모델 응답 생성 함수
def send_click(chat, prompt):
    # 시스템 명령과 사용자 입력을 포함하는 새로운 메시지 생성
    message = [
        SystemMessage(content='You are a pharmacist who is knowledgeable in cosmetics as well as a dermatologist.'
                                'When I say a lesion, you can recommend cosmetics with ingredients suitable for the lesion.'
                                'Search on Google for cosmetic data.'
                              ),
        HumanMessage(content=prompt)
    ]

    # 챗 모델로부터 응답 가져오기
    response = chat(message).content

    # 사용자 입력과 모델 응답을 채팅 히스토리에 추가
    i = 0
    st.session_state.chat_history.append({"role": "🧑‍💼 Interviewee", "content": prompt})
    st.session_state.chat_history.append({"role": "🧑‍💻 interviewer", "content": response})

    return response

# Streamlit 앱의 메인 함수
def main():
    # Streamlit 앱의 타이틀 설정
    st.title('Mock Interview')

    st.text("👉 To start a mock interview, type 'Start a mock interview' in your area")
    st.subheader("🧑‍💼 Interviewee")

    # 사용자 답변을 입력 받기
    user_input = st.text_area("You are interviewee. Please input your answer in this area", key='prompt')

    # 사용자 답변 제출 버튼 생성
    if st.button("Done"):
        # send_click 함수 호출하여 제출 처리
        response = send_click(chat, user_input)

        # "Interviewer" 소제목 아래에 모델 응답 표시
        st.subheader("🧑‍💻 Interviewer")
        st.success(response)

        # "Chat History" 소제목 아래에 채팅 히스토리 표시
        st.subheader("📝 Interview History")
        for message in st.session_state.chat_history:
            with st.expander(message["role"]):
                st.write(message["content"])

# 스크립트 실행 시 Streamlit 앱 시작
if __name__ == '__main__':
    main()
