# 작업 기록 (progress)

> 한 일을 요약해서 **아래에 계속 추가**해요 (append-only). 기존 기록은 고치거나 지우지 않습니다.

---

## 2026-11-01

1. `tasks/todo.md`, `tasks/progress.md` 생성
2. `SECURITY.md` 키 노출 비상 매뉴얼 작성
3. `README.md` 폴더 구조 정리
4. `.gitignore` 생성 (`.env`, `*.key`, `*.pem` 등 제외)
5. `.env` 템플릿 생성 (키 값은 비워 둠 — 직접 입력 필요)
6. `scripts/weather.py` 작성 (Open-Meteo, 키 불필요) → 직접 실행해 `weather.txt` 생성 확인
7. 작업 스케줄러 `SeongbukWeather` 등록 (매일 09:00, 꺼져 있었으면 켜진 뒤 실행) → 수동 실행 테스트 성공
8. `.env`에 `DISCORD_WEBHOOK_URL` 칸 추가, `scripts/discord_notify.py` 작성 (주소 비어 있을 때 안전하게 중단되는 것까지 확인)
9. `SECURITY.md`에 디스코드 웹후크 유출 시 대응 추가
10. 디스코드 실제 전송 테스트 성공 (HTTP 204, 채널에서 메시지 확인됨)
11. 스케줄러 `SeongbukWeather`에 2번째 동작 추가 (날씨 저장 → 디스코드 전송), 예약 경로 전체 실행 테스트 성공 (결과 코드 0)
12. 가족 소개 웹페이지 `family/index.html` 작성 (반응형, 다크모드 대응) → 데스크톱·모바일(375px) 화면 확인. 연락처는 빈칸으로 둠
13. 가족 페이지 연락처 섹션에 전화·이메일·주소 입력 (전화·이메일은 클릭 링크), 브라우저에서 텍스트 확인
14. README.md 폴더 구조 최신화, `git init`(이 폴더 전용 작성자: GitHub noreply), 첫 커밋 "Initial setup" (d4bdba6)
15. GitHub private 레포 `phk08060-pixel/claude-workspace-20261101` 생성 및 push (family 포함). 기존 `claude-workspace` 레포는 이름이 겹쳐 건드리지 않음. 확인: 레포 PRIVATE, `.env` 미업로드, 로컬·원격 커밋 일치

## 2026-11-02

16. 디스코드 웹후크 URL 변경 반영: `.env`의 `DISCORD_WEBHOOK_URL`에 새 주소 입력 확인 (형식 정상, 값은 비공개) → 전송 테스트 성공 (HTTP 204). 코드 수정은 없음
17. 가족 페이지 Vercel 배포 준비 (배포는 사용자가 직접): 연락처에서 집 주소·전화번호 제거(이메일, "서울 성북구"만 남김), noindex·공유 미리보기 메타 추가, `family/vercel.json`·`family/robots.txt` 추가, README에 배포 방법 정리. 브라우저에서 데스크톱 2열 확인, vercel.json 형식 검사 통과
    - 참고: 이전 커밋 기록(GitHub private 레포)에는 상세 주소·전화번호가 남아 있음
18. 🚨 GitHub 레포가 PUBLIC으로 바뀐 것을 발견 (처음 만들 때는 private 확인). 변경 원인은 모름. 사용자가 "나중에 하겠다"고 해서 공개 범위는 아직 그대로. 예전 커밋 기록에 상세 주소·전화번호·유치원명이 남아 있어 정리가 필요함
19. Vercel 배포 후 사이트가 안 보인다는 문의 진단: 세 프로젝트 모두 `/`는 404, `/family/`는 200 → Root Directory가 `family`가 아니라 레포 맨 위로 배포됨. 설정 변경(Root Directory=`family` 후 Redeploy)은 사용자가 직접 진행하기로 함 (결과 확인 전)
20. 가족 페이지 배경색을 따뜻한 색으로 변경(밝은 모드 `#fcecd8`, 어두운 모드 갈색 기운), 브라우저 확인 후 커밋 abc24bd 푸시
21. 방명록 DB 설계안 작성 (`docs/guestbook-schema.sql`, 테이블명 guestbook) — 이후 요청(messages)으로 대체됨

## 2026-11-03

22. 방명록(messages) 기능 로컬 구현:
    - `.env.local` 생성(Supabase 주소·anon 키, 값은 비공개), `.gitignore`에 `.env.local` 명시
    - `docs/messages-schema.sql` 작성(id, name, content, created_at + 글자 수 제한 + RLS: 누구나 읽기·쓰기, 수정·삭제 불가) → Supabase SQL Editor에서 사용자가 직접 실행
    - `scripts/dev_server.py` 작성(로컬 전용, `.env.local`을 읽어 `/config.js` 제공)
    - `family/index.html` 맨 아래에 방명록 폼·목록 추가(`textContent` 출력)
23. 로컬 테스트 통과: 읽기 200, 익명 삭제는 권한 오류로 차단, 글쓰기 후 목록 갱신, `<b>` 태그가 글자 그대로 표시, 밝은·어두운 모드 화면 확인. 테스트 글 1건("테스트")이 DB에 남아 있음(대시보드에서 삭제 필요). 커밋·Vercel 반영은 아직 안 함
