# -*- coding: utf-8 -*-
"""
插页：2020–2026 医学 CLIP 演进 —— 极简版
只留 7 代主干，每行：年份 | 模型 | 一句改动
不加底色、不加框、不加箭头，靠留白和对齐
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

OUT = "/root/.openclaw/workspace/figs/final9"
os.makedirs(OUT, exist_ok=True)

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#2C3E50"
SLATE = "#4A6D8C"
MIST = "#8FA5B8"
PALE = "#C5D2DC"
TXT = "#34495E"
GRAY = "#8B99A6"
ACCENT = "#C8873E"
WHITE = "#FFFFFF"

_F = _A = _R = None


def _init():
    global _F, _A, _R
    if _F is None:
        _F, _A = plt.subplots(figsize=(20, 10), dpi=200)
        _A.set_xlim(0, 20)
        _A.set_ylim(0, 10)
        _A.axis("off")
        _F.canvas.draw()
        _R = _F.canvas.get_renderer()


def tw(s, fs, weight="normal"):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.width / 200.0


def th(s, fs, weight="normal", ls=1.7):
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight, linespacing=ls)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.height / 200.0


def fit(s, fs, avail, weight="normal"):
    w = tw(s, fs, weight)
    return fs if w <= avail else fs * avail / w * 0.96


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center",
      avail=None, ls=1.7):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=7, linespacing=ls)


W, H = 14.6, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.60, "七年的演进：每一代补一个缺口", 23, NAVY, "bold",
  ha="center", avail=W - 1.6)

# 7 行主干
rows = [
    ("2020", "ConVIRT", "医学图文对比学习的起点", "—"),
    ("2021", "GLoRIA", "从整图对齐 → 子区域对齐", "粒度"),
    ("2022", "MedCLIP", "从硬配对 → 软标签挖假阴性", "数据"),
    ("2023", "MedKLIP", "从纯视觉 → 注入医学实体知识", "知识"),
    ("2024", "CP-CLIP", "从单一对齐 → 核心 / 外围两级对齐", "结构"),
    ("2025", "fVLM", "从区域对齐 → 解剖结构级对齐", "粒度"),
    ("2026", "M3GCD", "从单样本 → 类别间关系建模", "关系"),
]

XQ, XN, XD, XT = 1.05, 2.55, 5.55, W - 1.05
top = H - 1.55
bot = 1.15
row_h = (top - bot) / len(rows)

# 表头
P(ax, XQ, top + 0.34, "年份", 10.5, GRAY, "bold")
P(ax, XN, top + 0.34, "模型", 10.5, GRAY, "bold")
P(ax, XD, top + 0.34, "相对前一代的调整", 10.5, GRAY, "bold")
P(ax, XT, top + 0.34, "补的缺口", 10.5, GRAY, "bold", ha="right")

for i, (yr, name, delta, gapname) in enumerate(rows):
    y = top - row_h * (i + 0.5)
    is_cp = name == "CP-CLIP"

    if i < len(rows) - 1:
        ax.plot([XQ - 0.18, XT + 0.18], [y - row_h / 2, y - row_h / 2],
                color="#EFF3F7", lw=1.0, zorder=2)

    P(ax, XQ, y, yr, 13.0, MIST, "bold")
    P(ax, XN, y, name, 16.0, ACCENT if is_cp else NAVY, "bold", avail=2.85)
    P(ax, XD, y, delta, 14.0, TXT if not is_cp else NAVY, avail=8.3)
    P(ax, XT, y, gapname, 12.0, ACCENT if is_cp else GRAY, "bold", ha="right")

P(ax, W / 2, 0.56,
  "CP-CLIP 站在 2023 年之后：前面补齐了粒度、数据、知识，它补的是「结构」",
  12.5, NAVY, "bold", ha="center", avail=W - 1.6)

fig.savefig(f"{OUT}/p3b_evolution.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
