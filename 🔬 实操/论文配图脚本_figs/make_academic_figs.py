# -*- coding: utf-8 -*-
"""
学术汇报全套图 —— 低饱和蓝灰学术风
配色：主蓝灰 #4A6D8C / 深灰 #2C3E50 / 浅灰 #A8B5C0 / 强调橙 #C8873E（仅用于创新点/差异）
所有文字经宽度实测校验，保证不重叠、不出框。
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

OUT = "/root/.openclaw/workspace/figs/academic"

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

# ============ 低饱和蓝灰学术配色 ============
NAVY = "#2C3E50"      # 深灰蓝（主标题）
SLATE = "#4A6D8C"     # 主蓝灰（主要结构）
MIST = "#8FA5B8"      # 中灰蓝（次要元素）
PALE = "#C5D2DC"      # 浅灰蓝（背景块/分隔）
FOG = "#EEF2F5"       # 极浅底
TXT = "#34495E"       # 正文
GRAY = "#8B99A6"      # 注释
ACCENT = "#C8873E"    # 唯一强调色（创新/差异/核心指标）
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
    """文字宽度（英寸）"""
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
    WARN.append(f"{label or s[:16]}: {fs}->{new:.1f}pt")
    return new


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.6, r=0.10, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, x1, y1, x2, y2, color=MIST, lw=1.8, ms=15):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color, zorder=3))


def P(ax, x, y, s, fs, color=TXT, weight="normal", ha="left", va="center",
      avail=None, label="", ls=1.6, zorder=5):
    if avail:
        fs = fit(s, fs, avail, weight, label)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color,
            fontweight=weight, linespacing=ls, zorder=zorder)


def title_block(ax, W, H, main, sub=None):
    P(ax, W / 2, H - 0.48, main, 21, NAVY, "bold", ha="center", avail=W - 0.9,
      label="主标题")
    if sub:
        P(ax, W / 2, H - 0.95, sub, 11.5, GRAY, ha="center", avail=W - 0.9,
          label="副标题")


# =========================================================
# 图1：研究背景 —— 临床痛点（封面后第2页）
# =========================================================
W, H = 15, 7.6
fig, ax = setup(W, H)
title_block(ax, W, H, "研究背景：临床影像诊断的三个现实约束",
             "医学多模态模型要解决的问题，从临床现场开始")

pains = [
    ("阅片工作量大", "一位放射科医生日均需阅读\n上百份影像，报告撰写占用\n大量时间。", SLATE),
    ("单模态能力有限", "仅靠图像难以区分相似病灶；\n仅靠文本丢失空间信息，\n两者都缺一半。", SLATE),
    ("跨模态对齐困难", "一份报告对应多张图、\n一张图涉及多个病灶，\n图文之间天然不整齐。", ACCENT),
]
bw, bh, gap = 4.35, 3.30, 0.50
x0 = (W - 3 * bw - 2 * gap) / 2
y0 = 2.35
for i, (t, d, c) in enumerate(pains):
    x = x0 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, WHITE, c, lw=2.0 if c == ACCENT else 1.5)
    rbox(ax, x, y0 + bh - 0.62, bw, 0.62, c, c, lw=0, r=0.10, z=3)
    rbox(ax, x, y0 + bh - 0.62, bw, 0.30, c, c, lw=0, r=0.0, z=3)
    P(ax, x + bw / 2, y0 + bh - 0.31, t, 13.5, WHITE, "bold", ha="center",
      avail=bw - 0.4, label=f"痛点{i+1}")
    P(ax, x + bw / 2, y0 + 1.35, d, 10.5, TXT, ha="center", avail=bw - 0.6,
      label=f"痛点描述{i+1}", ls=1.9)

P(ax, W / 2, 1.35, "第三个约束是方法层面的核心矛盾，也是本文的切入位置。",
  12, ACCENT, "bold", ha="center", avail=W - 1.0, label="结论")
P(ax, W / 2, 0.72, "代表工作：CLIP (2021) · MedViLL · MIMIC-CXR · MedRGen",
  10, GRAY, ha="center", avail=W - 1.0, label="代表工作")

fig.savefig(f"{OUT}/01_background.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图2：相关工作演进时间线
# =========================================================
W, H = 15, 7.8
fig, ax = setup(W, H)
title_block(ax, W, H, "相关工作：医学图文对齐的五步演进",
             "共同前提：一份报告可以代表整张图 —— 后续工作都在这个前提上做改进")

nodes = [
    ("2020", "ConVIRT", "图文对比学习\n进入医学领域"),
    ("2021", "GloRIA", "拆局部区域\n细粒度对齐"),
    ("2022", "MedCLIP", "解耦假阴性\n改善配对质量"),
    ("2023", "MedKLIP", "抽取病名实体\n注入医学知识"),
    ("2025", "CP-CLIP", "核心—外围分解\n空间结构化对齐"),
]
axis_y = 4.30
ax.add_patch(FancyArrowPatch((0.75, axis_y), (W - 0.75, axis_y), arrowstyle="-|>",
                             mutation_scale=20, lw=2.2, color=PALE))
cw, ch = 2.45, 2.05
n = len(nodes)
span = W - 1.5 - cw
xs = [0.75 + cw / 2 + i * span / (n - 1) for i in range(n)]

for i, ((yr, name, desc), cx) in enumerate(zip(nodes, xs)):
    up = (i % 2 == 0)
    col = ACCENT if name == "CP-CLIP" else SLATE
    ax.add_patch(Circle((cx, axis_y), 0.11, fc=col, ec=WHITE, lw=1.8, zorder=5))
    cy0 = axis_y + 0.48 if up else axis_y - 0.48 - ch
    ax.plot([cx, cx], [axis_y + (0.11 if up else -0.11), cy0 if up else cy0 + ch],
            color=col, lw=1.3, zorder=2)
    rbox(ax, cx - cw / 2, cy0, cw, ch, WHITE, col, lw=2.2 if name == "CP-CLIP" else 1.4)
    P(ax, cx, cy0 + ch - 0.34, yr, 14, col, "bold", ha="center")
    P(ax, cx, cy0 + ch - 0.72, name, 12.5, NAVY, "bold", ha="center",
      avail=cw - 0.25, label=f"名称{i+1}")
    P(ax, cx, cy0 + 0.66, desc, 10, TXT, ha="center", avail=cw - 0.3,
      label=f"描述{i+1}", ls=1.9)

P(ax, W / 2, 1.10, "演进主线：对齐粒度不断变细 —— 从「整图对整文」到「区域对片段」，再到「核心对外围」。",
  12, NAVY, "bold", ha="center", avail=W - 1.0, label="主线")
P(ax, W / 2, 0.52, "资料来源：CLIP in Medical Imaging: A Survey, Medical Image Analysis 2025",
  9.5, GRAY, ha="center", avail=W - 1.0, label="来源")

fig.savefig(f"{OUT}/02_related_work.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图3：研究空白 —— 问题分解
# =========================================================
W, H = 15, 7.8
fig, ax = setup(W, H)
title_block(ax, W, H, "研究空白：现有方法留下的三个可优化方向",
             "不是否定已有工作，而是指出对齐环节仍有结构化空间")

gaps = [
    ("问题一", "对齐粒度偏粗", "整图压成一个向量参与对齐，\n病灶与背景的语义被平均，\n难以区分局部差异。", SLATE),
    ("问题二", "核心与外围未分离", "病灶区域与周边背景组织\n共享同一特征通道，\n背景噪声会干扰判别。", ACCENT),
    ("问题三", "关系结构未建模", "拆开之后仍是独立对齐，\n区域之间的语义关联\n没有被显式利用。", SLATE),
]
bw, bh, gap = 4.30, 3.45, 0.55
x0 = (W - 3 * bw - 2 * gap) / 2
y0 = 2.20
for i, (tag, t, d, c) in enumerate(gaps):
    x = x0 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, WHITE, c, lw=2.2 if c == ACCENT else 1.4)
    P(ax, x + bw / 2, y0 + bh - 0.38, tag, 10.5, c, "bold", ha="center")
    P(ax, x + bw / 2, y0 + bh - 0.85, t, 14, NAVY, "bold", ha="center",
      avail=bw - 0.4, label=f"空白{i+1}")
    ax.plot([x + 0.55, x + bw - 0.55], [y0 + bh - 1.22, y0 + bh - 1.22],
            color=PALE, lw=1.2)
    P(ax, x + bw / 2, y0 + 1.05, d, 10.5, TXT, ha="center", avail=bw - 0.6,
      label=f"空白描述{i+1}", ls=1.9)

P(ax, W / 2, 1.18, "本文聚焦问题二：把「核心 / 外围」显式拆开，各自对齐后再融合。",
  12.5, ACCENT, "bold", ha="center", avail=W - 1.0, label="聚焦")
P(ax, W / 2, 0.58, "问题三作为后续可延伸的方向，本文暂不展开。",
  10.5, GRAY, ha="center", avail=W - 1.0, label="延伸")

fig.savefig(f"{OUT}/03_gap.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图4：模型框架（模块化，左→右）
# =========================================================
W, H = 15, 8.2
fig, ax = setup(W, H)
title_block(ax, W, H, "模型框架：核心—外围双路对齐结构",
             "图像与文本各拆成核心、外围两支，分别编码、分别对齐、最后加权融合")

# --- 输入区 ---
rbox(ax, 0.55, 4.55, 2.15, 1.55, FOG, SLATE, lw=1.4)
P(ax, 1.62, 5.78, "输入图像", 12, NAVY, "bold", ha="center")
P(ax, 1.62, 5.35, "胸片 / CT", 10, GRAY, ha="center", avail=1.9, label="输入图像注")

rbox(ax, 0.55, 2.10, 2.15, 1.55, FOG, SLATE, lw=1.4)
P(ax, 1.62, 3.33, "输入文本", 12, NAVY, "bold", ha="center")
P(ax, 1.62, 2.90, "放射学报告", 10, GRAY, ha="center", avail=1.9, label="输入文本注")

# --- 分解区（核心/外围）---
rbox(ax, 3.15, 4.95, 2.05, 1.05, WHITE, ACCENT, lw=1.8)
P(ax, 4.17, 5.62, "核心区域", 11.5, ACCENT, "bold", ha="center", avail=1.8, label="核心区域")
P(ax, 4.17, 5.25, "病灶 RoI", 9.5, GRAY, ha="center", avail=1.8, label="核心区域注")

rbox(ax, 3.15, 4.10, 2.05, 1.05, WHITE, SLATE, lw=1.5)
P(ax, 4.17, 4.77, "外围区域", 11.5, SLATE, "bold", ha="center", avail=1.8, label="外围区域")
P(ax, 4.17, 4.40, "背景组织", 9.5, GRAY, ha="center", avail=1.8, label="外围区域注")

rbox(ax, 3.15, 2.90, 2.05, 1.05, WHITE, ACCENT, lw=1.8)
P(ax, 4.17, 3.57, "核心语汇", 11.5, ACCENT, "bold", ha="center", avail=1.8, label="核心语汇")
P(ax, 4.17, 3.20, "病变描述", 9.5, GRAY, ha="center", avail=1.8, label="核心语汇注")

rbox(ax, 3.15, 2.05, 2.05, 1.05, WHITE, SLATE, lw=1.5)
P(ax, 4.17, 2.72, "外围语汇", 11.5, SLATE, "bold", ha="center", avail=1.8, label="外围语汇")
P(ax, 4.17, 2.35, "位置 / 边界", 9.5, GRAY, ha="center", avail=1.8, label="外围语汇注")

# 输入→分解箭头
arrow(ax, 2.75, 5.20, 3.10, 5.40, color=SLATE)
arrow(ax, 2.75, 4.75, 3.10, 4.68, color=SLATE)
arrow(ax, 2.75, 3.00, 3.10, 3.45, color=SLATE)
arrow(ax, 2.75, 2.60, 3.10, 2.60, color=SLATE)

# --- 编码区 ---
rbox(ax, 5.65, 4.30, 3.00, 1.55, WHITE, SLATE, lw=1.8)
P(ax, 7.15, 5.50, "图像编码器  f_I", 12, SLATE, "bold", ha="center", avail=2.7, label="图像编码器")
P(ax, 7.15, 5.02, "核心特征 z_c\n外围特征 z_p", 10, TXT, ha="center", avail=2.7,
  label="图像编码器输出", ls=1.9)

rbox(ax, 5.65, 2.20, 3.00, 1.55, WHITE, SLATE, lw=1.8)
P(ax, 7.15, 3.40, "文本编码器  f_T", 12, SLATE, "bold", ha="center", avail=2.7, label="文本编码器")
P(ax, 7.15, 2.92, "核心文本 t_c\n外围文本 t_p", 10, TXT, ha="center", avail=2.7,
  label="文本编码器输出", ls=1.9)

arrow(ax, 5.25, 5.48, 5.60, 5.28, color=SLATE)
arrow(ax, 5.25, 4.62, 5.60, 4.85, color=SLATE)
arrow(ax, 5.25, 3.43, 5.60, 3.20, color=SLATE)
arrow(ax, 5.25, 2.57, 5.60, 2.78, color=SLATE)

# --- 对齐区 ---
rbox(ax, 9.15, 3.05, 2.60, 2.05, WHITE, ACCENT, lw=2.2)
P(ax, 10.45, 4.72, "两级对比对齐", 12, ACCENT, "bold", ha="center", avail=2.35, label="对齐标题")
P(ax, 10.45, 4.22, "L_core : z_c ↔ t_c", 10, TXT, ha="center", avail=2.35, label="对齐式1")
P(ax, 10.45, 3.80, "L_peri : z_p ↔ t_p", 10, TXT, ha="center", avail=2.35, label="对齐式2")
ax.plot([9.42, 11.48], [3.55, 3.55], color=PALE, lw=1.1)
P(ax, 10.45, 3.28, "L = L_core + λ·L_peri", 10.5, NAVY, "bold", ha="center",
  avail=2.35, label="总损失")

arrow(ax, 8.70, 5.08, 9.10, 4.55, color=SLATE)
arrow(ax, 8.70, 2.98, 9.10, 3.55, color=SLATE)

# --- 融合 + 输出 ---
rbox(ax, 12.25, 3.05, 2.30, 2.05, WHITE, SLATE, lw=1.8)
P(ax, 13.40, 4.72, "加权融合", 12, NAVY, "bold", ha="center", avail=2.05, label="融合标题")
P(ax, 13.40, 4.18, "f = w_c·z_c\n    + w_p·z_p", 10, TXT, ha="center", avail=2.05,
  label="融合式", ls=1.9)
ax.plot([12.52, 14.28], [3.55, 3.55], color=PALE, lw=1.1)
P(ax, 13.40, 3.28, "统一特征表示", 9.8, GRAY, ha="center", avail=2.05, label="融合输出")

arrow(ax, 11.80, 4.08, 12.20, 4.08, color=ACCENT)

P(ax, W / 2, 1.35, "最终用于：零样本分类 · 病灶分割 · 图文检索",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="下游")
P(ax, W / 2, 0.75, "改动位置：只在「对齐层」引入结构化拆分，不改动前序数据与编码流程。",
  10.5, GRAY, ha="center", avail=W - 1.0, label="改动说明")

fig.savefig(f"{OUT}/04_framework.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图5：CLIP vs CP-CLIP 差异对比
# =========================================================
W, H = 15, 7.8
fig, ax = setup(W, H)
title_block(ax, W, H, "方法对比：CLIP 与 CP-CLIP 的对齐方式差异",
             "目标相同，都在建立图文对应；差异在「对齐之前怎么拆」")

def panel(x, title, color, rows, hi=False):
    pw, ph = 6.40, 4.30
    py = 2.05
    rbox(ax, x, py, pw, ph, FOG if not hi else WHITE, color,
         lw=2.2 if hi else 1.5)
    rbox(ax, x, py + ph - 0.58, pw, 0.58, color, color, lw=0, r=0.10, z=3)
    rbox(ax, x, py + ph - 0.58, pw, 0.28, color, color, lw=0, r=0.0, z=3)
    P(ax, x + pw / 2, py + ph - 0.29, title, 13, WHITE, "bold", ha="center",
      avail=pw - 0.4, label=title)
    yy = py + ph - 1.05
    for k, v in rows:
        P(ax, x + 0.28, yy, k, 10, color, "bold")
        P(ax, x + 0.28, yy - 0.32, v, 10.2, TXT, avail=pw - 0.56, label=f"{title}{k}")
        yy -= 0.86

panel(0.65, "CLIP", MIST, [
    ("对齐单位", "整图 ↔ 整份报告"),
    ("向量数量", "各压成 1 个全局向量"),
    ("语义粒度", "多病灶语义被平均"),
    ("背景处理", "与病灶共用同一通道"),
], hi=False)

panel(7.95, "CP-CLIP", SLATE, [
    ("对齐单位", "核心 ↔ 核心，外围 ↔ 外围"),
    ("向量数量", "核心 / 外围各一组"),
    ("语义粒度", "病灶语义独立保留"),
    ("背景处理", "单独归入外围，隔离干扰"),
], hi=True)

# 中间差异标记
ax.plot([7.45, 7.45], [2.40, 6.05], color=PALE, lw=1.6, ls=(0, (5, 4)))
ax.add_patch(Circle((7.45, 4.20), 0.32, fc=ACCENT, ec=WHITE, lw=2, zorder=6))
P(ax, 7.45, 4.20, "差异", 9.5, WHITE, "bold", ha="center", zorder=7)

P(ax, W / 2, 1.32, "核心差异：CP-CLIP 把「一处对齐」改成「两处对齐 + 一次加权」。",
  12, NAVY, "bold", ha="center", avail=W - 1.0, label="差异结论")
P(ax, W / 2, 0.72, "改动集中在对齐目标函数，模型骨干与训练流程基本沿用原设定。",
  10.5, GRAY, ha="center", avail=W - 1.0, label="改动说明")

fig.savefig(f"{OUT}/05_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图6：创新点
# =========================================================
W, H = 15, 7.8
fig, ax = setup(W, H)
title_block(ax, W, H, "方法要点：三个可复用的设计选择",
             "务实描述，不夸大 —— 均为对齐环节的结构性调整")

items = [
    ("01", "显式核心—外围分解",
     "把图像与文本同时拆成核心、外围两支，\n使病灶语义与背景语义在特征空间中\n走独立通路，互不干扰。", SLATE),
    ("02", "两级对齐目标",
     "核心对核心、外围对外围分别计算对比损失，\n再用权重 λ 平衡；\n避免单一全局对齐带来的语义平均。", ACCENT),
    ("03", "可学习加权融合",
     "融合权重 w_c / w_p 由数据决定，\n模型自行学习「该更依赖核心还是外围」，\n无需手工设定。", SLATE),
]
bw, bh, gap = 4.30, 3.60, 0.55
x0 = (W - 3 * bw - 2 * gap) / 2
y0 = 2.10
for i, (num, t, d, c) in enumerate(items):
    x = x0 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, WHITE, c, lw=2.2 if c == ACCENT else 1.4)
    P(ax, x + 0.30, y0 + bh - 0.42, num, 22, c, "bold")
    P(ax, x + 0.30, y0 + bh - 0.98, t, 13, NAVY, "bold", avail=bw - 0.55, label=f"要点{i+1}")
    ax.plot([x + 0.30, x + bw - 0.30], [y0 + bh - 1.28, y0 + bh - 1.28], color=PALE, lw=1.2)
    P(ax, x + bw / 2, y0 + 1.02, d, 10.2, TXT, ha="center", avail=bw - 0.6,
      label=f"要点描述{i+1}", ls=1.9)

P(ax, W / 2, 1.18, "对课题的借鉴：问题二「核心与外围未分离」已由本方法给出解法；",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="借鉴1")
P(ax, W / 2, 0.68, "问题三「关系结构未建模」仍留白，是后续可接续的方向。",
  11.5, ACCENT, "bold", ha="center", avail=W - 1.0, label="借鉴2")

fig.savefig(f"{OUT}/06_innovation.png", dpi=200, facecolor=WHITE)
plt.close(fig)

print("=== 自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
