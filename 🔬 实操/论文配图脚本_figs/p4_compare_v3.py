# -*- coding: utf-8 -*-
"""
第4页：CLIP vs CP-CLIP 对比图 —— 突出创新点
核心创新 = 「对齐向量从 1 对 → 2 对」
左：CLIP 一条对齐线（整图↔整文，病灶语义被背景平均掉）
右：CP-CLIP 两条对齐线（核心↔核心、外围↔外围，病灶语义独立保留）+ 加权融合
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

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
BG1 = "#F2F6F9"
BG2 = "#FBF6EF"
LINE = "#DCE3EA"

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


def P(ax, x, y, s, fs, color, weight="normal", ha="center", va="center",
      avail=None, ls=1.7):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=7, linespacing=ls)


def pod(ax, x, y, w, h, fc, r=0.14, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec="none", zorder=z))


def arw(ax, x1, y1, x2, y2, color=LINE, lw=1.8, ms=14, style="-|>", z=4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, lw=lw, color=color,
                                 zorder=z, shrinkA=0, shrinkB=0))


W, H = 14.6, 8.0
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.52, "CLIP vs CP-CLIP：创新点在对齐粒度", 23, NAVY, "bold",
  ha="center", avail=W - 1.4)
P(ax, W / 2, H - 0.98, "原生 CLIP 一次对齐；CP-CLIP 把图与文同时拆成核心 / 外围，做两次对齐",
  12.2, GRAY, ha="center", avail=W - 1.4)

# ---------------- 两栏几何 ----------------
MX = 0.55
PW = 6.35
GAPM = W - 2 * MX - 2 * PW      # 中间空隙
xL = MX
xR = MX + PW + GAPM

pod(ax, xL, 1.55, PW, 4.55, BG1)
pod(ax, xR, 1.55, PW, 4.55, BG2)

# 栏标题
cxL = xL + PW / 2
cxR = xR + PW / 2
P(ax, cxL, 5.72, "原生 CLIP", 18.0, MIST, "bold", avail=PW - 0.6)
P(ax, cxR, 5.72, "CP-CLIP", 18.0, ACCENT, "bold", avail=PW - 0.6)
ax.plot([cxL - 0.75, cxL + 0.75], [5.44, 5.44], color=MIST, lw=1.6, zorder=3,
        solid_capstyle="round")
ax.plot([cxR - 0.75, cxR + 0.75], [5.44, 5.44], color=ACCENT, lw=1.6, zorder=3,
        solid_capstyle="round")

# ---------------- 左栏：CLIP 单条对齐 ----------------
# 图像块
pod(ax, xL + 0.55, 3.35, 2.05, 1.42, WHITE, r=0.10)
P(ax, xL + 1.575, 4.38, "整张胸片", 12.0, TXT, "bold", avail=1.9)
P(ax, xL + 1.575, 3.90, "病灶 + 背景", 10.0, GRAY, avail=1.9)
P(ax, xL + 1.575, 3.58, "全部纠缠在一个向量里", 9.2, GRAY, avail=1.9)

# 文本块
pod(ax, xL + 3.75, 3.35, 2.05, 1.42, WHITE, r=0.10)
P(ax, xL + 4.775, 4.38, "整份报告", 12.0, TXT, "bold", avail=1.9)
P(ax, xL + 4.775, 3.90, "病灶描述 + 背景描述", 10.0, GRAY, avail=1.9)
P(ax, xL + 4.775, 3.58, "同样压成一个向量", 9.2, GRAY, avail=1.9)

# 单条对齐线
arw(ax, xL + 2.68, 4.06, xL + 3.68, 4.06, color=MIST, lw=2.6, ms=18)
P(ax, cxL, 4.34, "1 次对齐", 10.5, MIST, "bold", avail=2.6)

# 后果
pod(ax, xL + 0.55, 1.95, PW - 1.10, 1.10, WHITE, r=0.10)
P(ax, cxL, 2.70, "病灶信号被背景稀释", 12.5, NAVY, "bold", avail=PW - 1.4)
P(ax, cxL, 2.30, "多病灶语义被平均，局部诊断线索丢失", 9.8, GRAY, avail=PW - 1.4)

# ---------------- 右栏：CP-CLIP 两条对齐 ----------------
# 图像：核心 / 外围
pod(ax, xR + 0.50, 4.28, 1.55, 0.72, WHITE, r=0.10)
P(ax, xR + 1.275, 4.80, "核心区域", 11.5, ACCENT, "bold", avail=1.4)
P(ax, xR + 1.275, 4.50, "病灶 RoI", 9.2, GRAY, avail=1.4)

pod(ax, xR + 0.50, 3.35, 1.55, 0.72, WHITE, r=0.10)
P(ax, xR + 1.275, 3.87, "外围区域", 11.5, SLATE, "bold", avail=1.4)
P(ax, xR + 1.275, 3.57, "背景组织", 9.2, GRAY, avail=1.4)

# 文本：核心 / 外围
pod(ax, xR + 3.15, 4.28, 1.55, 0.72, WHITE, r=0.10)
P(ax, xR + 3.925, 4.80, "核心语汇", 11.5, ACCENT, "bold", avail=1.4)
P(ax, xR + 3.925, 4.50, "病变描述", 9.2, GRAY, avail=1.4)

pod(ax, xR + 3.15, 3.35, 1.55, 0.72, WHITE, r=0.10)
P(ax, xR + 3.925, 3.87, "外围语汇", 11.5, SLATE, "bold", avail=1.4)
P(ax, xR + 3.925, 3.57, "位置 / 边界", 9.2, GRAY, avail=1.4)

# 两条对齐线
arw(ax, xR + 2.10, 4.64, xR + 3.10, 4.64, color=ACCENT, lw=2.6, ms=18)
arw(ax, xR + 2.10, 3.71, xR + 3.10, 3.71, color=SLATE, lw=2.6, ms=18)

P(ax, xR + 2.60, 4.94, "对齐 1", 10.0, ACCENT, "bold", avail=1.2)
P(ax, xR + 2.60, 3.43, "对齐 2", 10.0, SLATE, "bold", avail=1.2)

# 后果 + 融合
pod(ax, xR + 0.50, 1.95, PW - 1.00, 1.10, WHITE, r=0.10)
P(ax, cxR - 0.10, 2.72, "两级对齐 + 加权融合", 12.5, NAVY, "bold", avail=PW - 1.3)
P(ax, cxR - 0.10, 2.32, "病灶语义独立保留，背景干扰被隔离", 9.8, GRAY, avail=PW - 1.3)

# ---------------- 中间：核心创新标注 ----------------
gx = xL + PW + GAPM / 2
ax.plot([gx, gx], [2.05, 5.45], color=LINE, lw=1.2, ls=(0, (4, 5)), zorder=2)
ax.add_patch(Circle((gx, 3.95), 0.50, fc=ACCENT, ec=WHITE, lw=2.2, zorder=8))
P(ax, gx, 4.06, "1 → 2", 13.0, WHITE, "bold")
P(ax, gx, 3.72, "次对齐", 9.0, WHITE, "bold")

# ---------------- 底部：创新点三条 ----------------
by = 0.52
P(ax, W / 2, by + 0.44, "创新点", 12.5, NAVY, "bold", ha="center", avail=1.4)

pts = [
    ("① 一起拆", "图像与文本\n同时拆成核心 / 外围", ACCENT),
    ("② 分别对", "核心只对核心\n外围只对外围", ACCENT),
    ("③ 再加权", "两支特征按权重合并\n而非简单拼接", ACCENT),
]
seg = (W - 1.6) / 3
for i, (k, v, c) in enumerate(pts):
    xx = 0.80 + i * seg
    P(ax, xx, by + 0.44, k, 12.0, c, "bold", ha="left", avail=seg - 0.3)
    P(ax, xx, by + 0.02, v, 10.2, TXT, ha="left", avail=seg - 0.3, ls=1.75)

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
