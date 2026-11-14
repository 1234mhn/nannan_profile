import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

OUT = "/root/.openclaw/workspace/figs"

for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    if os.path.exists(p):
        fm.fontManager.addfont(p)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

DARK = "#1f2a37"
TXT = "#2b3645"
GRAY = "#8b949e"
LGRAY = "#dfe3e8"
ORANGE = "#c87d14"
BLUE = "#3d6fa8"
GREEN = "#2e7d5b"
PURPLE = "#8a5cb8"
BRICK = "#c0642f"

# ---------- 文字宽度测量 ----------
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
    """文字实际宽度（英寸）"""
    _init()
    t = _A.text(0, 0, s, fontsize=fs, fontweight=weight)
    bb = t.get_window_extent(renderer=_R)
    t.remove()
    return bb.width / 200.0


WARN = []


def fit(s, fs, avail, weight="normal", label=""):
    """超宽就缩小字号，返回最终字号"""
    w = tw(s, fs, weight)
    if w <= avail:
        return fs
    new = fs * avail / w * 0.97
    WARN.append(f"{label or s[:18]}: {fs}->{new:.1f}pt ({w:.2f}in > {avail:.2f}in)")
    return new


def setup(w, h):
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec, lw=1.8, r=0.12, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, x1, y1, x2, y2, color=GRAY, lw=2.2, ms=18):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color, zorder=3))


def placed(ax, x, y, s, fs, color=TXT, weight="normal", ha="left", va="center",
           avail=None, label="", ls=1.5):
    if avail:
        fs = fit(s, fs, avail, weight, label)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, fontweight=weight,
            linespacing=ls)


# =========================================================
# Fig A：CLIP vs CP-CLIP（第4页）
# =========================================================
W, H = 15, 8.6
fig, ax = setup(W, H)

placed(ax, W / 2, H - 0.52, "从 CLIP 到 CP-CLIP：把「整张图对整份报告」拆成核心与外围",
       22, DARK, "bold", ha="center", avail=W - 1.0, label="主标题")
placed(ax, W / 2, H - 1.05, "同一个目标：图像与文本在同一空间靠近。差别是——对齐之前，拆不拆、怎么拆。",
       12.5, GRAY, ha="center", avail=W - 1.0, label="副标题")

# --------- 上半 CLIP ---------
top_y = H - 1.55
rbox(ax, 0.55, top_y - 2.5, W - 1.1, 2.5, "#f7f9fb", LGRAY, lw=1.0, r=0.16)
placed(ax, 0.85, top_y - 0.30, "CLIP", 17, DARK, "bold")
placed(ax, 2.0, top_y - 0.32, "原始做法：单点对齐", 12, GRAY)

rbox(ax, 1.0, top_y - 2.12, 2.2, 1.28, "white", BLUE, lw=2)
placed(ax, 2.1, top_y - 1.14, "整张图", 13, BLUE, "bold", ha="center")
placed(ax, 2.1, top_y - 1.50, "压成 1 个向量", 10, GRAY, ha="center")

rbox(ax, 1.0, top_y - 0.76, 2.2, 0.56, "white", GREEN, lw=2)
placed(ax, 2.1, top_y - 0.48, "整份报告 → 1 个向量", 11, GREEN, "bold",
       ha="center", avail=2.05, label="CLIP文本")

cx, cy = 5.5, top_y - 1.16
ax.plot([cx], [cy], marker="o", ms=22, color=ORANGE, zorder=4)
ax.plot([cx], [cy], marker="o", ms=9, color="white", zorder=5)
arrow(ax, 3.35, top_y - 1.14, cx - 0.28, cy, color=BLUE)
arrow(ax, 3.35, top_y - 0.48, cx - 0.22, cy - 0.14, color=GREEN)
placed(ax, cx, cy - 0.50, "只对齐一次", 10.5, ORANGE, "bold", ha="center")

placed(ax, 7.4, top_y - 0.82, "问题", 12, BRICK, "bold")
placed(ax, 8.15, top_y - 0.82, "一张胸片有心影、肺野、肋骨、病灶，报告也写了好几件事。",
       11.3, TXT, avail=W - 8.45, label="CLIP问题1")
placed(ax, 7.4, top_y - 1.55,
       "全部压成一个点后，「心影」与「心影的描述」、\n「病灶」与「病灶的描述」再也分不开 —— 语义被平均掉。",
       11.3, TXT, avail=W - 7.7, label="CLIP问题2", ls=1.6)

# --------- 下半 CP-CLIP ---------
rbox(ax, 0.55, 0.78, W - 1.1, 4.02, "#fffdf7", ORANGE, lw=1.5, r=0.16)
placed(ax, 0.85, 4.52, "CP-CLIP", 17, ORANGE, "bold")
placed(ax, 2.5, 4.50, "核心—外围分解：先拆成主次，再各自对齐", 12, GRAY)

# 图像分解
rbox(ax, 0.95, 2.52, 2.75, 1.72, "white", BLUE, lw=1.8)
placed(ax, 2.32, 4.00, "图像 → 核心 / 外围", 12.5, BLUE, "bold", ha="center",
       avail=2.6, label="图像分解标题")
ax.add_patch(Circle((1.72, 3.32), 0.30, fc=BLUE, ec="none", alpha=0.9, zorder=4))
placed(ax, 1.72, 3.32, "核心", 9.5, "white", ha="center")
ax.add_patch(Rectangle((2.32, 2.82), 1.10, 1.00, fc="none", ec=GRAY, lw=1.6, ls="--", zorder=4))
placed(ax, 2.87, 3.32, "外围", 9.5, GRAY, ha="center")
placed(ax, 2.32, 2.70, "病灶区域 / 周边背景组织", 9.3, GRAY, ha="center",
       avail=2.7, label="图像分解注")

# 文本分解
rbox(ax, 4.10, 2.52, 2.75, 1.72, "white", GREEN, lw=1.8)
placed(ax, 5.47, 4.00, "文本 → 核心 / 外围", 12.5, GREEN, "bold", ha="center",
       avail=2.6, label="文本分解标题")
placed(ax, 5.47, 3.55, "「右下肺见斑片状\n高密度影，边界模糊」", 10.5, TXT, ha="center",
       avail=2.6, label="报告示例", ls=1.6)
placed(ax, 5.47, 3.00, "核心：斑片状高密度影\n外围：右下肺、边界模糊", 9.3, GRAY, ha="center",
       avail=2.62, label="文本核心外围", ls=1.7)

# 对齐箭头
placed(ax, 7.25, 3.40, "分别\n对齐", 11, ORANGE, "bold", ha="center", ls=1.4)
arrow(ax, 6.90, 3.58, 7.72, 3.58, color=ORANGE, lw=2)
arrow(ax, 6.90, 3.18, 7.72, 3.18, color=ORANGE, lw=2, ms=14)

# 融合
rbox(ax, 7.88, 2.52, 2.45, 1.72, "white", ORANGE, lw=1.8)
placed(ax, 9.10, 4.00, "融合 → 统一特征", 12.5, ORANGE, "bold", ha="center",
       avail=2.3, label="融合标题")
ax.plot([9.10], [3.42], marker="o", ms=20, color=ORANGE, zorder=4)
ax.plot([9.10], [3.42], marker="o", ms=8, color="white", zorder=5)
placed(ax, 9.10, 3.02, "零样本分类 / 分割", 9.8, GRAY, ha="center", avail=2.3, label="下游")

# 为什么更好
rbox(ax, 10.60, 2.52, 3.85, 1.72, "white", GREEN, lw=1.6)
placed(ax, 10.80, 4.00, "为什么这样更好", 12, GREEN, "bold", avail=3.5, label="收益标题")
for i, s in enumerate([
    "①「心影」与「心影的描述」独立成对，语义不被平均",
    "② 体外、伪影等噪声归到外围，不污染病灶特征",
    "③ 核心 / 外围权重可学，模型能学「该看哪里」",
]):
    placed(ax, 10.80, 3.55 - i * 0.44, s, 9.8, TXT, avail=3.45, label=f"收益{i+1}")

placed(ax, W / 2, 0.34,
       "一句话：CLIP 是「整图 ↔ 整文」，CP-CLIP 是「病灶 ↔ 病灶描述」+「背景 ↔ 背景描述」。",
       12.5, DARK, "bold", ha="center", avail=W - 1.2, label="底注")

fig.savefig(f"{OUT}/cpclip_vs_clip.png", dpi=200, facecolor="white")
plt.close(fig)


# =========================================================
# Fig B：CLIP 完整链路（第6页）
# =========================================================
W, H = 15, 8.4
fig, ax = setup(W, H)

placed(ax, W / 2, H - 0.52, "CLIP 的完整链路 —— 以及 CP-CLIP 改在哪一环",
       22, DARK, "bold", ha="center", avail=W - 1.0, label="链路主标题")
placed(ax, W / 2, H - 1.02, "五段流水线：数据 → 文本 → 编码 → 对齐 → 下游。每一段都有自己的坑。",
       12.5, GRAY, ha="center", avail=W - 1.0, label="链路副标题")

stages = [
    ("①", "数据构建", "图像-报告配对\nMIMIC-CXR / OpenI", "配对≠真相关\n大量假阴性", BLUE, False),
    ("②", "文本处理", "清洗报告、抽实体\n医学术语规范化", "报告啰嗦、说法不一\n一图多病、一文多事", BLUE, False),
    ("③", "双塔编码", "图像编码器 + 文本编码器\nResNet / ViT / BERT", "整图压成 1 个向量\n粒度损失", BLUE, False),
    ("④", "对比对齐", "InfoNCE 损失\n拉近正样本、推远负样本", "CP-CLIP 改这里：\n核心/外围分别对齐再融合", ORANGE, True),
    ("⑤", "下游应用", "零样本分类、检索\n报告生成、分割", "泛化到未见类别", GREEN, False),
]

bw, bh, gap = 2.55, 2.50, 0.38
x0 = 0.60
y0 = H - 4.40
for i, (num, name, what, pain, col, hi) in enumerate(stages):
    x = x0 + i * (bw + gap)
    rbox(ax, x, y0, bw, bh, "#fffdf7" if hi else "white", col, lw=2.8 if hi else 1.8, r=0.14)
    rbox(ax, x, y0 + bh - 0.50, bw, 0.50, col, col, lw=0, r=0.14, z=3)
    rbox(ax, x, y0 + bh - 0.50, bw, 0.24, col, col, lw=0, r=0.0, z=3)
    placed(ax, x + 0.18, y0 + bh - 0.25, f"{num} {name}", 12.5, "white", "bold",
           avail=bw - 0.3, label=f"阶段名{i+1}")
    placed(ax, x + bw / 2, y0 + bh - 0.98, what, 10.0, TXT, ha="center",
           avail=bw - 0.3, label=f"阶段内容{i+1}", ls=1.7)
    ax.plot([x + 0.22, x + bw - 0.22], [y0 + 1.10, y0 + 1.10], color=LGRAY, lw=1.2)
    placed(ax, x + bw / 2, y0 + 0.58, pain, 9.4, BRICK, ha="center",
           avail=bw - 0.25, label=f"阶段坑{i+1}", ls=1.7)
    if i < len(stages) - 1:
        arrow(ax, x + bw + 0.04, y0 + bh / 2, x + bw + gap - 0.04, y0 + bh / 2,
              color=GRAY, lw=2.4, ms=20)

hx = x0 + 3 * (bw + gap) + bw / 2
ax.annotate("", xy=(hx, y0 + bh + 0.10), xytext=(hx, y0 + bh + 0.52),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.2))
placed(ax, hx, y0 + bh + 0.76, "本篇论文的位置", 12, ORANGE, "bold", ha="center")

by = 0.60
rbox(ax, 0.60, by, W - 1.20, 1.45, "#f7f9fb", LGRAY, lw=1.0, r=0.14)
placed(ax, 0.88, by + 1.14, "链路里的三个断点 = 过去几年论文的来源", 12.5, DARK, "bold",
       avail=W - 1.8, label="断点标题")
notes = [
    ("② 文本脏", "MedCLIP 解耦配对、MedKLIP 抽病名", GREEN),
    ("③ 对齐粗", "GloRIA 拆区域、CP-CLIP 拆核心外围", ORANGE),
    ("⑤ 只做 2D", "MG-3D 上 3D、Merlin 上千万级数据", PURPLE),
]
for i, (k, v, c) in enumerate(notes):
    xx = 0.88 + i * 4.72
    ax.plot([xx, xx + 0.18], [by + 0.66, by + 0.66], color=c, lw=3.2)
    placed(ax, xx + 0.30, by + 0.68, k, 11, c, "bold")
    placed(ax, xx + 0.30, by + 0.34, v, 9.5, TXT, avail=4.1, label=f"断点注{i+1}")

placed(ax, W / 2, 0.28,
       "CP-CLIP 不改前面的数据与编码，只在「对齐」这一环做结构化拆分 —— 改动成本最低的位置。",
       11.5, DARK, "bold", ha="center", avail=W - 1.2, label="链路底注")

fig.savefig(f"{OUT}/clip_pipeline.png", dpi=200, facecolor="white")
plt.close(fig)


# =========================================================
# Fig C：CP-CLIP 核心机制（第5页）
# =========================================================
W, H = 12.5, 8.6
fig, ax = setup(W, H)

placed(ax, W / 2, H - 0.52, "CP-CLIP 的核心机制：两级对齐 + 加权融合",
       21, DARK, "bold", ha="center", avail=W - 0.8, label="机制主标题")
placed(ax, W / 2, H - 1.02, "核心与外围各走一遍对齐，再用权重把两者合起来。",
       12, GRAY, ha="center", avail=W - 0.8, label="机制副标题")

# 输入
rbox(ax, 0.60, 5.95, 3.30, 0.95, "white", BLUE, lw=1.8)
placed(ax, 2.25, 6.62, "输入图像 X", 12.5, BLUE, "bold", ha="center", avail=3.0, label="输入图像")
placed(ax, 2.25, 6.22, "胸片 / CT / OCT", 9.8, GRAY, ha="center", avail=3.0, label="输入图像注")

rbox(ax, 8.60, 5.95, 3.30, 0.95, "white", GREEN, lw=1.8)
placed(ax, 10.25, 6.62, "输入文本 T", 12.5, GREEN, "bold", ha="center", avail=3.0, label="输入文本")
placed(ax, 10.25, 6.22, "放射学报告", 9.8, GRAY, ha="center", avail=3.0, label="输入文本注")

# 分解
rbox(ax, 0.60, 4.55, 1.55, 0.85, "#eef3f9", BLUE, lw=1.5)
placed(ax, 1.37, 5.20, "核心区域", 11.5, BLUE, "bold", ha="center", avail=1.4, label="核心区域")
placed(ax, 1.37, 4.82, "病灶 RoI", 9.5, GRAY, ha="center", avail=1.4, label="核心区域注")

rbox(ax, 2.40, 4.55, 1.55, 0.85, "#eef3f9", BLUE, lw=1.5)
placed(ax, 3.17, 5.20, "外围区域", 11.5, BLUE, "bold", ha="center", avail=1.4, label="外围区域")
placed(ax, 3.17, 4.82, "背景组织", 9.5, GRAY, ha="center", avail=1.4, label="外围区域注")

rbox(ax, 8.60, 4.55, 1.55, 0.85, "#eef6f1", GREEN, lw=1.5)
placed(ax, 9.37, 5.20, "核心语汇", 11.5, GREEN, "bold", ha="center", avail=1.4, label="核心语汇")
placed(ax, 9.37, 4.82, "病变描述", 9.5, GRAY, ha="center", avail=1.4, label="核心语汇注")

rbox(ax, 10.40, 4.55, 1.55, 0.85, "#eef6f1", GREEN, lw=1.5)
placed(ax, 11.17, 5.20, "外围语汇", 11.5, GREEN, "bold", ha="center", avail=1.4, label="外围语汇")
placed(ax, 11.17, 4.82, "位置 / 边界", 9.5, GRAY, ha="center", avail=1.4, label="外围语汇注")

arrow(ax, 1.90, 5.90, 1.42, 5.44, color=BLUE)
arrow(ax, 2.62, 5.90, 3.10, 5.44, color=BLUE)
arrow(ax, 9.90, 5.90, 9.42, 5.44, color=GREEN)
arrow(ax, 10.62, 5.90, 11.10, 5.44, color=GREEN)

# 编码
rbox(ax, 0.85, 3.12, 4.15, 0.92, "white", BLUE, lw=1.8)
placed(ax, 2.92, 3.78, "图像编码器  f_I", 11.5, BLUE, "bold", ha="center", avail=3.9, label="图像编码器")
placed(ax, 2.92, 3.40, "核心特征 z_c   |   外围特征 z_p", 9.6, GRAY, ha="center",
       avail=3.9, label="图像编码器注")

rbox(ax, 7.50, 3.12, 4.15, 0.92, "white", GREEN, lw=1.8)
placed(ax, 9.58, 3.78, "文本编码器  f_T", 11.5, GREEN, "bold", ha="center", avail=3.9, label="文本编码器")
placed(ax, 9.58, 3.40, "核心文本 t_c   |   外围文本 t_p", 9.6, GRAY, ha="center",
       avail=3.9, label="文本编码器注")

arrow(ax, 1.37, 4.48, 1.85, 4.06, color=BLUE)
arrow(ax, 3.17, 4.48, 3.85, 4.06, color=BLUE)
arrow(ax, 9.37, 4.48, 8.90, 4.06, color=GREEN)
arrow(ax, 11.17, 4.48, 10.50, 4.06, color=GREEN)

# 两级对齐
rbox(ax, 1.85, 1.82, 8.80, 0.98, "#fffdf7", ORANGE, lw=2.2)
placed(ax, 6.25, 2.54, "两级对比对齐   L = L_core + λ · L_periphery",
       12.5, ORANGE, "bold", ha="center", avail=8.4, label="对齐公式")
placed(ax, 6.25, 2.10, "z_c ↔ t_c 拉近（病灶对齐病灶）      z_p ↔ t_p 拉近（背景对齐背景）",
       9.8, TXT, ha="center", avail=8.4, label="对齐说明")

arrow(ax, 2.92, 3.06, 4.10, 2.84, color=BLUE)
arrow(ax, 9.58, 3.06, 8.40, 2.84, color=GREEN)

# 融合输出
rbox(ax, 3.55, 0.62, 5.40, 0.95, "#fffdf7", ORANGE, lw=2.0)
placed(ax, 6.25, 1.28, "加权融合   f = w_c · z_c + w_p · z_p",
       11.5, DARK, "bold", ha="center", avail=5.1, label="融合公式")
placed(ax, 6.25, 0.88, "→ 零样本分类 / 病灶分割 / 图文检索",
       9.6, GRAY, ha="center", avail=5.1, label="融合下游")
arrow(ax, 6.25, 1.76, 6.25, 1.62, color=ORANGE, lw=2.4)

placed(ax, 0.30, 2.30, "改动\n只在\n这一层", 10, ORANGE, "bold", ls=1.5)

fig.savefig(f"{OUT}/cpclip_mechanism.png", dpi=200, facecolor="white")
plt.close(fig)

print("=== 超宽自动缩放记录 ===")
for w_ in WARN:
    print(" -", w_)
print("done")
