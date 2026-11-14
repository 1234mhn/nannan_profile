# -*- coding: utf-8 -*-
"""
第3页 v7：四项缺陷——小块居中版
方块高度收紧（不再拉长），四栏整体垂直居中，所有文字居中对齐
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

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

P(ax, W / 2, H - 0.62, "原生 CLIP 在医学影像上的四项固有缺陷", 22, NAVY, "bold",
  ha="center", avail=W - 1.6)

cols = [
    ("01", "语义粒度单一", MIST,
     "只在全局层级做图文对齐，\n病灶占像素极低，\n区域级线索对不上。",
     "GLoRIA ｜ LoVT ｜ CP-CLIP"),
    ("02", "数据稀缺", SLATE,
     "医学图文对规模差数个量级，\n语义重叠报告被误判为负样本，\n对比信号被削弱。",
     "MedCLIP ｜ MGCA ｜ CXR-CLIP"),
    ("03", "缺乏领域先验", SLATE,
     "只习得表观语义，\n不具备临床概念的层级依赖，\n遇分布偏移易退化。",
     "MedKLIP ｜ KAD ｜ KoBo"),
    ("04", "三维建模缺失", MIST,
     "预训练语料是二维自然图像，\nCT/MRI 仅以 2D 切片输入，\n层间连续性丢失。",
     "MG-3D ｜ Merlin ｜ fVLM"),
]

BG = ["#F4F7FA", "#F2F6F9", "#F4F7FA", "#F2F6F9"]

# 方块几何：宽窄一点、高度收紧，整体垂直居中
gx = 0.70
mx = 0.90
cw = (W - 2 * mx - 3 * gx) / 4
inner = cw - 0.56

TFS, DFS, MFS = 16.5, 11.6, 10.8
PAD_T, PAD_B = 0.42, 0.40
GAP_NUM, GAP_TD, GAP_DM, GAP_LBL = 0.30, 0.34, 0.40, 0.34

# 先算内容总高
dfs = min(DFS, fit("测" * 12, DFS, inner))
dh = th("字\n字\n字", DFS, ls=1.95)

content_h = (0.40 + GAP_NUM          # 编号
             + th("字", TFS, "bold") + GAP_TD
             + dh + GAP_DM
             + th("字", 9.0) + GAP_LBL
             + th("字", MFS, "bold"))
ch = content_h + PAD_T + PAD_B

# 垂直居中：让方块群中心 = 画布内容区中心
area_top = H - 1.05
area_bot = 1.45
mid = (area_top + area_bot) / 2
pod_top = mid + ch / 2
pod_bot = mid - ch / 2

for i, (num, title, col, desc, meth) in enumerate(cols):
    x = mx + i * (cw + gx) + gx / 2
    cx = x + cw / 2

    ax.add_patch(FancyBboxPatch((x, pod_bot), cw, ch,
                                boxstyle="round,pad=0,rounding_size=0.18",
                                fc=BG[i], ec="none", zorder=1))

    cy = pod_top - PAD_T
    # 编号（居中）
    P(ax, cx, cy - 0.14, num, 13.0, PALE, "bold", ha="center")
    cy -= 0.40 + GAP_NUM
    # 缺陷名（居中）
    tfs = min(TFS, fit(title, TFS, inner, "bold"))
    P(ax, cx, cy, title, tfs, NAVY, "bold", ha="center", avail=inner)
    cy -= th("字", TFS, "bold") + GAP_TD
    # 机理（居中）
    P(ax, cx, cy - dh / 2, desc, DFS, TXT, ha="center", va="center",
      avail=inner, ls=1.95)
    cy -= dh + GAP_DM
    # 代表方法标签（居中）
    P(ax, cx, cy, "代表方法", 9.0, GRAY, ha="center")
    cy -= th("字", 9.0) + GAP_LBL
    # 模型名（居中）
    mfs = min(MFS, fit(meth, MFS, inner, "bold"))
    P(ax, cx, cy, meth, mfs, SLATE, "bold", ha="center", avail=inner)

P(ax, W / 2, 0.74,
  "本文针对缺陷 01：将病灶与背景解耦为核心 / 外围两支，分别施加对比约束",
  12.4, ACCENT, "bold", ha="center", avail=W - 1.4)

fig.savefig(f"{OUT}/p3_taxonomy_clean.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print(f"saved cw={cw:.2f} ch={ch:.2f}")
