"""가족 페이지 로컬 테스트 서버 (내 PC에서만 접속 가능).

- family/ 폴더를 http://127.0.0.1:8000 으로 보여준다.
- /config.js 요청이 오면 .env.local 의 SUPABASE_URL / SUPABASE_ANON_KEY 를 읽어
  페이지가 쓸 수 있는 설정으로 만들어 준다. (키는 파일에 복사하지 않음)
- 실행: python scripts/dev_server.py   (종료: Ctrl+C)
"""

import json
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "family"
ENV_FILE = ROOT / ".env.local"
HOST, PORT = "127.0.0.1", 8000  # 127.0.0.1 = 이 PC에서만 접속 가능


def read_env_local():
    values = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return values


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/config.js":
            return self.send_config()
        return super().do_GET()

    def send_config(self):
        env = read_env_local()
        url, key = env.get("SUPABASE_URL"), env.get("SUPABASE_ANON_KEY")
        if not url or not key:
            body = b"console.error('.env.local \\uc5d0 SUPABASE_URL / SUPABASE_ANON_KEY \\uac00 \\ud544\\uc694\\ud569\\ub2c8\\ub2e4');"
            self.send_response(503)
        else:
            config = {"url": url, "anonKey": key}
            body = ("window.SUPABASE_CONFIG = " + json.dumps(config) + ";").encode("utf-8")
            self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = read_env_local()
    ok = bool(env.get("SUPABASE_URL") and env.get("SUPABASE_ANON_KEY"))
    print(f"서버 폴더: {SITE_DIR}")
    print(f".env.local: {'OK (값은 화면에 표시하지 않음)' if ok else '없음 또는 비어 있음 → 방명록이 동작하지 않아요'}")
    print(f"접속 주소: http://{HOST}:{PORT}/   (종료: Ctrl+C)")
    handler = partial(Handler, directory=str(SITE_DIR))
    with ThreadingHTTPServer((HOST, PORT), handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료했어요.")


if __name__ == "__main__":
    main()
