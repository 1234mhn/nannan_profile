#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题四 思路流程图（三栏蛇形 v3）—— 论文流程图标准格式
关键修正：
  1) 横跳走"栏间通道"：栏末框底 ↓ → 右移到两栏之间的空隙 → ↑ 上行到顶端 → 进入下一栏首框顶部
  2) 每条连线做几何断言：不得穿过任何框体
  3) 画布留足左右边距，框边线不被裁
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'   # 粗体（论文流程图加粗要求）
prop = fm.FontProperties(fname=FONT)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

WHITE='white'; INK='#000000'
BW, BH = 7.2, 1.20
TH = 1.10
ROW_GAP = 1.72
COL_GAP = 1.55              # 栏间净空（横向）
X0 = 4.30                   # 第1栏中心
YTOP = 7.15
LW, FS, ARROW_LW, MS = 3.0, 15.5, 3.0, 23

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
PER, NC = 4, 3
COL_STEP = BW + COL_GAP                          # 5.00 中心距
CX = X0 + (NC-1)*COL_STEP + BW/2 + 0.6           # 右侧留 0.6
CY = YTOP + BH/2 + 0.45

fig, ax = plt.subplots(figsize=(CX*0.97, CY*0.97), dpi=220)
ax.set_xlim(0, CX); ax.set_ylim(0, CY); ax.axis('off')

def hh(t): return TH/2 if t=='term' else BH/2

def box(x, y, w, h, text, fs=FS, round_r=0.07, lw=LW):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        edgecolor=INK, facecolor=WHITE, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=INK,
            fontproperties=prop, zorder=4, linespacing=1.45)

def terminal(x, y, text, fs=FS):
    box(x, y, BW, TH, text, fs=fs, round_r=0.26, lw=LW)

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

# ---- 几何断言工具 ----
boxes = [(pos[i][0]-BW/2, pos[i][1]-hh(NODES[i][0]),
          pos[i][0]+BW/2, pos[i][1]+hh(NODES[i][0])) for i in range(len(NODES))]
def hits(p1, p2, pad=0.03):
    """线段是否穿过任何框体（内部）"""
    (x1,y1),(x2,y2) = p1,p2
    bad=[]
    for k,(bx1,by1,bx2,by2) in enumerate(boxes):
        bx1+=pad; by1+=pad; bx2-=pad; by2-=pad
        # 采样检测
        for t in [j/40 for j in range(41)]:
            x=x1+(x2-x1)*t; y=y1+(y2-y1)*t
            if bx1<x<bx2 and by1<y<by2:
                bad.append(k); break
    return bad

problems=[]
# 栏内竖箭
for i in range(len(NODES)-1):
    if (i+1)%PER==0: continue
    x,y=pos[i]
    p1=(x, y-hh(NODES[i][0])); p2=(x, pos[i+1][1]+hh(NODES[i+1][0]))
    arrow(p1,p2)
# 横跳：走栏间通道（不穿框）
for c in range(NC-1):
    iL=c*PER+PER-1; iR=(c+1)*PER
    xL,yL=pos[iL]; xR,yR=pos[iR]
    yL_bot=yL-hh(NODES[iL][0]); yR_top=yR+hh(NODES[iR][0])
    xch = xL+BW/2 + COL_GAP/2          # 通道：第c栏右边线 与 第c+1栏左边线 的中点
    jumpY = yL_bot - 0.30
    segs=[((xL,yL_bot),(xL,jumpY)),
          ((xL,jumpY),(xch,jumpY)),
          ((xch,jumpY),(xch,yR_top+0.40)),
          ((xch,yR_top+0.40),(xR,yR_top+0.40))]
    for p in segs:
        for k in hits(*p):
            problems.append('跳线%d 穿框%d' % (c,k))
        line(*p)
    p_arrow=((xR,yR_top+0.40),(xR,yR_top))
    for k in hits(*p_arrow): problems.append('跳线%d 箭头穿框%d'%(c,k))
    arrow(*p_arrow)

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
out='/root/.openclaw/workspace/flowchart_q1/流程图_问题四_三栏版'
plt.savefig(out+'.png', dpi=220, bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.05)
plt.savefig(out+'.svg', bbox_inches='tight', facecolor='white', pad_inches=0.05)
print('OK ->', out)
print('\n--- 自检 ---')
print('几何断言（连线穿框）:', '全部通过 ✓' if not problems else problems)
print('栏心 x=', [round(X0+c*COL_STEP,2) for c in range(NC)])
print('通道 x=', [round(X0+c*COL_STEP+BW/2+COL_GAP/2,2) for c in range(NC-1)])
print('画布 %.2f x %.2f | 栏1左沿=%.2f 栏3右沿=%.2f (留边 %.2f/%.2f)' % (
    CX, CY, X0-BW/2, X0+2*COL_STEP+BW/2, X0-BW/2, CX-(X0+2*COL_STEP+BW/2)))
