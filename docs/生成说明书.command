#!/bin/bash
# 双击本文件 = 重新生成 使用说明.html
# 内容源只有一个：同目录下的 使用说明.md
cd "$(dirname "$0")" || exit 1

echo ""
echo "📖 正在从 使用说明.md 生成 使用说明.html ..."
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

"$PY" build_help.py
code=$?

echo ""
if [ $code -eq 0 ]; then
  echo "✅ 完成。可以双击上一层的 使用说明.html 查看效果。"
else
  echo "❌ 生成失败，退出码 $code"
fi
echo ""
read -r -p "按回车键关闭…"
