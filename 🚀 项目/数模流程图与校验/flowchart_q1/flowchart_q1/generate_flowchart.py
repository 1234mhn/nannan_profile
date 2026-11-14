#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术极简风流程图 —— 问题一数据处理与建模流程
参照：源图.png （问题一数据处理与建模流程）
使用 matplotlib 纯绘制，无外部依赖（除 matplotlib）。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm

# ---------- 字体：优先 Noto Sans CJK SC ----------
CJK_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
]
cjk_path = None
for p in CJK_CANDIDATES:
    try:
        fm.FontProperties(fname=p)
        cjk_path = p
        break
    except Exception:
        continue

BOLD_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
bold_path = None
for p in BOLD_CANDIDATES:
    try:
        fm.FontProperties(fname=p)
        bold_path = p
        break
    except Exception:
        continue

FP_TITLE = FontProperties(fname=bold_path, size=20)
FP_H1    = FontProperties(fname=bold_path, size=13.5)
FP_H2    = FontProperties(fname=bold_path, size=10.8)
FP_BODY  = FontProperties(fname=cjk_path, size=9.6)
FP_SMALL = FontProperties(fname=cjk_path, size=8.6)
FP_MONO  = FontProperties(fname=cjk_path, size=9.0)

# ---------- 配色（学术极简：低饱和、双色系） ----------
C_BG        = "#FFFFFF"
C_LINE      = "#2B2B2B"
C_SUBTLE    = "#8C8C8C"
C_FILL_A    = "#EDF2F7"   # 左通道（质量）浅蓝灰
C_FILL_B    = "#F5F1EA"   # 右通道（配比）浅米
C_FILL_OUT  = "#E8EEE6"   # 输出浅绿
C_ACCENT_A  = "#4A6C8C"   # 深蓝灰（质量）
C_ACCENT_B  = "#9A7B4F"   # 深米棕（配比）
C_ACCENT_O  = "#5C7A5C"   # 深绿（输出）

fig_w, fig_h = 22.0, 14.0
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=170)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.patch.set_facecolor(C_BG)


def rbox(x, y, w, h, fill, edge, lw=1.2, radius=0.9, alpha=1.0, z=2):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
        alpha=alpha, zorder=z,
    )
    ax.add_patch(p)
    return p


def txt(x, y, s, fp, color=C_LINE, ha="left", va="top", z=5, lh=1.5):
    return ax.text(x, y, s, fontproperties=fp, color=color,
                   ha=ha, va=va, zorder=z, linespacing=lh)


def arrow(x1, y1, x2, y2, color=C_SUBTLE, lw=1.3, style="-|>", z=3,
          rad=0.0, ls="-"):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=13,
        linewidth=lw, color=color, zorder=z,
        connectionstyle=f"arc3,rad={rad}",
        linestyle=ls, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(a)
    return a


# =========================================================
# 标题
# =========================================================
ax.text(50, 96.6, "问题一  数据处理与建模流程", fontproperties=FP_TITLE,
        color="#1F1F1F", ha="center", va="center", zorder=6)
ax.plot([6, 94], [94.4, 94.4], color=C_LINE, lw=1.4, zorder=3)

txt(6, 92.9, "质量评分、指标冲突识别 与 领域配比效应建模", FP_H2, color=C_ACCENT_A)
txt(94, 92.9, "子任务一 · 子任务二 · 子任务三", FP_SMALL, color=C_SUBTLE, ha="right")

# =========================================================
# 左通道：子任务一 + 子任务二
# =========================================================
LX, LW = 6.0, 40.5     # left column x, width
RX = 53.5              # right column x

# ---- 通道标题 ----
rbox(LX, 84.5, LW, 5.0, C_FILL_A, C_ACCENT_A, lw=1.4, radius=0.8)
txt(LX + 1.6, 88.0, "子任务一 · 子任务二", FP_H1, color=C_ACCENT_A, va="center")
txt(LX + 1.6, 85.9, "数据质量综合评价 与 指标冲突识别", FP_SMALL, color="#5A6773", va="center")

# ---- 输入 ----
rbox(LX, 77.5, LW, 5.2, "#FFFFFF", C_ACCENT_A, lw=1.0, radius=0.7)
txt(LX + 1.4, 81.6, "输入数据  A1—A3", FP_H2, color=C_ACCENT_A)
txt(LX + 1.4, 79.5, "272 505 条质量记录  ·  7 个领域  ·  22 项质量指标", FP_SMALL, color="#4A4A4A")

arrow(LX + LW / 2, 77.5, LX + LW / 2, 74.6, color=C_ACCENT_A, lw=1.2)

# ---- 指标预处理 ----
rbox(LX, 68.6, LW, 5.8, C_FILL_A, C_ACCENT_A, lw=1.0, radius=0.7, alpha=0.55)
txt(LX + 1.4, 73.6, "指标预处理", FP_H2, color=C_ACCENT_A)
txt(LX + 1.4, 71.6, "缺失值按领域中位数填补；重尾变量对数变换；", FP_SMALL, color="#3F3F3F")
txt(LX + 1.4, 69.7, "统一指标方向；全局 Min-Max 归一化得到  V(s,j)", FP_SMALL, color="#3F3F3F")

# 分叉到两列
arrow(LX + LW * 0.27, 68.6, LX + LW * 0.27, 65.8, color=C_SUBTLE)
arrow(LX + LW * 0.73, 68.6, LX + LW * 0.73, 65.8, color=C_SUBTLE)

CWA = LW * 0.46            # 左子列宽
CLX = LX                    # 左子列 x
CRX = LX + LW - CWA         # 右子列 x

# ---- 六类语义分组 ----
rbox(CLX, 60.4, CWA, 5.4, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.6)
txt(CLX + 1.0, 64.8, "六类语义分组", FP_H2, color="#333333")
txt(CLX + 1.0, 62.9, "教育与知识 · 语言与清洁 · 无广告", FP_SMALL, color="#555555")
txt(CLX + 1.0, 61.1, "参考域相似性 · 重复结构 · 文本形态", FP_SMALL, color="#555555")

# ---- 同域秩变换 ----
rbox(CRX, 60.4, CWA, 5.4, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.6)
txt(CRX + 1.0, 64.8, "同域秩变换", FP_H2, color="#333333")
txt(CRX + 1.0, 62.9, "计算同域百分位秩  R(s,j)", FP_SMALL, color="#555555")
txt(CRX + 1.0, 61.1, "消除指标量纲与分布差异", FP_SMALL, color="#555555")

arrow(CLX + CWA / 2, 60.4, CLX + CWA / 2, 57.4, color=C_SUBTLE)
arrow(CRX + CWA / 2, 60.4, CRX + CWA / 2, 57.4, color=C_SUBTLE)

# ---- 组内稳健聚合 ----
rbox(CLX, 51.9, CWA, 5.5, C_FILL_A, C_ACCENT_A, lw=1.0, radius=0.6, alpha=0.55)
txt(CLX + 1.0, 56.4, "组内稳健聚合", FP_H2, color=C_ACCENT_A)
txt(CLX + 1.0, 54.5, "组内取中位数", FP_SMALL, color="#3F3F3F")
txt(CLX + 1.0, 52.7, "G(s,g) = median{ V(s,j) }", FP_MONO, color="#2F3E4E")

# ---- 冲突强度识别 ----
rbox(CRX, 51.9, CWA, 5.5, C_FILL_A, C_ACCENT_A, lw=1.0, radius=0.6, alpha=0.55)
txt(CRX + 1.0, 56.4, "冲突强度识别", FP_H2, color=C_ACCENT_A)
txt(CRX + 1.0, 54.5, "c(s) = max R(s,j) − min R(s,j)", FP_MONO, color="#2F3E4E")
txt(CRX + 1.0, 52.7, "90% 分位阈值标记强冲突", FP_SMALL, color="#3F3F3F")

arrow(CLX + CWA / 2, 51.9, CLX + CWA / 2, 49.0, color=C_SUBTLE)
arrow(CRX + CWA / 2, 51.9, CRX + CWA / 2, 49.0, color=C_SUBTLE)

# ---- 熵权 ----
rbox(CLX, 43.4, CWA, 5.6, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.6)
txt(CLX + 1.0, 48.0, "熵权与综合评分", FP_H2, color="#333333")
txt(CLX + 1.0, 46.1, "计算六组熵权  w(g)", FP_SMALL, color="#555555")
txt(CLX + 1.0, 44.3, "S(s)=Σ w(g)G(s,g)；S(d)=mean S(s)", FP_MONO, color="#2F3E4E")

# ---- 冲突样本稳健复核 ----
rbox(CRX, 43.4, CWA, 5.6, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.6)
txt(CRX + 1.0, 48.0, "冲突样本稳健复核", FP_H2, color="#333333")
txt(CRX + 1.0, 46.1, "组权重均分至组内指标", FP_SMALL, color="#555555")
txt(CRX + 1.0, 44.3, "加权中位数 → 稳健秩评分  S*(s)", FP_SMALL, color="#555555")

arrow(CLX + CWA / 2, 43.4, CLX + CWA / 2, 40.5, color=C_SUBTLE)
arrow(CRX + CWA / 2, 43.4, CRX + CWA / 2, 40.5, color=C_SUBTLE)

# ---- 质量模块验证与输出 ----
rbox(LX, 34.4, LW, 6.1, C_FILL_OUT, C_ACCENT_O, lw=1.2, radius=0.7, alpha=0.7)
txt(LX + 1.4, 39.6, "质量模块验证与输出", FP_H2, color=C_ACCENT_O)
txt(LX + 1.4, 37.6, "同域同文档 id 抽样簇 Bootstrap 200 次，给出 95% 条件区间", FP_SMALL, color="#3F4C3F")
txt(LX + 1.4, 35.7, "输出  S(s)、S(d)、w(g)、冲突标记与 S*(s)；开展替代权重稳健性检验", FP_SMALL, color="#3F4C3F")

# ---- 左通道小节输出标签 ----
rbox(LX, 30.0, LW, 3.4, "#FFFFFF", C_ACCENT_O, lw=1.0, radius=0.6, alpha=0.85)
txt(LX + 1.4, 31.7, "输出：质量评分与不确定性  +  冲突样本稳健评价", FP_SMALL, color=C_ACCENT_O, va="center")

# =========================================================
# 右通道：子任务三
# =========================================================
rbox(RX, 84.5, LW, 5.0, C_FILL_B, C_ACCENT_B, lw=1.4, radius=0.8)
txt(RX + 1.6, 88.0, "子任务三", FP_H1, color=C_ACCENT_B, va="center")
txt(RX + 1.6, 85.9, "领域配比与验证 Loss 建模", FP_SMALL, color="#6B5C45", va="center")

# ---- 输入 ----
rbox(RX, 77.5, LW, 5.2, "#FFFFFF", C_ACCENT_B, lw=1.0, radius=0.7)
txt(RX + 1.4, 81.6, "输入数据  A4—A15", FP_H2, color=C_ACCENT_B)
txt(RX + 1.4, 79.5, "17 维领域配比向量 p  与  各验证域 Loss", FP_SMALL, color="#4A4A4A")

arrow(RX + LW / 2, 77.5, RX + LW / 2, 74.6, color=C_ACCENT_B, lw=1.2)

# ---- 数据分层 ----
rbox(RX, 68.2, LW, 6.2, C_FILL_B, C_ACCENT_B, lw=1.0, radius=0.7, alpha=0.55)
txt(RX + 1.4, 73.6, "数据分层与用途固定", FP_H2, color=C_ACCENT_B)
txt(RX + 1.4, 71.6, "A4—A5：1M 训练       A6—A11：实测独立检验", FP_SMALL, color="#3F3F3F")
txt(RX + 1.4, 69.7, "A12—A15：仅用于外推边界讨论", FP_SMALL, color="#3F3F3F")

arrow(RX + LW / 2, 68.2, RX + LW / 2, 65.3, color=C_ACCENT_B)

# ---- 单纯形约束 ----
rbox(RX, 59.2, LW, 6.0, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.7)
txt(RX + 1.4, 64.6, "单纯形约束与特征构造", FP_H2, color="#333333")
txt(RX + 1.4, 62.6, "p(i) ≥ 0，Σ p(i) = 1；逐行除以行和恢复严格约束", FP_SMALL, color="#555555")
txt(RX + 1.4, 60.7, "构造一次项 p(i) 与二阶项 p(i)p(j)，保持训练与验证口径一致", FP_SMALL, color="#555555")

arrow(RX + LW / 2, 59.2, RX + LW / 2, 56.3, color=C_SUBTLE)

# ---- 两个模型并列 ----
RWA = LW * 0.46
R1X = RX
R2X = RX + LW - RWA

rbox(R1X, 50.0, RWA, 6.1, C_FILL_B, C_ACCENT_B, lw=1.0, radius=0.6, alpha=0.7)
txt(R1X + 1.0, 55.2, "可解释基线", FP_H2, color=C_ACCENT_B)
txt(R1X + 1.0, 53.2, "和约束线性岭回归", FP_SMALL, color="#3F3F3F")
txt(R1X + 1.0, 51.3, "刻画参考配比附近的替代效应", FP_SMALL, color="#5A4F3D")

rbox(R2X, 50.0, RWA, 6.1, C_FILL_B, C_ACCENT_B, lw=1.0, radius=0.6, alpha=0.7)
txt(R2X + 1.0, 55.2, "组合效应模型", FP_H2, color=C_ACCENT_B)
txt(R2X + 1.0, 53.2, "二阶岭回归", FP_SMALL, color="#3F3F3F")
txt(R2X + 1.0, 51.3, "刻画弯曲效应与领域交互", FP_SMALL, color="#5A4F3D")

arrow(R1X + RWA / 2, 50.0, R1X + RWA / 2, 47.1, color=C_SUBTLE)
arrow(R2X + RWA / 2, 50.0, R2X + RWA / 2, 47.1, color=C_SUBTLE)

# ---- 训练与模型选择 ----
rbox(RX, 40.6, LW, 6.5, "#FFFFFF", C_SUBTLE, lw=1.0, radius=0.7)
txt(RX + 1.4, 46.4, "训练与模型选择", FP_H2, color="#333333")
txt(RX + 1.4, 44.4, "训练集内部五折交叉验证选择岭参数 λ", FP_SMALL, color="#555555")
txt(RX + 1.4, 42.5, "比较线性与二阶模型的 R²、RMSE 及配对 Bootstrap 差值区间", FP_SMALL, color="#555555")
txt(RX + 1.4, 40.9, "（L2 惩罚同时作用于一次项与二阶系数）", FP_SMALL, color=C_SUBTLE)

arrow(RX + LW / 2, 40.6, RX + LW / 2, 37.7, color=C_SUBTLE)

# ---- 独立验证与适用边界 ----
rbox(RX, 30.0, LW, 7.7, C_FILL_OUT, C_ACCENT_O, lw=1.2, radius=0.7, alpha=0.7)
txt(RX + 1.4, 36.6, "独立验证与适用边界", FP_H2, color=C_ACCENT_O)
txt(RX + 1.4, 34.6, "1M 同尺度检验二阶增益；1B 尺度检验跨尺度稳定性", FP_SMALL, color="#3F4C3F")
txt(RX + 1.4, 32.7, "输出局部配比模型、替代效应", FP_SMALL, color="#3F4C3F")
txt(RX + 1.4, 30.9, "及不可无条件外推的适用边界", FP_SMALL, color="#3F4C3F")

# =========================================================
# 底部：最终输出汇合
# =========================================================
arrow(LX + LW / 2, 30.0, 50, 26.4, color=C_ACCENT_O, lw=1.4, rad=-0.12)
arrow(RX + LW / 2, 30.0, 50, 26.4, color=C_ACCENT_O, lw=1.4, rad=0.12)

rbox(10, 19.4, 80, 6.6, C_FILL_OUT, C_ACCENT_O, lw=1.6, radius=0.9)
txt(50, 24.2, "问题一最终输出", FP_H1, color=C_ACCENT_O, ha="center", va="center")
txt(50, 21.4, "质量评分与不确定性   +   冲突样本稳健评价   +   局部领域配比效应及适用边界",
    FP_BODY, color="#334033", ha="center", va="center")

# =========================================================
# 图例
# =========================================================
lgy = 14.5
rbox(10, lgy, 5.2, 2.0, C_FILL_A, C_ACCENT_A, lw=1.0, radius=0.4)
txt(16.0, lgy + 1.0, "质量评价通道", FP_SMALL, color="#333333", va="center")
rbox(31, lgy, 5.2, 2.0, C_FILL_B, C_ACCENT_B, lw=1.0, radius=0.4)
txt(37.0, lgy + 1.0, "配比建模通道", FP_SMALL, color="#333333", va="center")
rbox(52, lgy, 5.2, 2.0, C_FILL_OUT, C_ACCENT_O, lw=1.0, radius=0.4)
txt(58.0, lgy + 1.0, "验证与输出", FP_SMALL, color="#333333", va="center")
txt(90, lgy + 1.0, "— 输入 / 处理 / 输出三段式，箭头表示数据流向 —",
    FP_SMALL, color=C_SUBTLE, ha="right", va="center")

# ---------- 保存 ----------
out_png = "/root/.openclaw/workspace/flowchart_q1/问题一_数据处理与建模流程_极简学术风.png"
out_pdf = "/root/.openclaw/workspace/flowchart_q1/问题一_数据处理与建模流程_极简学术风.pdf"
fig.savefig(out_png, dpi=200, bbox_inches="tight", facecolor=C_BG, pad_inches=0.25)
fig.savefig(out_pdf, bbox_inches="tight", facecolor=C_BG, pad_inches=0.25)
print("SAVED:", out_png)
print("SAVED:", out_pdf)
