
from api.example import ExampleAPI
import streamlit as st
from PIL import Image


@st.cache_resource
def get_api():
    return ExampleAPI(font="resources/malgun.ttf")


def main():
    api = get_api()

    st.title("2023 HAI 여름방학 과제")

    st.subheader("╰(*°▽°*)╯ 명구 형이 읽어주는 방학 과제~~!")

    st.subheader("명구 형이 읽어줬으면 하는 문구를 아래에 첨부해주세요!")
    st.markdown("- 사진을 받아 텍스트로 변환해주고 그걸 또 요약까지 해준답니다~~")    
    query = st.file_uploader('Input Image', key='image2text')

    if query is not None:
        st.image(query)
        response = api.query_image2text(query, key='image2text')
        st.markdown("**API Output**")
        st.code(f"{response}", language="python")
    
    st.markdown("")
    # Text2Text API 활용
    st.subheader("1. Text to Text API 활용")
    st.markdown("- 텍스트를 입력받아 텍스트를 출력하는 API를 사용해 보겠습니다.\n- 텍스트를 입력하면 줄 바꿈과 **HAI is the best!!** 를 추가해줍니다.")

    query = st.text_input('Input Text', "여기에 텍스트 입력", key="text2text")
    response = api.query_text2text(query)

    st.markdown("**API Output**")
    st.code(f"{response}", language="csv")

    # Text2Image API 활용
    st.subheader("2. Text to Image API 활용")
    st.markdown("- 텍스트를 입력받아 이미지를 출력하는 API를 사용해 보겠습니다.\n- 입력된 텍스트가 그려진 비트맵 이미지가 생성됩니다.")

    query = st.text_input('Input Text', "Hello, World!", key="text2image")
    response = api.query_text2image(query, size=(250, 150))

    st.markdown("**API Output**")
    st.image(response)

    # Image2Image API 활용
    st.subheader("3. Image to Image API 활용")
    st.markdown("- 이미지를 입력받아 이미지를 출력하는 API를 사용해 보겠습니다.\n- 입력된 이미지를 그레이스케일로 바꾼 이미지가 생성됩니다.")

    query = st.file_uploader('Input Image', key='image2image')
    if query is not None:
        st.image(query)
        response = api.query_image2image(query)
        st.markdown("**API Output**")
        st.image(response)

    # Image2Text API 활용
    st.subheader("4. Image to Text API 활용")
    st.markdown("- 이미지를 입력받아 텍스트를 출력하는 API를 사용해 보겠습니다.\n- 입력된 이미지의 해상도와 같은 주요 정보를 출력해줍니다.")
    query = st.file_uploader('Input Image')
    if query is not None:
        st.image(query)
        response = api.query_image2text(query, key='image2text')
        st.markdown("**API Output**")
        st.code(f"{response}", language="python")


if __name__ == '__main__':
    main()




