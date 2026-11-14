# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线 2020—2026
非等距时间轴：按每年模型数量分配宽度，后期年份留足空间不拥挤
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

# (年份, 模型列表, 该列权重)
groups = [
    ("2020", ["ConVIRT"], 1.0),
    ("2021", ["GLoRIA", "LocalMI"], 1.5),
    ("2022", ["MedCLIP", "MGCA", "BioViL", "LoVT", "ARL"], 3.6),
    ("2023", ["MedKLIP", "KAD", "KoBo", "MOTOR", "SAT", "UMCL",
              "CXR-CLIP", "PRIOR", "MRM", "BioViL-T", "UniBrain"], 5.0),
    ("2024", ["Merlin", "KeepFIT", "EchoPrime", "PeskaVLP"], 3.2),
    ("2025", ["MedFILIP", "CP-CLIP", "fVLM", "BrgSA", "FLAIR", "FetalCLIP"], 4.0),
    ("2026", ["MG-3D", "Abn-BLIP", "Dual-geometry", "AFLoc", "PathPT", "M3GCD"], 4.4),
]

HIGHLIGHT = {"CP-CLIP", "M3GCD"}

# 按权重分配 x 位置（权重=该年占的宽度）
xL, xR = 0.75, W - 0.75
MINW = 1.42
raw = [w for _, _, w in groups]
tot = sum(raw)
widths = [w / tot * (xR - xL) for w in raw]
# 迭代补足最小宽度
for _ in range(12):
    need = sum(MINW - w for w in widths if w < MINW)
    if need <= 0:
        break
    big = [i for i, w in enumerate(widths) if w > MINW]
    avail_extra = sum(widths[i] - MINW for i in big)
    if avail_extra <= 0:
        break
    for i in big:
        widths[i] -= (widths[i] - MINW) / avail_extra * need
    for i, w in enumerate(widths):
        if w < MINW:
            widths[i] = MINW
s = sum(widths)
widths = [w * (xR - xL) / s for w in widths]
cx_list = []
acc = xL
for wd in widths:
    cx_list.append(acc + wd / 2)
    acc += wd

for (yr, names, _w), cx, wd in zip(groups, cx_list, widths):
    ax.plot([cx, cx], [axis_y - 0.07, axis_y + 0.07], color=MIST, lw=2.2, zorder=2)
    ax.add_patch(Circle((cx, axis_y), 0.070, fc=SLATE, ec=WHITE, lw=1.5, zorder=5))
    P(ax, cx, axis_y + 0.34, yr, 13.0, NAVY, "bold", ha="center")

    # 上下交错 + 左右交错：四象限轮转，同侧同水平带不重叠
    for idx, nm in enumerate(names):
        q = idx % 4              # 0=上右 1=上左 2=下右 3=下左
        up = (q < 2)
        right_side = (q % 2 == 0)
        lvl = idx // 4
        dy = 0.52 + lvl * 0.42
        py = axis_y + (dy if up else -dy)
        line_end = py - 0.045 if up else py + 0.045
        hi = nm in HIGHLIGHT
        col = ACCENT if hi else MIST
        r = 0.050 if hi else 0.028
        ax.plot([cx, cx],
                [axis_y + (0.075 if up else -0.075), line_end],
                color=ACCENT if hi else PALE, lw=0.85, alpha=0.5, zorder=1)
        ax.add_patch(Circle((cx, py), r, fc=col,
                            ec=WHITE if hi else "none", lw=1.1, zorder=5))
        # 单侧可用宽度 = 列宽一半 - 圆点 - 间隙 - 与邻列的安全距离
        side_avail = wd / 2 - r - 0.055 - 0.12
        fs = 9.3 if not hi else 9.5
        if nm in ("Dual-geometry",):
            fs = 8.2
        if right_side:
            P(ax, cx + r + 0.05, py, nm, fs,
              ACCENT if hi else TXT, "bold" if hi else "normal",
              va="center", ha="left", avail=side_avail)
        else:
            P(ax, cx - r - 0.05, py, nm, fs,
              ACCENT if hi else TXT, "bold" if hi else "normal",
              va="center", ha="right", avail=side_avail)

fig.savefig(f"{OUT}/p2_timeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
