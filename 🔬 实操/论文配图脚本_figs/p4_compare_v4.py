# -*- coding: utf-8 -*-
"""
第4页：CLIP vs CP-CLIP 对比图（漏斗版）
起点完全相同：一张胸片 + 一段报告
分叉点：CLIP 直接整图对齐 / CP-CLIP 先拆核心外围再分别对齐
落点：特征与效果
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


def pod(ax, x, y, w, h, fc, r=0.13, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec="none", zorder=z))


def arw(ax, x1, y1, x2, y2, color=LINE, lw=1.8, ms=13, style="-|>", z=4,
        connectionstyle="arc3,rad=0"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, lw=lw, color=color,
                                 zorder=z, shrinkA=0, shrinkB=0,
                                 connectionstyle=connectionstyle))


W, H = 14.6, 8.0
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.50, "CLIP vs CP-CLIP：输入相同，中间分岔", 23, NAVY, "bold",
  ha="center", avail=W - 1.6)
P(ax, W / 2, H - 0.94, "同样一张胸片、同样一段报告 —— 差别只在「送到对齐层之前怎么处理」",
  12.2, GRAY, ha="center", avail=W - 1.6)

# ---------------- 起点（共用） ----------------
IN_Y = 5.55
IN_H = 1.15
IMG_W = 2.30
TXT_W = 5.10
GAPIN = 0.55
tot = IMG_W + GAPIN + TXT_W
x0 = (W - tot) / 2

pod(ax, x0, IN_Y, IMG_W, IN_H, WHITE, r=0.12)
P(ax, x0 + IMG_W / 2, IN_Y + 0.78, "胸部 X 光片", 13.5, NAVY, "bold", avail=IMG_W - 0.2)
P(ax, x0 + IMG_W / 2, IN_Y + 0.38, "一张图", 10.2, GRAY, avail=IMG_W - 0.2)

pod(ax, x0 + IMG_W + GAPIN, IN_Y, TXT_W, IN_H, WHITE, r=0.12)
tx = x0 + IMG_W + GAPIN
P(ax, tx + TXT_W / 2, IN_Y + 0.78, "放射学报告", 13.5, NAVY, "bold", avail=TXT_W - 0.2)
P(ax, tx + TXT_W / 2, IN_Y + 0.38, "一段文字", 10.2, GRAY, avail=TXT_W - 0.2)

P(ax, W / 2, IN_Y - 0.30, "两种方法的输入完全相同", 10.5, MIST, avail=W - 2)

# ---------------- 分岔点 ----------------
FORK_Y = 4.55
P(ax, W / 2, FORK_Y + 0.10, "分岔", 12.0, ACCENT, "bold", ha="center", avail=1.6)
ax.add_patch(Circle((W / 2, FORK_Y + 0.10), 0.34, fc=ACCENT, ec=WHITE, lw=1.8, zorder=8))
P(ax, W / 2, FORK_Y + 0.10, "分岔", 10.5, WHITE, "bold", ha="center")

# 从输入到分岔的两根箭头（左右斜下）
arw(ax, x0 + IMG_W / 2, IN_Y - 0.06, W / 2 - 1.30, FORK_Y - 0.30,
    color=PALE, lw=2.0, ms=15, connectionstyle="arc3,rad=-0.12")
arw(ax, tx + TXT_W / 2, IN_Y - 0.06, W / 2 + 1.30, FORK_Y - 0.30,
    color=PALE, lw=2.0, ms=15, connectionstyle="arc3,rad=0.12")

# ---------------- 两条支路 ----------------
BR_TOP = 3.62           # 支路标题 y
COL_W = 6.30
MX = 0.55
xL = MX
xR = W - MX - COL_W
cxL = xL + COL_W / 2
cxR = xR + COL_W / 2

# 分岔到左右两栏的箭头
arw(ax, W / 2 - 0.60, FORK_Y - 0.22, cxL + 1.60, BR_TOP + 0.30,
    color=MIST, lw=2.2, ms=16, connectionstyle="arc3,rad=0.10")
arw(ax, W / 2 + 0.60, FORK_Y - 0.22, cxR - 1.60, BR_TOP + 0.30,
    color=ACCENT, lw=2.2, ms=16, connectionstyle="arc3,rad=-0.10")

# 左：CLIP
P(ax, cxL, BR_TOP + 0.18, "原生 CLIP：不拆，直接对齐", 15.0, MIST, "bold",
  avail=COL_W - 0.4)
pod(ax, xL, BR_TOP - 0.78, COL_W, 0.72, BG1, r=0.12)
P(ax, cxL, BR_TOP - 0.42, "整图 ↔ 整份报告（1 次对齐）", 12.0, SLATE, "bold",
  avail=COL_W - 0.5)

# 右：CP-CLIP
P(ax, cxR, BR_TOP + 0.18, "CP-CLIP：先拆，再分别对齐", 15.0, ACCENT, "bold",
  avail=COL_W - 0.4)
P(ax, cxR, BR_TOP + 0.18, "CP-CLIP：先拆，再分别对齐", 15.0, ACCENT, "bold",
  avail=COL_W - 0.4)

# 右栏两个小块：核心 / 外围
HW = (COL_W - 0.36) / 2
pod(ax, xR, BR_TOP - 0.78, HW, 0.72, BG2, r=0.12)
P(ax, xR + HW / 2, BR_TOP - 0.42, "核心 ↔ 核心", 11.8, ACCENT, "bold", avail=HW - 0.2)
pod(ax, xR + HW + 0.36, BR_TOP - 0.78, HW, 0.72, BG2, r=0.12)
P(ax, xR + HW + 0.36 + HW / 2, BR_TOP - 0.42, "外围 ↔ 外围", 11.8, SLATE, "bold",
  avail=HW - 0.2)

# ---------------- 落点：结果 ----------------
RES_Y = 1.62
RES_H = 1.30

pod(ax, xL, RES_Y, COL_W, RES_H, WHITE, r=0.13)
P(ax, cxL, RES_Y + 0.92, "病灶信号被背景稀释", 13.0, NAVY, "bold", avail=COL_W - 0.5)
P(ax, cxL, RES_Y + 0.46, "多病灶语义被平均成一个点，局部诊断线索丢失", 10.2, GRAY,
  avail=COL_W - 0.5)
arw(ax, cxL, BR_TOP - 0.86, cxL, RES_Y + RES_H + 0.10, color=MIST, lw=2.0, ms=15)

pod(ax, xR, RES_Y, COL_W, RES_H, WHITE, r=0.13)
P(ax, cxR, RES_Y + 0.92, "核心 / 外围语义各自保留", 13.0, NAVY, "bold", avail=COL_W - 0.5)
P(ax, cxR, RES_Y + 0.46, "加权重构最终特征，背景干扰被隔离", 10.2, GRAY,
  avail=COL_W - 0.5)
arw(ax, cxR, BR_TOP - 0.86, cxR, RES_Y + RES_H + 0.10, color=ACCENT, lw=2.0, ms=15)

# ---------------- 底部：创新点 ----------------
P(ax, W / 2, 0.76, "创新点：把「一处对齐」改成「先结构解构、再两处对齐、最后加权融合」",
  12.8, ACCENT, "bold", ha="center", avail=W - 1.4)

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
