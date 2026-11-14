# -*- coding: utf-8 -*-
"""补齐 15 分钟组会汇报所需的新页图（低饱和蓝灰学术风）"""
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

NAVY = "#2C3E50"
SLATE = "#4A6D8C"
MIST = "#8FA5B8"
PALE = "#C5D2DC"
FOG = "#EEF2F5"
TXT = "#34495E"
GRAY = "#8B99A6"
ACCENT = "#C8873E"
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
    P(ax, W / 2, H - 0.48, main, 21, NAVY, "bold", ha="center", avail=W - 0.9, label="主标题")
    if sub:
        P(ax, W / 2, H - 0.95, sub, 11.5, GRAY, ha="center", avail=W - 0.9, label="副标题")


# =========================================================
# 图7：汇报大纲
# =========================================================
W, H = 15, 6.0
fig, ax = setup(W, H)
title_block(ax, W, H, "汇报大纲", "六部分 · 约 15 分钟")

items = [
    ("01", "研究背景", "临床痛点"),
    ("02", "相关工作", "演进脉络"),
    ("03", "技术基础", "CLIP 范式"),
    ("04", "研究空白", "三个方向"),
    ("05", "方法结构", "框架与对齐"),
    ("06", "实验与总结", "指标与启示"),
]
bw, bh, gap = 2.10, 1.85, 0.30
x0 = (W - 6 * bw - 5 * gap) / 2
y0 = 2.55
for i, (num, t, d) in enumerate(items):
    x = x0 + i * (bw + gap)
    c = ACCENT if i == 4 else SLATE
    rbox(ax, x, y0, bw, bh, WHITE, c, lw=2.0 if i == 4 else 1.3)
    P(ax, x + bw / 2, y0 + bh - 0.38, num, 16, c, "bold", ha="center")
    P(ax, x + bw / 2, y0 + bh - 0.82, t, 12, NAVY, "bold", ha="center", avail=bw - 0.25, label=f"大纲{i+1}")
    P(ax, x + bw / 2, y0 + 0.42, d, 9.5, GRAY, ha="center", avail=bw - 0.25, label=f"大纲注{i+1}")

P(ax, W / 2, 1.55, "重点：方法结构（05）与实验验证（06）",
  11.5, ACCENT, "bold", ha="center", avail=W - 1.0, label="重点")
fig.savefig(f"{OUT}/07_outline.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图8：CLIP 双塔范式
# =========================================================
W, H = 15, 7.0
fig, ax = setup(W, H)
title_block(ax, W, H, "技术基础：CLIP 的双塔对比学习范式",
             "图像与文本各过一个编码器，在共享空间中拉近配对、推远非配对")

# 图像塔
rbox(ax, 1.10, 4.35, 2.30, 1.20, FOG, SLATE, lw=1.4)
P(ax, 2.25, 5.16, "输入图像", 12, NAVY, "bold", ha="center", avail=2.0, label="输入图像")
P(ax, 2.25, 4.72, "胸片 / CT", 9.8, GRAY, ha="center", avail=2.0, label="输入图像注")

rbox(ax, 4.10, 4.35, 2.55, 1.20, WHITE, SLATE, lw=1.8)
P(ax, 5.37, 5.16, "图像编码器  f_I", 12, SLATE, "bold", ha="center", avail=2.25, label="图像编码器")
P(ax, 5.37, 4.72, "ResNet / ViT", 9.8, GRAY, ha="center", avail=2.25, label="图像编码器注")

# 文本塔
rbox(ax, 1.10, 2.35, 2.30, 1.20, FOG, SLATE, lw=1.4)
P(ax, 2.25, 3.16, "输入文本", 12, NAVY, "bold", ha="center", avail=2.0, label="输入文本")
P(ax, 2.25, 2.72, "放射学报告", 9.8, GRAY, ha="center", avail=2.0, label="输入文本注")

rbox(ax, 4.10, 2.35, 2.55, 1.20, WHITE, SLATE, lw=1.8)
P(ax, 5.37, 3.16, "文本编码器  f_T", 12, SLATE, "bold", ha="center", avail=2.25, label="文本编码器")
P(ax, 5.37, 2.72, "BERT / ClinicalBERT", 9.8, GRAY, ha="center", avail=2.25, label="文本编码器注")

arrow(ax, 3.45, 4.95, 4.05, 4.95, color=SLATE)
arrow(ax, 3.45, 2.95, 4.05, 2.95, color=SLATE)

# 特征向量
ax.plot([7.45], [4.95], marker="o", ms=17, color=SLATE, zorder=4)
ax.plot([7.45], [2.95], marker="o", ms=17, color=SLATE, zorder=4)
P(ax, 7.45, 4.55, "图像向量", 9.5, GRAY, ha="center", avail=1.6, label="图像向量")
P(ax, 7.45, 2.55, "文本向量", 9.5, GRAY, ha="center", avail=1.6, label="文本向量")
arrow(ax, 6.70, 4.95, 7.28, 4.95, color=SLATE)
arrow(ax, 6.70, 2.95, 7.28, 2.95, color=SLATE)

# 共享空间
rbox(ax, 8.60, 2.65, 2.60, 2.60, FOG, ACCENT, lw=2.0)
P(ax, 9.90, 4.92, "共享特征空间", 11.5, ACCENT, "bold", ha="center", avail=2.35, label="共享空间")
# 配对拉近
ax.plot([9.35, 10.35], [3.95, 4.05], color=ACCENT, lw=2.2)
ax.plot([9.35], [3.95], marker="o", ms=12, color=SLATE, zorder=5)
ax.plot([10.35], [4.05], marker="o", ms=12, color=SLATE, zorder=5)
P(ax, 9.85, 3.55, "配对：拉近", 9.5, ACCENT, "bold", ha="center", avail=2.3, label="配对拉近")
ax.plot([9.20, 10.45], [3.05, 3.12], color=MIST, lw=1.4, ls=(0, (4, 3)))
ax.plot([9.20], [3.05], marker="o", ms=9, color=PALE, zorder=5)
ax.plot([10.45], [3.12], marker="o", ms=9, color=PALE, zorder=5)
P(ax, 9.85, 2.82, "非配对：推远", 9.5, GRAY, ha="center", avail=2.3, label="非配对推远")

arrow(ax, 7.72, 4.90, 8.55, 4.30, color=SLATE)
arrow(ax, 7.72, 3.00, 8.55, 3.45, color=SLATE)

# 右侧说明
rbox(ax, 11.70, 2.65, 2.75, 2.60, WHITE, SLATE, lw=1.5)
P(ax, 13.07, 4.92, "损失与优势", 11.5, NAVY, "bold", ha="center", avail=2.5, label="损失标题")
ax.plot([11.95, 14.20], [4.68, 4.68], color=PALE, lw=1.1)
P(ax, 11.90, 4.28, "损失：InfoNCE", 10, TXT, avail=2.45, label="损失")
P(ax, 11.90, 3.62, "优势：无需人工标签\n可做零样本分类", 10, TXT, avail=2.45, label="优势", ls=1.9)
P(ax, 11.90, 2.95, "前提：一图一语义", 9.8, ACCENT, "bold", avail=2.45, label="前提")

P(ax, W / 2, 1.30, "医学场景下这个前提不成立：一张胸片有多个器官与病灶，一份报告也讲好几件事。",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="结论")

fig.savefig(f"{OUT}/08_clip_paradigm.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图9：核心—外围分解
# =========================================================
W, H = 15, 7.4
fig, ax = setup(W, H)
title_block(ax, W, H, "关键设计：核心—外围如何分解",
             "图像侧靠弱监督定位，文本侧靠词性区分，均不引入额外标注")

# 左：图像侧
rbox(ax, 0.75, 2.30, 6.30, 3.85, WHITE, SLATE, lw=1.6)
P(ax, 3.90, 5.80, "图像侧：弱监督提取核心区域", 12.5, NAVY, "bold", ha="center",
  avail=6.0, label="图像侧标题")
ax.plot([1.05, 6.75], [5.58, 5.58], color=PALE, lw=1.1)

# 示意图
ax.add_patch(Rectangle((1.30, 3.40), 2.35, 1.95, fc=FOG, ec=MIST, lw=1.4))
ax.add_patch(Circle((2.15, 4.42), 0.44, fc=ACCENT, ec=WHITE, lw=1.8, alpha=0.85, zorder=4))
P(ax, 2.15, 4.42, "核心", 9.5, WHITE, "bold", ha="center", zorder=5)
ax.add_patch(Rectangle((2.90, 3.65), 0.58, 1.45, fc="none", ec=SLATE, lw=1.4, ls="--", zorder=4))
P(ax, 3.19, 4.38, "外围", 9, SLATE, ha="center", zorder=5)

P(ax, 4.00, 4.90, "① 报告中的病灶描述词", 10.2, TXT, avail=2.75, label="图像侧1")
P(ax, 4.00, 4.34, "② 与图像注意力响应\n    做弱对应", 10.2, TXT, avail=2.75, label="图像侧2", ls=1.9)
P(ax, 4.00, 3.72, "③ 响应高 → 核心 RoI", 10.2, ACCENT, "bold", avail=2.75, label="图像侧3")
P(ax, 3.90, 2.75, "不增加标注成本，可直接在公开数据集上训练", 9.6, GRAY, ha="center",
  avail=5.9, label="图像侧注")

# 右：文本侧
rbox(ax, 7.95, 2.30, 6.30, 3.85, WHITE, ACCENT, lw=2.0)
P(ax, 11.10, 5.80, "文本侧：按语义角色划分", 12.5, NAVY, "bold", ha="center",
  avail=6.0, label="文本侧标题")
ax.plot([8.25, 13.95], [5.58, 5.58], color=PALE, lw=1.1)

rbox(ax, 8.30, 3.85, 2.55, 1.35, FOG, ACCENT, lw=1.6)
P(ax, 9.57, 4.92, "核心语汇", 11, ACCENT, "bold", ha="center", avail=2.3, label="核心语汇标题")
P(ax, 9.57, 4.42, "描述病变本身", 9.4, GRAY, ha="center", avail=2.3, label="核心语汇注")
P(ax, 9.57, 4.10, "「斑片状高密度影」", 9.4, TXT, ha="center", avail=2.3, label="核心语汇例")

rbox(ax, 11.20, 3.85, 2.55, 1.35, FOG, SLATE, lw=1.4)
P(ax, 12.47, 4.92, "外围语汇", 11, SLATE, "bold", ha="center", avail=2.3, label="外围语汇标题")
P(ax, 12.47, 4.42, "位置 / 边界 / 程度", 9.4, GRAY, ha="center", avail=2.3, label="外围语汇注")
P(ax, 12.47, 4.10, "「右下肺」「边界模糊」", 9.4, TXT, ha="center", avail=2.3, label="外围语汇例")

P(ax, 11.10, 3.32, "核心承载判别信息 · 外围承载上下文",
  10.2, NAVY, "bold", ha="center", avail=6.0, label="文本侧分工")
P(ax, 11.10, 2.75, "两者作用不同，混在同一向量里会互相稀释",
  9.6, GRAY, ha="center", avail=6.0, label="文本侧注")

P(ax, W / 2, 1.32, "分解的目的是让两类语义走独立通路 —— 不是增加信息量，而是避免彼此干扰。",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="结论")

fig.savefig(f"{OUT}/09_decompose.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图10：两级对齐与加权融合
# =========================================================
W, H = 15, 7.4
fig, ax = setup(W, H)
title_block(ax, W, H, "关键设计：两级对齐与可学习加权融合",
             "一处全局对齐 → 两处语义明确的分别对齐 + 一次加权")

# 上：特征
rbox(ax, 1.05, 4.60, 2.45, 1.05, WHITE, SLATE, lw=1.6)
P(ax, 2.27, 5.30, "图像侧特征", 11, SLATE, "bold", ha="center", avail=2.2, label="图像特征")
P(ax, 2.27, 4.90, "z_c   |   z_p", 10, TXT, ha="center", avail=2.2, label="图像特征值")

rbox(ax, 1.05, 3.20, 2.45, 1.05, WHITE, SLATE, lw=1.6)
P(ax, 2.27, 3.90, "文本侧特征", 11, SLATE, "bold", ha="center", avail=2.2, label="文本特征")
P(ax, 2.27, 3.50, "t_c   |   t_p", 10, TXT, ha="center", avail=2.2, label="文本特征值")

# 中：两级损失
rbox(ax, 4.30, 4.55, 3.65, 1.15, WHITE, ACCENT, lw=2.0)
P(ax, 6.12, 5.32, "核心对齐损失  L_core", 11.5, ACCENT, "bold", ha="center", avail=3.4, label="核心损失")
P(ax, 6.12, 4.88, "z_c  ↔  t_c", 10, TXT, ha="center", avail=3.4, label="核心对齐")

rbox(ax, 4.30, 3.15, 3.65, 1.15, WHITE, SLATE, lw=1.6)
P(ax, 6.12, 3.92, "外围对齐损失  L_peri", 11.5, SLATE, "bold", ha="center", avail=3.4, label="外围损失")
P(ax, 6.12, 3.48, "z_p  ↔  t_p", 10, TXT, ha="center", avail=3.4, label="外围对齐")

arrow(ax, 3.55, 5.15, 4.25, 5.12, color=SLATE)
arrow(ax, 3.55, 3.72, 4.25, 3.72, color=SLATE)

# 下：总损失
rbox(ax, 4.30, 1.72, 3.65, 0.95, FOG, NAVY, lw=1.6)
P(ax, 6.12, 2.32, "L = L_core + λ · L_peri", 12, NAVY, "bold", ha="center", avail=3.4, label="总损失")
P(ax, 6.12, 1.94, "λ 控制外围贡献强度（通常 < 1）", 9.4, GRAY, ha="center", avail=3.4, label="λ说明")

arrow(ax, 6.12, 4.50, 6.12, 2.72, color=ACCENT, lw=2.0)

# 右：融合
rbox(ax, 8.90, 2.55, 2.55, 2.10, WHITE, ACCENT, lw=2.0)
P(ax, 10.17, 4.30, "加权融合", 11.5, ACCENT, "bold", ha="center", avail=2.3, label="融合标题")
P(ax, 10.17, 3.72, "f = w_c·z_c", 10, TXT, ha="center", avail=2.3, label="融合1")
P(ax, 10.17, 3.38, "  + w_p·z_p", 10, TXT, ha="center", avail=2.3, label="融合2")
ax.plot([9.20, 11.15], [3.10, 3.10], color=PALE, lw=1.1)
P(ax, 10.17, 2.82, "权重由数据学习", 9.6, NAVY, "bold", ha="center", avail=2.3, label="权重说明")

arrow(ax, 8.00, 2.20, 8.85, 3.30, color=ACCENT, lw=2.0)

# 最右：作用说明
rbox(ax, 11.85, 2.55, 2.60, 2.10, WHITE, SLATE, lw=1.5)
P(ax, 13.15, 4.30, "两个设计的分工", 11.5, NAVY, "bold", ha="center", avail=2.35, label="分工标题")
P(ax, 12.05, 3.75, "λ：损失层平衡\n     控制外围话语权", 9.6, TXT, avail=2.35, label="λ分工", ls=1.9)
P(ax, 12.05, 3.02, "w：特征层占比\n     控制最终表示构成", 9.6, TXT, avail=2.35, label="w分工", ls=1.9)

P(ax, W / 2, 1.20, "改动只在对齐层：骨干不变、数据流程不变，结构代价极小。",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="结论")

fig.savefig(f"{OUT}/10_align_fuse.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图11：总结与展望
# =========================================================
W, H = 15, 7.4
fig, ax = setup(W, H)
title_block(ax, W, H, "总结与展望", "三点可复用结论 · 一个明确留白 · 后续计划")

cols = [
    ("可复用的结论", SLATE, [
        "显式分解：让病灶语义与背景语义走独立通路",
        "两级对齐：避免全局平均带来的语义损失",
        "可学习加权：用两个标量换来自适应能力",
    ]),
    ("仍然的留白", ACCENT, [
        "核心与外围拆开后仍是独立对齐",
        "区域之间的语义关联未被显式建模",
        "这正是 M3GCD 可以接续的位置",
    ]),
]
bw, gap = 6.45, 0.55
x0 = (W - 2 * bw - gap) / 2
y0 = 3.05
bh = 2.95
for i, (t, c, lines) in enumerate(cols):
    x = x0 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, WHITE, c, lw=2.2 if c == ACCENT else 1.5)
    rbox(ax, x, y0 + bh - 0.55, bw, 0.55, c, c, lw=0, r=0.10, z=3)
    rbox(ax, x, y0 + bh - 0.55, bw, 0.26, c, c, lw=0, r=0.0, z=3)
    P(ax, x + bw / 2, y0 + bh - 0.28, t, 12.5, WHITE, "bold", ha="center",
      avail=bw - 0.4, label=f"总结列{i+1}")
    yy = y0 + bh - 1.05
    for ln in lines:
        ax.add_patch(Circle((x + 0.42, yy), 0.055, fc=c, ec="none", zorder=4))
        P(ax, x + 0.62, yy, ln, 10.5, TXT, avail=bw - 0.95, label=f"列{i+1}项")
        yy -= 0.62

# 后续计划条
rbox(ax, x0, 1.35, 2 * bw + gap, 1.15, FOG, SLATE, lw=1.4)
P(ax, W / 2, 2.18, "后续计划", 11.5, NAVY, "bold", ha="center", avail=2 * bw, label="计划标题")
P(ax, W / 2, 1.72, "先复现核心—外围对齐结构  →  在其上引入关系建模模块  →  在公开数据集上验证",
  10.5, TXT, ha="center", avail=2 * bw - 0.6, label="计划内容")

P(ax, W / 2, 0.68, "结构化处理从「图像空间的主次分离」迁移到「语义空间的类别关联」",
  12, ACCENT, "bold", ha="center", avail=W - 1.0, label="核心句")

fig.savefig(f"{OUT}/11_summary.png", dpi=200, facecolor=WHITE)
plt.close(fig)

print("=== 自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
