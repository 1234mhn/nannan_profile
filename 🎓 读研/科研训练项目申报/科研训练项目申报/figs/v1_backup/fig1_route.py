"""图1 总体技术路线 —— 16cm x 8.8cm。运行: python3 fig1_route.py"""
from matplotlib.patches import Circle
from figstyle import *

W, H = 16.0, 8.8
fig, ax = new_fig(W, H)
BAND3 = "#E8F2FB"
TIMES = dict(family="STIXGeneral", style="italic")

# ---- 水平几何 (cm)：输入列 | 色带1(M1) | 色带2(M2,M3) | 色带3(M4,M5) | 输出列 ----
L = 0.15
IN_X, IN_W = L, 1.70
OUT_W = 2.00
G_IN, G_OUT, G_BAND, G_MOD, PAD = 0.50, 0.70, 0.42, 0.42, 0.06
MW = (W - 2 * L - IN_W - OUT_W - G_IN - G_OUT - 2 * G_BAND - 2 * G_MOD - 6 * PAD) / 5

B1X = IN_X + IN_W + G_IN
M1X = B1X + PAD
B2X = M1X + MW + PAD + G_BAND
M2X = B2X + PAD
M3X = M2X + MW + G_MOD
B3X = M3X + MW + PAD + G_BAND
M4X = B3X + PAD
M5X = M4X + MW + G_MOD
B3R = M5X + MW + PAD
OUT_X = B3R + G_OUT
assert abs(OUT_X + OUT_W - (W - L)) < 1e-6

# ---- 垂直几何 ----
BAND_Y0, BAND_Y1 = 0.62, 8.25
MY0, MY1 = 0.82, 6.55
MH = MY1 - MY0
SPINE = (MY0 + MY1) / 2
LANE = 7.05
INSET = 0.12
INNER = MW - 2 * INSET


def cx(x):
    return x + MW / 2


# ---- 三列分栏：小标题 + 虚线分隔 ----
for xs in (B1X - 0.12, B3R + 0.12):
    ax.plot([xs, xs], [BAND_Y0, 8.65], color=EDGE, lw=0.8, ls=(0, (4, 3)), zorder=1)
text(ax, IN_X + IN_W / 2, 8.50, "输入", size=9.5, color=ACCENT, weight="bold")
text(ax, (B1X + B3R) / 2, 8.50, "处理链路（五模块主链）", size=9.5, color=ACCENT, weight="bold")
text(ax, OUT_X + OUT_W / 2, 8.50, "输出", size=9.5, color=ACCENT, weight="bold")

# ---- 研究内容色带：整组包住 ----
bands = [(B1X, MW + 2 * PAD, PURPLE, "研究内容一", "（2.1）"),
         (B2X, 2 * MW + G_MOD + 2 * PAD, GREEN, "研究内容二", "（2.2）"),
         (B3X, 2 * MW + G_MOD + 2 * PAD, BAND3, "研究内容三", "（2.3）")]
for bx, bw, fc, t1, t2 in bands:
    box(ax, bx, BAND_Y0, bw, BAND_Y1 - BAND_Y0, fc, ec=EDGE, lw=1.0, r=0.15, z=0)
    text(ax, bx + bw / 2, 7.98, t1, size=8.5, color=ACCENT, weight="bold")
    text(ax, bx + bw / 2, 7.68, t2, size=7, color=ACCENT)


def module(num, x, title):
    box(ax, x, MY0, MW, MH, WHITE, ec=EDGE, lw=1.0, z=2)
    text(ax, cx(x), MY1 - 0.55, title, size=8.5, color=ACCENT, weight="bold")
    ax.add_patch(Circle((x, MY1), 0.17, fc=ACCENT, ec=WHITE, lw=0.8, zorder=6))
    text(ax, x, MY1, str(num), size=7, color=WHITE, weight="bold", z=7)


def sub(x, yc, h, lines, fc, size=6.5, ec=EDGE, ls="-", color=TEXT, sp=0.29):
    """模块内小框，lines 居中堆叠。"""
    box(ax, x + INSET, yc - h / 2, INNER, h, fc, lw=0.8, r=0.06, ls=ls, z=3)
    n = len(lines)
    for i, s in enumerate(lines):
        text(ax, cx(x), yc + (n - 1) * sp / 2 - i * sp, s, size=size, color=color)


def label(x, y, s, size=7, color=ACCENT, **kw):
    text(ax, cx(x), y, s, size=size, color=color, **kw)


# ================= 输入列 =================
IMG_H = 1.20
box(ax, IN_X, LANE - IMG_H / 2, IN_W, IMG_H, BLUE, lw=1.0, z=2)
text(ax, IN_X + IN_W / 2, LANE + 0.28, "胸部 X 线\n图像", size=8, weight="bold")
text(ax, IN_X + IN_W / 2, LANE - 0.38, "Chest X-ray", size=7, **TIMES)

REP_H = 4.20
box(ax, IN_X, SPINE - REP_H / 2, IN_W, REP_H, BLUE, lw=1.0, z=2)
text(ax, IN_X + IN_W / 2, SPINE + 1.15, "影像报告", size=8, weight="bold")
text(ax, IN_X + IN_W / 2, SPINE + 0.78, "（自由文本）", size=7)
text(ax, IN_X + IN_W / 2, SPINE - 0.55, "“There is a\nsmall left\npleural\neffusion...”", size=6.5, **TIMES)

# ================= M1 报告语义结构化解析 =================
module(1, M1X, "报告语义\n结构化解析")
for y, s in zip([5.35, 5.06, 4.77], ["大语言模型", "+ 提示模板", "+ 少样本示例"]):
    label(M1X, y, s, color=TEXT)
label(M1X, 4.25, "三级语义单元")
sub(M1X, 3.84, 0.34, ["全局层"], PURPLE, size=7)
sub(M1X, 3.38, 0.34, ["器官层"], PURPLE, size=7)
sub(M1X, 2.48, 1.10, ["病灶层", "征象·位置", "程度·性质"], PURPLE, size=6.5)
sub(M1X, 1.38, 0.72, ["模板化表述", "阴性意见过滤"], WHITE, ls=(0, (3, 2)))

# ================= M2 细粒度图文对齐 =================
module(2, M2X, "细粒度\n图文对齐")
for y, s in zip([5.35, 5.06, 4.77], ["双编码器", "区域级对比", "学习 + 软标签"]):
    label(M2X, y, s, color=TEXT)
sub(M2X, 4.10, 0.38, [r"视觉主干→$v_j$"], GREEN, size=6.5)
sub(M2X, 3.60, 0.38, [r"语义编码→$t_k$"], GREEN, size=6.5)
sub(M2X, 3.10, 0.38, [r"匹配分数 $s_{jk}$"], GREEN, size=6.5)
label(M2X, 2.30, "区域—语义", color=TEXT)
label(M2X, 2.01, "对比损失", color=TEXT)

# ================= M3 匹配关系图建模 =================
module(3, M3X, "匹配关系图\n建模")
label(M3X, 5.30, "图神经网络")
sub(M3X, 4.65, 0.40, [r"$G=(V,E)$"], GREEN, size=7.5)
label(M3X, 3.95, "节点")
label(M3X, 3.66, "局部匹配", color=TEXT)
label(M3X, 3.15, "边")
label(M3X, 2.86, "解剖邻近性", color=TEXT)
label(M3X, 2.57, "+ 病理共现性", color=TEXT)
sub(M3X, 1.55, 0.72, ["聚合更新", "局部表征"], GREEN)

# ================= M4 层次化分类与语义回溯 =================
module(4, M4X, "层次化分类\n与语义回溯")
label(M4X, 5.30, "逐级预测")
for i, s in enumerate(["病灶层", "器官层", "全局层"]):
    yy = 4.70 - 0.62 * i
    sub(M4X, yy, 0.36, [s], BAND3, size=7)
    if i < 2:
        arrow(ax, [(cx(M4X), yy - 0.18), (cx(M4X), yy - 0.44)], head=4, lw=1.0)
sub(M4X, 2.00, 0.72, ["预测可回溯到", "报告描述片段"], WHITE, ls=(0, (3, 2)))

# ================= M5 跨数据集验证 =================
module(5, M5X, "跨数据集\n验证")
for yy, name in [(4.55, "MIMIC-CXR"), (3.70, "CheXpert")]:
    sub(M5X, yy, 0.42, [name], BAND3, size=7)
sub(M5X, 2.60, 0.80, ["NIH", "ChestX-ray14"], BAND3, size=7, sp=0.34)
for t in ax.texts[-5:]:
    if t.get_text() in ("MIMIC-CXR", "CheXpert", "NIH", "ChestX-ray14"):
        t.set_fontfamily("STIXGeneral")

# ================= 输出列 =================
def out_box(yc, h):
    box(ax, OUT_X, yc - h / 2, OUT_W, h, BLUE, lw=1.0, z=2)


Y_TOP, Y_BOT = SPINE + 2.30, SPINE - 2.30
out_box(Y_TOP, 1.50)
text(ax, OUT_X + OUT_W / 2, Y_TOP, "疾病类别预测\n（多标签）", size=8, weight="bold")

out_box(SPINE, 2.30)
text(ax, OUT_X + OUT_W / 2, SPINE + 0.78, "可回溯的\n证据片段", size=8, weight="bold")
ax.add_patch(Rectangle((OUT_X + 0.15, SPINE - 0.62), OUT_W - 0.30, 0.34, fc=ACCENT, alpha=0.25, ec="none", zorder=4))
text(ax, OUT_X + OUT_W / 2, SPINE - 0.08, "There is a small", size=6.5, **TIMES)
text(ax, OUT_X + OUT_W / 2, SPINE - 0.45, "left pleural", size=6.5, **TIMES)
text(ax, OUT_X + OUT_W / 2, SPINE - 0.92, "高亮对应报告句子", size=6.5, color=ACCENT)

out_box(Y_BOT, 1.50)
text(ax, OUT_X + OUT_W / 2, Y_BOT, "跨数据集性能\n与语义层级\n衰减分析", size=8, weight="bold")

# ================= 箭头：主链 2pt，分支 1.2pt =================
MAIN = dict(lw=2.0, head=7)
spine_pairs = [(IN_X + IN_W, M1X), (M1X + MW, M2X), (M2X + MW, M3X),
               (M3X + MW, M4X), (M4X + MW, M5X)]
for a, b in spine_pairs:
    arrow(ax, [(a, SPINE), (b, SPINE)], **MAIN)

# 图像支路：自输入顶部越过 M1，自上而下进入 M2
arrow(ax, [(IN_X + IN_W, LANE), (cx(M2X), LANE), (cx(M2X), MY1 + 0.02)], lw=1.2, head=6)
text(ax, B1X + 0.95, LANE + 0.20, "图像支路", size=6.5, color=ACCENT)

# 输出：主链进入中间框，同时分叉到上下两框
XF = OUT_X - 0.32
arrow(ax, [(M5X + MW, SPINE), (OUT_X, SPINE)], **MAIN)
arrow(ax, [(XF, SPINE), (XF, Y_TOP), (OUT_X, Y_TOP)], lw=1.2, head=6)
arrow(ax, [(XF, SPINE), (XF, Y_BOT), (OUT_X, Y_BOT)], lw=1.2, head=6)

# ---- 图题 ----
text(ax, W / 2, 0.28, "图 1  总体技术路线", size=10.5, color=TEXT,
     family=["Noto Serif CJK SC", "DejaVu Serif"])

if __name__ == "__main__":
    audit(fig, ax)
    save(fig, "图1-总体技术路线")
