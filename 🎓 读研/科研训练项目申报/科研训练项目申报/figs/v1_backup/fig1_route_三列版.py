"""图1 总体技术路线 —— 16cm x 8cm，三列式（挑战 ⇒ 研究内容 → 预期效果）。运行: python3 fig1_route.py"""
from matplotlib.patches import Rectangle
from figstyle import *

W, H = 16.0, 8.0
fig, ax = new_fig(W, H)

LX, LW_ = 0.30, 4.70
MX, MW_ = 5.85, 5.00
RX, RW_ = 11.40, 4.30
TOP, RH, STEP = 7.20, 1.50, 1.80
rows = [(TOP - i * STEP - RH, TOP - i * STEP) for i in range(3)]   # (y0, y1)
yc = [(a + b) / 2 for a, b in rows]

# ---- 列标题 ----
for x, w, s in [(LX, LW_, "挑　战"), (MX, MW_, "研究内容"), (RX, RW_, "预期效果")]:
    text(ax, x + w / 2, 7.62, s, size=9, weight="bold")
    line(ax, [(x, 7.40), (x + w, 7.40)], color=GRAY, lw=0.5)

# ---- 左列：挑战（白底细黑框，暗红标题带下划线）----
challenge = [("挑战一", "报告语义冗余、\n粒度失配"),
             ("挑战二", "局部匹配关系\n未被显式建模"),
             ("挑战三", "分类依据不可回溯、\n跨数据集性能衰减")]
for (y0, y1), (t, s) in zip(rows, challenge):
    box(ax, LX, y0, LW_, RH)
    text(ax, LX + LW_ / 2, y1 - 0.36, t, size=8.5, color=RED, weight="bold")
    line(ax, [(LX + LW_ / 2 - 0.55, y1 - 0.58), (LX + LW_ / 2 + 0.55, y1 - 0.58)], color=RED, lw=0.6)
    text(ax, LX + LW_ / 2, y0 + 0.50, s, size=8)

# ---- 中列：研究内容（实心深蓝）----
content = [("研究内容 2.1", "基于大语言模型的报告语义\n多粒度结构化解析"),
           ("研究内容 2.2", "基于区域级对比学习与\n匹配关系图的细粒度对齐"),
           ("研究内容 2.3", "基于层次化分类头的可回溯分类\n与跨数据集验证")]
for (y0, y1), (t, s) in zip(rows, content):
    box(ax, MX, y0, MW_, RH, fc="#EAF0FA", ec="#9DB3D8", lw=0.8)
    text(ax, MX + MW_ / 2, y1 - 0.34, t, size=8, color="#6B7FA8", weight="bold")
    text(ax, MX + MW_ / 2, y0 + 0.50, s, size=8.5, color="#1F3864", weight="bold")

# ---- 左 ⇒ 中：双线粗箭头；中 → 右：细箭头 ----
for y in yc:
    dbl_arrow(ax, LX + LW_ + 0.10, MX - 0.10, y)
    arrow(ax, [(MX + MW_ + 0.05, y), (RX - 0.05, y)], lw=0.8, head=0.2)

# ---- 右列：一个整框，虚线分条，小字左对齐 ----
box(ax, RX, rows[2][0], RW_, rows[0][1] - rows[2][0])
for ya, yb in [(rows[0][0], rows[1][1]), (rows[1][0], rows[2][1])]:
    line(ax, [(RX, (ya + yb) / 2), (RX + RW_, (ya + yb) / 2)], color=GRAY, lw=0.5, ls=(0, (3, 2)))
effects = ["语义单元抽取稳定，\n模板与阴性表述可控",
           "病灶级图文对应显式建模，\n相似征象可消歧",
           "预测可回溯到报告片段，\n跨数据集性能衰减可分析"]
for y, s, n in zip(yc, effects, ["(1)", "(2)", "(3)"]):
    text(ax, RX + 0.20, y, n, size=7.5, color=BLUE, ha="left", weight="bold")
    text(ax, RX + 0.75, y, s, size=8, ha="left")

# ---- 底部跨度条：验证模态 ----
BY0, BY1 = 0.78, 1.50
ax.add_patch(Rectangle((LX, BY0), 15.4, BY1 - BY0, fc=PALE, ec=GRAY, lw=0.5, zorder=1))
text(ax, LX + 0.25, (BY0 + BY1) / 2, "验证模态", size=8.5, weight="bold", ha="left")
text(ax, 3.55, (BY0 + BY1) / 2, "胸部 X 线（主要验证）", size=8.5, ha="left", color=BLUE, weight="bold")
arrow(ax, [(6.75, (BY0 + BY1) / 2), (7.60, (BY0 + BY1) / 2)], lw=0.8, head=0.2)
ax.add_patch(Rectangle((7.85, BY0 + 0.12), 5.65, BY1 - BY0 - 0.24, fc=WHITE, ec=INK, lw=0.6, ls=(0, (3, 2)), zorder=2))
text(ax, 7.85 + 5.65 / 2, (BY0 + BY1) / 2, "CT / 病理（条件允许时扩展）", size=8, color="#404040")
arrow(ax, [(MX + MW_ / 2, BY1 + 0.02), (MX + MW_ / 2, rows[2][0] - 0.02)], lw=0.6, head=0.18, ls=(0, (3, 2)), color=GRAY)

# ---- 图题 ----
text(ax, W / 2, 0.30, "图 1　总体技术路线", size=10, family=["Noto Serif CJK SC", "STIXGeneral"])

if __name__ == "__main__":
    audit(fig, ax)
    save(fig, "图1-总体技术路线")
