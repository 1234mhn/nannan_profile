#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题四 思路流程图 —— 论文流程图标准格式（flowchart-paper-standard）
纯白底 / 全黑线条文字 / 竖版 / 无分支 / 无图题
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

BW, BH = 8.2, 0.86          # 主块
TX, TH = 3.4, 0.72          # 终端
XS = 8.0; GAP = 1.36; XMAX = 16.0

MAIN = [
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
    ('out',  '结果分析与结论'),
]
YTOP = 17.35

fig, ax = plt.subplots(figsize=(11.2, 18.3), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 18.3); ax.axis('off')

def box(x, y, w, h, text, fs=11.0, round_r=0.07, lw=1.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.65)

def terminal(x, y, text, w=None, fs=11.0):
    box(x, y, w or TX, TH, text, fs=fs, round_r=0.34, lw=1.3)

def seg(p1, p2, head=False):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
        mutation_scale=13, color=INK, linewidth=1.2, zorder=2,
        shrinkA=0, shrinkB=0))

ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    if t == 'term':
        terminal(XS, y, txt, w=BW, fs=11.0)
    else:
        box(XS, y, BW, BH, txt, fs=11.0)

for i in range(len(MAIN)-1):
    top = ys[i] - (BH/2 if MAIN[i][0] != 'term' else TH/2)
    bot = ys[i+1] + (BH/2 if MAIN[i+1][0] != 'term' else TH/2)
    seg((XS, top), (XS, bot), head=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题四_终版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white')
print('OK ->', out)
print('\n--- 自检 ---')
print('节点=%d 块宽=%.1f 净空=%.2f 顶余量=%.2f 底余量=%.2f' % (
    len(MAIN), BW, GAP-BH, 18.3-(ys[0]+BH/2), ys[-1]-BH/2))
