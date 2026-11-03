-- 방명록(guestbook) 스키마 — Supabase(Postgres)
-- 정책: 누구나 읽기 + 누구나 작성 (바로 공개). 수정·삭제는 대시보드에서만.
-- 아직 Supabase에 적용하지 않음. 적용 전에 사용자 확인 필요.

create table public.guestbook (
  id         bigint generated always as identity primary key,
  name       text        not null check (char_length(btrim(name))    between 1 and 30),
  message    text        not null check (char_length(btrim(message)) between 1 and 500),
  created_at timestamptz not null default now(),
  is_visible boolean     not null default true   -- 나쁜 글을 숨길 때 false로 변경
);

create index guestbook_created_at_idx on public.guestbook (created_at desc);

-- RLS
alter table public.guestbook enable row level security;

-- 읽기: 보이는 글만
create policy "anyone can read"
  on public.guestbook for select
  to anon, authenticated
  using (is_visible);

-- 쓰기: 누구나. 단, 숨김 처리된 글로는 못 씀
create policy "anyone can write"
  on public.guestbook for insert
  to anon, authenticated
  with check (is_visible);

-- 수정·삭제 정책은 만들지 않음 → 기본적으로 모두 거부됨

-- 방문자가 채울 수 있는 칸을 이름·메시지로만 제한
revoke all on public.guestbook from anon, authenticated;
grant select on public.guestbook to anon, authenticated;
grant insert (name, message) on public.guestbook to anon, authenticated;

-- 주의: 화면에 출력할 때는 innerHTML 대신 textContent 사용 (스크립트 삽입 방지)
-- 주의: service_role 키는 HTML·GitHub에 넣지 말고 .env에만 보관
