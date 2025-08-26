import requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 기상청 API 키를 여기에 입력하세요.
KMA_API_KEY = "발급받은_API_키를_여기에_붙여넣으세요"

class WeatherQuery(BaseModel):
    location: str

def get_weather_data_from_kma(location: str):
    # 기상청 API 엔드포인트와 파라미터 설정
    # (실제 API 문서에 맞춰 엔드포인트와 파라미터를 수정해야 합니다.)
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        'serviceKey': KMA_API_KEY,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': '20250827',  # 현재 날짜 (동적 생성 필요)
        'base_time': '0600',  # 현재 시간 (동적 생성 필요)
        'nx': '60',  # 예시: 서울 (실제 위치 좌표 필요)
        'ny': '127'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        # JSON 데이터에서 필요한 날씨 정보를 추출하는 로직
        # (예: 기온, 습도 등)
        weather_info = "현재 서울의 기온은 25도입니다." # 추출된 정보로 대체
        return {"status": "success", "data": weather_info}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

@app.post("/get_weather")
def get_weather(query: WeatherQuery):
    weather_result = get_weather_data_from_kma(query.location)
    return weather_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)