# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线 2020—2026
中间一条时间轴；每一年一列，同年份的模型并列竖排；年份大字标在列头
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
                   ha=ha, va=va, zorder=6, linespacing=1.5)


W, H = 14.6, 7.8
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.42, "医学 CLIP 的发展时间线（2020—2026）", 19.5, NAVY, "bold",
  ha="center", avail=W - 0.9)
P(ax, W / 2, H - 0.80,
  "同一年的模型并列；橙色为本工作",
  10.2, GRAY, ha="center", avail=W - 0.9)

axis_y = 3.55
ax.add_patch(FancyArrowPatch((0.42, axis_y), (W - 0.42, axis_y),
                             arrowstyle="-|>", mutation_scale=15,
                             lw=1.4, color=PALE, zorder=1))

# 每年一列： (年份, [模型...], 备注)
groups = [
    ("2020", ["ConVIRT"], None),
    ("2021", ["GLoRIA", "LocalMI"], None),
    ("2022", ["MedCLIP", "MGCA", "BioViL", "LoVT", "ARL"], None),
    ("2023", ["MedKLIP", "KAD", "KoBo", "MOTOR",
              "SAT", "UMCL", "CXR-CLIP",
              "PRIOR", "MRM", "BioViL-T",
              "UniBrain"], "综述 Table 2"),
    ("2024", ["Merlin", "KeepFIT", "EchoPrime", "PeskaVLP"], None),
    ("2025", ["MedFILIP", "CP-CLIP", "fVLM", "BrgSA",
              "FLAIR", "FetalCLIP"], None),
    ("2026", ["MG-3D", "Abn-BLIP", "Dual-geometry", "AFLoc",
              "PathPT", "M3GCD"], "综述之后"),
]

HIGHLIGHT = {"CP-CLIP", "M3GCD"}

NG = len(groups)
x0, x1 = 0.85, W - 0.85
gx = [x0 + i * (x1 - x0) / (NG - 1) for i in range(NG)]
colw = (x1 - x0) / (NG - 1)
avail = colw - 0.10

for (yr, names, note), cx in zip(groups, gx):
    ax.plot([cx, cx], [axis_y - 0.07, axis_y + 0.07], color=MIST, lw=2.2, zorder=2)
    ax.add_patch(Circle((cx, axis_y), 0.065, fc=SLATE, ec=WHITE, lw=1.4, zorder=5))
    # 年份：轴上
    P(ax, cx, axis_y + 0.34, yr, 13.5, NAVY, "bold", ha="center")
    if note:
        P(ax, cx, axis_y + 0.72, note, 7.8, GRAY, ha="center", avail=avail)
    # 模型：轴下竖排，先序并列
    top_y = axis_y - 0.62
    lh = 0.44
    for j, nm in enumerate(names):
        y = top_y - j * lh
        hi = nm in HIGHLIGHT
        if hi:
            ax.add_patch(Circle((cx - 0.055, y), 0.058, fc=ACCENT, ec=WHITE,
                                lw=1.2, zorder=5))
            P(ax, cx + 0.10, y, nm, 9.6, ACCENT, "bold", va="center", avail=avail - 0.10)
        else:
            ax.add_patch(Circle((cx - 0.055, y), 0.035, fc=MIST, ec="none", zorder=5))
            P(ax, cx + 0.10, y, nm, 9.3, TXT, va="center", avail=avail - 0.10)

# 图例
lx, ly = 0.85, 0.95
ax.add_patch(Circle((lx + 0.03, ly), 0.035, fc=MIST, ec="none", zorder=5))
P(ax, lx + 0.16, ly, "综述 Table 2 收录", 8.8, TXT)
ax.add_patch(Circle((lx + 2.30, ly), 0.055, fc=ACCENT, ec=WHITE, lw=1.1, zorder=5))
P(ax, lx + 2.46, ly, "本工作（CP-CLIP / M3GCD）", 8.8, ACCENT, "bold")

P(ax, W / 2, 0.40,
  "资料来源：CLIP in Medical Imaging: A Survey, MedIA 2025（arXiv:2312.07353）；2026 年为综述之后的新进展，取自本文参考文献",
  8.2, GRAY, ha="center", avail=W - 0.9)

fig.savefig(f"{OUT}/p2_timeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
