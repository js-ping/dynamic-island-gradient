#!/bin/bash
# 双击本文件 = 在本机起一个小服务器并打开浏览器
#
# 平时其实用不到它 —— 直接双击 index.html 就能用。
# 只有在下面两种情况才需要：
#   1. 双击 index.html 打不开（个别系统会拦）
#   2. 想用手机访问（手机连同一个 WiFi，输下面显示的局域网地址）
cd "$(dirname "$0")" || exit 1

PORT=9527
echo ""
echo "  ◒  灵动岛渐变工具"
echo "  ────────────────────────────────"
echo ""

# 挑一个没被占用的端口
for p in $(seq $PORT $((PORT+20))); do
  if ! lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1; then PORT=$p; break; fi
done

# 本机局域网 IP
LAN=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)
[ -z "$LAN" ] && LAN=$(ifconfig 2>/dev/null | awk '/inet 192\.|inet 10\.|inet 172\./{print $2; exit}')

echo "  本机打开：  http://localhost:$PORT"
if [ -n "$LAN" ]; then
  echo "  手机打开：  http://$LAN:$PORT     （手机需连同一个 WiFi）"
else
  echo "  手机打开：  没检测到局域网地址，先确认 WiFi 已连接"
fi
echo ""
echo "  按 Ctrl+C 停止服务"
echo ""

sleep 1
open "http://localhost:$PORT" >/dev/null 2>&1

PY=""
for c in /usr/bin/python3 python3 /opt/homebrew/bin/python3; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done

if [ -z "$PY" ]; then
  echo "❌ 没找到 Python 3，请直接双击 index.html 使用。"
  read -r -p "按回车键关闭…"
  exit 1
fi

exec "$PY" -m http.server "$PORT" --bind 0.0.0.0
