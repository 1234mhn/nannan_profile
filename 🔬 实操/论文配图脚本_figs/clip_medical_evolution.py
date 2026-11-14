#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLIP in Medical Imaging 演进图（依据 Medical Image Analysis 2025 综述）
主线：每一代都在解决「报告长/脏/不对齐 → 怎么监督到正确的图」这个问题
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

# 字体
for cand in ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Serif CJK SC", "AR PL UMing CN"]:
    try:
        fm.findfont(cand, fallback_to_default=False)
        plt.rcParams["font.sans-serif"] = [cand]
        break
    except Exception:
        continue
plt.rcParams["axes.unicode_minus"] = False

DARK = "#2b3a4a"
GREY = "#7a8590"
ORANGE = "#c87d14"
BLUE = "#3d6fa8"
GREEN = "#2e7d5b"
LIGHT = "#f5f6f7"

fig, ax = plt.subplots(figsize=(14, 9.6), dpi=200)
ax.set_xlim(0, 14)
ax.set_ylim(0, 9.6)
ax.axis("off")

# 标题
ax.text(0.35, 9.25, "医学影像中的 CLIP：一条「修补假设」的演进线",
        fontsize=19, color=DARK, fontweight="bold", va="center")
ax.text(0.35, 8.83, "依据  CLIP in Medical Imaging: A Survey（Medical Image Analysis 2025，被引 237）",
        fontsize=10.5, color=GREY, va="center")
ax.plot([0.35, 1.05], [8.62, 8.62], color=ORANGE, lw=3, solid_capstyle="butt")

# 核心命题框
box = FancyBboxPatch((0.35, 7.5), 13.3, 0.78, boxstyle="round,pad=0.03,rounding_size=0.08",
                     linewidth=0, facecolor=LIGHT)
ax.add_patch(box)
ax.text(0.6, 8.0, "贯穿全线的核心矛盾", fontsize=11, color=ORANGE, fontweight="bold", va="center")
ax.text(0.6, 7.72, "CLIP 的价值是「用文本当监督」，而医学文本 又长、又脏、又和图像对不齐 —— "
        "每一代方法都在回答同一句：怎么让一句不准确的报告，监督到正确的那部分图像。",
        fontsize=11.2, color=DARK, va="center")

# 演进链条
stages = [
    ("ConVIRT\n2020", "整体对齐", "一份报告\n代表整张图", BLUE, "起点"),
    ("GloRIA\n2021", "局部对齐", "拆成区域\n做全局+局部", BLUE, "粒度变细"),
    ("MedCLIP\n2022", "假阴性问题", "配对 ≠ 真相关\n用语义相似度解耦", BLUE, "数据质量"),
    ("MedKLIP\n2023", "引入疾病知识", "抽病名 + 模板\n先清文本再用", BLUE, "知识注入"),
    ("MedFILIP\n2025", "细粒度实体", "实体级对齐\n关系更准", GREEN, "粒度再细"),
    ("CP-CLIP\n2024/25", "核心—外围", "病变 vs 背景\n分开对齐", GREEN, "空间结构化"),
    ("MG-3D / Merlin\n2026", "3D + 多粒度 + 规模", "从 2D 到 3D\n从百万到千万级", ORANGE, "当前前沿"),
]

n = len(stages)
x0, x1 = 1.15, 12.9
step = (x1 - x0) / (n - 1)
y_axis = 5.0

# 主轴
ax.annotate("", xy=(13.35, y_axis), xytext=(0.55, y_axis),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2.2, mutation_scale=22))
ax.text(13.42, y_axis, "时间 / 方法演进", fontsize=9.5, color=GREY,
        rotation=90, va="center", ha="left")

for i, (name, tag, desc, color, note) in enumerate(stages):
    x = x0 + i * step
    # 轴上的圆点
    ax.plot(x, y_axis, "o", ms=13, color="white", mec=color, mew=3, zorder=5)
    # 上下交替
    up = (i % 2 == 0)
    box_y = y_axis + 0.95 if up else y_axis - 2.05
    h = 1.5
    b = FancyBboxPatch((x - 0.83, box_y), 1.66, h,
                       boxstyle="round,pad=0.02,rounding_size=0.07",
                       linewidth=1.6, edgecolor=color, facecolor="white", zorder=4)
    ax.add_patch(b)

    # 名称
    ax.text(x, box_y + h - 0.34, name, fontsize=10.6, color=color,
            fontweight="bold", ha="center", va="center", linespacing=1.35, zorder=6)
    # 解决的问题（标签）
    ax.text(x, box_y + h - 0.92, tag, fontsize=9.2, color=DARK,
            fontweight="bold", ha="center", va="center", zorder=6)
    # 做法
    ax.text(x, box_y + 0.31, desc, fontsize=8.4, color=GREY,
            ha="center", va="center", linespacing=1.45, zorder=6)

    # 连接线
    y_from = box_y if up else box_y + h
    ax.annotate("", xy=(x, y_axis), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.2, ls=(0, (3, 3))), zorder=3)

# 阶段分组（底部色带）
bands = [
    ("① 对齐粒度：从整图到局部", 0.55, 3.55, BLUE),
    ("② 数据与知识：把脏文本洗干净", 3.75, 7.35, BLUE),
    ("③ 结构化与规模：走向 3D", 7.55, 13.35, ORANGE),
]
for label, bx0, bx1, color in bands:
    ax.plot([bx0, bx1], [1.55, 1.55], lw=5, color=color, alpha=0.35,
            solid_capstyle="round")
    ax.text((bx0 + bx1) / 2, 1.25, label, fontsize=9.6, color=color,
            fontweight="bold", ha="center", va="center")

# 底部结论
ax.text(0.35, 0.62, "一句话记住：所有方法的共同假设是「一份报告可以代表整张图」，"
        "每一次进步都是在这个假设上打补丁 —— 看清补丁，才能找到自己的可质疑点。",
        fontsize=10.6, color=DARK, va="center")
ax.text(0.35, 0.22, "制图：楠楠  |  数据源：MedIA 2025 综述  |  DOI: 10.1016/j.media.2025.103551",
        fontsize=8.5, color=GREY, va="center")

plt.tight_layout()
out = "/root/.openclaw/workspace/figs/clip_medical_evolution.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("saved:", out)
