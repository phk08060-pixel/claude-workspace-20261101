# 📁 Claude Workspace

Claude Code와 함께 일하는 나의 작업 공간이에요.
Claude Code는 시작할 때마다 `CLAUDE.md` 를 읽고 그 규칙을 따릅니다.

---

## 🗂️ 폴더 구조

```
claude_workspace_20261101/
├── CLAUDE.md          ← Claude Code에게 주는 지침서 (규칙·소통 방식)
├── SECURITY.md        ← 🚨 키 노출 시 비상 매뉴얼
├── README.md          ← 지금 보는 파일 (폴더 안내)
├── .env               ← 🔒 환경변수(키) 보관 (GitHub에 올라가지 않음, 절대 공유 금지)
├── .env.local         ← 🔒 방명록(Supabase) 주소·공개용 키 (GitHub에 올라가지 않음)
├── .gitignore         ← 민감 파일이 git에 올라가지 않게 막기
├── weather.txt        ← 성북구 날씨·미세먼지 (매일 09:00 자동 갱신)
├── scripts/
│   ├── weather.py     ← 날씨 가져오는 스크립트 (API 키 불필요)
│   ├── discord_notify.py ← weather.txt를 디스코드로 전송 (웹후크 필요)
│   └── dev_server.py  ← 가족 페이지 로컬 테스트 서버 (방명록용, 이 PC에서만 접속)
├── family/
│   ├── index.html     ← 가족 소개 웹페이지 (더블클릭하면 브라우저에서 열림)
│   ├── build-config.js ← Vercel 배포 때 방명록 설정(config.js)을 환경변수로 생성
│   ├── vercel.json    ← Vercel 배포 설정 (보안·검색 차단 헤더)
│   └── robots.txt     ← 검색엔진 수집 차단
├── tasks/
│   ├── todo.md        ← 오늘 할 일 (체크리스트)
│   └── progress.md    ← 한 일 기록 (아래로 계속 추가)
└── docs/
    ├── messages-schema.sql   ← 방명록 테이블·RLS (Supabase SQL Editor에 붙여넣기)
    └── guestbook-schema.sql  ← 처음 설계안 (messages-schema.sql로 대체됨)
```

## 📄 파일 설명

| 파일 | 용도 | 언제 보나요? |
|------|------|--------------|
| `CLAUDE.md` | 보안 규칙, 위험 작업 확인, 소통·작업 원칙 | Claude가 작업 시작할 때 자동으로 |
| `SECURITY.md` | 키 폐기 → 재발급 → 교체 순서 | 키 노출이 의심될 때 |
| `tasks/todo.md` | 오늘 할 일 | 작업 시작할 때 |
| `tasks/progress.md` | 한 일 요약 (지우지 않고 추가만) | 작업 끝날 때 |
| `scripts/weather.py` | 성북구 날씨·미세먼지를 가져와 `weather.txt`에 저장 | 매일 09:00 자동 실행 |
| `scripts/discord_notify.py` | `weather.txt`를 디스코드 채널로 전송 | 날씨 저장 직후 자동 실행 |
| `family/index.html` | 가족 소개 웹페이지 (반응형) | 더블클릭해서 브라우저로 열기 |
| `docs/` | 참고 자료 | 필요할 때 |

---

## ⏰ 자동 실행 (Windows 작업 스케줄러)

작업 이름 `SeongbukWeather` — 매일 오전 9시에 아래 순서로 실행돼요.

1. `scripts/weather.py` → 날씨·미세먼지를 `weather.txt`에 저장 (API 키 불필요, Open-Meteo 사용)
2. `scripts/discord_notify.py` → 디스코드 웹후크로 전송 (`.env`의 `DISCORD_WEBHOOK_URL` 필요)

> 스케줄러 설정은 PC에 저장돼요. 다른 PC에서 쓰려면 다시 등록해야 합니다.

---

## 🔄 하루 작업 흐름

1. **시작** → `tasks/todo.md` 확인
2. **큰 작업(3단계 이상)** → 계획을 `todo.md` 에 먼저 적고, OK 후 실행
3. **작업 중** → 한 단계씩 바꾸고 확인
4. **끝** → 실제로 돌려서 확인 → `tasks/progress.md` 에 기록

---

## 🔒 지켜야 할 것 (요약)

- API 키·비밀번호는 **마스킹**해서 보기 (`sk-or-v1-***`)
- 키는 코드에 쓰지 말고 **`.env` 환경변수**로만
- `.env`, `*.key`, `*.pem`, `id_rsa`, `credentials` 는 **절대 `git add` 금지**
- 삭제·되돌리기 같은 위험한 작업은 **먼저 물어보기**
- 키 노출이 의심되면 → **`SECURITY.md`** 를 열기

자세한 규칙은 [CLAUDE.md](CLAUDE.md), 비상 대응은 [SECURITY.md](SECURITY.md) 를 보세요.

---

## 🚀 가족 페이지 Vercel 배포 방법

빌드가 필요 없는 정적 사이트예요.

1. [vercel.com](https://vercel.com) 로그인 → **Add New… → Project**
2. GitHub 레포 `claude-workspace-20261101` 선택 (private 레포는 Vercel의 GitHub 연결 허용이 필요해요)
3. **Root Directory** 를 `family` 로 지정 (중요)
4. Framework Preset은 **Other**, Build Command·Output Directory는 비워 둠
5. **Deploy**

배포 후에는 주소를 아는 누구나 볼 수 있어요. 공개용이라 `index.html`에는 집 주소·전화번호를 넣지 않았고(지역은 "서울 성북구"까지만), 검색엔진에 노출되지 않도록 `noindex`와 `robots.txt`를 설정했어요. 단, 이건 **접속을 막는 게 아니라** 검색에 안 나오게 하는 거예요.

---

## 💬 방명록 로컬 테스트

가족 페이지 맨 아래 방명록은 Supabase(`messages` 테이블)를 사용해요.

1. `.env.local`에 `SUPABASE_URL`, `SUPABASE_ANON_KEY`를 적어요 (공개용 `anon` 키만. `service_role` 키는 절대 넣지 않기)
2. Supabase 대시보드 SQL Editor에 `docs/messages-schema.sql` 내용을 붙여넣고 Run (한 번만, 여러 번 실행해도 안전)
3. 터미널에서 실행: `python scripts/dev_server.py`
4. 브라우저에서 `http://127.0.0.1:8000/` 접속 (종료는 `Ctrl+C`)

- 파일을 더블클릭해서 열면 방명록은 꺼져 있어요 (설정을 전달해 주는 서버가 없기 때문). 나머지 페이지는 그대로 보여요.
- 수정·삭제는 방문자가 못 해요. 글을 지우려면 Supabase 대시보드 → Table Editor에서 직접 삭제하세요.
- Vercel 배포에서 방명록 켜기: Vercel → Settings → Environment Variables에 `SUPABASE_URL`, `SUPABASE_ANON_KEY` 등록 → Build Command `node build-config.js`, Output Directory `.`, Root Directory `family` → Redeploy. 배포할 때 `family/build-config.js`가 `config.js`를 만들어 줘요 (`family/config.js`는 GitHub에 올라가지 않아요).

---

## 🛠️ 다른 곳에서 내려받았다면

`.env`는 GitHub에 올라가지 않으므로 직접 만들어야 해요. 아래 항목을 적고 값은 직접 입력하세요 (**채팅에 붙여 넣지 말기**).

```
OPENROUTER_API_KEY=
WORDPRESS_URL=
WORDPRESS_USER=
WORDPRESS_APP_PASSWORD=
DISCORD_WEBHOOK_URL=
ORACLE_SSH_KEY_PATH=~/.ssh/oracle-server.key
ORACLE_SERVER_ALIAS=oracle-server
```
