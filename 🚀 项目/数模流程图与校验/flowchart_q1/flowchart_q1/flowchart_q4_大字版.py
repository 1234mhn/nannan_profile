#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题四 思路流程图（两栏蛇形 · 大字版）—— 论文流程图标准格式
白底 / 全黑 / 粗体 / 大字 / 两栏蛇形（左栏1-6下，横跳，右栏7-12下）/ 无图题
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE='white'; INK='#000000'
BW, BH = 7.4, 1.30           # 主块（大框大字）
TH = 1.20                    # 终端
ROW_GAP = 1.90               # 行距
COL_GAP = 2.30               # 栏间净空
X0 = 4.60                    # 第1栏中心
YTOP = 11.60
LW, FS, ARROW_LW, MS = 3.0, 14.5, 3.0, 23

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
PER, NC = 6, 2
COL_STEP = BW + COL_GAP
CX = X0 + (NC-1)*COL_STEP + BW/2 + 0.7
CY = YTOP + BH/2 + 0.6

fig, ax = plt.subplots(figsize=(CX*0.95, CY*0.95), dpi=220)
ax.set_xlim(0, CX); ax.set_ylim(0, CY); ax.axis('off')

def hh(t): return TH/2 if t=='term' else BH/2

def box(x, y, w, h, text, fs=FS, round_r=0.07, lw=LW):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.5)

def terminal(x, y, text, fs=FS):
    box(x, y, BW, TH, text, fs=fs, round_r=0.30, lw=LW)

def arrow(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=MS,
        color=INK, linewidth=ARROW_LW, zorder=2, shrinkA=0, shrinkB=0,
        joinstyle='miter', capstyle='butt'))

def line(p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-', mutation_scale=1,
        color=INK, linewidth=ARROW_LW, zorder=2, shrinkA=0, shrinkB=0,
        joinstyle='miter', capstyle='butt'))

pos = {i: (X0 + (i//PER)*COL_STEP, YTOP - (i%PER)*ROW_GAP) for i in range(len(NODES))}
for i,(t,txt) in enumerate(NODES):
    x,y = pos[i]
    terminal(x,y,txt) if t=='term' else box(x,y,BW,BH,txt)

boxes=[(pos[i][0]-BW/2, pos[i][1]-hh(NODES[i][0]),
        pos[i][0]+BW/2, pos[i][1]+hh(NODES[i][0])) for i in range(len(NODES))]
def hits(p1,p2,pad=0.03):
    (x1,y1),(x2,y2)=p1,p2; bad=[]
    for k,(bx1,by1,bx2,by2) in enumerate(boxes):
        bx1+=pad; by1+=pad; bx2-=pad; by2-=pad
        for t in [j/40 for j in range(41)]:
            x=x1+(x2-x1)*t; y=y1+(y2-y1)*t
            if bx1<x<bx2 and by1<y<by2: bad.append(k); break
    return bad

problems=[]
# 栏内竖箭
for i in range(len(NODES)-1):
    if (i+1)%PER==0: continue
    x,y=pos[i]
    arrow((x, y-hh(NODES[i][0])), (x, pos[i+1][1]+hh(NODES[i+1][0])))
# 横跳走栏间通道
for c in range(NC-1):
    iL=c*PER+PER-1; iR=(c+1)*PER
    xL,yL=pos[iL]; xR,yR=pos[iR]
    yL_bot=yL-hh(NODES[iL][0]); yR_top=yR+hh(NODES[iR][0])
    xch = xL+BW/2 + COL_GAP/2
    jumpY = yL_bot - 0.40
    for p in [((xL,yL_bot),(xL,jumpY)),((xL,jumpY),(xch,jumpY)),
              ((xch,jumpY),(xch,yR_top+0.55)),((xch,yR_top+0.55),(xR,yR_top+0.55))]:
        for k in hits(*p): problems.append('跳线%d穿框%d'%(c,k))
        line(*p)
    pa=((xR,yR_top+0.55),(xR,yR_top))
    for k in hits(*pa): problems.append('跳线%d箭头穿框%d'%(c,k))
    arrow(*pa)

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
out='/root/.openclaw/workspace/flowchart_q1/流程图_问题四_大字版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white', pad_inches=0.05)
print('OK ->', out)
print('\n--- 自检 ---')
print('几何断言:', '全部通过 ✓' if not problems else problems)
print('框 %.1fx%.2f 行距%.2f 栏间%.2f 两栏 每栏6个' % (BW,BH,ROW_GAP,COL_GAP))
print('画布 %.2f x %.2f 比例 %.2f' % (CX,CY,CX/CY))
print('字号=%.1f 线宽=%.1f 箭头头=%.0f' % (FS,LW,MS))
