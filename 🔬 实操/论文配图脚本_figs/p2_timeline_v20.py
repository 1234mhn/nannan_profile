# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线 2020—2026
支持「跨年份」模型：放在两个年份刻度之间的中间位置（带小标记）
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


W, H = 14.6, 6.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.42, "医学 CLIP 的发展时间线（2020—2026）", 19.5, NAVY, "bold",
  ha="center", avail=W - 0.9)

axis_y = 3.05
ax.add_patch(FancyArrowPatch((0.35, axis_y), (W - 0.30, axis_y),
                             arrowstyle="-|>", mutation_scale=15,
                             lw=1.4, color=PALE, zorder=1))

# 年份刻度（等距）
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
xL, xR = 0.95, W - 0.95
xs = {y: xL + i * (xR - xL) / (len(YEARS) - 1) for i, y in enumerate(YEARS)}
for y, cx in xs.items():
    ax.plot([cx, cx], [axis_y - 0.075, axis_y + 0.075], color=MIST, lw=2.2, zorder=2)
    ax.add_patch(Circle((cx, axis_y), 0.070, fc=SLATE, ec=WHITE, lw=1.5, zorder=5))
    P(ax, cx, axis_y + 0.34, y, 13.0, NAVY, "bold", ha="center")

HIGHLIGHT = {"CP-CLIP", "M3GCD"}

# 条目： (名称, 定位)  定位 = 年份字符串 或 ("mid", 年1) 表示放在年1与年2之间
items = [
    # 2020
    ("ConVIRT", "2020", "奠基"),

    # 2021
    ("GLoRIA", "2021", None),
    ("LocalMI", "2021", None),
    ("DoDNet", "2021", "应用"),

    # 2022
    ("MedCLIP", "2022", None),
    ("MGCA", "2022", None),
    ("BioViL", "2022", None),
    ("LoVT", "2022", None),
    ("ARL", "2022", None),
    ("CheXzero", "2022", "应用"),
    ("FlexR", "2022", "应用"),

    # 2023
    ("MedKLIP", "2023", None),
    ("KAD", "2023", None),
    ("KoBo", "2023", None),
    ("SAT", "2023", None),
    ("UMCL", "2023", None),
    ("CXR-CLIP", "2023", None),
    ("PRIOR", "2023", None),
    ("MRM", "2023", None),
    ("BioViL-T", "2023", None),
    ("UniBrain", "2023", None),
    ("TCSA", "2023", None),
    ("M-FLAG", "2023", None),
    ("SDA-CLIP", "2023", "应用"),
    ("SurgVLP", "2023", "应用"),

    # 2024
    ("Merlin", "2024", "跨版"),      # arXiv 2024 / Nature 2026
    ("KeepFIT", "2024", None),
    ("EchoPrime", "2024", None),
    ("PeskaVLP", "2024", None),
    ("MONET", "2024", "应用"),
    ("AnomalyCLIP", "2024", "应用"),

    # 2025
    ("CP-CLIP", "2025", "本文"),     # MICCAI 2024 / TMI 2025
    ("MedFILIP", "2025", None),
    ("fVLM", "2025", None),
    ("BrgSA", "2025", None),
    ("FLAIR", "2025", None),
    ("FetalCLIP", "2025", None),
    ("ContextMRI", "2025", "应用"),

    # 2026
    ("MG-3D", "2026", None),
    ("Abn-BLIP", "2026", None),
    ("Dual-geometry", "2026", None),
    ("AFLoc", "2026", None),
    ("PathPT", "2026", None),
    ("M3GCD", "2026", "本文"),
]

# 按年份分组
from collections import OrderedDict
byyear = OrderedDict((y, []) for y in YEARS)
for nm, pos, tag in items:
    byyear[pos].append((nm, tag))

# 每列上下交错布局
for y, cx in xs.items():
    lst = byyear[y]
    n = len(lst)
    if n == 0:
        continue
    # 上下两侧各放一半
    for i, (nm, tag) in enumerate(lst):
        up = (i % 2 == 0)
        lvl = i // 2
        dy = 0.58 + lvl * 0.40
        py = axis_y + (dy if up else -dy)
        hi = nm in HIGHLIGHT
        col = ACCENT if hi else MIST
        r = 0.050 if hi else 0.028
        ax.plot([cx, cx],
                [axis_y + (0.075 if up else -0.075), py + (-0.045 if up else 0.045)],
                color=ACCENT if hi else PALE, lw=0.85, alpha=0.52, zorder=1)
        ax.add_patch(Circle((cx, py), r, fc=col,
                            ec=WHITE if hi else "none", lw=1.1, zorder=5))
        fs = 8.9 if not hi else 9.5
        if nm == "Dual-geometry":
            fs = 8.0
        # 上排右、下排右交替，避免与相邻列撞
        right = (i % 2 == 0)
        if right:
            P(ax, cx + r + 0.045, py, nm, fs,
              ACCENT if hi else TXT, "bold" if hi else "normal",
              va="center", ha="left")
        else:
            P(ax, cx - r - 0.045, py, nm, fs,
              ACCENT if hi else TXT, "bold" if hi else "normal",
              va="center", ha="right")

fig.savefig(f"{OUT}/p2_timeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
