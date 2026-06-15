#!/usr/bin/env python3
"""Convert Markdown report to styled HTML for PDF generation."""

import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'markdown', '-q'])
    import markdown

def convert(md_path: str, html_path: str):
    md_content = Path(md_path).read_text(encoding='utf-8')
    
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc', 'attr_list']
    )
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>菲律宾跨境电商选品分析正式项目报告 2026-06-08</title>
<style>
@page {{
  size: A4;
  margin: 20mm 18mm 18mm 18mm;
  @bottom-center {{
    content: "第 " counter(page) " 页 | 机密文件";
    font-size: 8px;
    color: #6b7280;
  }}
}}
body {{
  font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", "Microsoft YaHei", sans-serif;
  max-width: 100%;
  margin: 0;
  padding: 0;
  color: #1a1a1a;
  line-height: 1.7;
  background: #fff;
  font-size: 11px;
}}
h1 {{ font-size: 24px; color: #1a56db; border-bottom: 3px solid #1a56db; padding-bottom: 10px; margin-top: 36px; page-break-after: avoid; }}
h2 {{ font-size: 18px; color: #1e40af; border-bottom: 1px solid #dbeafe; padding-bottom: 6px; margin-top: 28px; page-break-after: avoid; }}
h3 {{ font-size: 15px; color: #1e3a5f; margin-top: 20px; page-break-after: avoid; }}
h4 {{ font-size: 13px; color: #374151; margin-top: 16px; page-break-after: avoid; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10px; }}
th {{ background: #1a56db; color: #fff; padding: 6px 8px; text-align: center; font-weight: 600; }}
td {{ padding: 5px 8px; border-bottom: 1px solid #e5e7eb; text-align: center; }}
tr:nth-child(even) td {{ background: #f9fafb; }}
blockquote {{ border-left: 4px solid #1a56db; margin: 12px 0; padding: 6px 12px; background: #f0f7ff; font-size: 10px; }}
code {{ background: #f3f4f6; padding: 2px 4px; border-radius: 3px; font-size: 10px; }}
pre {{ background: #f3f4f6; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 10px; }}
hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }}
ul, ol {{ padding-left: 20px; }}
li {{ margin: 3px 0; }}
strong {{ color: #1e40af; }}
a {{ color: #1a56db; text-decoration: none; }}
img {{ max-width: 100%; }}
.page-break {{ page-break-before: always; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""
    
    Path(html_path).write_text(html_template, encoding='utf-8')
    print(f"✅ HTML generated: {html_path}")
    print(f"   Size: {Path(html_path).stat().st_size / 1024:.1f} KB")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python md2html.py <input.md> <output.html>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
