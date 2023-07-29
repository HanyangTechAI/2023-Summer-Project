from api.AI import AIAPI
import streamlit as st

def main():
    text = None
    
    st.title("2023_HAI_web_project")

    st.header("1. OCR API를 이용한 이미지 파일 인식\n")
    image = st.file_uploader("이미지 파일을 업로드하세요.\n (jpg, png, jpeg 형식만 가능)", type=['jpg', 'png', 'jpeg'])
    
    if 'button' not in st.session_state :
        st.session_state.button = False
        
    def click_button():
        st.session_state.button = not st.session_state.button
    
    st.button('Run',key=1, on_click=click_button)
    
    if st.session_state.button :
        with st.expander("입력된 이미지 보기") :
            st.image(image)
        with st.expander("OCR 결과 확인하기") :
            text = AIAPI.query_image2text(image, image)
            st.write(text)
            
    st.divider()
    
    st.header("2. GPT API를 이용하여 텍스트 요약하기\n")
    st.subheader("원문")
    if text == None :
        text = ' '
    st.info(text)
    
    if st.button("Run", key=2) :
        with st.expander("요약본 보기") :
            title, summary = AIAPI.query_text2text(text, text)
            st.subheader(title)
            st.write(summary)
    
if __name__ == '__main__' :
    main()