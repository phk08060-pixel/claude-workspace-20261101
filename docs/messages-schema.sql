-- 가족 페이지 방명록(messages) — Supabase(Postgres)
-- 정책: 누구나 읽기 + 누구나 작성. 수정·삭제는 대시보드(관리자)에서만.
-- 여러 번 실행해도 안전하도록 작성함.

create table if not exists public.messages (
  id         bigint generated always as identity primary key,
  name       text        not null check (char_length(btrim(name))    between 1 and 30),
  content    text        not null check (char_length(btrim(content)) between 1 and 500),
  created_at timestamptz not null default now()
);

create index if not exists messages_created_at_idx on public.messages (created_at desc);

-- RLS
alter table public.messages enable row level security;

drop policy if exists "anyone can read"  on public.messages;
drop policy if exists "anyone can write" on public.messages;

create policy "anyone can read"
  on public.messages for select
  to anon, authenticated
  using (true);

create policy "anyone can write"
  on public.messages for insert
  to anon, authenticated
  with check (true);

-- 수정·삭제 정책은 만들지 않음 → 방문자는 수정·삭제 불가

-- 방문자가 채울 수 있는 칸은 이름·내용뿐 (id, created_at은 서버가 채움)
revoke all on public.messages from anon, authenticated;
grant select on public.messages to anon, authenticated;
grant insert (name, content) on public.messages to anon, authenticated;
