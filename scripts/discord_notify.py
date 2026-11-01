"""weather.txt 의 내용을 디스코드 웹후크로 보낸다.

웹후크 주소는 .env 의 DISCORD_WEBHOOK_URL (또는 같은 이름의 환경변수)에서만 읽는다.
주소는 비밀번호와 같으므로 화면/로그에 출력하지 않는다. 표준 라이브러리만 사용.
"""
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
WEATHER_FILE = ROOT / "weather.txt"
ALLOWED_PREFIXES = (
    "https://discord.com/api/webhooks/",
    "https://discordapp.com/api/webhooks/",
)


def read_env(name):
    """환경변수 우선, 없으면 .env 파일에서 찾는다."""
    if os.environ.get(name):
        return os.environ[name].strip()
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() == name:
                return value.strip().strip('"').strip("'")
    return ""


def main():
    url = read_env("DISCORD_WEBHOOK_URL")
    if not url:
        raise RuntimeError(".env 의 DISCORD_WEBHOOK_URL 이 비어 있어요")
    if not url.startswith(ALLOWED_PREFIXES):
        raise RuntimeError("DISCORD_WEBHOOK_URL 형식이 올바르지 않아요 (디스코드 웹후크 주소가 아님)")
    if not WEATHER_FILE.exists():
        raise RuntimeError("weather.txt 가 없어요 (weather.py 를 먼저 실행하세요)")

    text = WEATHER_FILE.read_text(encoding="utf-8").strip()
    payload = {"content": f"```\n{text[:1900]}\n```"}  # 디스코드 글자 제한 2000자
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "weather-notify/1.0"},
        method="POST",
    )
    with urlopen(req, timeout=20) as res:
        print(f"sent to discord (HTTP {res.status})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # 주소가 로그에 남지 않도록 예외 종류와 메시지만 출력
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
