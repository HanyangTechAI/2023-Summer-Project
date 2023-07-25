
from api.base import HaiAPI
from api.secret import OPENAI_API_KEY, NCLOUD_OCR_API_KEY
from PIL import Image, ImageDraw, ImageFont
import time, uuid, requests, json
import openai

openai.api_key = OPENAI_API_KEY
ocr_secret = NCLOUD_OCR_API_KEY

def get_summarization_result(input_text):
    # add prompt to input
    prompt = f"""다음 OCR 결과에 적절한 제목을 붙이고 4줄 이내로 요약하세요.
    항상 한국어로 답변해 주세요.

    ### OCR 결과:

    {input_text}
    제목: 다음에 본문의 제목을, 요약 결과: 다음에 요약 결과를 입력하세요.
    요약 결과의 각 줄은 1. 2. 3. 과 같이 숫자로 시작해야 합니다.
    """

    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", temperature=0,
        messages=[{"role": "user", "content": prompt}], 
        )

    # return the chat completion
    return chat_completion.choices[0].message.content

def get_text_ocr_result(file):
    ocr_url = "https://cxl3q4nzrt.apigw.ntruss.com/custom/v1/23717/d7931b0cf28602762bbfd6fcfd3e42b141bd7a4c5c0bad5dbec4ca350644ac01/general"

    request_json = {
        'images': [
            {
                'format': 'png',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', file)]
    headers = {'X-OCR-SECRET': ocr_secret}

    response = requests.request("POST", ocr_url, headers=headers, data = payload, files = files)
    rescode = response.status_code
    if(rescode == 200):
        return json.loads(response.text)
    else:
        print("Error : " + response.text)
        return None

class AIAPI(HaiAPI):
    def __init__(self, font=None):
        if font is not None:
            self.font = ImageFont.truetype(font, size=20)
        else:
            self.font = ImageFont.load_default()

    def query_image2text(self, file, **kwargs):
        """returns the information of the image as text"""
        image_info = get_text_ocr_result(file)
        ocr_text = ""
        for field in image_info["images"][0]["fields"]:
            ocr_text += field["inferText"]
            if field["lineBreak"]:
                ocr_text += "\n"
            else:
                ocr_text += " "
        return ocr_text

    def query_image2image(self, file, **kwargs):
        """convert the image into grayscale"""
        image = Image.open(file)
        image_grayscale = image.convert('L')
        return image_grayscale

    def query_text2text(self, text: str, **kwargs):
        chatgpt_response = get_summarization_result(text)
        try:
            title = chatgpt_response.split("제목:")[-1].split("요약 결과:")[0].strip()
            summary = chatgpt_response.split("요약 결과:")[-1].strip()
        except:
            title = "에러가 발생했습니다"
            summary = "내용 없음"
        return title, summary        

    def query_text2image(
            self,
            text: str,
            size=(800, 600),
            position=(50, 50),
            bg_color=(0, 0, 0)
    ):
        image = Image.new(mode='RGB', size=size, color=bg_color)
        img_draw = ImageDraw.Draw(image)

        img_draw.text(xy=position, text=text, font=self.font)
        return image
