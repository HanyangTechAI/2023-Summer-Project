
from api.AI import AIAPI
import streamlit as st
from PIL import Image


@st.cache_resource
def get_api():
    return AIAPI(font="resources/malgun.ttf")


def main():
    api = get_api()

    st.title("2023 HAI 여름방학 과제")
    st.divider()
    st.subheader("╰(*°▽°*)╯ 명구 형이 읽어주는 방학 과제~~!")
    st.markdown("- 명구 형이 읽어줬으면 하는 문구를 아래에 첨부해주세요!")
    st.markdown("- 사진을 받아 텍스트로 추출해주고 그걸 또 요약까지 해준답니다~~")    
    query = st.file_uploader('사진 첨부', key='image2text')

    if query is not None:
        st.image(query)
        response = api.query_image2text(query, key='image2text')
        st.markdown("### **텍스트로 추출!**")
        st.markdown("> " + response)
        title, summary = api.query_text2text(response, key='text2text')
        st.markdown("### **요약!**")
        st.markdown(title)
        st.markdown(summary)
        st.divider()
        st.subheader("끝~~ 안녕!")

if __name__ == '__main__':
    main()




