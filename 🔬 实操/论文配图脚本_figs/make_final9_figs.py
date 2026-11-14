# -*- coding: utf-8 -*-
"""
按用户原始 9 页大纲重做全套图
低饱和蓝灰学术风 · 文字实测不重叠 · 节点≤8 层级≤3 连线不交叉
"""
import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

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


def arrow(ax, x1, y1, x2, y2, color=MIST, lw=1.8, ms=15):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color, zorder=3))


def P(ax, x, y, s, fs, color=TXT, weight="normal", ha="left", va="center",
      avail=None, label="", ls=1.6, zorder=5):
    if avail:
        fs = fit(s, fs, avail, weight, label)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color,
            fontweight=weight, linespacing=ls, zorder=zorder)


# =========================================================
# 图 A（第2页）：CLIP 近几年发展梳理
# 6 节点 · 横轴上下交错 · 同年合并
# =========================================================
W, H = 14.6, 7.7
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "医学图文对比学习的发展脉络", 20, NAVY, "bold",
  ha="center", avail=W - 0.8, label="总标题")
P(ax, W / 2, H - 0.88,
  "共同前提：一份报告代表整张图 —— 后续工作都在这个前提上做改进",
  11, GRAY, ha="center", avail=W - 0.8, label="副标题")

nodes = [
    ("2020", "ConVIRT", "图文对比学习\n进入医学领域"),
    ("2021", "GloRIA", "拆局部区域\n做细粒度对齐"),
    ("2022", "MedCLIP", "解耦假阴性\n改善配对质量"),
    ("2023", "MedKLIP", "抽取病名实体\n注入医学知识"),
    ("2025", "MedFILIP\nCP-CLIP", "实体级对齐\n核心—外围分解"),
    ("2026", "MG-3D\nMerlin", "三维数据\n千万级规模"),
]
axis_y = 3.95
ax.add_patch(FancyArrowPatch((0.80, axis_y), (W - 0.80, axis_y), arrowstyle="-|>",
                             mutation_scale=18, lw=2.0, color=PALE))
cw, ch = 2.10, 1.95
n = len(nodes)
span = W - 1.60 - cw
xs = [0.80 + cw / 2 + i * span / (n - 1) for i in range(n)]

for i, ((yr, name, desc), cx) in enumerate(zip(nodes, xs)):
    up = (i % 2 == 0)
    hi = ("CP-CLIP" in name)
    col = ACCENT if hi else SLATE
    ax.add_patch(Circle((cx, axis_y), 0.10, fc=col, ec=WHITE, lw=1.6, zorder=5))
    cy0 = axis_y + 0.45 if up else axis_y - 0.45 - ch
    ax.plot([cx, cx], [axis_y + (0.10 if up else -0.10), cy0 if up else cy0 + ch],
            color=col, lw=1.2, zorder=2)
    rbox(ax, cx - cw / 2, cy0, cw, ch, WHITE, col, lw=2.0 if hi else 1.3)
    P(ax, cx, cy0 + ch - 0.30, yr, 13, col, "bold", ha="center")
    nm = name.replace("\n", " · ")
    P(ax, cx, cy0 + ch - 0.63, nm, 10.5, NAVY, "bold", ha="center",
      avail=cw - 0.20, label=f"名{i+1}")
    P(ax, cx, cy0 + 0.58, desc, 9.2, TXT, ha="center", avail=cw - 0.26,
      label=f"述{i+1}", ls=1.9)

P(ax, W / 2, 0.95, "演进主线：对齐粒度不断变细 —— 整图对整文 → 区域对片段 → 核心对外围",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="主线")
P(ax, W / 2, 0.45, "资料来源：CLIP in Medical Imaging: A Survey, Medical Image Analysis 2025",
  9, GRAY, ha="center", avail=W - 1.0, label="来源")

fig.savefig(f"{OUT}/p2_evolution.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图 B（第3页）：四类问题分类
# 4 行 · 左序号 中描述 右方法 · 层级 2 层
# =========================================================
W, H = 14.6, 7.9
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "医学 CLIP 的四类问题：后续方法都在补什么", 20, NAVY, "bold",
  ha="center", avail=W - 0.8, label="总标题")
P(ax, W / 2, H - 0.88, "CLIP 解决了「不靠人工标签」；医学场景又带来四个新缺口",
  11, GRAY, ha="center", avail=W - 0.8, label="副标题")

rows = [
    ("①", "对齐粒度太粗", SLATE,
     "整图压成一个向量、整份报告压成一个向量，对齐一次就结束；\n但一张胸片有多个器官与病灶，报告也讲好几件事。",
     ["GloRIA", "MedFILIP", "CP-CLIP"]),
    ("②", "文本脏、配对不准", MIST,
     "医学报告冗长、说法不统一，常有「正常报告配异常图像」的\n假阴性，硬对齐会学到错误关联。",
     ["MedCLIP", "MedKLIP"]),
    ("③", "缺医学先验知识", SLATE,
     "通用 CLIP 只学到「图上有什么」；医学要判断病变性质、\n疾病类别与解剖关系。",
     ["MedKLIP", "Abn-BLIP"]),
    ("④", "只做 2D、规模上不去", MIST,
     "CT、MRI 是三维体数据，早期方法只切 2D 切片，丢掉空间\n信息；配对数据量也上不去。",
     ["MG-3D", "Merlin"]),
]
rh, gap = 1.28, 0.20
top = H - 1.35
sq = 0.72
for i, (num, title, col, desc, meth) in enumerate(rows):
    y = top - (i + 1) * rh - i * gap
    rbox(ax, 0.62, y + (rh - sq) / 2, sq, sq, col, col, lw=0, r=0.10)
    P(ax, 0.62 + sq / 2, y + rh / 2, num, 15, WHITE, "bold", ha="center")
    cx0, cwid = 1.52, 8.55
    rbox(ax, cx0, y, cwid, rh, WHITE, col, lw=1.4)
    P(ax, cx0 + 0.20, y + rh - 0.30, title, 12.5, col, "bold",
      avail=cwid - 0.4, label=f"题{i+1}")
    P(ax, cx0 + 0.20, y + 0.44, desc, 9.4, TXT,
      avail=cwid - 0.4, label=f"述{i+1}", ls=1.8)
    mx = cx0 + cwid + 0.35
    P(ax, mx, y + rh - 0.30, "代表方法", 9, GRAY)
    P(ax, mx, y + 0.44, " · ".join(meth), 10.2, col, "bold",
      avail=W - mx - 0.55, label=f"法{i+1}")

P(ax, W / 2, 0.42, "本文聚焦问题①中的「核心—外围」这一支：把病灶与背景显式拆开分别对齐。",
  11, ACCENT, "bold", ha="center", avail=W - 1.0, label="聚焦")

fig.savefig(f"{OUT}/p3_taxonomy.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图 C（第4页）：CP-CLIP 与 CLIP 对比
# 左栏 / 右栏 + 中间分隔，层级 2
# =========================================================
W, H = 14.6, 7.5
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "CP-CLIP 与 CLIP：同一任务，两种对齐方式", 20, NAVY, "bold",
  ha="center", avail=W - 0.8, label="总标题")
P(ax, W / 2, H - 0.88, "目标相同 —— 都在建立图文对应；差别在「对齐之前怎么拆」",
  11, GRAY, ha="center", avail=W - 0.8, label="副标题")


def panel(x, title, color, rows, hi):
    pw, ph = 6.15, 4.15
    py = 1.90
    rbox(ax, x, py, pw, ph, WHITE if hi else FOG, color, lw=2.0 if hi else 1.3)
    rbox(ax, x, py + ph - 0.52, pw, 0.52, color, color, lw=0, r=0.10, z=3)
    rbox(ax, x, py + ph - 0.52, pw, 0.24, color, color, lw=0, r=0.0, z=3)
    P(ax, x + pw / 2, py + ph - 0.26, title, 12.5, WHITE, "bold", ha="center",
      avail=pw - 0.4, label=title)
    yy = py + ph - 1.02
    for k, v in rows:
        P(ax, x + 0.26, yy, k, 9.5, color, "bold")
        P(ax, x + 0.26, yy - 0.30, v, 10.0, TXT, avail=pw - 0.52, label=f"{title}{k}")
        yy -= 0.80


panel(0.62, "CLIP", MIST, [
    ("对齐单位", "整图 ↔ 整份报告"),
    ("向量数量", "各压成 1 个全局向量"),
    ("语义粒度", "多病灶语义被平均"),
    ("背景处理", "与病灶共用同一通道"),
], hi=False)

panel(8.05, "CP-CLIP", SLATE, [
    ("对齐单位", "核心 ↔ 核心，外围 ↔ 外围"),
    ("向量数量", "核心 / 外围各一组"),
    ("语义粒度", "病灶语义独立保留"),
    ("背景处理", "单独归入外围，隔离干扰"),
], hi=True)

# 中间分隔（虚线 + 圆标，不交叉）
ax.plot([7.40, 7.40], [2.20, 5.75], color=PALE, lw=1.5, ls=(0, (5, 4)))
ax.add_patch(Circle((7.40, 3.95), 0.30, fc=ACCENT, ec=WHITE, lw=1.8, zorder=6))
P(ax, 7.40, 3.95, "差异", 9, WHITE, "bold", ha="center", zorder=7)

P(ax, W / 2, 1.18, "核心差异：把「一处对齐」改成「两处对齐 + 一次加权」。",
  11.5, NAVY, "bold", ha="center", avail=W - 1.0, label="结论")
P(ax, W / 2, 0.66, "改动集中在对齐目标函数，骨干网络与训练流程基本沿用原设定。",
  10, GRAY, ha="center", avail=W - 1.0, label="说明")

fig.savefig(f"{OUT}/p4_compare.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图 D（第5页左）：CP-CLIP 机制放大
# 纵向 4 层 · 单链不交叉
# =========================================================
W, H = 7.0, 7.6
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.45, "CP-CLIP 核心机制", 17, NAVY, "bold", ha="center",
  avail=W - 0.6, label="标题")
P(ax, W / 2, H - 0.85, "核心 / 外围分别对齐，再加权融合", 10, GRAY,
  ha="center", avail=W - 0.6, label="副标题")

bw = 5.60
bx = (W - bw) / 2

# 第1层 输入
rbox(ax, bx, 5.55, bw, 0.72, FOG, SLATE, lw=1.3)
P(ax, W / 2, 6.08, "输入图像 X  +  输入文本 T", 11, NAVY, "bold", ha="center",
  avail=bw - 0.3, label="输入")
P(ax, W / 2, 5.76, "胸片 / CT  ·  放射学报告", 9, GRAY, ha="center",
  avail=bw - 0.3, label="输入注")
arrow(ax, W / 2, 5.50, W / 2, 5.20, color=SLATE)

# 第2层 分解（左右两支）
half = (bw - 0.30) / 2
rbox(ax, bx, 4.40, half, 0.78, WHITE, ACCENT, lw=1.6)
P(ax, bx + half / 2, 4.98, "核心", 10.5, ACCENT, "bold", ha="center", avail=half - 0.2, label="核心")
P(ax, bx + half / 2, 4.62, "病灶 / 病变词", 8.8, GRAY, ha="center", avail=half - 0.2, label="核心注")

rbox(ax, bx + half + 0.30, 4.40, half, 0.78, WHITE, SLATE, lw=1.3)
P(ax, bx + half + 0.30 + half / 2, 4.98, "外围", 10.5, SLATE, "bold", ha="center",
  avail=half - 0.2, label="外围")
P(ax, bx + half + 0.30 + half / 2, 4.62, "背景 / 修饰词", 8.8, GRAY, ha="center",
  avail=half - 0.2, label="外围注")

arrow(ax, bx + half / 2, 4.34, bx + half / 2, 4.02, color=ACCENT)
arrow(ax, bx + half + 0.30 + half / 2, 4.34, bx + half + 0.30 + half / 2, 4.02, color=SLATE)

# 第3层 编码 + 对齐
rbox(ax, bx, 3.15, bw, 0.82, WHITE, ACCENT, lw=1.8)
P(ax, W / 2, 3.78, "两级对比对齐", 11, ACCENT, "bold", ha="center", avail=bw - 0.3, label="对齐")
P(ax, W / 2, 3.36, "L = L_core + λ · L_peri", 10.5, TXT, ha="center", avail=bw - 0.3, label="对齐式")
arrow(ax, W / 2, 3.10, W / 2, 2.80, color=ACCENT)

# 第4层 融合
rbox(ax, bx, 1.92, bw, 0.82, FOG, NAVY, lw=1.5)
P(ax, W / 2, 2.55, "加权融合", 11, NAVY, "bold", ha="center", avail=bw - 0.3, label="融合")
P(ax, W / 2, 2.13, "f = w_c · z_c + w_p · z_p", 10.5, TXT, ha="center", avail=bw - 0.3, label="融合式")
arrow(ax, W / 2, 1.86, W / 2, 1.58, color=NAVY)

# 输出
rbox(ax, bx + 0.55, 0.92, bw - 1.10, 0.62, WHITE, SLATE, lw=1.3)
P(ax, W / 2, 1.30, "零样本分类 / 分割 / 检索", 9.8, SLATE, "bold", ha="center",
  avail=bw - 1.3, label="输出")

P(ax, W / 2, 0.40, "改动只在「对齐层」", 10, ACCENT, "bold", ha="center",
  avail=W - 0.6, label="注")

fig.savefig(f"{OUT}/p5_mechanism.png", dpi=200, facecolor=WHITE)
plt.close(fig)


# =========================================================
# 图 E（第6页）：CLIP 完整链路
# 横向 5 段 · 单行不交叉 · 层级 2
# =========================================================
W, H = 14.6, 7.4
fig, ax = setup(W, H)

P(ax, W / 2, H - 0.46, "CLIP 的完整链路：从数据到下游任务", 20, NAVY, "bold",
  ha="center", avail=W - 0.8, label="总标题")
P(ax, W / 2, H - 0.88, "五段流水线 —— CP-CLIP 只改动第四段「对比对齐」",
  11, GRAY, ha="center", avail=W - 0.8, label="副标题")

stages = [
    ("①", "数据构建", "图像-报告配对\nMIMIC-CXR","配对≠真相关"),
    ("②", "文本处理", "清洗报告、抽实体\n术语规范化", "说法不一、一文多事"),
    ("③", "双塔编码", "图像 / 文本编码器\nResNet · ViT · BERT", "整图压成 1 个向量"),
    ("④", "对比对齐", "InfoNCE 损失\n拉近正样本", "CP-CLIP 改这里"),
    ("⑤", "下游应用", "分类 · 检索\n报告生成 · 分割", "泛化到未见类别"),
]

bw, bh, gap = 2.42, 2.35, 0.30
total = 5 * bw + 4 * gap
x0 = (W - total) / 2
y0 = 2.45
for i, (num, name, what, pain) in enumerate(stages):
    x = x0 + i * (bw + gap)
    hi = (num == "④")
    col = ACCENT if hi else SLATE
    rbox(ax, x, y0, bw, bh, WHITE if hi else FOG, col, lw=2.0 if hi else 1.3)
    rbox(ax, x, y0 + bh - 0.48, bw, 0.48, col, col, lw=0, r=0.10, z=3)
    rbox(ax, x, y0 + bh - 0.48, bw, 0.22, col, col, lw=0, r=0.0, z=3)
    P(ax, x + bw / 2, y0 + bh - 0.24, f"{num} {name}", 10.8, WHITE, "bold",
      ha="center", avail=bw - 0.20, label=f"段{i+1}")
    P(ax, x + bw / 2, y0 + bh - 0.92, what, 9.2, TXT, ha="center",
      avail=bw - 0.24, label=f"内容{i+1}", ls=1.8)
    ax.plot([x + 0.20, x + bw - 0.20], [y0 + 0.72, y0 + 0.72], color=PALE, lw=1.0)
    P(ax, x + bw / 2, y0 + 0.38, pain, 8.8,
      ACCENT if hi else GRAY, "bold" if hi else "normal", ha="center",
      avail=bw - 0.24, label=f"坑{i+1}")
    if i < 4:
        arrow(ax, x + bw + 0.03, y0 + bh / 2, x + bw + gap - 0.03, y0 + bh / 2,
              color=MIST, lw=1.8, ms=13)

# 高亮标注
hx = x0 + 3 * (bw + gap) + bw / 2
ax.annotate("", xy=(hx, y0 + bh + 0.10), xytext=(hx, y0 + bh + 0.48),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.8))
P(ax, hx, y0 + bh + 0.68, "本篇论文的位置", 10.5, ACCENT, "bold", ha="center",
  avail=2.4, label="高亮")

P(ax, W / 2, 1.32, "链路中的三个断点，就是过去几年论文的来源。",
  11, NAVY, "bold", ha="center", avail=W - 1.0, label="断点说明")
P(ax, W / 2, 0.82, "② 文本脏 → MedCLIP、MedKLIP      ③ 对齐粗 → GloRIA、CP-CLIP      ⑤ 只做 2D → MG-3D、Merlin",
  9.8, TXT, ha="center", avail=W - 0.8, label="断点列表")
P(ax, W / 2, 0.38, "CP-CLIP 不改前面的数据与编码，只在对齐环节做结构化拆分 —— 改动成本最低。",
  10, GRAY, ha="center", avail=W - 1.0, label="结论")

fig.savefig(f"{OUT}/p6_pipeline.png", dpi=200, facecolor=WHITE)
plt.close(fig)

print("=== 自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
