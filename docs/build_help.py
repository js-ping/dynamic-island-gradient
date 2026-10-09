#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用说明.md  ->  使用说明.html

零依赖（只用 Python 标准库），零第三方包。
设计原则：说明书只维护 md 一份，html 永远由本脚本重新生成，避免两个版本内容打架。

用法：
    python3 build_help.py            # 用默认路径
    python3 build_help.py in.md out.html
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC_DEFAULT = os.path.join(HERE, "使用说明.md")
OUT_DEFAULT = os.path.join(ROOT, "使用说明.html")
OUT_ALIAS = os.path.join(ROOT, "help.html")   # 英文名副本，手机上好输网址


# ---------------------------------------------------------------- 行内格式
def inline(text: str) -> str:
    """把一行里的行内标记转成 HTML。调用前必须已经做过 HTML 转义。"""
    # 行内代码优先（内部不再解析其他标记）
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash, text)
    # 图片 ![alt](src)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # 链接 [text](url)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    for i, c in enumerate(codes):
        text = text.replace("\x00%d\x00" % i, "<code>%s</code>" % c)
    return text


def slug(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s).strip("-").lower()
    return s or "sec"


# ---------------------------------------------------------------- 主体转换
def convert(md: str) -> str:
    lines = md.split("\n")
    out = []
    toc = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # ---- 围栏代码块
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = ' class="lang-%s"' % lang if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, html.escape("\n".join(buf))))
            continue

        # ---- 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            body = inline(html.escape(m.group(2).strip()))
            sid = slug(m.group(2))
            if lvl == 1:
                out.append('<h1 id="%s">%s</h1>' % (sid, body))
            else:
                out.append(
                    '<h%d id="%s"><a class="anchor" href="#%s">#</a>%s</h%d>'
                    % (lvl, sid, sid, body, lvl)
                )
                if lvl == 2:
                    toc.append((sid, re.sub(r"<[^>]+>", "", body)))
            i += 1
            continue

        # ---- 分隔线
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # ---- 表格
        if line.strip().startswith("|") and i + 1 < n and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]
        ):
            def cells(row):
                row = row.strip()
                if row.startswith("|"):
                    row = row[1:]
                if row.endswith("|"):
                    row = row[:-1]
                return [c.strip() for c in row.split("|")]

            head = cells(line)
            aligns = []
            for c in cells(lines[i + 1]):
                if c.startswith(":") and c.endswith(":"):
                    aligns.append("center")
                elif c.endswith(":"):
                    aligns.append("right")
                elif c.startswith(":"):
                    aligns.append("left")
                else:
                    aligns.append("")
            i += 2
            body_rows = []
            while i < n and lines[i].strip().startswith("|"):
                body_rows.append(cells(lines[i]))
                i += 1

            t = ['<div class="tw"><table>', "<thead><tr>"]
            for k, c in enumerate(head):
                a = ' style="text-align:%s"' % aligns[k] if aligns[k] else ""
                t.append("<th%s>%s</th>" % (a, inline(html.escape(c))))
            t.append("</tr></thead><tbody>")
            for r in body_rows:
                t.append("<tr>")
                for k in range(len(head)):
                    c = r[k] if k < len(r) else ""
                    a = ' style="text-align:%s"' % aligns[k] if aligns[k] else ""
                    t.append(
                        '<td data-label="%s"%s>%s</td>'
                        % (html.escape(head[k]), a, inline(html.escape(c)))
                    )
                t.append("</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        # ---- 引用块
        if line.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = "<br>".join(inline(html.escape(b)) for b in buf if b.strip())
            out.append("<blockquote>%s</blockquote>" % inner)
            continue

        # ---- 列表
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s", line))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i]):
                items.append(
                    re.sub(r"^\s*([-*+]|\d+\.)\s+", "", lines[i]).strip()
                )
                i += 1
            lis = "".join("<li>%s</li>" % inline(html.escape(x)) for x in items)
            out.append("<%s>%s</%s>" % (tag, lis, tag))
            continue

        # ---- 空行
        if not line.strip():
            i += 1
            continue

        # ---- 段落
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
            r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|>|\||```|-{3,})", lines[i]
        ):
            buf.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(html.escape(" ".join(buf))))

    body = "\n".join(out)

    nav = ""
    if toc:
        nav = '<nav class="toc"><b>目录</b><ul>' + "".join(
            '<li><a href="#%s">%s</a></li>' % (s, t) for s, t in toc
        ) + "</ul></nav>"
        # 目录插在正文第一个 h1 之后，读起来更顺
        if "</h1>" in body:
            body = body.replace("</h1>", "</h1>\n" + nav, 1)
        else:
            body = nav + body

    return TPL.replace("{{BODY}}", body)


# ---------------------------------------------------------------- 页面模板
TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>灵动岛渐变工具 · 使用说明</title>
<meta name="color-scheme" content="light dark">
<style>
:root{
  --bg:#f4f5f9; --card:#fff; --text:#191d27; --text2:#4d5568; --text3:#868ea3;
  --line:#e2e5ee; --accent:#6d5efc; --code-bg:#f0f1f7; --quote:#6d5efc;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0e0f15; --card:#161922; --text:#eceef5; --text2:#a6adc0; --text3:#767e93;
    --line:#262b38; --accent:#8b7dff; --code-bg:#1e2230; --quote:#8b7dff;
  }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--text);
  font:15px/1.85 -apple-system,BlinkMacSystemFont,"PingFang SC","Segoe UI","Microsoft YaHei",sans-serif;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:820px;margin:0 auto;padding:40px 22px 90px}
h1{font-size:28px;line-height:1.35;margin:0 0 6px;letter-spacing:-.02em}
h2{font-size:21px;margin:46px 0 14px;padding-top:22px;border-top:1px solid var(--line);letter-spacing:-.01em}
h3{font-size:17px;margin:30px 0 10px}
h4{font-size:15px;margin:22px 0 8px;color:var(--text2)}
p{margin:12px 0;color:var(--text)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.anchor{float:left;margin-left:-20px;opacity:0;color:var(--text3);font-weight:400;text-decoration:none}
h2:hover .anchor,h3:hover .anchor{opacity:.7}
hr{border:none;border-top:1px solid var(--line);margin:34px 0}
strong{font-weight:650}
code{
  background:var(--code-bg);padding:2px 6px;border-radius:6px;
  font:13px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  word-break:break-word;
}
pre{
  background:var(--code-bg);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;overflow:auto;margin:18px 0;
}
pre code{background:none;padding:0;font-size:12.5px;line-height:1.85;color:var(--text2)}
blockquote{
  margin:18px 0;padding:12px 18px;border-left:3px solid var(--quote);
  background:color-mix(in srgb, var(--quote) 7%, transparent);
  border-radius:0 10px 10px 0;color:var(--text2);
}
blockquote p{margin:0}
ul,ol{margin:12px 0;padding-left:24px}
li{margin:6px 0}
.tw{overflow-x:auto;margin:18px 0}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card);border-radius:12px;overflow:hidden}
th,td{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:color-mix(in srgb, var(--accent) 9%, var(--card));font-weight:650;font-size:13px;white-space:nowrap}
tr:last-child td{border-bottom:none}
.toc{
  background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:16px 20px 10px;margin:26px 0 8px;
}
.toc b{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--text3)}
.toc ul{list-style:none;padding:0;margin:10px 0 6px;display:flex;flex-wrap:wrap;gap:6px 8px}
.toc li{margin:0}
.toc a{
  display:inline-block;padding:4px 12px;border-radius:100px;font-size:13px;
  background:color-mix(in srgb, var(--accent) 10%, transparent);color:var(--text2);
  border:1px solid var(--line);
}
.toc a:hover{color:var(--accent);text-decoration:none}
footer{
  margin-top:60px;padding-top:20px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--text3);text-align:center;line-height:1.9;
}
/* 窄屏：表格转卡片 */
@media (max-width:640px){
  .wrap{padding:26px 15px 70px}
  h1{font-size:23px} h2{font-size:18.5px}
  table,thead,tbody,tr,td,th{display:block;width:100%}
  thead{display:none}
  table{background:none;border-radius:0}
  tr{
    background:var(--card);border:1px solid var(--line);border-radius:12px;
    margin-bottom:12px;padding:6px 0;overflow:hidden;
  }
  td{border:none;border-bottom:1px dashed var(--line);padding:9px 14px;font-size:13.5px}
  tr td:last-child{border-bottom:none}
  td::before{
    content:attr(data-label);display:block;
    font-size:11px;font-weight:650;letter-spacing:.05em;
    color:var(--accent);margin-bottom:3px;
  }
  td[data-label=""]::before{display:none}
  .anchor{display:none}
}
/* 打印 */
@media print{
  :root{--bg:#fff;--card:#fff;--text:#000;--text2:#333;--text3:#666;--line:#ccc}
  body{font-size:11pt}
  .toc,.anchor{display:none}
  h2{page-break-after:avoid;break-after:avoid}
  table,pre,blockquote{page-break-inside:avoid;break-inside:avoid}
  a{color:#000;text-decoration:underline}
}
</style>
</head>
<body>
<div class="wrap">
{{BODY}}
<footer>
  <p>本页由 <code>docs/使用说明.md</code> 自动生成 · 内容源只有一份<br>
  修改说明请改 md 文件，然后双击 <code>docs/生成说明书.command</code></p>
</footer>
</div>
</body>
</html>
"""


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else SRC_DEFAULT
    out = sys.argv[2] if len(sys.argv) > 2 else OUT_DEFAULT

    if not os.path.exists(src):
        print("找不到源文件：%s" % src)
        return 1

    with open(src, encoding="utf-8") as f:
        md = f.read()

    page = convert(md)

    with open(out, "w", encoding="utf-8") as f:
        f.write(page)

    # 英文名副本，方便手机直接输网址
    if os.path.abspath(out) == os.path.abspath(OUT_DEFAULT):
        with open(OUT_ALIAS, "w", encoding="utf-8") as f:
            f.write(page)
        print("已生成：%s" % OUT_ALIAS)

    print("已生成：%s" % out)
    print("源文件：%s（%.1f KB）" % (src, len(md.encode()) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
