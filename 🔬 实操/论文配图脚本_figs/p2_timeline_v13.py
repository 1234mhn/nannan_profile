# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线 2020—2026
中间横轴；每年一列（可拆两栏）。模型上下交错分布，避免全挤在下方
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


W, H = 14.6, 7.3
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.52, "医学 CLIP 的发展时间线（2020—2026）", 19.5, NAVY, "bold",
  ha="center", avail=W - 0.9)

axis_y = 3.32
ax.add_patch(FancyArrowPatch((0.42, axis_y), (W - 0.42, axis_y),
                             arrowstyle="-|>", mutation_scale=15,
                             lw=1.4, color=PALE, zorder=1))

# (年份, [上下交错: 'u'/'d' 由位置决定], 名称, 该年分几栏)
groups = [
    ("2020", ["ConVIRT"], 1),
    ("2021", ["GLoRIA", "LocalMI"], 1),
    ("2022", ["MedCLIP", "MGCA", "BioViL", "LoVT", "ARL"], 2),
    ("2023", ["MedKLIP", "KAD", "KoBo", "MOTOR", "SAT", "UMCL",
              "CXR-CLIP", "PRIOR", "MRM", "BioViL-T", "UniBrain"], 2),
    ("2024", ["Merlin", "KeepFIT", "EchoPrime", "PeskaVLP"], 2),
    ("2025", ["MedFILIP", "CP-CLIP", "fVLM", "BrgSA", "FLAIR", "FetalCLIP"], 2),
    ("2026", ["MG-3D", "Abn-BLIP", "Dual-geometry", "AFLoc", "PathPT", "M3GCD"], 2),
]

HIGHLIGHT = {"CP-CLIP", "M3GCD"}

NG = len(groups)
x0, x1 = 1.55, W - 1.55
gx = [x0 + i * (x1 - x0) / (NG - 1) for i in range(NG)]
colw = (x1 - x0) / (NG - 1)

for (yr, names, ncol), cx in zip(groups, gx):
    # 轴刻度
    ax.plot([cx, cx], [axis_y - 0.08, axis_y + 0.08], color=MIST, lw=2.2, zorder=2)
    ax.add_patch(Circle((cx, axis_y), 0.075, fc=SLATE, ec=WHITE, lw=1.5, zorder=5))
    P(ax, cx, axis_y + 0.36, yr, 13.2, NAVY, "bold", ha="center")

    # 最后一列（2026）文字向左展开，防止出界
    last = (yr == "2026")
    half = (colw - 0.14) / ncol
    avail = half - 0.10
    per = (len(names) + ncol - 1) // ncol  # 每栏最多几个

    for idx, nm in enumerate(names):
        c = idx // per
        r = idx % per           # 栏内序号
        slot_cx = cx - (colw - 0.14) / 2 + half * (c + 0.5)
        up = (r % 2 == 0)
        lvl = r // 2            # 同侧第几层
        dy = 0.66 + lvl * 0.44
        py = axis_y + (dy if up else -dy)
        hi = nm in HIGHLIGHT
        col = ACCENT if hi else MIST
        # 引线
        ax.plot([slot_cx, slot_cx],
                [axis_y + (0.09 if up else -0.09), py + (-0.055 if up else 0.055)],
                color=PALE if not hi else ACCENT, lw=0.8,
                alpha=0.55 if not hi else 0.45, zorder=1)
        ax.add_patch(Circle((slot_cx, py), 0.055 if hi else 0.032,
                            fc=col, ec=WHITE if hi else "none",
                            lw=1.1, zorder=5))
        if last:
            P(ax, slot_cx - (0.085 if hi else 0.065), py, nm,
              9.4 if hi else 9.2, ACCENT if hi else TXT,
              "bold" if hi else "normal", va="center", ha="right", avail=avail + 0.14)
        else:
            P(ax, slot_cx + (0.085 if hi else 0.065), py, nm,
              9.4 if hi else 9.2, ACCENT if hi else TXT,
              "bold" if hi else "normal", va="center", avail=avail)

fig.savefig(f"{OUT}/p2_timeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
