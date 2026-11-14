#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题四 思路流程图（双栏蛇形版）—— 论文流程图标准格式
纯白底 / 全黑线条文字 / 双栏蛇形走位 / 无图题
走位：左列 1→6 向下，底部横跳到右列，右列 7→12 向下
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE = 'white'
INK = '#000000'

BW, BH = 5.6, 0.90          # 主块宽/高
LX, RX = 4.4, 12.4          # 左/右栏中心
ROW_GAP = 1.42              # 同行距
YTOP = 9.00

NODES = [
    ('term', '输入：六项 Benchmark 数据'),
    ('proc', '稳健归一化处理'),
    ('proc', '等权汇总，得到综合能力分数'),
    ('proc', '匹配训练算力与训练数据量'),
    ('proc', '构建模型家族面板'),
    ('proc', '建立面板回归模型'),
    ('proc', '分解规模投入贡献与非规模技术贡献'),
    ('proc', '采用 Shapley 方法进行贡献测算'),
    ('proc', '设定算力增速放缓情景'),
    ('proc', '预测未来能力前沿'),
    ('proc', '通过 Bootstrap 和滚动回测检验可靠性'),
    ('term', '得到结果分析与结论'),
]
HALF = 6      # 左列前 6 个

fig, ax = plt.subplots(figsize=(15.4, 10.6), dpi=220)
ax.set_xlim(0, 16.8); ax.set_ylim(0, 10.6); ax.axis('off')

def box(x, y, w, h, text, fs=11.0, round_r=0.07, lw=1.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.5)

def terminal(x, y, text, fs=10.5):
    box(x, y, BW, BH, text, fs=fs, round_r=0.36, lw=1.3)

def seg(p1, p2, head=False):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
        mutation_scale=13, color=INK, linewidth=1.2, zorder=2,
        shrinkA=0, shrinkB=0))

# 计算坐标
pos = {}
for i in range(len(NODES)):
    if i < HALF:
        pos[i] = (LX, YTOP - i*ROW_GAP)
    else:
        pos[i] = (RX, YTOP - (i-HALF)*ROW_GAP)

for i,(t,txt) in enumerate(NODES):
    x, y = pos[i]
    if t == 'term':
        terminal(x, y, txt, fs=(10.5 if len(txt) > 9 else 11.0))
    else:
        box(x, y, BW, BH, txt, fs=11.0)

# 箭头：左列向下
for i in range(HALF-1):
    x, y = pos[i]
    ax.add_patch(FancyArrowPatch((x, y-BH/2), (x, y-ROW_GAP+BH/2),
        arrowstyle='-|>', mutation_scale=13, color=INK, linewidth=1.2, zorder=2))
# 横跳：左列底框右侧 → 右行 → 上折 → 右列顶框（折线走位，减少底部留白）
xL, yL = pos[HALF-1]; xR, yR = pos[HALF]
jumpY = yL - BH/2 - 0.34          # 横跳线：紧贴左列底框下方
ax.add_patch(FancyArrowPatch((xL, yL-BH/2), (xL, jumpY), arrowstyle='-',
    mutation_scale=13, color=INK, linewidth=1.2, zorder=2))
ax.add_patch(FancyArrowPatch((xL, jumpY), (xR, jumpY), arrowstyle='-',
    mutation_scale=13, color=INK, linewidth=1.2, zorder=2))
ax.add_patch(FancyArrowPatch((xR, jumpY), (xR, yR-BH/2), arrowstyle='-|>',
    mutation_scale=13, color=INK, linewidth=1.2, zorder=2))
# 右列向下
for i in range(HALF, len(NODES)-1):
    x, y = pos[i]
    ax.add_patch(FancyArrowPatch((x, y-BH/2), (x, y-ROW_GAP+BH/2),
        arrowstyle='-|>', mutation_scale=13, color=INK, linewidth=1.2, zorder=2))

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题四_双栏版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white')
print('OK ->', out)

# 自检
print('\n--- 自检 ---')
print('左列 x=%.1f 右列 x=%.1f 间距=%.2f' % (LX, RX, RX-LX-BW))
print('左列顶 y=%.2f 底 y=%.2f | 右列顶 y=%.2f 底 y=%.2f' % (
    pos[0][1], pos[HALF-1][1], pos[HALF][1], pos[len(NODES)-1][1]))
print('横向跳线 y=%.2f' % jumpY)
print('顶部余量=%.2f 底部余量=%.2f' % (10.6-(pos[0][1]+BH/2), jumpY-0.0))
