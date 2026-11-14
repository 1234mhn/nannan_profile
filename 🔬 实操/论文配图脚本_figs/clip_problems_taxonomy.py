#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLIP 医学影像 · 问题分类图（四类问题 → 代表方法）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm

for cand in ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Serif CJK SC"]:
    try:
        fm.findfont(cand, fallback_to_default=False)
        plt.rcParams["font.sans-serif"] = [cand]
        break
    except Exception:
        continue
plt.rcParams["axes.unicode_minus"] = False

DARK = "#243141"
GREY = "#8b949e"
ORANGE = "#c87d14"
C1 = "#3d6fa8"
C2 = "#2e7d5b"
C3 = "#8a5cb8"
C4 = "#c0642f"

fig, ax = plt.subplots(figsize=(14.5, 9.2), dpi=200)
ax.set_xlim(0, 14.5)
ax.set_ylim(0, 9.2)
ax.axis("off")

# 标题
ax.text(0.5, 8.75, "医学 CLIP 的四类问题：后续方法都在补什么",
        fontsize=22, color=DARK, fontweight="bold", va="center")
ax.text(0.5, 8.28, "CLIP 解决了「不靠人工标签」；但医学场景带来了新的四个洞",
        fontsize=12.5, color=GREY, va="center")
ax.plot([0.5, 1.4], [8.05, 8.05], color=ORANGE, lw=3.2, solid_capstyle="butt")

# 起点小框
sb = FancyBboxPatch((0.5, 7.15), 13.5, 0.66, boxstyle="round,pad=0.03,rounding_size=0.08",
                    linewidth=1.5, edgecolor=GREY, facecolor="#f7f8f9")
ax.add_patch(sb)
ax.text(0.78, 7.48, "CLIP 的原始贡献：用「图 + 自然语言」做对比学习，视觉模型摆脱人工标签，可零样本分类。",
        fontsize=11.2, color=DARK, va="center")

cats = [
    (C1, "①", "对齐粒度太粗", "整图压成一个向量、整份报告压成一个向量，对齐一次就完事。\n但一张胸片有多个器官和病灶，报告也讲好几件事。",
     ["GloRIA", "MedFILIP", "CP-CLIP", "MG-3D"]),
    (C2, "②", "文本脏、配对不准", "医学报告冗长啰嗦、说法不统一，还常有「正常报告配异常图像」的假阴性。\n硬对齐会学到错误关联。",
     ["MedCLIP", "MedKLIP"]),
    (C3, "③", "缺医学先验知识", "通用 CLIP 只学到「图上有什么」；医学要判断病变、疾病、解剖关系。",
     ["MedKLIP", "MG-3D", "Abn-BLIP"]),
    (C4, "④", "只做 2D、规模上不去", "CT / MRI 是三维体数据，早期方法只切 2D 片，丢掉空间信息；配对数据量也上不去。",
     ["Merlin", "MG-3D", "Abn-BLIP"]),
]

top = 6.70
rh = 1.48
gap = 0.14
for i, (color, num, title, desc, methods) in enumerate(cats):
    y = top - (i + 1) * (rh + gap) + gap

    # 左侧编号色块
    nb = FancyBboxPatch((0.5, y), 0.62, rh, boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=0, facecolor=color, zorder=3)
    ax.add_patch(nb)
    ax.text(0.81, y + rh / 2, num, fontsize=17, color="white", fontweight="bold",
            ha="center", va="center", zorder=4)

    # 主体框
    mb = FancyBboxPatch((1.18, y), 8.75, rh, boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=1.5, edgecolor=color, facecolor="white", zorder=3)
    ax.add_patch(mb)
    ax.text(1.45, y + rh - 0.33, title, fontsize=13.5, color=color, fontweight="bold",
            ha="left", va="center", zorder=4)
    ax.text(1.45, y + 0.52, desc, fontsize=10.2, color=DARK, ha="left", va="center",
            linespacing=1.7, zorder=4)

    # 代表方法
    ax.text(10.15, y + rh - 0.3, "代表方法", fontsize=9.5, color=GREY, va="center")
    txt = "  ·  ".join(methods)
    ax.text(10.15, y + 0.62, txt, fontsize=11, color=DARK, fontweight="bold",
            va="center", linespacing=1.9)

# 底部：M3GCD 定位
fb = FancyBboxPatch((0.5, 0.28), 13.5, 0.82, boxstyle="round,pad=0.03,rounding_size=0.08",
                    linewidth=2.0, edgecolor=ORANGE, facecolor="#fdf8ef")
ax.add_patch(fb)
ax.text(0.78, 0.86, "你的位置（M3GCD）", fontsize=10.5, color=ORANGE, fontweight="bold", va="center")
ax.text(0.78, 0.55, "同时落在 ② 和 ③：用「类别描述」替代原始报告（绕开文本脏），"
        "并用软标签建模类别之间的语义关系（注入先验知识）。", fontsize=11, color=DARK, va="center")

ax.text(0.5, 0.06, "依据：CLIP in Medical Imaging: A Survey · Medical Image Analysis 2025",
        fontsize=9, color=GREY, va="center")

plt.tight_layout()
out = "/root/.openclaw/workspace/figs/clip_problems_taxonomy.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("saved:", out)
