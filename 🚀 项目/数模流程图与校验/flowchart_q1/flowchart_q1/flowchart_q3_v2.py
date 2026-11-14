#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题三 思路流程图（v2 · 线性版）—— 论文流程图标准格式
纯白底 / 全黑线条文字 / 竖版 / 无判断分支 / 无图题
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
XS = 8.0; GAP = 1.38; XMAX = 16.0

MAIN = [
    ('term', '输入：问题二广义标度律\nL_hat(N_B, D_B, Q; p_star)'),
    ('proc', '成本约束：\nC_train + C_quality + C_attn ≤ C'),
    ('proc', '联合优化求解：\nSLSQP 多初值 + 对数网格交叉验证'),
    ('proc', '最优解稳定性检验'),
    ('proc', 'KKT 条件解析与数值验证'),
    ('proc', '结构转移识别：\nPELT 变点 + 成本份额变化 + 活跃集跃迁'),
    ('proc', '上下文长度与成本函数敏感性分析'),
    ('out',  '输出：\n最优资源配置与结构性转移结论'),
    ('term', '结束'),
]
YTOP = 13.05

fig, ax = plt.subplots(figsize=(11.2, 13.9), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 13.9); ax.axis('off')

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
        terminal(XS, y, txt, w=(BW if '\n' in txt else TX), fs=11.0)
    else:
        box(XS, y, BW, BH, txt, fs=11.0)

for i in range(len(MAIN)-1):
    top = ys[i] - (BH/2 if MAIN[i][0] != 'term' else TH/2)
    bot = ys[i+1] + (BH/2 if MAIN[i+1][0] != 'term' else TH/2)
    seg((XS, top), (XS, bot), head=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题三_终版v2'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white')
print('OK ->', out)

print('\n--- 自检 ---')
print('节点数=%d 主轴 x=%.1f 块宽=%.2f' % (len(MAIN), XS, BW))
print('键间净空=%.2f' % (GAP - BH))
print('顶部余量=%.2f 底部余量=%.2f' % (13.9-(ys[0]+TH/2), ys[-1]-TH/2))
