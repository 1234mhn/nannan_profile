# -*- coding: utf-8 -*-
"""
第2页 · 第一张图：医学 CLIP 发展时间线（最清晰版）
布局原则：一年一列，列宽按模型数量分配；同年模型竖排成列表；
上方年份大字；年份之间用竖向淡分隔线；模型前统一小圆点，不交错不绕圈
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
                   ha=ha, va=va, zorder=6, linespacing=1.5)


W, H = 14.6, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.50, "医学 CLIP 的发展时间线（2020—2026）", 21, NAVY, "bold",
  ha="center", avail=W - 0.9)

# 每年数据
groups = [
    ("2020", [("ConVIRT", 0)]),
    ("2021", [("GLoRIA", 0), ("LocalMI", 0)]),
    ("2022", [("MedCLIP", 0), ("MGCA", 0), ("BioViL", 0), ("LoVT", 0), ("ARL", 0)]),
    ("2023", [("MedKLIP", 0), ("KAD", 0), ("KoBo", 0), ("SAT", 0), ("CXR-CLIP", 0),
              ("PRIOR", 0), ("MRM", 0), ("BioViL-T", 0), ("UniBrain", 0), ("TCSA", 0)]),
    ("2024", [("Merlin", 0), ("KeepFIT", 0), ("EchoPrime", 0), ("PeskaVLP", 0)]),
    ("2025", [("CP-CLIP", 1), ("MedFILIP", 0), ("fVLM", 0), ("BrgSA", 0),
              ("FLAIR", 0), ("FetalCLIP", 0)]),
    ("2026", [("MG-3D", 0), ("Abn-BLIP", 0), ("AFLoc", 0), ("M3GCD", 1)]),
]

# 列宽按模型数量分配（带最小值）
xL, xR = 0.55, W - 0.55
MINW = 1.55
raw = [max(len(v), 1.6) for _, v in groups]
tot = sum(raw)
widths = [r / tot * (xR - xL) for r in raw]
for _ in range(20):
    need = sum(MINW - w for w in widths if w < MINW)
    if need <= 0:
        break
    big = [i for i, w in enumerate(widths) if w > MINW]
    extra = sum(widths[i] - MINW for i in big)
    if extra <= 0:
        break
    for i in big:
        widths[i] -= (widths[i] - MINW) / extra * need
    for i, w in enumerate(widths):
        if w < MINW:
            widths[i] = MINW
t = sum(widths)
widths = [w * (xR - xL) / t for w in widths]

colxs = []
acc = xL
for wd in widths:
    colxs.append((acc, acc + wd, acc + wd / 2))
    acc += wd

top_y = H - 1.35
# 年份表头 + 竖向分隔线
for i, ((yr, lst), (l, r, c)) in enumerate(zip(groups, colxs)):
    # 竖向淡分隔
    if i > 0:
        ax.plot([l, l], [0.55, top_y + 0.05], color="#E4EAEF", lw=1.0, zorder=1)
    # 年份
    P(ax, c, top_y, yr, 15, SLATE, "bold", ha="center")
    ax.plot([c - 0.24, c + 0.24], [top_y - 0.34, top_y - 0.34],
            color=MIST, lw=1.6, zorder=2)
    # 该年模型数
    P(ax, c, top_y - 0.62, f"{len(lst)} 项", 8.4, GRAY, ha="center")

# 模型列表：竖排，圆点+名字，左对齐，视觉最清晰
row_h = 0.50
for (yr, lst), (l, r, c) in zip(groups, colxs):
    start_y = top_y - 1.10
    avail = (r - l) - 0.30
    for j, (nm, hi) in enumerate(lst):
        y = start_y - j * row_h
        if hi:
            ax.add_patch(Circle((l + 0.22, y), 0.055, fc=ACCENT, ec=WHITE,
                                lw=1.2, zorder=5))
            P(ax, l + 0.36, y, nm, 9.8, ACCENT, "bold", va="center", avail=avail)
        else:
            ax.add_patch(Circle((l + 0.22, y), 0.034, fc=MIST, ec="none", zorder=5))
            P(ax, l + 0.36, y, nm, 9.8, TXT, va="center", avail=avail)

fig.savefig(f"{OUT}/p2_timeline_clear.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
