"""图 1 本项目主要研究内容（三列式：研究问题 ⇒ 研究内容 → 预期产出；底部 2.4 横条）。16cm x 8cm。"""
from figstyle import new_fig, box, text, dbl_arrow, arrow, audit, save, INK, GRAY, WHITE

plt_font = ["Noto Serif CJK SC", "STIXGeneral"]
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = plt_font

BLUE, MID_FC, MID_EC, MID_TX, RED = "#2F5597", "#EAF0FA", "#9DB3D8", "#1F3864", "#C00000"

fig, ax = new_fig(16, 8)

LX, LW = 0.3, 3.4
MX, MW = 4.5, 7.5
RX, RW = 12.5, 3.2
ROW_H, GAP, TOP = 1.7, 0.18, 7.4

for x, w, s in ((LX, LW, "研究问题"), (MX, MW, "研究内容"), (RX, RW, "预期产出")):
    text(ax, x + w / 2, 7.68, s, size=9, weight="bold")

problems = [("问题一", "报告语义冗余、\n粒度失配"),
            ("问题二", "局部匹配关系\n未被显式建模"),
            ("问题三", "分类依据\n不可追溯")]
contents = [("研究内容 2.1", "基于大语言模型的报告语义多粒度结构化解析",
             "大语言模型 + 提示工程 + 少样本示例\n模板过滤 / 阴性降权 / 术语归一化"),
            ("研究内容 2.2", "细粒度图文对齐与匹配关系图建模",
             "双编码器 + 区域级对比学习 + 软标签\n关系图 G=(V,E)，边 = 解剖邻近性 + 病理共现性"),
            ("研究内容 2.3", "层次化分类与语义回溯",
             "病灶层 → 器官层 → 全局层 逐级预测\n注意力回溯到报告描述片段")]
outputs = [("三级语义单元", "全局层 / 器官层 / 病灶层"),
           ("病灶级匹配表征", "相似征象可消歧"),
           ("可回溯的\n疾病类别预测", "")]

for i in range(3):
    y = TOP - ROW_H * (i + 1) - GAP * i
    c = y + ROW_H / 2

    box(ax, LX, y, LW, ROW_H, fc=WHITE, ec=GRAY, lw=0.6)
    text(ax, LX + LW / 2, c + 0.42, problems[i][0], size=8.5, color=RED, weight="bold")
    text(ax, LX + LW / 2, c - 0.20, problems[i][1], size=8.5, linespacing=1.4)

    box(ax, MX, y, MW, ROW_H, fc=MID_FC, ec=MID_EC, lw=0.9)
    t, name, detail = contents[i]
    text(ax, MX + MW / 2, c + 0.55, t, size=9, color=MID_TX, weight="bold")
    text(ax, MX + MW / 2, c + 0.19, name, size=8.5, color=MID_TX)
    text(ax, MX + MW / 2, c - 0.36, detail, size=7.5, color=MID_TX, linespacing=1.5)

    box(ax, RX, y, RW, ROW_H, fc=WHITE, ec=GRAY, lw=0.6)
    main, sub = outputs[i]
    if sub:
        text(ax, RX + RW / 2, c + 0.25, main, size=8.5, weight="bold")
        text(ax, RX + RW / 2, c - 0.30, sub, size=7.5)
    else:
        text(ax, RX + RW / 2, c, main, size=8.5, weight="bold", linespacing=1.4)

    dbl_arrow(ax, LX + LW + 0.08, MX - 0.08, c, gap=0.10, lw=1.5, color=BLUE)
    arrow(ax, [(MX + MW + 0.08, c), (RX - 0.08, c)], color=BLUE, lw=0.8, head=0.2)

box(ax, LX, 0.75, RX + RW - LX, 0.85, fc=MID_FC, ec=MID_EC, lw=0.9)
text(ax, 8.0, 1.35, "研究内容 2.4　跨数据集泛化验证（贯穿全程）", size=9, color=MID_TX, weight="bold")
text(ax, 8.0, 1.00, "内部测试 + 外部测试，分析性能衰减在语义层级中的分布", size=7.5, color=MID_TX)

text(ax, 8.0, 0.30, "图 1  本项目主要研究内容", size=9)

audit(fig, ax)
save(fig, "图1-本项目主要研究内容")
