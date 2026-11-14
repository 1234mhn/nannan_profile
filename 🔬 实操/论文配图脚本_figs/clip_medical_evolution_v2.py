#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLIP in Medical Imaging 演进图 v2 —— 更清晰、更少干扰"""
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
BLUE = "#3d6fa8"
GREEN = "#2e7d5b"

fig, ax = plt.subplots(figsize=(15, 8.4), dpi=200)
ax.set_xlim(0, 15)
ax.set_ylim(0, 8.4)
ax.axis("off")

# 标题
ax.text(0.5, 7.95, "医学影像中的 CLIP：七代方法在补同一个洞",
        fontsize=22, color=DARK, fontweight="bold", va="center")
ax.text(0.5, 7.45, "核心矛盾：文本是 CLIP 的监督信号，但医学报告太长、太脏、又和图像对不齐",
        fontsize=12.5, color=GREY, va="center")
ax.plot([0.5, 1.4], [7.18, 7.18], color=ORANGE, lw=3.2, solid_capstyle="butt")

stages = [
    ("ConVIRT", "2020", "整份报告\n代表整张图", "起点", BLUE),
    ("GloRIA", "2021", "拆区域\n局部也参与对齐", "粒度变细", BLUE),
    ("MedCLIP", "2022", "配对≠真相关\n解耦假阴性", "数据质量", BLUE),
    ("MedKLIP", "2023", "先抽病名\n再对齐", "知识注入", BLUE),
    ("MedFILIP", "2025", "实体级对齐\n关系更准", "细粒度", GREEN),
    ("CP-CLIP", "2025", "病变与背景\n分开对齐", "空间结构化", GREEN),
    ("MG-3D / Merlin", "2026", "从 2D 到 3D\n从小数据到千万级", "当前前沿", ORANGE),
]

n = len(stages)
x0, x1 = 1.25, 13.75
step = (x1 - x0) / (n - 1)
y_axis = 4.05
BW, BH = 1.86, 1.62

# 主轴
ax.annotate("", xy=(14.55, y_axis), xytext=(0.6, y_axis),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2.4, mutation_scale=26))

for i, (name, year, desc, tag, color) in enumerate(stages):
    x = x0 + i * step
    ax.plot(x, y_axis, "o", ms=15, color=color, mec="white", mew=3, zorder=6)
    up = (i % 2 == 0)
    by = y_axis + 0.62 if up else y_axis - 0.62 - BH

    b = FancyBboxPatch((x - BW / 2, by), BW, BH,
                       boxstyle="round,pad=0.02,rounding_size=0.09",
                       linewidth=2.0, edgecolor=color, facecolor="white", zorder=4)
    ax.add_patch(b)

    ax.text(x, by + BH - 0.34, name, fontsize=13.5, color=color,
            fontweight="bold", ha="center", va="center", zorder=6)
    ax.text(x, by + BH - 0.68, year, fontsize=10, color=GREY,
            ha="center", va="center", zorder=6)
    ax.text(x, by + 0.48, desc, fontsize=10.5, color=DARK,
            ha="center", va="center", linespacing=1.6, zorder=6)
    ax.text(x, by + 0.13, tag, fontsize=9.2, color=GREY,
            ha="center", va="center", zorder=6)

    y_from = by if up else by + BH
    ax.annotate("", xy=(x, y_axis), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.4, alpha=0.55), zorder=3)

# 底部结论
ax.text(0.5, 1.05, "共同假设：一份报告可以代表整张图。", fontsize=13, color=DARK, va="center")
ax.text(0.5, 0.6, "每一次进步都是在这个假设上打补丁 —— 看清补丁，才找得到自己的可质疑点。",
        fontsize=13, color=ORANGE, va="center")
ax.text(0.5, 0.16, "依据：CLIP in Medical Imaging: A Survey · Medical Image Analysis 2025 · 被引 237",
        fontsize=9.5, color=GREY, va="center")

plt.tight_layout()
out = "/root/.openclaw/workspace/figs/clip_medical_evolution_v2.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("saved:", out)
