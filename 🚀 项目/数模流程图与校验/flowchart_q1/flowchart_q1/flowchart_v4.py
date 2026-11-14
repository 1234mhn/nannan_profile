#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题一 思路流程图 v4 —— 对齐 2024 华为杯优秀论文图表规范
规范: 图题图下方/五号10.5pt/宋体+TNR/不加粗/居中; 竖版; 菱形判断; 是-否左右分支
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

C_IN, C_PROC, C_DEC, C_OUT, C_END = '#E8EAF6', '#F5F5F5', '#FFF9E6', '#E8F5E9', '#ECEFF1'
EDGE, ARROW, TXT = '#37474F', '#546E7A', '#212121'
RED = '#B71C1C'

BW, BH = 6.2, 0.80          # 主块
DW, DH = 3.4, 1.10          # 菱形
SBW, SBH = 4.6, 0.80        # 右分支块
XS = 5.2                    # 主轴
GAP = 1.00                  # 主轴步距

MAIN = [                    # (type, text)
    ('in',   '数据预处理：去重、指标处理、6类语义分组'),
    ('proc', '组内中位数聚合分组得分'),
    ('proc', '熵权法计算质量得分（文本+领域）'),
    ('proc', '计算样本冲突强度'),
    ('dec',  '强冲突样本？'),
    ('proc', '输出质量评分、冲突标记'),
    ('proc', '配比归一化，划分数据集'),
    ('proc', '建立线性、二阶岭回归配比模型'),
    ('proc', '模型检验\n（独立集 + Bootstrap + 跨尺度）'),
    ('out',  '输出结果，限定模型适用边界'),
    ('end',  '结束'),
]
DI  = 4                      # 菱形索引
SY, SX = '计算稳健评分，标记冲突', 11.6   # 右分支（是）位置
NY, NX = '使用综合质量评分',       6.0    # 左分支（否）位置   —— 主轴左侧

fig, ax = plt.subplots(figsize=(10.6, 15.6), dpi=220)
ax.set_xlim(0, 16.8); ax.set_ylim(0, 15.6); ax.axis('off')

def box(x, y, w, h, text, fc, fs=11.5):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.07",
        edgecolor=EDGE, facecolor=fc, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4, linespacing=1.55)

def diamond(x, y, w, h, text, fs=11):
    ax.add_patch(Polygon([(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)],
        closed=True, edgecolor=EDGE, facecolor=C_DEC, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=TXT,
            fontproperties=prop, zorder=4)

def arr(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
        mutation_scale=13, color=ARROW, linewidth=1.2, zorder=2,
        shrinkA=1, shrinkB=1))

def elbow(x1, y1, x2, y2, lab=None, labx=None, laby=None):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
        mutation_scale=13, color=ARROW, linewidth=1.2, zorder=2,
        connectionstyle="angle,angleA=0,angleB=90,rad=8", shrinkA=2, shrinkB=2))
    if lab:
        ax.text(labx, laby, lab, ha='center', va='center', fontsize=10,
                color=RED, fontproperties=prop, zorder=6,
                bbox=dict(boxstyle='round,pad=0.14', fc='white', ec='none'))

# ---- 主轴 ----
YTOP = 14.90
ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i, (t, txt) in enumerate(MAIN):
    y = ys[i]
    if t == 'dec':
        diamond(XS, y, DW, DH, txt)
    else:
        box(XS, y, BW, BH, txt, {'in':C_IN,'proc':C_PROC,'out':C_OUT,'end':C_END}[t],
            fs=(11.0 if '\n' in txt else 11.5))

# 主轴竖直箭头：菱形前面正常连，菱形→(否)→输出质量评分，其余顺连
for i in range(len(MAIN)-1):
    if i == DI:          # 菱形出口走左右分支，不画竖直
        continue
    arr(XS, ys[i]-BH/2, XS, ys[i+1]+BH/2)

# ---- 菱形分支 ----
# 是 → 右
elbow(XS+DW/2-0.06, ys[DI], SX-SBW/2+0.06, ys[DI],
      '是', XS+DW/2+0.55, ys[DI]+0.30)
box(SX, ys[DI], SBW, SBH, SY, C_PROC, fs=11)
# 右分支 → 向左下汇合到"输出质量评分"节点右侧
arr(SX-SBW/2+0.06, ys[DI], SX-SBW/2+0.06, ys[DI+1]+0.0) if False else None
elbow(SX-SBW/2+0.06, ys[DI], XS+BW/2-0.06, ys[DI+1], None)
arr(SX, ys[DI]-SBH/2, SX, ys[DI+1]+0.30)   # 右分支向下
elbow(SX, ys[DI+1]+0.30, XS+BW/2-0.06, ys[DI+1], None)

# 否 → 左
elbow(XS-DW/2+0.06, ys[DI], NX+ (0), ys[DI], '否', XS-DW/2-0.55, ys[DI]+0.30)
box(NX, ys[DI], SBW, SBH, NY, C_PROC, fs=11)
arr(NX, ys[DI]-SBH/2, NX, ys[DI+1]+0.30)
elbow(NX, ys[DI+1]+0.30, XS-BW/2+0.06, ys[DI+1], None)

# 图题：图下方、五号10.5pt、宋体+TNR、不加粗、居中
ax.text(8.4, 0.42, '图 3.1  问题一数据处理与建模总体流程', ha='center', va='center',
        fontsize=10.5, color=TXT, fontproperties=prop)

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题一_v3_规范版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
print('OK ->', out)

# 自检几何
def rect(i):
    return (XS-BW/2, XS+BW/2, ys[i]-BH/2, ys[i]+BH/2)
print('--- 重叠自检 ---')
lb = (NX-SBW/2, NX+SBW/2); rb = (SX-SBW/2, SX+SBW/2)
print('左分支 x范围', lb, '主块 x范围', (XS-BW/2, XS+BW/2), '→ 间距', round((XS-BW/2)-lb[1],2))
print('右分支 x范围', rb, '→ 间距', round(rb[0]-(XS+BW/2),2))
print('左分支 y=', ys[DI], '右分支 y=', ys[DI], '主轴 y=', ys[DI])
