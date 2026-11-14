# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线
一条居中横轴 · 上下交错 · 圆点 + 文字，无卡片框
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Circle

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


def fit(s, fs, avail, weight="normal"):
    w = tw(s, fs, weight)
    return fs if w <= avail else fs * avail / w * 0.97


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center", avail=None):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=1.6)


W, H = 14.6, 7.8
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.44, "医学 CLIP 的发展时间线（2020—2026）", 20, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.84,
  "按发表年份列出「精化 CLIP 预训练」的代表方法；2026 年为综述之后的新进展",
  10.5, GRAY, ha="center", avail=W - 0.9)

axis_y = 3.95
ax.add_patch(FancyArrowPatch((0.45, axis_y), (W - 0.45, axis_y),
                             arrowstyle="-|>", mutation_scale=16,
                             lw=1.5, color=PALE, zorder=1))

# 每个方法一个圆点：年份做分组锚点，方法圆点沿时间轴排布
# (年份, [(方法名, 色, 是否本文)])
groups = [
    ("2020", [("ConVIRT", SLATE, False)]),
    ("2021", [("GLoRIA", SLATE, False), ("LocalMI", SLATE, False), ("TCSA", SLATE, False)]),
    ("2022", [("MedCLIP", SLATE, False), ("MGCA", SLATE, False), ("BioViL", SLATE, False),
              ("LoVT", SLATE, False), ("ARL", SLATE, False)]),
    ("2023", [("MedKLIP", SLATE, False), ("KAD", SLATE, False), ("KoBo", SLATE, False),
              ("SAT", SLATE, False), ("UMCL", SLATE, False), ("CXR-CLIP", SLATE, False),
              ("PRIOR", SLATE, False), ("MRM", SLATE, False), ("BioViL-T", SLATE, False)]),
    ("2024", [("Merlin", SLATE, False), ("KeepFIT", SLATE, False),
              ("EchoPrime", SLATE, False), ("PeskaVLP", SLATE, False)]),
    ("2025", [("MedFILIP", SLATE, False), ("CP-CLIP", ACCENT, True),
              ("fVLM", SLATE, False), ("BrgSA", SLATE, False),
              ("FLAIR", SLATE, False), ("FetalCLIP", SLATE, False)]),
    ("2026", [("MG-3D", SLATE, False), ("Merlin", SLATE, False),
              ("Abn-BLIP", SLATE, False), ("Dual-geometry", SLATE, False),
              ("AFLoc", SLATE, False), ("PathPT", SLATE, False),
              ("M3GCD", ACCENT, True)]),
]

x0, x1 = 0.95, W - 0.95
NG = len(groups)
gx = [x0 + i * (x1 - x0) / (NG - 1) for i in range(NG)]
colw = (x1 - x0) / (NG - 1) / 2 - 0.06
avail = colw * 1.96

# 年份刻度（轴上小竖线 + 年份）
for (yr, items), cx in zip(groups, gx):
    ax.plot([cx, cx], [axis_y - 0.09, axis_y + 0.09], color=PALE, lw=2.4, zorder=2)
    P(ax, cx, axis_y + 0.30, yr, 12.5, SLATE, "bold", ha="center")

# 每个方法画一个圆点，上下交错，名字贴在圆点外侧
for (yr, items), cx in zip(groups, gx):
    k = len(items)
    spread = min(colw * 2.0, 0.40 * k)
    offs = [(-spread / 2 + i * spread / max(k - 1, 1)) if k > 1 else 0 for i in range(k)]
    order = sorted(range(k), key=lambda i: offs[i])
    for rank, i in enumerate(order):
        nm, col, hi = items[i]
        up = (rank % 2 == 0)
        px = cx + offs[i]
        r = 0.125 if hi else 0.062
        # 引线
        ly2 = axis_y + (0.62 if up else -0.62)
        ax.plot([px, px], [axis_y + (0.09 if up else -0.09), ly2],
                color=col, lw=0.9, alpha=0.55, zorder=2)
        ax.add_patch(Circle((px, axis_y), r, fc=col, ec=WHITE, lw=1.5, zorder=5))
        if hi:
            ax.add_patch(Circle((px, axis_y), 0.24, fc="none", ec=ACCENT,
                                lw=1.0, alpha=0.40, zorder=4))
        ty = ly2 + (0.34 if up else -0.34)
        P(ax, px, ty, nm, 8.4 if not hi else 9.4, ACCENT if hi else NAVY,
          "bold", ha="center", avail=avail)

# 图例
lx, ly = 0.90, 1.48
ax.add_patch(Circle((lx, ly), 0.07, fc=SLATE, ec=WHITE, lw=1.3, zorder=5))
P(ax, lx + 0.17, ly, "既有工作", 9.4, TXT)
ax.add_patch(Circle((lx + 1.30, ly), 0.09, fc=ACCENT, ec=WHITE, lw=1.3, zorder=5))
P(ax, lx + 1.53, ly, "本文相关工作（CP-CLIP / M3GCD）", 9.4, ACCENT, "bold")

P(ax, W / 2, 0.92,
  "演进主线：对齐粒度不断变细 —— 整图对整文 → 区域对片段 → 核心对外围",
  11, NAVY, "bold", ha="center", avail=W - 1.0)
P(ax, W / 2, 0.44,
  "资料来源：CLIP in Medical Imaging: A Survey, Medical Image Analysis 2025（arXiv:2312.07353）",
  8.6, GRAY, ha="center", avail=W - 1.0)

fig.savefig(f"{OUT}/p2_timeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
