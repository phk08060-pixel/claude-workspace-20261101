# 오늘 할 일 (todo)

> 작업 시작 시 이 파일을 확인하고, 끝난 항목은 `[x]`로 바꿔요.
> 끝난 일의 요약은 `progress.md`에 기록합니다.

## 오늘 (2026-11-01)

- [x] CLAUDE.md 지침서 작성
- [x] 작업 환경 구축
  - [x] tasks/todo.md, tasks/progress.md 생성
  - [x] SECURITY.md 비상 매뉴얼 작성
  - [x] README.md 폴더 구조 정리
- [x] `.env` 템플릿 만들기
- [x] `.gitignore` 만들기 (`.env`, `*.key`, `*.pem` 제외)
- [ ] `.env` 빈칸에 키 직접 입력 (채팅에 붙여 넣지 말기)

## 계획: 성북구 날씨·미세먼지 자동 저장 (완료)

- 데이터: Open-Meteo 날씨 API + Open-Meteo 대기질 API (둘 다 API 키 불필요, 동작 확인함)
- 위치: 성북구 위도 37.5894, 경도 127.0167
- 도구: Python 3.14 (설치 확인됨), 외부 라이브러리 없이 표준 라이브러리만 사용

- [x] 1. `scripts/weather.py` 작성 (날씨 + PM10/PM2.5 가져와서 한국어로 정리)
- [x] 2. 직접 한 번 실행해서 `weather.txt`가 잘 생기는지 확인
- [x] 3. 윈도우 작업 스케줄러에 "매일 09:00" 등록
- [x] 4. 등록 확인 (예약 목록 조회) 및 progress.md 기록

## 계획: 날씨 정보를 디스코드로 전송 (완료)

- 방식: 디스코드 Webhook (봇·토큰 불필요, 주소 하나로 전송)
- 웹후크 주소는 비밀번호와 같아서 `.env`의 `DISCORD_WEBHOOK_URL`에만 저장 (코드에 쓰지 않음, 화면에는 마스킹)
- 기존 `weather.py`는 건드리지 않고 새 파일 `scripts/discord_notify.py`를 추가 (weather.txt를 읽어서 전송)

- [x] 0. (사용자) 디스코드에서 웹후크 만들고, 주소를 `.env`에 직접 입력
- [x] 1. `scripts/discord_notify.py` 작성 (`.env`에서 주소 읽기, weather.txt 내용 전송)
- [x] 2. 직접 한 번 실행해서 디스코드 채널에 메시지가 오는지 확인
- [x] 3. 작업 스케줄러 `SeongbukWeather`에 2번째 동작으로 추가 (날씨 저장 → 디스코드 전송 순서)
- [x] 4. 예약 실행 테스트 및 progress.md, SECURITY.md(웹후크 유출 시 대응) 갱신

## 계획: GitHub private 레포로 올리기 (완료 — 레포 이름은 claude-workspace-20261101)

- 점검 결과: git·gh 설치됨, GitHub 로그인됨(계정 phk08060-pixel), `.gitignore` 이미 있음, 코드 속 키·웹후크 주소 없음
- 레포 이름: `claude-workspace` (private)
- 커밋 작성자: 이 폴더에만 적용되는 설정으로 GitHub 계정 이름 + noreply 이메일 사용 (진짜 이메일 노출 방지)
- 주의: `family/index.html`에 전화번호·이메일·집 주소·아이 유치원명이 들어 있음 → 포함 여부를 승인 때 결정

- [ ] 1. `.gitignore` 확인 및 필요 시 보강 (이미 있음, `.env` 등 제외 확인)
- [ ] 2. `README.md` 폴더 구조 최신화
- [ ] 3. `git init` + 이 폴더 전용 작성자 설정
- [ ] 4. `git add` 후 **올라갈 파일 목록 확인** (`.env`가 없는지 검사)
- [ ] 5. 커밋 `Initial setup`
- [ ] 6. `gh repo create claude-workspace --private --source=. --push`
- [ ] 7. 레포가 private인지, `.env`가 올라가지 않았는지 확인 후 progress.md 기록

## 계획: 가족 페이지 Vercel 배포 준비 (1~5 완료, 6은 사용자 몫) — 배포는 사용자가 직접

- 방식: 빌드 없는 정적 사이트. Vercel에서 Root Directory를 `family`로 지정
- 개인정보: 공개 웹에는 집 주소·전화·아이 유치원명이 누구에게나 보임 → 공개 범위 결정 필요
- 검색 노출 방지: noindex 메타 + `robots.txt` + `X-Robots-Tag` 헤더 (주소를 아는 사람만 접속하게 하는 보호는 아님)

- [x] 1. (결정) 공개용 연락처 처리 방식 선택 → 주소·전화 가리기
- [x] 2. `family/vercel.json` 추가 (cleanUrls, 보안·noindex 헤더)
- [x] 3. `family/robots.txt` 추가 (검색 수집 차단)
- [x] 4. `family/index.html`에 noindex 메타, 공유 미리보기(OG) 태그 추가
- [x] 5. 브라우저에서 화면 확인 + README에 "Vercel 배포 방법" 정리 + 기록
- [ ] 6. (사용자) Vercel에서 GitHub 레포 연결 → Root Directory `family` → Deploy

## 계획: 가족 페이지 방명록(messages) — 로컬 테스트까지 (완료, 커밋·배포 반영은 아직)

- 점검 결과: 받은 키는 공개용 `anon` 역할(service_role 아님), 프로젝트 주소와 일치. `.env.local`은 `.gitignore`의 `.env.*`에 이미 걸림
- 키·주소는 `.env.local`에만 저장 (이 문서·커밋·채팅에는 쓰지 않음, 화면엔 마스킹)
- 정적 HTML은 `.env.local`을 직접 못 읽음 → 로컬 전용 서버(`scripts/dev_server.py`)가 `.env.local`을 읽어 `/config.js`를 만들어 줌
- 이전 설계(`docs/guestbook-schema.sql`, 테이블명 guestbook)는 이번 요청(messages, content)이 대신함 → 새 파일로 작성, 옛 파일은 그대로 둠
- 이번 범위는 **로컬 테스트까지**. Vercel 배포 반영과 커밋은 따로 확인

- [x] 1. `.env.local` 생성 (`SUPABASE_URL`, `SUPABASE_ANON_KEY`) + `.gitignore`에 `.env.local` 줄 명시 추가
- [x] 2. `docs/messages-schema.sql` 작성 (id, name, content, created_at + 글자 수 제한 + RLS: 누구나 읽기·쓰기, 수정·삭제 불가)
- [x] 3. Supabase에 테이블·RLS 적용 — 사용자가 SQL Editor에서 직접 실행
- [x] 4. `scripts/dev_server.py` 작성 (family/ 서빙 + `/config.js` 생성, 내 PC에서만 접속)
- [x] 5. `family/index.html` 맨 아래에 폼 + 목록 추가 (`textContent` 사용, 글자 수 제한, 등록 후 목록 갱신, 다크모드·모바일 대응)
- [x] 6. 로컬 서버를 띄워 글 작성 → 목록 표시 확인 (빈 값·긴 글 거부는 브라우저 입력 제한에 맡기고 직접 시험하진 않음)
- [x] 7. progress.md 기록, README에 로컬 실행 방법 추가
- [x] 8. Vercel 배포에서도 방명록이 동작하게 하는 방법 정하기 → 환경변수 + 빌드 때 `config.js` 자동 생성으로 결정
- [ ] 9. 테스트 글("테스트") 삭제 (사용자, Supabase Table Editor)

## 계획: Vercel에서 방명록 켜기 (코드는 완료, 커밋·Vercel 설정은 아직)

- 방식: Vercel 환경변수 `SUPABASE_URL`, `SUPABASE_ANON_KEY` → 배포할 때 `node build-config.js`가 `config.js` 생성 (키를 레포에 넣지 않음)

- [x] 1. `family/build-config.js` 작성 (환경변수가 없으면 방명록만 꺼진 채로 배포)
- [x] 2. `.gitignore`에 `family/config.js` 추가
- [x] 3. 내 PC에서 시험 (환경변수 있을 때 생성 OK, 없을 때 경고만, git 무시 확인)
- [ ] 4. 커밋·푸시
- [ ] 5. (사용자) Vercel Settings → Environment Variables 2개 등록
- [ ] 6. (사용자) Build Command `node build-config.js`, Output Directory `.`, Root Directory `family` → Redeploy
- [ ] 7. 배포 주소에서 방명록 동작 확인

## 나중에

- [ ] (여기에 추가)
