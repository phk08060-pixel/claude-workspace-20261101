"""서울 성북구 날씨 + 미세먼지를 가져와 weather.txt 에 저장한다.

API 키 없이 Open-Meteo(날씨, 대기질)를 사용한다. 표준 라이브러리만 사용.
저장 위치: 이 파일의 상위 폴더(작업 폴더)의 weather.txt (실행할 때마다 덮어씀)
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

LAT, LON = 37.5894, 127.0167  # 서울 성북구
OUT = Path(__file__).resolve().parent.parent / "weather.txt"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast?" + urlencode({
    "latitude": LAT, "longitude": LON, "timezone": "Asia/Seoul", "forecast_days": 1,
    "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
})
AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality?" + urlencode({
    "latitude": LAT, "longitude": LON, "timezone": "Asia/Seoul",
    "current": "pm10,pm2_5",
})

# WMO 날씨 코드 -> 한국어
WMO = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "서리 안개",
    51: "약한 이슬비", 53: "이슬비", 55: "강한 이슬비",
    56: "약한 어는 이슬비", 57: "강한 어는 이슬비",
    61: "약한 비", 63: "비", 65: "강한 비",
    66: "약한 어는 비", 67: "강한 어는 비",
    71: "약한 눈", 73: "눈", 75: "강한 눈", 77: "싸락눈",
    80: "약한 소나기", 81: "소나기", 82: "강한 소나기",
    85: "약한 소낙눈", 86: "강한 소낙눈",
    95: "뇌우", 96: "우박 동반 뇌우", 99: "강한 우박 동반 뇌우",
}


def fetch(url):
    with urlopen(url, timeout=20) as res:
        return json.load(res)


def grade(value, limits):
    """한국 환경부 기준 등급. limits = (좋음 상한, 보통 상한, 나쁨 상한)"""
    for name, limit in zip(("좋음", "보통", "나쁨"), limits):
        if value <= limit:
            return name
    return "매우나쁨"


def main():
    w = fetch(WEATHER_URL)
    a = fetch(AIR_URL)
    cur, day, air = w["current"], w["daily"], a["current"]

    pm10, pm25 = air["pm10"], air["pm2_5"]
    lines = [
        f"[서울 성북구] {datetime.now():%Y-%m-%d %H:%M} 기준",
        "",
        f"날씨      : {WMO.get(cur['weather_code'], '알 수 없음')}",
        f"현재 기온 : {cur['temperature_2m']}°C (체감 {cur['apparent_temperature']}°C)",
        f"오늘 기온 : 최저 {day['temperature_2m_min'][0]}°C / 최고 {day['temperature_2m_max'][0]}°C",
        f"강수확률  : {day['precipitation_probability_max'][0]}%",
        f"습도      : {cur['relative_humidity_2m']}%",
        f"바람      : {cur['wind_speed_10m']} km/h",
        "",
        f"미세먼지(PM10)    : {pm10} ㎍/㎥ ({grade(pm10, (30, 80, 150))})",
        f"초미세먼지(PM2.5) : {pm25} ㎍/㎥ ({grade(pm25, (15, 35, 75))})",
        "",
        "출처: Open-Meteo (모델 기반 추정값, 측정소 실측값과 다를 수 있음)",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"saved: {OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # 실패 시 기존 weather.txt 는 그대로 둔다
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
