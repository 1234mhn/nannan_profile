"""图1 总体技术路线 —— 16cm x 7.5cm，横向流程主链（7 节点）。运行: python3 fig1_route.py"""
from matplotlib.patches import Rectangle
from figstyle import *

W, H = 16.0, 7.5
fig, ax = new_fig(W, H)

SUB = "#404040"
YC = 4.70          # 主链中心线

# (标题, 技术手段, 宽度, 数据形态)
nodes = [
    ("图像—报告\n数据", "MIMIC-CXR\nCheXpert\nNIH", 1.65, "图像 + 报告\n（原始数据）"),
    ("报告结构化\n解析", "大语言模型\n+ 提示模板\n+ 少样本示例", 1.95, "自由文本 →\n三级语义单元"),
    ("语义单元\n构建", "全局层\n器官层\n病灶层", 1.55, "三级层级结构"),
    ("区域级\n对比学习", "双编码器\n+ 软标签机制", 1.80, "(图像, 文本) →\n匹配分数"),
    ("匹配关系图\n推理", "图神经网络\n解剖邻近性\n病理共现性", 1.95, "匹配 → 关系图\n→ 更新表征"),
    ("层次化\n分类", "病灶→器官\n→全局层\n逐级预测", 1.95, "表征 → 疾病类别\n+ 回溯片段（输出）"),
    ("跨数据集\n验证", "跨数据集性能\n与语义层级\n衰减分析", 1.95, "模型 → 性能评估"),
]

MARGIN = 0.20
GAP = (W - 2 * MARGIN - sum(n[2] for n in nodes)) / (len(nodes) - 1)
xs, x = [], MARGIN
for n in nodes:
    xs.append(x)
    x += n[2] + GAP

# ---- 顶部阶段色带（仅作背景，无边线）----
LANE_Y0, LANE_Y1 = 2.95, 7.30
lanes = [(1, 2, "研究内容 2.1", "报告语义多粒度结构化解析", "#EAF0FA"),
         (3, 4, "研究内容 2.2", "区域级对比学习与匹配关系图", "#F5F0E8"),
         (5, 6, "研究内容 2.3", "层次化可回溯分类与跨数据集验证", "#F2F2F2")]
for a, b, t, s, col in lanes:
    lx0 = xs[a] - GAP * 0.42
    lx1 = xs[b] + nodes[b][2] + GAP * 0.42
    ax.add_patch(Rectangle((lx0, LANE_Y0), lx1 - lx0, LANE_Y1 - LANE_Y0, fc=col, ec="none", zorder=0))
    cx = (lx0 + lx1) / 2
    text(ax, cx, 6.95, t, size=8.5, weight="bold", color="#1F3864")
    text(ax, cx, 6.52, s, size=7, color=SUB)

# ---- 数据形态底栏 ----
PY0, PY1 = 0.78, 2.62
ax.add_patch(Rectangle((MARGIN, PY0), W - 2 * MARGIN, PY1 - PY0, fc="#F7F7F7", ec="none", zorder=0))
text(ax, W / 2, 1.07, "各步数据形态变化", size=7, color=GRAY)

# ---- 节点 ----
for (title, sub, w, form), x0 in zip(nodes, xs):
    n_sub = sub.count("\n") + 1
    h = 0.22 + 0.62 + 0.14 + 0.32 * n_sub + 0.16
    y0, y1 = YC - h / 2, YC + h / 2
    box(ax, x0, y0, w, h, lw=0.9, r=0.04)
    cx = x0 + w / 2
    text(ax, cx, y1 - 0.22 - 0.31, title, size=8, weight="bold")
    text(ax, cx, y0 + 0.16 + 0.16 * n_sub, sub, size=7, color=SUB)
    arrow(ax, [(cx, y0 - 0.03), (cx, PY1 + 0.02)], lw=0.6, head=0.15, ls=(0, (2.5, 2)), color=GRAY)
    text(ax, cx, 1.93, form, size=7)

# ---- 主链箭头 ----
for i in range(len(nodes) - 1):
    xa = xs[i] + nodes[i][2] + 0.03
    xb = xs[i + 1] - 0.03
    arrow(ax, [(xa, YC), (xb, YC)], color=BLUE, lw=1.8, head=0.24)

# ---- 图题 ----
text(ax, W / 2, 0.33, "图 1　总体技术路线", size=10, family=["Noto Serif CJK SC", "STIXGeneral"])

if __name__ == "__main__":
    audit(fig, ax)
    save(fig, "图1-总体技术路线")
