import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
name = fm.FontProperties(fname=fp).get_name()
plt.rcParams['font.family'] = name
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(15.0, 9.0), dpi=170)
ax.set_xlim(0, 15.0); ax.set_ylim(0, 9.0); ax.axis('off')

C_OLD='#C3CFDE'; C_OLD_B='#4A5F7A'
C_NEW='#AFD9BA'; C_NEW_B='#2E7D5B'
C_BAD='#C0392B'; C_BG1='#F5F7FA'; C_BG2='#F1F9F4'

def box(x,y,w,h,main,sub='',fc='#fff',ec='#333',fs=12.5,fs2=10,tc='#1F2937',tc2='#5A6572'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=fc,ec=ec,lw=2))
    if sub:
        ax.text(x+w/2, y+h*0.66, main, ha='center', va='center', fontsize=fs,
                fontweight='bold', color=tc)
        ax.text(x+w/2, y+h*0.27, sub, ha='center', va='center', fontsize=fs2,
                color=tc2, style='italic')
    else:
        ax.text(x+w/2, y+h/2, main, ha='center', va='center', fontsize=fs,
                fontweight='bold', color=tc, linespacing=1.4)

def arrow(x1,y1,x2,y2,color='#4B5563',lw=2.2,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=20,
                                 color=color,lw=lw,linestyle=ls,shrinkA=1,shrinkB=1))

# ===== 背景两块 =====
ax.add_patch(FancyBboxPatch((0.30,0.55),7.00,7.10,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1,ec=C_OLD_B,lw=2.5,ls='--'))
ax.add_patch(FancyBboxPatch((7.65,0.55),7.05,7.10,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2,ec=C_NEW_B,lw=2.5,ls='--'))
ax.text(3.80,8.32,'【旧】之前的方法：主流 LLaVA 式两段拼接',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_OLD_B)
ax.text(11.17,8.32,'【新】现在的方法：CheXmix 早期融合',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_NEW_B)

# ================= 左：旧方法 =================
# 行1: 胸片 -> 视觉编码器
box(0.62,6.45,2.00,0.88,'胸片图像','',fs=13)
box(3.10,6.38,2.05,1.02,'闭嘴只看图的专家','（视觉编码器 CLIP）',fc=C_OLD,ec=C_OLD_B,fs=12.5)
arrow(2.64,6.89,3.07,6.89)

# 行1: 视觉编码器 -> 投影层
box(5.62,6.30,1.50,1.16,'翻译','（投影层）',fc='#FADBD8',ec=C_BAD,fs=14,tc='#922B21',tc2='#B03A2E')
arrow(5.18,6.89,5.59,6.89)

# 投影层 -> 语言模型（垂直向下，不再斜穿）
box(3.10,4.55,2.05,1.02,'闭眼看字、开口说话的人','（语言模型 LLM）',fc=C_OLD,ec=C_OLD_B,fs=11.0)
arrow(6.37,6.28,6.37,4.20, color=C_BAD, ls=(0,(4.5,3.5)), lw=2.4)
ax.plot([6.37,4.15],[4.20,4.20], color=C_BAD, lw=2.4, linestyle=(0,(4.5,3.5)))
arrow(4.15,4.20,4.15,4.53, color=C_BAD)

# 警示文字
ax.text(6.37,3.72,'⚠ 翻译会漏掉\n最要紧的细节',ha='center',va='center',fontsize=11.5,
        color=C_BAD,fontweight='bold',linespacing=1.5)
ax.text(6.37,3.05,'（视觉细节被压缩）',ha='center',va='center',fontsize=9.5,
        color='#B03A2E',style='italic')

# 行2: 文本 -> 语言模型
box(0.62,4.62,2.00,0.88,'放射报告文本','',fs=13)
arrow(2.64,5.06,3.07,5.06)

# 语言模型 -> 输出
box(0.85,2.35,5.00,0.95,'分类 / 报告生成','',fs=14)
arrow(4.12,4.52,4.12,3.32)

ax.text(3.80,1.55,'两个专家无法直接交流，中间必须有人翻译 → 翻译这一步必失真',
        ha='center',va='center',fontsize=12.5,color='#3E4C5E',style='italic',fontweight='bold')
ax.text(3.80,1.10,'信息流：只看图专家 → 翻译 → 说话的人',ha='center',va='center',
        fontsize=11,color='#5A6572')

# ================= 右：新方法 =================
box(7.95,6.45,1.95,0.88,'胸片图像','',fs=13)
box(7.95,4.55,1.95,0.88,'放射报告文本','',fs=13)

box(10.42,6.32,2.05,1.14,'切成 1024 个小块','（图像 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
box(10.42,4.42,2.05,1.14,'切成一个个词','（文本 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
arrow(9.92,6.89,10.39,6.89)
arrow(9.92,4.99,10.39,4.99)

# 统一序列列
ax.add_patch(FancyBboxPatch((12.95,4.30),2.00,3.20,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#fff',ec=C_NEW_B,lw=2.5))
ax.text(13.95,7.18,'大家都在说',ha='center',va='center',fontsize=12,
        fontweight='bold',color=C_NEW_B)
ax.text(13.95,6.90,'同一种语言',ha='center',va='center',fontsize=12,
        fontweight='bold',color=C_NEW_B)
ax.text(13.95,6.58,'（统一 token 序列）',ha='center',va='center',fontsize=9.5,
        color='#5A6572',style='italic')
labels=['图','图','图','文','文']
for i,lb in enumerate(labels):
    yy=6.12-i*0.36
    fc='#D5EBDC' if lb=='图' else '#FFF3CD'
    ax.add_patch(Rectangle((13.20,yy),1.50,0.30,fc=fc,ec=C_NEW_B,lw=1.2))
    ax.text(13.95,yy+0.15,lb,ha='center',va='center',fontsize=10.5,color='#1F2937')

arrow(12.49,6.89,12.92,6.35)
arrow(12.49,4.99,12.92,5.55)

# 统一序列 -> Transformer（从列底垂直下行，不压字）
box(9.20,2.35,3.60,0.98,'一个 Transformer 就够了','',fc=C_NEW,ec=C_NEW_B,fs=14)
arrow(13.95,4.28,13.95,3.55)
ax.plot([13.95,11.00],[3.55,3.55],color='#4B5563',lw=2.2)
arrow(11.00,3.55,11.00,3.35)

# Transformer -> 输出
box(8.95,1.05,4.10,0.88,'分类 / 报告生成 / 补图','',fc='#fff',ec=C_NEW_B,fs=13.5)
arrow(11.00,2.33,11.00,1.95)

# ✓ 不需要翻译（放在右侧独立空白区，Transformer 右边）
ax.text(14.15,2.83,'✓',ha='center',va='center',fontsize=34,color=C_NEW_B,fontweight='bold')
ax.text(14.15,2.15,'不需要\n翻译',ha='center',va='center',fontsize=11.5,color=C_NEW_B,
        fontweight='bold',linespacing=1.35)

ax.text(11.17,1.55,'一开始就说同一种语言，根本没有翻译这一步',
        ha='center',va='center',fontsize=12.5,color='#2E7D5B',style='italic',fontweight='bold')

# ===== 底部条 =====
ax.add_patch(FancyBboxPatch((0.30,0.08),14.40,0.36,boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50',ec='#2C3E50'))
ax.text(7.50,0.26,'左边：两个专家靠「翻译」对话，翻译必失真     ｜     右边：一开始就说同一种语言，根本没有翻译',
        ha='center',va='center',fontsize=13,color='#fff',fontweight='bold')

plt.tight_layout(pad=0.3)
out='/root/.openclaw/workspace/figs/architecture_compare_v5.png'
plt.savefig(out,bbox_inches='tight',facecolor='white')
print('saved',out)
