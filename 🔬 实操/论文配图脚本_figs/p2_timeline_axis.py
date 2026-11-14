# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线（圆点版·极简）
中间一条时间轴，轴上只有年份圆点。模型名挂在圆点上方/下方，上下交替排列
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
    return fs if w <= avail else fs * avail / w * 0.96


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
                   ha=ha, va=va, zorder=6, linespacing=1.45)


W, H = 14.6, 7.4
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.48, "医学 CLIP 的发展时间线（2020—2026）", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)

axis_y = 3.55
ax.add_patch(FancyArrowPatch((0.30, axis_y), (W - 0.22, axis_y),
                             arrowstyle="-|>", mutation_scale=16,
                             lw=1.5, color=PALE, zorder=1))

groups = [
    ("2020", ["ConVIRT"]),
    ("2021", ["GLoRIA", "LocalMI"]),
    ("2022", ["MedCLIP", "MGCA", "BioViL", "LoVT", "ARL"]),
    ("2023", ["MedKLIP", "KAD", "KoBo", "SAT", "CXR-CLIP",
              "PRIOR", "MRM", "BioViL-T", "UniBrain", "TCSA"]),
    ("2024", ["Merlin", "KeepFIT", "EchoPrime", "PeskaVLP"]),
    ("2025", ["CP-CLIP", "MedFILIP", "fVLM", "BrgSA", "FLAIR", "FetalCLIP"]),
    ("2026", ["MG-3D", "Abn-BLIP", "AFLoc", "M3GCD"]),
]
HIGHLIGHT = {"CP-CLIP", "M3GCD"}

NG = len(groups)
x0, x1 = 0.95, W - 1.05
xs = [x0 + i * (x1 - x0) / (NG - 1) for i in range(NG)]
colw = (x1 - x0) / (NG - 1)
avail = colw - 0.08

for (yr, names), cx in zip(groups, xs):
    # 轴上：年份圆点
    ax.add_patch(Circle((cx, axis_y), 0.115, fc=SLATE, ec=WHITE, lw=2.0, zorder=5))
    # 年份字，放圆点正下方一点点（轴下）
    P(ax, cx, axis_y - 0.36, yr, 13.5, NAVY, "bold", ha="center")

    # 模型名：上下来回交替，从轴往外排
    for j, nm in enumerate(names):
        up = (j % 2 == 0)
        lvl = j // 2
        # 上方从轴上沿起排，下方从年份字下方起排
        if up:
            y = axis_y + 0.36 + lvl * 0.44
        else:
            y = axis_y - 0.72 - lvl * 0.44
        hi = nm in HIGHLIGHT
        P(ax, cx, y, nm, 10.4 if hi else 9.8,
          ACCENT if hi else TXT, "bold" if hi else "normal",
          ha="center", avail=avail)

fig.savefig(f"{OUT}/p2_timeline_axis.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
