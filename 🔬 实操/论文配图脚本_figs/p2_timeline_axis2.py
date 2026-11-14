# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线（圆点版 · 含跨年条目）
中间一条时间轴，轴上 7 个年份圆点；代表性模型挂在上下；
会议版/期刊版跨年的模型放在两年份之间的中间位置
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


W, H = 14.6, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.48, "医学 CLIP 的发展时间线（2020—2026）", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)

axis_y = 3.60
ax.add_patch(FancyArrowPatch((0.28, axis_y), (W - 0.20, axis_y),
                             arrowstyle="-|>", mutation_scale=16,
                             lw=1.5, color=PALE, zorder=1))

# 年份圆点位置（等距）
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
x0, x1 = 1.00, W - 1.10
xs = {y: x0 + i * (x1 - x0) / (len(YEARS) - 1) for i, y in enumerate(YEARS)}
colw = (x1 - x0) / (len(YEARS) - 1)

for y, cx in xs.items():
    ax.add_patch(Circle((cx, axis_y), 0.115, fc=SLATE, ec=WHITE, lw=2.0, zorder=5))
    P(ax, cx, axis_y - 0.38, y, 13.5, NAVY, "bold", ha="center")

HIGHLIGHT = {"CP-CLIP", "M3GCD"}

# 每个年份的代表模型（精简，只挑代表性）
buckets = {
    "2020": ["ConVIRT"],
    "2021": ["GLoRIA", "LocalMI"],
    "2022": ["MedCLIP", "MGCA", "BioViL"],
    "2023": ["MedKLIP", "KAD", "KoBo", "CXR-CLIP", "PRIOR", "TCSA"],
    "2024": ["Merlin", "KeepFIT", "EchoPrime"],
    "2025": ["CP-CLIP", "MedFILIP", "fVLM", "FLAIR"],
    "2026": ["MG-3D", "Abn-BLIP", "M3GCD"],
}

# 跨年份条目：放在两个年份圆点之间
# (名字, 左年, 右年, 上下)
mids = [
    ("LoVT", "2022", "2023", "up"),      # Müller 2022b，衔接 2022→2023
    ("PeskaVLP", "2023", "2024", "down"),
    ("BrgSA", "2024", "2025", "up"),
    ("FetalCLIP", "2025", "2026", "up"),
]

# 画同年的模型：上下交替，从轴往外排
avail = colw - 0.06
for yr in YEARS:
    cx = xs[yr]
    for j, nm in enumerate(buckets[yr]):
        up = (j % 2 == 0)
        lvl = j // 2
        y = axis_y + 0.46 + lvl * 0.46 if up else axis_y - 0.80 - lvl * 0.46
        hi = nm in HIGHLIGHT
        P(ax, cx, y, nm, 10.6 if hi else 10.0,
          ACCENT if hi else TXT, "bold" if hi else "normal",
          ha="center", avail=avail)

# 画跨年份条目：落在两年之间，用小三角/小点标记
for nm, yl, yr_, side in mids:
    cx = (xs[yl] + xs[yr_]) / 2
    up = (side == "up")
    y = axis_y + 0.46 if up else axis_y - 0.80
    # 轴上小菱形标记，表示"跨年"
    ax.add_patch(Circle((cx, axis_y), 0.055, fc=MIST, ec=WHITE, lw=1.3, zorder=5))
    P(ax, cx, y, nm, 9.6, GRAY, "normal", ha="center", avail=colw - 0.10)

fig.savefig(f"{OUT}/p2_timeline_axis.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
