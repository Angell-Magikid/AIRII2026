#!/usr/bin/env python3
import os, subprocess, re, html

IMG_DIR = "images"
OUT = "gallery.html"

# group rules
def group_of(name):
    if name.startswith("Banner_"):
        return "A"
    if "_Big_" in name:
        return "B"
    if name in ("Home_2.png", "airii-logo.png", "magikid-logo.png"):
        return "D"
    return "C"

GROUP_META = {
    "A": ("底部半透明模糊大图 · Bottom Banners", "background-size: cover（自动裁切）", "建议：宽屏横图 ≥16:9"),
    "B": ("整屏英雄大图 · Hero / Big", "object-fit: cover（自动裁切）", "建议：宽屏横图 3:2 ~ 16:9"),
    "C": ("板块配图 / 卡片图 · Section & Card", "object-fit: cover（自动裁切）", "建议：4:3 或 16:10"),
    "D": ("特殊图 · 按原始比例显示（不裁切）", "原始比例显示（不裁切）", "透明 PNG，保持比例"),
}

GROUP_ORDER = ["A", "B", "C", "D"]

def dims(name):
    p = os.path.join(IMG_DIR, name)
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                         capture_output=True, text=True).stdout
    w = h = 0
    for line in out.splitlines():
        m = re.search(r"pixelWidth:\s*(\d+)", line)
        if m: w = int(m.group(1))
        m = re.search(r"pixelHeight:\s*(\d+)", line)
        if m: h = int(m.group(1))
    return w, h

files = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(".png"))
by_group = {g: [] for g in GROUP_ORDER}
for f in files:
    by_group[group_of(f)].append(f)

rows = []
for g in GROUP_ORDER:
    if not by_group[g]:
        continue
    title, crop, suggest = GROUP_META[g]
    rows.append(f'<section class="grp">')
    rows.append(f'<h2>{html.escape(title)}</h2>')
    rows.append(f'<p class="meta">{html.escape(crop)} ｜ {html.escape(suggest)}</p>')
    rows.append('<div class="grid">')
    for f in by_group[g]:
        w, h = dims(f)
        ratio = f"{w}:{h}"
        # simplify ratio display
        rows.append('<figure class="card">')
        rows.append(f'<div class="thumb"><img loading="lazy" src="images/{html.escape(f)}" alt="{html.escape(f)}"></div>')
        rows.append(f'<figcaption>')
        rows.append(f'<div class="fname">{html.escape(f)}</div>')
        rows.append(f'<div class="dim">{w} × {h} px <span class="ratio">({ratio})</span></div>')
        rows.append(f'</figcaption>')
        rows.append('</figure>')
    rows.append('</div></section>')

css = """
:root{--bg:#06081a;--panel:#0e1230;--line:#232a55;--txt:#e8ecff;--muted:#9aa3d0;--cyan:#00D4FF;--green:#3ddc84;}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;}
header{padding:48px 24px 24px;max-width:1200px;margin:0 auto;}
header h1{font-size:2rem;margin:0 0 8px;}
header p{color:var(--muted);margin:0;}
main{max-width:1200px;margin:0 auto;padding:0 24px 80px;}
.grp{margin-top:48px;}
.grp h2{font-size:1.25rem;border-left:4px solid var(--cyan);padding-left:12px;margin:0 0 4px;}
.grp p.meta{color:var(--muted);font-size:.85rem;margin:0 0 18px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px;}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;}
.thumb{aspect-ratio:4/3;background:#05060f;overflow:hidden;display:flex;align-items:center;justify-content:center;}
.thumb img{width:100%;height:100%;object-fit:cover;}
.card figcaption{padding:10px 12px;}
.fname{font-size:.8rem;word-break:break-all;color:var(--txt);}
.dim{font-size:.8rem;color:var(--cyan);margin-top:4px;}
.ratio{color:var(--muted);}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:.8rem;text-align:center;padding:24px;}
a{color:var(--cyan);}
"""

html_doc = f"""<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>图片库 · AIRII2026 Image Library</title>
<style>{css}</style>
</head>
<body>
<header>
<h1>图片库 · AIRII2026 Image Library</h1>
<p>全部 {len(files)} 张图片，含尺寸、比例与裁切说明。替换图片时保留文件名即可，系统会自动裁切（D 类不裁切）。</p>
</header>
<main>
{''.join(rows)}
</main>
<footer>Generated reference · {len(files)} images · 替换请保持文件名</footer>
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html_doc)
print(f"wrote {OUT} with {len(files)} images")
