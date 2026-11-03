// Vercel 배포 때 실행: 환경변수로 config.js 를 만든다. (키 값은 이 파일에 쓰지 않음)
// 사용: node build-config.js [출력 경로]   (기본: 이 폴더의 config.js)
const fs = require("fs");
const path = require("path");

const out = process.argv[2] || path.join(__dirname, "config.js");
const url = (process.env.SUPABASE_URL || "").trim();
const anonKey = (process.env.SUPABASE_ANON_KEY || "").trim();

let body;
if (url && anonKey) {
  body = "window.SUPABASE_CONFIG = " + JSON.stringify({ url, anonKey }) + ";\n";
  console.log("config.js 생성 완료 (값은 표시하지 않음)");
} else {
  // 배포는 깨뜨리지 않고, 방명록만 꺼진 상태로 둔다.
  body = "// SUPABASE_URL / SUPABASE_ANON_KEY 환경변수가 없어 방명록이 꺼져 있어요.\n";
  console.warn("경고: SUPABASE_URL / SUPABASE_ANON_KEY 가 없어요. 방명록이 꺼진 채로 배포돼요.");
}
fs.writeFileSync(out, body);
