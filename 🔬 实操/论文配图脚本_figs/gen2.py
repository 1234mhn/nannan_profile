import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fb = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
fm.fontManager.addfont(fp)
name = fm.FontProperties(fname=fp).get_name()
plt.rcParams['font.family'] = name
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14.6, 8.6), dpi=170)
ax.set_xlim(0, 14.6); ax.set_ylim(0, 8.6); ax.axis('off')

C_OLD='#C3CFDE'; C_OLD_B='#4A5F7A'
C_NEW='#AFD9BA'; C_NEW_B='#2E7D5B'
C_BAD='#C0392B'; C_BG1='#F5F7FA'; C_BG2='#F1F9F4'

def box(x,y,w,h,main,sub='',fc='#fff',ec='#333',fs=12.5,fs2=10,bold=True,tc='#1F2937',tc2='#5A6572'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=fc,ec=ec,lw=2))
    if sub:
        ax.text(x+w/2, y+h*0.64, main, ha='center', va='center', fontsize=fs,
                fontweight='bold' if bold else 'normal', color=tc)
        ax.text(x+w/2, y+h*0.28, sub, ha='center', va='center', fontsize=fs2,
                color=tc2, style='italic')
    else:
        ax.text(x+w/2, y+h/2, main, ha='center', va='center', fontsize=fs,
                fontweight='bold' if bold else 'normal', color=tc, linespacing=1.4)

def arrow(x1,y1,x2,y2,color='#4B5563',lw=2.2,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=20,
                                 color=color,lw=lw,linestyle=ls,shrinkA=2,shrinkB=2))

# 背景
ax.add_patch(FancyBboxPatch((0.3,0.5),6.85,6.35,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1,ec=C_OLD_B,lw=2.5,ls='--'))
ax.text(3.72,6.42,'【旧】 之前的方法（主流 LLaVA 式：两段拼接）',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_OLD_B)

ax.add_patch(FancyBboxPatch((7.45,0.5),6.85,6.35,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2,ec=C_NEW_B,lw=2.5,ls='--'))
ax.text(10.87,6.42,'【新】 现在的方法（CheXmix：早期融合）',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_NEW_B)

# ===== 左：旧方法 =====
box(0.6,5.15,1.95,0.85,'胸片图像','',fc='#fff',ec=C_OLD_B,fs=13)
box(3.0,5.10,1.95,0.95,'闭嘴只看图的专家','（视觉编码器 CLIP）',fc=C_OLD,ec=C_OLD_B,fs=12.5)
arrow(2.57,5.57,2.97,5.57)

box(5.42,5.02,1.55,1.10,'翻译','（投影层）',fc='#FADBD8',ec=C_BAD,fs=14,tc='#922B21',tc2='#B03A2E')
arrow(4.97,5.57,5.39,5.57)

ax.text(6.19,4.68,'⚠',ha='center',va='center',fontsize=26,color=C_BAD)
ax.text(6.19,4.20,'翻译会漏掉\n最要紧的细节',ha='center',va='center',fontsize=11.5,
        color=C_BAD,fontweight='bold',linespacing=1.45)

box(3.0,3.25,1.95,0.95,'闭眼看字、开口说话的人','（语言模型 LLM）',fc=C_OLD,ec=C_OLD_B,fs=11.5)
arrow(6.19,5.0,4.2,4.22,color=C_BAD,ls=(0,(4,3)))

box(0.6,3.30,1.95,0.85,'放射报告文本','',fc='#fff',ec=C_OLD_B,fs=13)
arrow(2.57,3.72,2.97,3.72)

box(0.75,1.35,5.55,0.95,'分类 / 报告生成','',fc='#fff',ec=C_OLD_B,fs=14)
arrow(3.95,3.22,3.55,2.32)

ax.text(3.72,0.92,'两个专家无法直接交流，中间必须有人翻译',ha='center',va='center',
        fontsize=12.5,color='#3E4C5E',style='italic',fontweight='bold')

# ===== 右：新方法 =====
box(7.85,5.15,1.9,0.85,'胸片图像','',fc='#fff',ec=C_NEW_B,fs=13)
box(7.85,3.35,1.9,0.85,'放射报告文本','',fc='#fff',ec=C_NEW_B,fs=13)

box(10.15,5.02,1.75,1.05,'切成 1024 个小块','（图像 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
box(10.15,3.25,1.75,1.05,'切成一个个词','（文本 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
arrow(9.77,5.57,10.13,5.57)
arrow(9.77,3.77,10.13,3.77)

# 统一序列
ax.add_patch(FancyBboxPatch((12.25,3.30),1.85,2.85,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#fff',ec=C_NEW_B,lw=2.5))
ax.text(13.17,5.88,'大家都在\n说同一种语言',ha='center',va='center',fontsize=11.5,
        fontweight='bold',color=C_NEW_B,linespacing=1.4)
ax.text(13.17,5.50,'（统一 token 序列）',ha='center',va='center',fontsize=9.5,
        color='#5A6572',style='italic')
labels=['图','图','图','文','文']
for i,lb in enumerate(labels):
    yy=5.12-i*0.35
    fc='#D5EBDC' if lb=='图' else '#FFF3CD'
    ax.add_patch(Rectangle((12.45,yy),1.45,0.29,fc=fc,ec=C_NEW_B,lw=1.2))
    ax.text(13.17,yy+0.145,lb,ha='center',va='center',fontsize=10.5,color='#1F2937')

arrow(11.92,5.57,12.23,5.15)
arrow(11.92,3.77,12.23,4.15)

box(8.75,1.85,3.1,0.95,'一个 Transformer 就够了','',fc=C_NEW,ec=C_NEW_B,fs=14)
arrow(13.17,3.28,11.35,2.82)

box(8.45,0.85,3.7,0.80,'分类 / 报告生成 / 补图','',fc='#fff',ec=C_NEW_B,fs=13.5)
arrow(10.3,1.83,10.3,1.67)

ax.text(13.05,2.2,'✓',ha='center',va='center',fontsize=32,color=C_NEW_B,fontweight='bold')
ax.text(13.05,1.62,'不需要\n翻译',ha='center',va='center',fontsize=11.5,color=C_NEW_B,
        fontweight='bold',linespacing=1.3)

# 底部
ax.add_patch(FancyBboxPatch((0.3,0.06),14.0,0.34,boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50',ec='#2C3E50'))
ax.text(7.3,0.23,'左边：两个专家靠“翻译”对话，翻译必失真     |     右边：一开始就说同一种语言，根本没有翻译',
        ha='center',va='center',fontsize=13,color='#fff',fontweight='bold')

plt.tight_layout(pad=0.3)
out='/root/.openclaw/workspace/figs/architecture_compare_v4.png'
plt.savefig(out,bbox_inches='tight',facecolor='white')
print('saved',out)
