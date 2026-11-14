import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

fp='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False

fig,ax=plt.subplots(figsize=(15.4,10.6),dpi=165)
ax.set_xlim(0,15.4);ax.set_ylim(0,10.6);ax.axis('off')

C_OLD='#C3CFDE'; C_OLD_B='#4A5F7A'
C_NEW='#AFD9BA'; C_NEW_B='#2E7D5B'
C_BAD='#C0392B'; C_BG1='#F5F7FA'; C_BG2='#F1F9F4'
C_HOT='#FDEBD0'; C_HOT_B='#B9770E'
C_BORROW='#E8F0FA'; C_BORROW_B='#4A6FA5'

def box(x,y,w,h,main,sub='',fc='#fff',ec='#333',fs=12.5,fs2=9.8,tc='#1F2937',tc2='#5A6572',lw=2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=fc,ec=ec,lw=lw))
    if sub:
        ax.text(x+w/2,y+h*0.66,main,ha='center',va='center',fontsize=fs,fontweight='bold',color=tc)
        ax.text(x+w/2,y+h*0.27,sub,ha='center',va='center',fontsize=fs2,color=tc2,style='italic')
    else:
        ax.text(x+w/2,y+h/2,main,ha='center',va='center',fontsize=fs,fontweight='bold',
                color=tc,linespacing=1.45)

def arrow(x1,y1,x2,y2,color='#4B5563',lw=2.2,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=19,
                                 color=color,lw=lw,linestyle=ls,shrinkA=1,shrinkB=1))

# ===== 两大背景 =====
ax.add_patch(FancyBboxPatch((0.25,0.55),7.05,8.85,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1,ec=C_OLD_B,lw=2.5,ls='--'))
ax.add_patch(FancyBboxPatch((7.60,0.55),7.55,8.85,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2,ec=C_NEW_B,lw=2.5,ls='--'))
ax.text(3.78,9.90,'【旧】之前的方法：主流 LLaVA 式两段拼接',ha='center',va='center',
        fontsize=16,fontweight='bold',color=C_OLD_B)
ax.text(11.38,9.90,'【新】现在的方法：CheXmix 早期融合',ha='center',va='center',
        fontsize=16,fontweight='bold',color=C_NEW_B)

# ==================== 左：旧方法 ====================
box(0.55,8.05,1.95,0.86,'胸片图像','',fs=13)
box(3.00,7.98,2.05,1.00,'闭嘴只看图的专家','（视觉编码器 CLIP）',fc=C_OLD,ec=C_OLD_B,fs=12.3)
arrow(2.52,8.48,2.97,8.48)

box(5.50,7.90,1.50,1.16,'翻译','（投影层）',fc='#FADBD8',ec=C_BAD,fs=14,tc='#922B21',tc2='#B03A2E')
arrow(5.07,8.48,5.47,8.48)

box(3.00,6.15,2.05,1.00,'闭眼看字、开口说话的人','（语言模型 LLM）',fc=C_OLD,ec=C_OLD_B,fs=10.6)
arrow(6.25,7.88,6.25,5.80,color=C_BAD,ls=(0,(4.5,3.5)),lw=2.4)
ax.plot([6.25,4.02],[5.80,5.80],color=C_BAD,lw=2.4,linestyle=(0,(4.5,3.5)))
arrow(4.02,5.80,4.02,6.13,color=C_BAD)

ax.text(6.25,5.35,'⚠ 翻译会漏掉\n最要紧的细节',ha='center',va='center',fontsize=11.3,
        color=C_BAD,fontweight='bold',linespacing=1.5)
ax.text(6.25,4.72,'（视觉细节被压缩）',ha='center',va='center',fontsize=9.3,
        color='#B03A2E',style='italic')

box(0.55,6.22,1.95,0.86,'放射报告文本','',fs=13)
arrow(2.52,6.65,2.97,6.65)

box(0.80,4.00,5.05,0.92,'分类 / 报告生成','',fs=14)
arrow(4.02,6.13,4.02,4.94)

# 左侧训练说明（对比用：只有一步）
ax.add_patch(FancyBboxPatch((0.80,2.95),5.05,0.78,boxstyle="round,pad=0.02,rounding_size=0.10",
                            fc='#FFFFFF',ec=C_OLD_B,lw=2,ls=':'))
ax.text(3.32,3.50,'训练方式：只有一步',ha='center',va='center',fontsize=12.5,
        fontweight='bold',color=C_OLD_B)
ax.text(3.32,3.18,'先把视觉编码器训好，再训投影层 —— 两段分开训',ha='center',va='center',
        fontsize=10,color='#5A6572',style='italic')
arrow(3.32,3.93,3.32,4.92,color=C_OLD_B,ls=(0,(3,3)))

ax.text(3.78,2.05,'两个专家无法直接交流，中间必须有人翻译 → 翻译这一步必失真',
        ha='center',va='center',fontsize=12.3,color='#3E4C5E',style='italic',fontweight='bold')
ax.text(3.78,1.55,'信息流：只看图专家 → 翻译 → 说话的人',ha='center',va='center',
        fontsize=10.8,color='#5A6572')

# ==================== 右：新方法 ====================
box(7.90,8.05,1.90,0.86,'胸片图像','',fs=13)
box(7.90,6.20,1.90,0.86,'放射报告文本','',fs=13)

box(10.30,7.92,2.05,1.12,'切成 1024 个小块','（图像 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
box(10.30,6.07,2.05,1.12,'切成一个个词','（文本 token 化）',fc=C_NEW,ec=C_NEW_B,fs=12)
arrow(9.82,8.48,10.27,8.48)
arrow(9.82,6.63,10.27,6.63)

# 统一序列
ax.add_patch(FancyBboxPatch((12.80,5.95),2.10,3.12,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#fff',ec=C_NEW_B,lw=2.5))
ax.text(13.85,8.78,'大家都在说',ha='center',va='center',fontsize=12,fontweight='bold',color=C_NEW_B)
ax.text(13.85,8.50,'同一种语言',ha='center',va='center',fontsize=12,fontweight='bold',color=C_NEW_B)
ax.text(13.85,8.18,'（统一 token 序列）',ha='center',va='center',fontsize=9.3,
        color='#5A6572',style='italic')
labels=['图','图','图','文','文']
for i,lb in enumerate(labels):
    yy=7.72-i*0.35
    fc='#D5EBDC' if lb=='图' else '#FFF3CD'
    ax.add_patch(Rectangle((13.02,yy),1.66,0.29,fc=fc,ec=C_NEW_B,lw=1.2))
    ax.text(13.85,yy+0.145,lb,ha='center',va='center',fontsize=10.4,color='#1F2937')
arrow(12.37,8.48,12.77,8.10)
arrow(12.37,6.63,12.77,7.00)

box(8.95,4.25,3.60,0.92,'一个 Transformer 就够了','',fc=C_NEW,ec=C_NEW_B,fs=13.5)
arrow(13.85,5.93,13.85,5.30)
ax.plot([13.85,10.75],[5.30,5.30],color='#4B5563',lw=2.2)
arrow(10.75,5.30,10.75,5.19)

ax.text(14.05,4.72,'✓',ha='center',va='center',fontsize=30,color=C_NEW_B,fontweight='bold')
ax.text(14.05,4.10,'不需要\n翻译',ha='center',va='center',fontsize=10.8,color=C_NEW_B,
        fontweight='bold',linespacing=1.3)

# 🔥 训练流程（核心新增区）
ax.add_patch(FancyBboxPatch((7.85,0.95),7.10,2.90,boxstyle="round,pad=0.02,rounding_size=0.14",
                            fc=C_HOT,ec=C_HOT_B,lw=2.6))
ax.text(11.40,3.55,'★ CheXmix 真正的原创：两阶段训练',ha='center',va='center',
        fontsize=14.5,fontweight='bold',color='#7E5109')

# S1 / S2 两块
box(8.10,2.35,2.50,0.95,'阶段一 S1：自回归','（顺着往下写）',fc=C_BORROW,ec=C_BORROW_B,fs=12,fs2=9.5,tc='#2C4A73')
ax.text(9.35,2.20,'← 继承自变色龙',ha='center',va='center',fontsize=9.5,color=C_BORROW_B,
        style='italic',fontweight='bold')

box(11.95,2.35,2.50,0.95,'阶段二 S2：掩码重建','（遮住补回来）',fc='#FFFFFF',ec=C_HOT_B,fs=12,fs2=9.5,
    tc='#7E5109',tc2='#A04000',lw=2.6)
ax.text(13.20,2.20,'← CheXmix 新增（原创）',ha='center',va='center',fontsize=9.5,color=C_HOT_B,
        style='italic',fontweight='bold')

arrow(10.63,2.83,11.92,2.83,color=C_HOT_B,lw=2.6)

# 说明行
ax.text(11.40,1.72,'S1 学会「生成表达」  ·  S2 逼模型「抓细节」  ·  两者结合 = 判别 + 生成都行',
        ha='center',va='center',fontsize=11.3,color='#6E4409',fontweight='bold')
ax.text(11.40,1.30,'（MAE 的表示优势 + MLLM 的生成能力）',ha='center',va='center',
        fontsize=10,color='#8A6023',style='italic')

# 底部条
ax.add_patch(FancyBboxPatch((0.25,0.08),14.90,0.36,boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50',ec='#2C3E50'))
ax.text(7.70,0.26,'架构上：右边取消了投影层（借自变色龙）    ｜    训练上：右边多了一个掩码重建阶段（CheXmix 自己的原创）',
        ha='center',va='center',fontsize=12.6,color='#fff',fontweight='bold')

plt.tight_layout(pad=0.3)
out='/root/.openclaw/workspace/figs/architecture_compare_v8.png'
plt.savefig(out,bbox_inches='tight',facecolor='white')
print('saved',out)
