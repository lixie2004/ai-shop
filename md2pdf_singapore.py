#!/usr/bin/env python3
"""Convert Singapore formal project report from Markdown to PDF via weasyprint."""

import markdown_it
import weasyprint
import os

INPUT_MD = "/home/nicli/.openclaw/workspace/reports/singapore-formal-project-report-2026-05-25.md"
OUTPUT_PDF = "/home/nicli/.openclaw/workspace/reports/singapore-formal-project-report-2026-05-25.pdf"

# Read markdown
with open(INPUT_MD, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert to HTML
md = markdown_it.MarkdownIt("commonmark", {"typographer": True})
md.enable(["table", "strikethrough"])
html_body = md.render(md_content)

# Wrap in a styled HTML document
html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
    @bottom-center {{
        content: "新加坡选品分析正式报告 | 机密文件 | 第 " counter(page) " 页";
        font-family: 'Noto Sans CJK SC', 'Noto Sans SC', 'WenQuanYi Micro Hei', sans-serif;
        font-size: 8pt;
        color: #9ca3af;
    }}
}}

body {{
    font-family: 'Noto Sans CJK SC', 'Noto Sans SC', 'WenQuanYi Micro Hei', sans-serif;
    font-size: 10.5pt;
    line-height: 1.8;
    color: #1f2937;
}}

h1 {{
    font-size: 22pt;
    color: #0f766e;
    text-align: center;
    margin-top: 60mm;
    margin-bottom: 10mm;
    page-break-before: always;
    page-break-after: avoid;
}}

h1:first-of-type {{
    margin-top: 20mm;
}}

h2 {{
    font-size: 16pt;
    color: #0f766e;
    border-bottom: 2px solid #0f766e;
    padding-bottom: 4px;
    margin-top: 30mm;
    page-break-after: avoid;
}}

h3 {{
    font-size: 13pt;
    color: #374151;
    margin-top: 20mm;
    page-break-after: avoid;
}}

h4 {{
    font-size: 11pt;
    color: #4b5563;
    margin-top: 15mm;
}}

p {{
    margin: 6pt 0;
    text-align: justify;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    font-size: 9pt;
    page-break-inside: auto;
}}

tr {{
    page-break-inside: avoid;
}}

th {{
    background-color: #0f766e;
    color: white;
    padding: 6pt 8pt;
    text-align: center;
    font-weight: bold;
}}

td {{
    padding: 5pt 8pt;
    border: 1px solid #e5e7eb;
    text-align: center;
}}

tr:nth-child(even) td {{
    background-color: #f9fafb;
}}

ul, ol {{
    margin: 6pt 0;
    padding-left: 20pt;
}}

li {{
    margin: 3pt 0;
}}

strong {{
    color: #111827;
}}

blockquote {{
    margin: 10pt 0;
    padding: 8pt 16pt;
    background: #f3f4f6;
    border-left: 4px solid #0f766e;
    font-size: 10pt;
}}

code {{
    background: #f3f4f6;
    padding: 1pt 4pt;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 9pt;
}}

pre {{
    background: #f3f4f6;
    padding: 10pt;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
}}

hr {{
    border: none;
    border-top: 1px solid #d1d5db;
    margin: 20pt 0;
}}
</style>
</head>
<body>

{html_body}

</body>
</html>"""

# Write HTML for debugging
html_path = INPUT_MD.replace(".md", ".html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_full)
print(f"HTML written: {html_path}")

# Convert to PDF
print("Converting to PDF via weasyprint...")
weasyprint.HTML(string=html_full).write_pdf(OUTPUT_PDF)
print(f"PDF generated: {OUTPUT_PDF}")

# Check file size
size_kb = os.path.getsize(OUTPUT_PDF) / 1024
print(f"PDF size: {size_kb:.0f} KB")