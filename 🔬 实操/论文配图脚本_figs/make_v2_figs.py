# -*- coding: utf-8 -*-
"""
按 Claude Code 视觉诊断重画 P3 / P4 / P5
修正点：
  P3：卡片正文横向铺满、左右对称、字号整体放大、交替色改深浅不置灰
  P4：卡片内每行内容加长、字号放大、上下内边距统一
  P5：框内文字垂直居中、行距收紧、公式用 matplotlib mathtext 正式排版
统一：字号 +20%，灰阶加深，左右留白对称
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

OUT = "/root/.openclaw/workspace/figs/final9_v2"
os.makedirs(OUT, exist_ok=True)

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"

# 加深后的配色（原 GRAY #8B99A6 太浅）
NAVY = "#243447"
SLATE = "#3D6280"
MIST = "#5F7E96"      # 加深，不再发虚
PALE = "#C5D2DC"
FOG = "#F2F5F7"
TXT = "#2B3A47"
GRAY = "#6B7B88"      # 加深
ACCENT = "#B8722F"    # 加深的橙
WHITE = "#FFFFFF"

_F = _A = _R = None
WARN = []


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


def fit(s, fs, avail, weight="normal", label=""):
    w = tw(s, fs, weight)
    if w <= avail:
        return fs
    new = fs * avail / w * 0.96
    WARN.append(f"{label or s[:14]}: {fs}->{new:.1f}")
    return new


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.5, r=0.10, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def P(ax, x, y, s, fs, color=TXT, weight="normal", ha="left", va="center",
      avail=None, label="", ls=1.5, zorder=5):
    if avail:
        fs = fit(s, fs, avail, weight, label)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color,
            fontweight=weight, linespacing=ls, zorder=zorder)


# =========================================================
# P3 分类图 —— 4 行，正文横向铺满，左右严格对称
# =========================================================
W, H = 15.0, 7.9
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.44, "医学 CLIP 的四类问题：后续方法都在补什么", 20.5, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.86, "CLIP 解决了「不靠人工标签」；医学场景又带来四个新缺口",
  11.5, GRAY, ha="center", avail=W - 0.7, label="副标题")

rows = [
    ("①", "对齐粒度太粗", SLATE,
     "整图压成一个向量、整份报告也压成一个向量，只对齐一次；但一张胸片有多个器官与病灶，一份报告同时讲好几件事，全局平均会把判别信息抹平。",
     ["GloRIA", "MedFILIP", "CP-CLIP"]),
    ("②", "文本脏、配对不准", MIST,
     "医学报告冗长、表述不统一，常出现「正常报告配异常图像」的假阴性；直接硬对齐会让模型学到错误关联。",
     ["MedCLIP", "MedKLIP"]),
    ("③", "缺医学先验知识", SLATE,
     "通用 CLIP 只学到「图上有什么」，医学还要判断病变性质、疾病类别与解剖位置关系，这些知识需要显式注入。",
     ["MedKLIP", "Abn-BLIP"]),
    ("④", "只做 2D、规模上不去", MIST,
     "CT、MRI 是三维体数据，早期方法只切 2D 切片，丢掉空间连续性；同时大规模高质量图文配对数据也难获得。",
     ["MG-3D", "Merlin"]),
]

M = 0.55                  # 左右统一页边距
TOP = H - 1.32
BOT = 1.05
rh = (TOP - BOT - 3 * 0.16) / 4
sq_w = 0.80
card_x = M + sq_w + 0.18
card_w = W - M - card_x
meth_w = 2.30             # 右侧方法列固定宽
text_w = card_w - 0.42 - meth_w - 0.30

for i, (num, title, col, desc, meth) in enumerate(rows):
    y = TOP - (i + 1) * rh - i * 0.16
    # 序号方块
    rbox(ax, M, y + (rh - sq_w) / 2, sq_w, sq_w, col, col, lw=0, r=0.11)
    P(ax, M + sq_w / 2, y + rh / 2, num, 17, WHITE, "bold", ha="center")
    # 主卡片
    rbox(ax, card_x, y, card_w, rh, WHITE, col, lw=1.5)
    # 标题（垂直居中在卡片上部 1/3）
    P(ax, card_x + 0.24, y + rh - 0.30, title, 13.5, col, "bold",
      avail=text_w, label=f"题{i+1}")
    # 正文（横向铺满，垂直居中在下部）
    P(ax, card_x + 0.24, y + (rh - 0.48) / 2 + 0.02, desc, 10.0, TXT,
      avail=text_w, label=f"述{i+1}", ls=1.75)
    # 右侧方法列：标签在上、方法名在下，整体垂直居中
    mx = card_x + card_w - meth_w - 0.10
    ax.plot([mx - 0.14, mx - 0.14], [y + 0.18, y + rh - 0.18], color=PALE, lw=1.1)
    P(ax, mx, y + rh / 2 + 0.20, "代表方法", 9.6, GRAY, avail=meth_w - 0.10, label=f"标{i+1}")
    P(ax, mx, y + rh / 2 - 0.22, " · ".join(meth), 10.6, col, "bold",
      avail=meth_w - 0.10, label=f"法{i+1}")

P(ax, W / 2, 0.52, "本文聚焦问题①中的「核心—外围」这一支：把病灶与背景显式拆开，分别对齐。",
  11.8, ACCENT, "bold", ha="center", avail=W - 0.7, label="聚焦")

fig.savefig(f"{OUT}/p3_taxonomy.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# P4 对比图 —— 每行内容加长、字号放大、上下内边距统一
# =========================================================
W, H = 15.0, 7.5
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.44, "CP-CLIP 与 CLIP：同一任务，两种对齐方式", 20.5, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.86, "目标相同 —— 都在建立图文对应；差别在「对齐之前怎么拆」",
  11.5, GRAY, ha="center", avail=W - 0.7, label="副标题")

M = 0.55
GAP_MID = 0.85
pw = (W - 2 * M - GAP_MID) / 2
py = 1.85
ph = 3.95
PAD = 0.24                     # 统一内边距

CLIP_ROWS = [
    ("对齐单位", "整张图像 ↔ 整份报告，一对一"),
    ("向量数量", "图像、文本各压成 1 个全局向量"),
    ("语义粒度", "多病灶语义在平均时被抹平，无法区分"),
    ("背景干扰", "背景与病灶共用同一特征通道，无法隔离"),
]
CP_ROWS = [
    ("对齐单位", "核心 ↔ 核心、外围 ↔ 外围，两两配对"),
    ("向量数量", "核心与外围各一组向量，信息分行"),
    ("语义粒度", "病灶语义独立保留，不被背景稀释"),
    ("背景干扰", "背景单独归入外围通路，主动隔离干扰"),
]


def panel(x, title, color, rows, hi):
    rbox(ax, x, py, pw, ph, WHITE if hi else FOG, color, lw=2.2 if hi else 1.4)
    rbox(ax, x, py + ph - 0.54, pw, 0.54, color, color, lw=0, r=0.10, z=3)
    rbox(ax, x, py + ph - 0.54, pw, 0.24, color, color, lw=0, r=0.0, z=3)
    P(ax, x + pw / 2, py + ph - 0.27, title, 13.5, WHITE, "bold", ha="center",
      avail=pw - 0.4, label=title)
    # 4 行等分剩余空间，上下内边距完全一致
    inner_top = py + ph - 0.54 - 0.20
    inner_bot = py + 0.20
    seg = (inner_top - inner_bot) / 4
    for i, (k, v) in enumerate(rows):
        cy = inner_top - seg * (i + 0.5)
        P(ax, x + PAD, cy + 0.20, k, 10.2, color, "bold")
        P(ax, x + PAD, cy - 0.20, v, 10.4, TXT, avail=pw - 2 * PAD, label=f"{title}{k}")
        if i < 3:
            ax.plot([x + PAD, x + pw - PAD], [inner_top - seg * (i + 1), inner_top - seg * (i + 1)],
                    color=PALE, lw=0.9, alpha=0.75)


panel(M, "CLIP", MIST, CLIP_ROWS, hi=False)
panel(M + pw + GAP_MID, "CP-CLIP", SLATE, CP_ROWS, hi=True)

# 中间分隔
cx = M + pw + GAP_MID / 2
ax.plot([cx, cx], [py + 0.30, py + ph - 0.30], color=PALE, lw=1.6, ls=(0, (5, 4)))
ax.add_patch(Circle((cx, py + ph / 2), 0.33, fc=ACCENT, ec=WHITE, lw=2.0, zorder=6))
P(ax, cx, py + ph / 2, "差异", 9.5, WHITE, "bold", ha="center", zorder=7)

P(ax, W / 2, 1.26, "核心差异：把「一处对齐」改成「两处对齐 + 一次加权融合」。",
  12.5, NAVY, "bold", ha="center", avail=W - 0.7, label="结论")
P(ax, W / 2, 0.72, "改动集中在对齐目标函数，骨干网络与训练流程基本沿用原设定，工程代价低。",
  10.5, GRAY, ha="center", avail=W - 0.7, label="说明")

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# P5 机制图 —— 横向铺满，框内垂直居中，公式用 mathtext
# =========================================================
W, H = 15.0, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.44, "CP-CLIP 核心机制：核心—外围分别对齐，再加权融合", 20.5, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.86, "把「一处对齐」拆成「两处语义明确的分别对齐」，再用可学习权重合成",
  11.5, GRAY, ha="center", avail=W - 0.7, label="副标题")

M = 0.55
# 第1层：输入（横向两条）
row1_y, row1_h = 5.30, 0.92
half_w = (W - 2 * M - 0.45) / 2
rbox(ax, M, row1_y, half_w, row1_h, FOG, SLATE, lw=1.5)
P(ax, M + half_w / 2, row1_y + row1_h / 2 + 0.19, "输入图像 X", 12.5, NAVY, "bold",
  ha="center", avail=half_w - 0.3, label="输入图像")
P(ax, M + half_w / 2, row1_y + row1_h / 2 - 0.21, "胸片 / CT 三维体数据", 10.0, GRAY,
  ha="center", avail=half_w - 0.3, label="输入图像注")

rbox(ax, M + half_w + 0.45, row1_y, half_w, row1_h, FOG, SLATE, lw=1.5)
P(ax, M + half_w + 0.45 + half_w / 2, row1_y + row1_h / 2 + 0.19, "输入文本 T", 12.5, NAVY, "bold",
  ha="center", avail=half_w - 0.3, label="输入文本")
P(ax, M + half_w + 0.45 + half_w / 2, row1_y + row1_h / 2 - 0.21, "放射学报告原文", 10.0, GRAY,
  ha="center", avail=half_w - 0.3, label="输入文本注")

# 向下箭头
for xx in [M + half_w / 2, M + half_w + 0.45 + half_w / 2]:
    ax.add_patch(FancyArrowPatch((xx, row1_y - 0.06), (xx, row1_y - 0.46), arrowstyle="-|>",
                                 mutation_scale=15, lw=2.0, color=SLATE, zorder=3))

# 第2层：分解（左右两支）
row2_y, row2_h = 4.10, 0.86
ax.add_patch(Circle((M + half_w / 2, row2_y + row2_h / 2), 0.0, alpha=0))  # 占位
rbox(ax, M, row2_y, half_w, row2_h, WHITE, ACCENT, lw=1.8)
P(ax, M + half_w / 2, row2_y + row2_h / 2 + 0.18, "核心语义", 12.0, ACCENT, "bold",
  ha="center", avail=half_w - 0.3, label="核心语义")
P(ax, M + half_w / 2, row2_y + row2_h / 2 - 0.20, "病灶描述词 · 图像高响应区域", 9.8, GRAY,
  ha="center", avail=half_w - 0.3, label="核心语义注")

rbox(ax, M + half_w + 0.45, row2_y, half_w, row2_h, WHITE, SLATE, lw=1.4)
P(ax, M + half_w + 0.45 + half_w / 2, row2_y + row2_h / 2 + 0.18, "外围语义", 12.0, SLATE, "bold",
  ha="center", avail=half_w - 0.3, label="外围语义")
P(ax, M + half_w + 0.45 + half_w / 2, row2_y + row2_h / 2 - 0.20, "位置 · 边界 · 程度修饰词", 9.8, GRAY,
  ha="center", avail=half_w - 0.3, label="外围语义注")

# 汇合箭头
merge_x = W / 2
ax.add_patch(FancyArrowPatch((M + half_w / 2, row2_y - 0.06), (merge_x - 0.06, row2_y - 0.62),
                             arrowstyle="-|>", mutation_scale=15, lw=2.0, color=ACCENT, zorder=3))
ax.add_patch(FancyArrowPatch((M + half_w + 0.45 + half_w / 2, row2_y - 0.06), (merge_x + 0.06, row2_y - 0.62),
                             arrowstyle="-|>", mutation_scale=15, lw=2.0, color=SLATE, zorder=3))

# 第3层：两级对齐（横向大框）
row3_y, row3_h = 2.85, 0.92
rbox(ax, M + 1.10, row3_y, W - 2 * M - 2.20, row3_h, WHITE, ACCENT, lw=2.0)
P(ax, W / 2, row3_y + row3_h / 2 + 0.20, "两级对比对齐损失", 12.5, ACCENT, "bold",
  ha="center", avail=W - 3.0, label="对齐")
ax.text(W / 2, row3_y + row3_h / 2 - 0.22, r"$\mathcal{L} = \mathcal{L}_{core} + \lambda \cdot \mathcal{L}_{peri}$",
        ha="center", va="center", fontsize=13.5, color=TXT, zorder=5)

ax.add_patch(FancyArrowPatch((W / 2, row3_y - 0.06), (W / 2, row3_y - 0.46), arrowstyle="-|>",
                             mutation_scale=15, lw=2.0, color=ACCENT, zorder=3))

# 第4层：融合
row4_y, row4_h = 1.78, 0.92
rbox(ax, M + 1.10, row4_y, W - 2 * M - 2.20, row4_h, FOG, NAVY, lw=1.6)
P(ax, W / 2, row4_y + row4_h / 2 + 0.20, "可学习加权融合", 12.5, NAVY, "bold",
  ha="center", avail=W - 3.0, label="融合")
ax.text(W / 2, row4_y + row4_h / 2 - 0.22, r"$f = w_c \cdot z_c + w_p \cdot z_p$",
        ha="center", va="center", fontsize=13.5, color=TXT, zorder=5)

ax.add_patch(FancyArrowPatch((W / 2, row4_y - 0.06), (W / 2, row4_y - 0.44), arrowstyle="-|>",
                             mutation_scale=15, lw=2.0, color=NAVY, zorder=3))

# 输出
row5_y, row5_h = 0.92, 0.72
rbox(ax, M + 2.60, row5_y, W - 2 * M - 5.20, row5_h, WHITE, SLATE, lw=1.5)
P(ax, W / 2, row5_y + row5_h / 2, "零样本分类 · 跨模态检索 · 病灶分割", 11.5, SLATE, "bold",
  ha="center", avail=W - 2 * M - 5.5, label="输出")

P(ax, W / 2, 0.46, "改动只发生在对齐层：骨干网络、数据流程、下游接口全部沿用原设定。",
  11.8, ACCENT, "bold", ha="center", avail=W - 0.7, label="注")

fig.savefig(f"{OUT}/p5_mechanism.png", dpi=200, facecolor=WHITE)
plt.close(fig)

print("=== 自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
