# -*- coding: utf-8 -*-
"""
第4页：CP-CLIP 与 CLIP 对比（改版 · 去大框、居中、淡底色）
左 CLIP / 右 CP-CLIP，中间一个「对比」圆标；四项维度逐行对齐，不用整框
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle

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


def th(s, fs, weight="normal", ls=1.6):
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


def P(ax, x, y, s, fs, color, weight="normal", ha="left", va="center",
      avail=None, ls=1.6):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=ls)


W, H = 14.6, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.62, "CP-CLIP 与原生 CLIP：同一次对齐，两种拆法", 22, NAVY, "bold",
  ha="center", avail=W - 1.6)

rows = [
    ("对齐单位", "整图 ↔ 整份报告", "核心 ↔ 核心，外围 ↔ 外围"),
    ("向量数量", "各压成 1 个全局向量", "核心 / 外围各一组向量"),
    ("语义粒度", "多病灶语义被平均", "病灶语义独立保留"),
    ("背景处理", "与病灶共用同一通道", "单独归入外围，隔离干扰"),
]

# 几何
pw = 5.55                 # 面板宽
mx = 0.95
gx = (W - 2 * mx - 2 * pw)  # 中间留给对比圆标的宽度
xL = mx
xR = W - mx - pw
inner = pw - 0.60

TFS = 17.0
KFS, VFS = 9.8, 12.2

# 内容高度：标题 + 4 行
head_h = 0.95
row_h = 0.86
ch = head_h + len(rows) * row_h + 0.30

# 垂直居中
area_top = H - 1.20
area_bot = 1.30
mid = (area_top + area_bot) / 2
pod_top = mid + ch / 2
pod_bot = mid - ch / 2

for x, title, bg, tcol in [(xL, "原生 CLIP", "#F2F6F9", MIST),
                           (xR, "CP-CLIP", "#F4F7FA", SLATE)]:
    cx = x + pw / 2
    ax.add_patch(FancyBboxPatch((x, pod_bot), pw, ch,
                                boxstyle="round,pad=0,rounding_size=0.18",
                                fc=bg, ec="none", zorder=1))
    # 面板标题（居中）
    P(ax, cx, pod_top - 0.50, title, TFS, tcol, "bold", ha="center", avail=inner)
    # 标题下细线
    ax.plot([cx - 0.85, cx + 0.85], [pod_top - 0.82, pod_top - 0.82],
            color=tcol, lw=1.6, zorder=3, solid_capstyle="round")

# 逐行内容
for j, (k, vl, vr) in enumerate(rows):
    yy = pod_top - head_h - row_h * (j + 0.5) + 0.10
    # 左
    P(ax, xL + pw / 2, yy + 0.18, k, KFS, GRAY, ha="center")
    P(ax, xL + pw / 2, yy - 0.20, vl, VFS, TXT, ha="center", avail=inner)
    # 右
    P(ax, xR + pw / 2, yy + 0.18, k, KFS, GRAY, ha="center")
    P(ax, xR + pw / 2, yy - 0.20, vr, VFS, NAVY, "bold", ha="center", avail=inner)

# 中间对比圆标
ccx = xL + pw + gx / 2
ax.add_patch(Circle((ccx, mid), 0.42, fc=ACCENT, ec=WHITE, lw=2.0, zorder=6))
P(ax, ccx, mid, "对比", 11.5, WHITE, "bold", ha="center")

# 底部结论
P(ax, W / 2, 0.86,
  "核心差异：把「一处对齐」改成「两处对齐 + 一次加权」",
  13.0, NAVY, "bold", ha="center", avail=W - 1.6)
P(ax, W / 2, 0.50,
  "改动集中在对齐目标函数，骨干网络与训练流程基本沿用原设定",
  10.8, GRAY, ha="center", avail=W - 1.6)

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved ch={ch:.2f}")
