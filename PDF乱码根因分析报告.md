# PDF 乱码根因分析报告

**日期**: 2026-05-14
**调查人**: Emma XIE
**问题**: 上传到 IMA 知识库的 PDF 文件中文显示乱码

---

## 根因结论

**fontconfig 缓存过期导致 weasyprint 字体匹配失败，回退到不兼容的字体。**

### 详细分析

#### 1. 现象对比

| 文件 | 生成时间 | 主字体 | IMA 显示 |
|------|---------|--------|---------|
| Indonesia 5-12 | 5/13 21:48 | Noto Sans CJK SC (CIDFontType0) | ✅ 正常 |
| Vietnam 5-12 | 5/13 06:17 | Noto Sans CJK SC (CIDFontType0) | ✅ 正常 |
| Malaysia 5-12 | 5/13 06:27 | Noto Sans CJK SC (CIDFontType0) | ✅ 正常 |
| **Vietnam 5-14** | **5/14 03:24** | **WenQuanYi Micro Hei (CIDFontType2)** | ❌ **乱码** |
| **Malaysia 5-14** | **5/14 04:56** | **WenQuanYi Micro Hei (CIDFontType2)** | ❌ **乱码** |
| **Indonesia 5-14** | **5/14 06:16** | **WenQuanYi Micro Hei (CIDFontType2)** | ❌ **乱码** |
| Philippines 5-14 | 5/14 07:53 | Noto Sans CJK SC (CIDFontType0) | ✅ 正常 |

#### 2. 关键发现

1. **fontconfig 缓存过期**: 系统 fontconfig 缓存最后更新于 **5月11日**，已 3 天未更新
2. **字体回退**: 当 weasyprint 通过 Pango 请求 "Noto Sans CJK SC" 时，由于缓存过期，fontconfig 返回了错误的字体匹配结果，导致 Pango 回退到 WenQuanYi Micro Hei
3. **CIDFontType2 vs CIDFontType0**: WenQuanYi 使用 CIDFontType2（基于 TrueType），而 Noto CJK 使用 CIDFontType0（基于 CFF/PostScript）。IMA 的 PDF 渲染器对 CIDFontType2 + Identity-H 编码的 CJK 字体支持不佳，导致中文显示乱码
4. **时间线吻合**: 5-14 凌晨 03:24-06:16 生成的 PDF 都用了错误的字体，而 07:53 生成的 Philippines PDF 恢复正常（可能因为系统状态变化）

#### 3. 验证

执行 `fc-cache -fv` 更新 fontconfig 缓存后，重新生成 Indonesia PDF：
- **修复前**: 主字体 = WenQuanYi Micro Hei (CIDFontType2) → IMA 乱码
- **修复后**: 主字体 = Noto Sans CJK SC (CIDFontType0) → 正常显示

#### 4. 为什么之前"改正不了"

每次修复都只针对表面症状（换字体、改 CSS），没有发现底层原因是 **fontconfig 缓存过期**。缓存不更新，weasyprint 每次启动时都会读到错误的字体匹配结果。

---

## 修复方案

### 立即修复
```bash
# 更新 fontconfig 缓存
fc-cache -fv
```

### 长期方案
1. **在 md2pdf.py 开头自动更新字体缓存**（或在 PDF 生成前检查缓存时效）
2. **在 CSS 中明确指定字体文件路径**，绕过 fontconfig 匹配
3. **定期清理 fontconfig 缓存**（每周一次）

### 建议的 CSS 修复
将字体回退改为直接指定字体文件：
```css
@font-face {
    font-family: 'CJK';
    src: url('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc') format('truetype');
    font-weight: normal;
}
@font-face {
    font-family: 'CJK';
    src: url('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc') format('truetype');
    font-weight: bold;
}
body {
    font-family: 'CJK', sans-serif;
}
```

---

## 受影响文件

需要重新生成并重新上传以下 PDF：
- indonesia-formal-project-report-2026-05-14.pdf
- vietnam-formal-project-report-2026-05-14.pdf
- malaysia-formal-project-report-2026-05-14.pdf

（所有在 5/14 03:24-06:16 期间生成的使用 WenQuanYi 字体的 PDF）
