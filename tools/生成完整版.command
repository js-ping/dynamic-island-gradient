#!/bin/bash
# 双击本文件 = 把 tools/vendor 里的 HEIC 解码器拼进 index.html，产出「完整版」单文件
# index.html 本身保持干净（纯 MIT），拼装结果写到 ../dist/Daoying-full-heic.html
cd "$(dirname "$0")" || exit 1

echo ""
echo "📦 正在打包「完整版」（含内置 HEIC 解码器）…"
echo ""

PY=""
for c in /usr/bin/python3 python3 /opt/homebrew/bin/python3; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done

if [ -z "$PY" ]; then
  echo "❌ 没找到 Python 3。"
  echo "   macOS 自带 /usr/bin/python3，如果报错请先运行： xcode-select --install"
  echo ""
  read -r -p "按回车键关闭…"
  exit 1
fi

"$PY" build_full.py
code=$?

echo ""
if [ $code -eq 0 ]; then
  echo "✅ 完成。产物在上一层的 dist/ 目录里，双击即可试。"
else
  echo "❌ 打包失败，退出码 $code"
fi
echo ""
read -r -p "按回车键关闭…"
