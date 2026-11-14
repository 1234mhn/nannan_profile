# -*- coding: utf-8 -*-
"""
v3：按 Claude Code 第二轮诊断修
  P3：标题与正文间距调匀、字号 +25%、左右严格对称
  P4：标签紧贴内容、行距均匀、字号 +20%、上下边距收紧
  P5：箭头全部改垂直、终点停在框外留 8px 间隙、各排间距统一、字号放大
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = "/root/.openclaw/workspace/figs/final9_v3"
os.makedirs(OUT, exist_ok=True)

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "cm"

NAVY = "#243447"
SLATE = "#3D6280"
MIST = "#5F7E96"
PALE = "#C5D2DC"
FOG = "#F2F5F7"
TXT = "#2B3A47"
GRAY = "#6B7B88"
ACCENT = "#B8722F"
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


def varrow(ax, x, y1, y2, color, lw=2.4, ms=19):
    """垂直箭头：y1 起点(下) -> y2 终点(上)，两端由调用方留好间隙"""
    ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color, zorder=3))


def P(ax, x, y, s, fs, color=TXT, weight="normal", ha="left", va="center",
      avail=None, label="", ls=1.5, zorder=5):
    if avail:
        fs = fit(s, fs, avail, weight, label)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color,
            fontweight=weight, linespacing=ls, zorder=zorder)


# =========================================================
# P3 —— 卡片内标题+正文作为一个整体垂直居中，间距固定
# =========================================================
W, H = 15.0, 7.9
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "医学 CLIP 的四类问题：后续方法都在补什么", 21, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.90, "CLIP 解决了「不靠人工标签」；医学场景又带来四个新缺口",
  12.2, GRAY, ha="center", avail=W - 0.7, label="副标题")

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

M = 0.60
TOP, BOT, RGAP = H - 1.38, 1.10, 0.16
rh = (TOP - BOT - 3 * RGAP) / 4
SQ = 0.86
card_x = M + SQ + 0.20
card_w = W - M - card_x
meth_w = 2.55
text_w = card_w - 0.52 - meth_w - 0.34

for i, (num, title, col, desc, meth) in enumerate(rows):
    y = TOP - (i + 1) * rh - i * RGAP
    rbox(ax, M, y + (rh - SQ) / 2, SQ, SQ, col, col, lw=0, r=0.12)
    P(ax, M + SQ / 2, y + rh / 2, num, 18, WHITE, "bold", ha="center")
    rbox(ax, card_x, y, card_w, rh, WHITE, col, lw=1.6)

    # 显式坐标：标题一行、正文两行，全部用"行高"算出精确 y，绝不用 va=top 叠加
    t_fs, d_fs = 13.5, 10.5
    TH = 0.26                            # 标题一行占高
    GAP = 0.05                           # 标题与正文之间净间隙
    DH = 0.50                            # 正文两行占高
    block_h = TH + GAP + DH
    b_bot = y + (rh - block_h) / 2       # 组底（绝对）
    title_y = b_bot + DH + GAP + TH / 2  # 标题中心
    desc_y = b_bot + DH / 2              # 正文块中心
    P(ax, card_x + 0.26, title_y, title, t_fs, col, "bold",
      va="center", avail=text_w, label=f"题{i+1}")
    P(ax, card_x + 0.26, desc_y, desc, d_fs, TXT,
      va="center", avail=text_w, label=f"述{i+1}", ls=1.75)

    # 右列：标签+方法名整体垂直居中，间距固定
    mx = card_x + card_w - meth_w - 0.14
    ax.plot([mx - 0.16, mx - 0.16], [y + 0.20, y + rh - 0.20], color=PALE, lw=1.1)
    P(ax, mx, y + rh / 2 + 0.13, "代表方法", 9.8, GRAY, avail=meth_w - 0.14, label=f"标{i+1}")
    P(ax, mx, y + rh / 2 - 0.16, " · ".join(meth), 10.8, col, "bold",
      avail=meth_w - 0.14, label=f"法{i+1}")

P(ax, W / 2, 0.55, "本文聚焦问题①中的「核心—外围」这一支：把病灶与背景显式拆开，分别对齐。",
  12.2, ACCENT, "bold", ha="center", avail=W - 0.7, label="聚焦")

fig.savefig(f"{OUT}/p3_taxonomy.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# P4 —— 每组「标签+内容」作为一个整体，行距完全均分
# =========================================================
W, H = 15.0, 7.5
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "CP-CLIP 与 CLIP：同一任务，两种对齐方式", 21, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.90, "目标相同 —— 都在建立图文对应；差别在「对齐之前怎么拆」",
  12.2, GRAY, ha="center", avail=W - 0.7, label="副标题")

M, GAP_MID = 0.60, 0.90
pw = (W - 2 * M - GAP_MID) / 2
py, ph = 1.80, 4.05
PAD = 0.28

CLIP_ROWS = [
    ("对齐单位", "整张图像 ↔ 整份报告，一对一"),
    ("向量数量", "图像、文本各压成 1 个全局向量"),
    ("语义粒度", "多病灶语义在平均时被抹平"),
    ("背景干扰", "背景与病灶共用同一特征通道"),
]
CP_ROWS = [
    ("对齐单位", "核心 ↔ 核心、外围 ↔ 外围，两两配对"),
    ("向量数量", "核心与外围各一组向量，信息分行"),
    ("语义粒度", "病灶语义独立保留，不被背景稀释"),
    ("背景干扰", "背景单独归入外围通路，主动隔离"),
]


def panel(x, title, color, rows, hi):
    rbox(ax, x, py, pw, ph, WHITE if hi else FOG, color, lw=2.2 if hi else 1.4)
    rbox(ax, x, py + ph - 0.56, pw, 0.56, color, color, lw=0, r=0.10, z=3)
    rbox(ax, x, py + ph - 0.56, pw, 0.26, color, color, lw=0, r=0.0, z=3)
    P(ax, x + pw / 2, py + ph - 0.28, title, 14.5, WHITE, "bold", ha="center",
      avail=pw - 0.4, label=title)

    inner_top = py + ph - 0.56 - 0.24
    inner_bot = py + 0.24
    seg = (inner_top - inner_bot) / 4
    for i, (k, v) in enumerate(rows):
        ctop = inner_top - seg * i
        # 组内：标签在上，内容紧跟其下（间距固定 0.06），组整体在 seg 内垂直居中
        gh = 0.26 + 0.06 + 0.30
        gy = ctop - (seg - gh) / 2
        P(ax, x + PAD, gy - 0.13, k, 11.0, color, "bold")
        P(ax, x + PAD, gy - 0.26 - 0.06 - 0.15, v, 11.4, TXT,
          avail=pw - 2 * PAD, label=f"{title}{k}")
        if i < 3:
            yl = ctop - seg
            ax.plot([x + PAD, x + pw - PAD], [yl, yl], color=PALE, lw=1.0)


panel(M, "CLIP", MIST, CLIP_ROWS, hi=False)
panel(M + pw + GAP_MID, "CP-CLIP", SLATE, CP_ROWS, hi=True)

cx = M + pw + GAP_MID / 2
ax.plot([cx, cx], [py + 0.34, py + ph - 0.34], color=PALE, lw=1.6, ls=(0, (5, 4)))
ax.add_patch(Circle((cx, py + ph / 2), 0.35, fc=ACCENT, ec=WHITE, lw=2.0, zorder=6))
P(ax, cx, py + ph / 2, "差异", 10.0, WHITE, "bold", ha="center", zorder=7)

P(ax, W / 2, 1.22, "核心差异：把「一处对齐」改成「两处对齐 + 一次加权融合」。",
  13.0, NAVY, "bold", ha="center", avail=W - 0.7, label="结论")
P(ax, W / 2, 0.68, "改动集中在对齐目标函数，骨干网络与训练流程基本沿用原设定，工程代价低。",
  11.0, GRAY, ha="center", avail=W - 0.7, label="说明")

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# P5 —— 箭头全垂直，终点距框 0.10 间隙，各排间距统一
# =========================================================
W, H = 15.0, 9.05
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "CP-CLIP 核心机制：核心—外围分别对齐，再加权融合", 21, NAVY, "bold",
  ha="center", avail=W - 0.7, label="总标题")
P(ax, W / 2, H - 0.90, "把「一处对齐」拆成「两处语义明确的分别对齐」，再用可学习权重合成",
  12.2, GRAY, ha="center", avail=W - 0.7, label="副标题")

M = 0.60
ARROW_GAP = 0.52        # 箭头区高度（框与框之间统一留这么多）
BOXM = 1.20             # 中部大框左右缩进

# 行参数：从下往上算，保证间距绝对一致
h_out, h_fuse, h_align, h_part, h_in = 0.66, 0.94, 0.94, 0.90, 0.94
y_out = 1.02
y_fuse = y_out + h_out + ARROW_GAP
y_align = y_fuse + h_fuse + ARROW_GAP
y_part = y_align + h_align + ARROW_GAP
y_in = y_part + h_part + ARROW_GAP
assert y_in + h_in < H - 1.05, f"too tall: {y_in+h_in}"

# 输入两框
half_w = (W - 2 * M - 0.50) / 2
rbox(ax, M, y_in, half_w, h_in, FOG, SLATE, lw=1.5)
P(ax, M + half_w / 2, y_in + h_in / 2 + 0.19, "输入图像 X", 13.0, NAVY, "bold",
  ha="center", avail=half_w - 0.3, label="输入图像")
P(ax, M + half_w / 2, y_in + h_in / 2 - 0.21, "胸片 / CT 三维体数据", 10.6, GRAY,
  ha="center", avail=half_w - 0.3, label="输入图像注")

x2 = M + half_w + 0.50
rbox(ax, x2, y_in, half_w, h_in, FOG, SLATE, lw=1.5)
P(ax, x2 + half_w / 2, y_in + h_in / 2 + 0.19, "输入文本 T", 13.0, NAVY, "bold",
  ha="center", avail=half_w - 0.3, label="输入文本")
P(ax, x2 + half_w / 2, y_in + h_in / 2 - 0.21, "放射学报告原文", 10.6, GRAY,
  ha="center", avail=half_w - 0.3, label="输入文本注")

# 垂直箭头 输入 -> 分解
varrow(ax, M + half_w / 2, y_in - 0.08, y_part + h_part + 0.08, SLATE)
varrow(ax, x2 + half_w / 2, y_in - 0.08, y_part + h_part + 0.08, SLATE)

# 分解两框
rbox(ax, M, y_part, half_w, h_part, WHITE, ACCENT, lw=1.9)
P(ax, M + half_w / 2, y_part + h_part / 2 + 0.19, "核心语义", 12.8, ACCENT, "bold",
  ha="center", avail=half_w - 0.3, label="核心语义")
P(ax, M + half_w / 2, y_part + h_part / 2 - 0.21, "病灶描述词 · 图像高响应区域", 10.4, GRAY,
  ha="center", avail=half_w - 0.3, label="核心语义注")

rbox(ax, x2, y_part, half_w, h_part, WHITE, SLATE, lw=1.5)
P(ax, x2 + half_w / 2, y_part + h_part / 2 + 0.19, "外围语义", 12.8, SLATE, "bold",
  ha="center", avail=half_w - 0.3, label="外围语义")
P(ax, x2 + half_w / 2, y_part + h_part / 2 - 0.21, "位置 · 边界 · 程度修饰词", 10.4, GRAY,
  ha="center", avail=half_w - 0.3, label="外围语义注")

# 垂直箭头 分解 -> 对齐（两框各自向下，不再斜穿）
varrow(ax, M + half_w / 2, y_part - 0.08, y_align + h_align + 0.08, ACCENT)
varrow(ax, x2 + half_w / 2, y_part - 0.08, y_align + h_align + 0.08, SLATE)

# 对齐大框
bx, bw = M + BOXM, W - 2 * (M + BOXM)
rbox(ax, bx, y_align, bw, h_align, WHITE, ACCENT, lw=2.1)
P(ax, W / 2, y_align + h_align / 2 + 0.21, "两级对比对齐损失", 13.2, ACCENT, "bold",
  ha="center", avail=bw - 0.5, label="对齐")
ax.text(W / 2, y_align + h_align / 2 - 0.22,
        r"$\mathcal{L} = \mathcal{L}_{core} + \lambda \cdot \mathcal{L}_{peri}$",
        ha="center", va="center", fontsize=14.5, color=TXT, zorder=5)

varrow(ax, W / 2, y_align - 0.08, y_fuse + h_fuse + 0.08, ACCENT)

# 融合大框
rbox(ax, bx, y_fuse, bw, h_fuse, FOG, NAVY, lw=1.7)
P(ax, W / 2, y_fuse + h_fuse / 2 + 0.21, "可学习加权融合", 13.2, NAVY, "bold",
  ha="center", avail=bw - 0.5, label="融合")
ax.text(W / 2, y_fuse + h_fuse / 2 - 0.22,
        r"$f = w_c \cdot z_c + w_p \cdot z_p$",
        ha="center", va="center", fontsize=14.5, color=TXT, zorder=5)

varrow(ax, W / 2, y_fuse - 0.08, y_out + h_out + 0.08, NAVY)

# 输出框（窄）
ow = 6.40
rbox(ax, (W - ow) / 2, y_out, ow, h_out, WHITE, SLATE, lw=1.5)
P(ax, W / 2, y_out + h_out / 2, "零样本分类 · 跨模态检索 · 病灶分割", 12.2, SLATE, "bold",
  ha="center", avail=ow - 0.4, label="输出")

P(ax, W / 2, 0.50, "改动只发生在对齐层：骨干网络、数据流程、下游接口全部沿用原设定。",
  12.2, ACCENT, "bold", ha="center", avail=W - 0.7, label="注")

fig.savefig(f"{OUT}/p5_mechanism.png", dpi=200, facecolor=WHITE)
plt.close(fig)

print("=== 自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
