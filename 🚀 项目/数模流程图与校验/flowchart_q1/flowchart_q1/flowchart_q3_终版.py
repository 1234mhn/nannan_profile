#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题三 思路流程图 —— 论文流程图标准格式（flowchart-paper-standard）
纯白底 / 全黑线条文字 / 竖版 / 菱形判断 / 分支同高汇合 / 无图题
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE = 'white'
INK = '#000000'

BW, BH  = 6.0, 0.80         # 主块宽/高
DW, DH  = 4.2, 1.15         # 菱形（文字较长，加宽）
SW, SH  = 5.0, 0.92         # 分支块（两行文字，加高）
TX, TH  = 3.4, 0.72         # 终端
XS = 8.5; LX = 2.55; RX = 14.45
GAP = 1.46; XMAX = 17.0

MAIN = [
    ('term', '输入：目标函数\n问题二广义标度律 L(N, D, Q)'),
    ('proc', '成本与约束：训练 + 质量提升\n+ 长文注意力 ≤ 预算 C'),
    ('proc', '联合优化求解\n（SLSQP + 对数网格穷举 交叉验证）'),
    ('dec',  'Loss 曲面是否平坦？'),
    ('proc', 'KKT 条件解析与数值验证'),
    ('proc', '结构转移识别\n（PELT 变点 + 成分切换 + 活跃集跃迁）'),
    ('proc', '上下文长度与成本函数敏感性分析'),
    ('out',  '输出最优资源配置\n与结构性转移结论'),
    ('term', '结束'),
]
DI = 3      # 菱形索引
YTOP = 13.05

fig, ax = plt.subplots(figsize=(12.6, 14.0), dpi=220)
ax.set_xlim(0, XMAX); ax.set_ylim(0, 13.9); ax.axis('off')

def box(x, y, w, h, text, fs=11.0, round_r=0.07, lw=1.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.6)

def terminal(x, y, text, w=None, fs=11.0):
    box(x, y, w or TX, TH, text, fs=fs, round_r=0.34, lw=1.3)

def diamond(x, y, w, h, text, fs=11.0):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],
        closed=True, edgecolor=INK, facecolor=WHITE, linewidth=1.2, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4)

def seg(p1, p2, head=False):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
        mutation_scale=13, color=INK, linewidth=1.2, zorder=2,
        shrinkA=0, shrinkB=0))

def hlabel(x, y, text, ha='center'):
    ax.text(x, y, text, ha=ha, va='bottom', fontsize=10.5,
            color=INK, fontproperties=prop, zorder=6)

ys = [YTOP - i*GAP for i in range(len(MAIN))]
for i,(t,txt) in enumerate(MAIN):
    y = ys[i]
    if t == 'dec':
        diamond(XS, y, DW, DH, txt)
    elif t == 'term':
        terminal(XS, y, txt, w=(BW if '\n' in txt else TX), fs=11.0)
    else:
        box(XS, y, BW, BH, txt, fs=11.0)

for i in range(len(MAIN)-1):
    if i == DI: continue
    seg((XS, ys[i]-BH/2), (XS, ys[i+1]+BH/2), head=True)

yd = ys[DI]; NY = ys[DI+1]

# === 分支（与菱形同层）=== 左=否(陡峭) / 右=是(平坦)
box(LX, yd, SW, SH, '解唯一\n按 KKT 条件取最优', fs=10.5)
box(RX, yd, SW, SH, '多重近最优解\n改以吃满预算为准则取解', fs=10.5)

# 菱形 → 左（否）
seg((XS-DW/2, yd), (LX+SW/2, yd), head=True)
hlabel((XS-DW/2 + LX+SW/2)/2, yd+0.08, '否（陡峭）')
# 菱形 → 右（是）
seg((XS+DW/2, yd), (RX-SW/2, yd), head=True)
hlabel((XS+DW/2 + RX-SW/2)/2, yd+0.08, '是（平坦）')

# === 汇合：同高横线合并成一个交点，再下行 ===
midy = (yd - SH/2) - (yd - SH/2 - (NY + BH/2))/3
seg((LX, yd-SH/2), (LX, midy))
seg((LX, midy), (XS, midy))
seg((RX, yd-SH/2), (RX, midy))
seg((RX, midy), (XS, midy))
seg((XS, midy), (XS, NY+BH/2), head=True)

plt.subplots_adjust(left=0.01, right=0.99, top=0.995, bottom=0.005)
out = '/root/.openclaw/workspace/flowchart_q1/流程图_问题三_终版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white')
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white')
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white')
print('OK ->', out)

print('\n--- 几何自检 ---')
print('主块 x=[%.2f,%.2f] 左块 x=[%.2f,%.2f] 右块 x=[%.2f,%.2f]' % (
    XS-BW/2, XS+BW/2, LX-SW/2, LX+SW/2, RX-SW/2, RX+SW/2))
print('左间隙=%.2f  右间隙=%.2f  菱形宽=%.2f 左右分支间距=%.2f' % (
    (XS-BW/2)-(LX+SW/2), (RX-SW/2)-(XS+BW/2), DW, (RX-SW/2)-(LX+SW/2)))
print('分支块下沿=%.2f 下节点上沿=%.2f 汇合线=%.2f 汇合竖箭=%.2f' % (
    yd-SH/2, NY+BH/2, midy, midy-(NY+BH/2)))
print('顶部余量=%.2f 底部余量=%.2f' % (13.9-(ys[0]+BH/2), ys[-1]-TH/2))
