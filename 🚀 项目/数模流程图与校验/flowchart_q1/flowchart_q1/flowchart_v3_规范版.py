#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题一 思路流程图 —— 对齐 2024 华为杯优秀论文规范
规范依据：ref_papers_2024/图表格式规范清单.md
 - 图题在图下方，五号(10.5pt)，宋体+TNR，不加粗，居中
 - 竖版从上到下，流程块居中，宽度一致
 - 决策节点用菱形，"是/否"左右分支
 - 学术风：低饱和配色，边框细，箭头清晰
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

C_IN    = '#E8EAF6'   # 输入
C_PROC  = '#F5F5F5'   # 处理
C_DEC   = '#FFF9E6'   # 判断
C_OUT   = '#E8F5E9'   # 输出
C_END   = '#ECEFF1'   # 起止
EDGE    = '#37474F'
ARROW   = '#546E7A'
TXT     = '#212121'

# 纵向排布的节点： (类型, 文本, 备注)
STEPS = [
    ('in',   '数据预处理：去重、指标处理、6类语义分组', ''),
    ('proc', '组内中位数聚合分组得分', ''),
    ('proc', '熵权法计算质量得分（文本+领域）', ''),
    ('proc', '计算样本冲突强度', ''),
    ('dec',  '强冲突样本？', ''),
    ('proc', '计算稳健评分，标记冲突', 'BRANCH_YES'),
    ('proc', '使用综合质量评分',       'BRANCH_NO'),
    ('proc', '输出质量评分、冲突标记', ''),
    ('proc', '配比归一化，划分数据集', ''),
    ('proc', '建立线性、二阶岭回归配比模型', ''),
    ('proc', '模型检验\n（独立集 + Bootstrap + 跨尺度）', ''),
    ('out',  '输出结果，限定模型适用边界', ''),
    ('end',  '结束', ''),
]

BW, BH = 6.4, 0.82      # 主流程块宽高
DW, DH = 3.6, 1.15      # 菱形宽高
GAP    = 1.02           # 垂直步距
XS     = 5.0            # 主轴 x
BX     = 9.0            # 右分支 x

# 画布：竖版
n = len(STEPS)
fig_h = 2.2 + (n + 1) * GAP
fig, ax = plt.subplots(figsize=(9.2, fig_h), dpi=220)
ax.set_xlim(0, 12.6)
ytop = fig_h - 0.55
ax.set_ylim(0, fig_h)
ax.axis('off')

def box(x, y, w, h, text, fc, fs=11, bold=False, r=0.06):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={r}",
        edgecolor=EDGE, facecolor=fc, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal',
            color=TXT, fontproperties=prop, zorder=4, linespacing=1.5)

def diamond(x, y, w, h, text, fs=10.5):
    v = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    ax.add_patch(Polygon(v, closed=True, edgecolor=EDGE,
        facecolor=C_DEC, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            color=TXT, fontproperties=prop, zorder=4)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
        mutation_scale=13, color=ARROW, linewidth=1.2, zorder=2,
        shrinkA=1, shrinkB=1))

def elbow(x1, y1, x2, y2, label='', lx=None):
    """折线：先水平后垂直再水平到目标"""
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=13, color=ARROW, linewidth=1.2,
        connectionstyle="angle,angleA=0,angleB=90,rad=6", zorder=2,
        shrinkA=2, shrinkB=2))
    if label:
        ax.text(lx if lx else (x1+x2)/2, y1, label, ha='center', va='center',
                fontsize=9.5, color='#B71C1C', fontproperties=prop, zorder=5,
                bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))

ys = []
for i, (t, text, note) in enumerate(STEPS):
    y = ytop - i * GAP
    ys.append(y)
    if t == 'dec':
        diamond(XS, y, DW, DH, text)
    else:
        fc = {'in':C_IN, 'proc':C_PROC, 'out':C_OUT, 'end':C_END}[t]
        box(XS, y, BW, BH, text, fc,
            bold=(t == 'end'), fs=(10.5 if '\n' in text else 11))

# 主轴箭头（跳过菱形→分支的特殊处理）
di = next(i for i, s in enumerate(STEPS) if s[0] == 'dec')
for i in range(len(STEPS) - 1):
    if i == di:      # 菱形往下：由分支汇合后继续
        continue
    if i == di+2:    # 分支汇合点 -> 下一节点
        arrow(XS, ys[i]-BH/2, XS, ys[i+1]+BH/2)
        continue
    if i == di+1:
        continue
    arrow(XS, ys[i]-BH/2, XS, ys[i+1]+BH/2)

# 菱形 → 右分支（是）
dy = ys[di]; yy = ys[di+1]
elbow(XS+DW/2-0.08, dy, BX-BW/2+0.05, yy, '是', lx=(XS+DW/2+BX-BW/2)/2)
box(BX, yy, BW*0.72, BH, STEPS[di+1][1], C_PROC, fs=10.5)

# 菱形 → 直下（否）到 综合质量评分
yn = ys[di+2]
arrow(XS, dy-DH/2, XS, yn+BH/2)
ax.text(XS+0.16, (dy-DH/2+yn+BH/2)/2, '否', ha='left', va='center',
        fontsize=9.5, color='#B71C1C', fontproperties=prop, zorder=5,
        bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))

# 右分支 → 汇合到 输出质量评分节点
elbow(BX-BW*0.72/2+0.05, yy, XS+BW/2-0.05, ys[di+3], '', )
arrow(BX, yy-BH/2, BX, ys[di+3]+0.42)
elbow(BX, ys[di+3]+0.42, XS+BW/2-0.05, ys[di+3])

# 图题（图下方，五号=10.5pt，不加粗，居中）—— 规范 1.1/1.3
ax.text(6.3, 0.42, '图 3.1  问题一数据处理与建模总体流程',
        ha='center', va='center', fontsize=10.5,
        color=TEXT if False else TXT, fontproperties=prop)

plt.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.02)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题一_v3_规范版'
plt.savefig(out + '.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out + '.pdf', bbox_inches='tight', facecolor='white')
print('OK ->', out + '.png')
