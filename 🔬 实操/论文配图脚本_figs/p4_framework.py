# -*- coding: utf-8 -*-
"""
第4页：CP-CLIP 整体框架图
一条完整链路：输入图+文 → 核心/外围解构 → 双塔编码 → 两级对齐 → 加权融合 → 下游任务
视觉语言与第3页 / 第4页对比图统一：淡底圆角块、居中文字、无粗边框
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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
BG1 = "#F4F7FA"
BG2 = "#F2F6F9"
BG3 = "#FBF6EF"

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


def P(ax, x, y, s, fs, color, weight="normal", ha="center", va="center",
      avail=None, ls=1.7):
    if avail is not None:
        fs = fit(s, fs, avail, weight)
    return ax.text(x, y, s, fontsize=fs, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=6, linespacing=ls)


def pod(ax, x, y, w, h, fc, r=0.16, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec="none", zorder=z))


def arw(ax, x1, y1, x2, y2, color=PALE, lw=2.0, ms=16, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, lw=lw, color=color,
                                 zorder=4, shrinkA=0, shrinkB=0))


W, H = 14.6, 8.0
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.52, "CP-CLIP 整体框架", 23, NAVY, "bold", ha="center",
  avail=W - 1.4)
P(ax, W / 2, H - 0.98, "输入 → 核心 / 外围解构 → 双塔编码 → 两级对比对齐 → 加权融合 → 下游任务",
  12.2, GRAY, ha="center", avail=W - 1.4)

# ---------------- 横向主链几何 ----------------
MX = 0.62
CW = (W - 2 * MX) / 5          # 五列
GAP = 0.42
colx = [MX + i * CW for i in range(5)]
iw = CW - GAP                  # 每列内部块宽
ix = [colx[i] + GAP / 2 for i in range(5)]

rowA_y, rowA_h = 4.05, 1.62    # 上部：解构 + 编码
rowB_y, rowB_h = 2.10, 1.30    # 下部：对齐 + 融合
topY = rowA_y + rowA_h

# ============ ① 输入 ============
pod(ax, ix[0], rowA_y, iw, rowA_h, BG1)
P(ax, ix[0] + iw / 2, topY - 0.34, "① 输入", 12.0, MIST, "bold", avail=iw - 0.2)
P(ax, ix[0] + iw / 2, topY - 0.86, "胸部 X 光片 X", 13.5, NAVY, "bold", avail=iw - 0.24)
P(ax, ix[0] + iw / 2, topY - 1.24, "放射学报告 T", 13.5, NAVY, "bold", avail=iw - 0.24)

# ============ ② 结构解构 ============
pod(ax, ix[1], rowA_y, iw, rowA_h, BG2)
P(ax, ix[1] + iw / 2, topY - 0.34, "② 结构解构", 12.0, MIST, "bold", avail=iw - 0.2)

half_w = (iw - 0.22) / 2
bx = ix[1] + 0.06
# 核心
pod(ax, bx, rowA_y + 0.28, half_w, 0.72, WHITE)
P(ax, bx + half_w / 2, rowA_y + 0.80, "核心区域", 11.5, ACCENT, "bold", avail=half_w - 0.1)
P(ax, bx + half_w / 2, rowA_y + 0.50, "病灶 RoI", 9.4, GRAY, avail=half_w - 0.08)
# 外围
bx2 = bx + half_w + 0.10
pod(ax, bx2, rowA_y + 0.28, half_w, 0.72, WHITE)
P(ax, bx2 + half_w / 2, rowA_y + 0.80, "外围区域", 11.5, SLATE, "bold", avail=half_w - 0.1)
P(ax, bx2 + half_w / 2, rowA_y + 0.50, "背景组织", 9.4, GRAY, avail=half_w - 0.08)

# ============ ③ 双塔编码 ============
pod(ax, ix[2], rowA_y, iw, rowA_h, BG1)
P(ax, ix[2] + iw / 2, topY - 0.34, "③ 双塔编码", 12.0, MIST, "bold", avail=iw - 0.2)
pod(ax, ix[2] + 0.06, rowA_y + 0.28, iw - 0.12, 0.72, WHITE)
cx3 = ix[2] + iw / 2
P(ax, cx3, rowA_y + 0.80, "图像编码器 f_I", 11.5, SLATE, "bold", avail=iw - 0.24)
P(ax, cx3, rowA_y + 0.50, "文本编码器 f_T", 11.5, SLATE, "bold", avail=iw - 0.24)

# ============ ④ 两级对比对齐 ============
pod(ax, ix[3], rowA_y, iw, rowA_h, BG3)
P(ax, ix[3] + iw / 2, topY - 0.34, "④ 两级对比对齐", 12.0, ACCENT, "bold", avail=iw - 0.2)
pod(ax, ix[3] + 0.06, rowA_y + 0.62, iw - 0.12, 0.62, WHITE)
cx4 = ix[3] + iw / 2
P(ax, cx4, rowA_y + 1.02, "L = L_core + λ·L_peri", 12.0, TXT, "bold", avail=iw - 0.24)
P(ax, cx4, rowA_y + 0.42, "核心↔核心 · 外围↔外围", 9.8, GRAY, avail=iw - 0.22)

# ============ ⑤ 加权融合 + 输出 ============
pod(ax, ix[4], rowA_y, iw, rowA_h, BG1)
P(ax, ix[4] + iw / 2, topY - 0.34, "⑤ 加权融合", 12.0, MIST, "bold", avail=iw - 0.2)
pod(ax, ix[4] + 0.06, rowA_y + 0.62, iw - 0.12, 0.62, WHITE)
cx5 = ix[4] + iw / 2
P(ax, cx5, rowA_y + 1.02, "f = w_c·z_c + w_p·z_p", 11.6, TXT, "bold", avail=iw - 0.24)
P(ax, cx5, rowA_y + 0.42, "零样本分类 / 分割 / 检索", 9.8, GRAY, avail=iw - 0.22)

# ============ 主链箭头 ============
for i in range(4):
    x1 = ix[i] + iw
    x2 = ix[i + 1]
    arw(ax, x1 + 0.03, rowA_y + rowA_h / 2, x2 - 0.03, rowA_y + rowA_h / 2,
        color=PALE, lw=2.2, ms=17)

# ============ 下部：对照两条对齐分支（强调两级） ============
by = 1.38
bw_all = W - 2 * MX
pod(ax, MX, by - 0.92, bw_all, 1.34, BG3, r=0.16)

P(ax, MX + 0.34, by + 0.10, "两级对齐怎么走", 12.5, ACCENT, "bold", ha="left")


def chain(x, label, sub, color):
    w0 = 1.98
    pod(ax, x, by - 0.62, w0, 0.52, WHITE, r=0.10)
    P(ax, x + w0 / 2, by - 0.36, label, 10.6, color, "bold", avail=w0 - 0.16)
    return x + w0


# 核心支
x_core = MX + 0.34
x_core = chain(x_core, "核心特征 z_c", "", ACCENT)
arw(ax, x_core + 0.04, by - 0.36, x_core + 0.42, by - 0.36, color=ACCENT, lw=1.8, ms=14)
x_core = chain(x_core + 0.46, "核心文本 t_c", "", ACCENT)
P(ax, x_core + 0.10, by - 0.36, "→ 拉近（病灶对齐病灶）", 9.8, GRAY, ha="left")

# 外围支（放右侧，避免交叉）
x_peri = MX + 7.45
x_peri = chain(x_peri, "外围特征 z_p", "", SLATE)
arw(ax, x_peri + 0.04, by - 0.36, x_peri + 0.42, by - 0.36, color=SLATE, lw=1.8, ms=14)
x_peri = chain(x_peri + 0.46, "外围文本 t_p", "", SLATE)
P(ax, x_peri + 0.10, by - 0.36, "→ 拉近（背景对齐背景）", 9.8, GRAY, ha="left")

# 底部注
P(ax, W / 2, 0.42,
  "改动只在「对齐目标函数」这一环：骨干网络与训练流程沿用原生 CLIP",
  12.0, NAVY, "bold", ha="center", avail=W - 1.2)

fig.savefig(f"{OUT}/p4_framework.png", dpi=200, facecolor=WHITE)
plt.close(fig)
print("saved")
