import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

fp='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False

fig,ax=plt.subplots(figsize=(16.0,10.2),dpi=165)
ax.set_xlim(0,16.0);ax.set_ylim(0,10.2);ax.axis('off')

C_OLD='#C3CFDE'; C_OLD_B='#4A5F7A'
C_NEW='#AFD9BA'; C_NEW_B='#2E7D5B'
C_BAD='#C0392B'; C_BG1='#F5F7FA'; C_BG2='#F1F9F4'
C_HOT_B='#B9770E'; C_BORROW_B='#4A6FA5'

def box(x,y,w,h,main,sub='',fc='#fff',ec='#333',fs=12.5,fs2=9.6,tc='#1F2937',tc2='#5A6572',lw=2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc=fc,ec=ec,lw=lw))
    if sub:
        ax.text(x+w/2,y+h*0.67,main,ha='center',va='center',fontsize=fs,fontweight='bold',color=tc)
        ax.text(x+w/2,y+h*0.28,sub,ha='center',va='center',fontsize=fs2,color=tc2,style='italic')
    else:
        ax.text(x+w/2,y+h/2,main,ha='center',va='center',fontsize=fs,fontweight='bold',
                color=tc,linespacing=1.45)

def arrow(x1,y1,x2,y2,color='#4B5563',lw=2.2,ls='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=19,
                                 color=color,lw=lw,linestyle=ls,shrinkA=1,shrinkB=1))

# ===== 两栏背景 =====
ax.add_patch(FancyBboxPatch((0.25,0.55),6.55,8.75,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG1,ec=C_OLD_B,lw=2.5,ls='--'))
ax.add_patch(FancyBboxPatch((7.10,0.55),8.65,8.75,boxstyle="round,pad=0.02,rounding_size=0.18",
                            fc=C_BG2,ec=C_NEW_B,lw=2.5,ls='--'))
ax.text(3.52,9.82,'【旧】主流 LLaVA 式：两段拼接',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_OLD_B)
ax.text(11.42,9.82,'【新】CheXmix：早期融合 + 两阶段训练',ha='center',va='center',
        fontsize=15.5,fontweight='bold',color=C_NEW_B)

# ==================== 左：旧方法 ====================
box(0.50,8.00,1.85,0.82,'胸片图像','',fs=12.5)
box(2.80,7.93,1.95,0.96,'看图专家','（视觉编码器 CLIP）',fc=C_OLD,ec=C_OLD_B,fs=12.5)
arrow(2.37,8.41,2.77,8.41)

box(5.18,7.85,1.45,1.12,'翻译','（投影层）',fc='#FADBD8',ec=C_BAD,fs=13.5,tc='#922B21',tc2='#B03A2E')
arrow(4.77,8.41,5.15,8.41)

box(2.80,5.95,1.95,0.96,'说话的人','（语言模型 LLM）',fc=C_OLD,ec=C_OLD_B,fs=12.5)
arrow(5.90,7.83,5.90,5.60,color=C_BAD,ls=(0,(4.5,3.5)),lw=2.3)
ax.plot([5.90,3.78],[5.60,5.60],color=C_BAD,lw=2.3,linestyle=(0,(4.5,3.5)))
arrow(3.78,5.60,3.78,5.93,color=C_BAD)

ax.text(5.90,5.18,'⚠ 细节被压掉',ha='center',va='center',fontsize=11.2,
        color=C_BAD,fontweight='bold')

box(0.50,6.02,1.85,0.82,'放射报告','',fs=12.5)
arrow(2.37,6.43,2.77,6.43)

box(0.72,3.95,4.80,0.88,'分类 / 报告生成','',fs=13.5)
arrow(3.78,5.93,3.78,4.85)

# 左侧训练说明
ax.add_patch(FancyBboxPatch((0.72,3.00),4.80,0.70,boxstyle="round,pad=0.02,rounding_size=0.10",
                            fc='#fff',ec=C_OLD_B,lw=1.8,ls=':'))
ax.text(3.12,3.48,'训练：只有一步（两段分开训）',ha='center',va='center',fontsize=11.5,
        fontweight='bold',color=C_OLD_B)
ax.text(3.12,3.20,'先训视觉编码器，再训投影层',ha='center',va='center',
        fontsize=9.6,color='#5A6572',style='italic')
arrow(3.12,3.72,3.12,3.93,color=C_OLD_B,ls=(0,(3,3)))

ax.text(3.52,1.95,'两个专家靠「翻译」对话，翻译必失真',
        ha='center',va='center',fontsize=12.2,color='#3E4C5E',style='italic',fontweight='bold')

# ==================== 右：新方法 ====================
# 上：数据变成 token
box(7.40,8.00,1.65,0.82,'胸片图像','',fs=12.5)
box(7.40,6.35,1.65,0.82,'放射报告','',fs=12.5)

box(9.42,7.92,1.95,1.05,'切成 1024 小块','（图像 token）',fc=C_NEW,ec=C_NEW_B,fs=11.8,fs2=9.3)
box(9.42,6.28,1.95,1.05,'切成一个个词','（文本 token）',fc=C_NEW,ec=C_NEW_B,fs=11.8,fs2=9.3)
arrow(9.07,8.41,9.39,8.41)
arrow(9.07,6.76,9.39,6.76)

# 统一序列（竖向小列）
ax.add_patch(FancyBboxPatch((11.70,6.20),1.85,2.92,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#fff',ec=C_NEW_B,lw=2.4))
ax.text(12.62,8.82,'同一种语言',ha='center',va='center',fontsize=11.5,fontweight='bold',color=C_NEW_B)
ax.text(12.62,8.53,'（统一 token 序列）',ha='center',va='center',fontsize=8.8,
        color='#5A6572',style='italic')
labels=['图','图','图','文','文']
for i,lb in enumerate(labels):
    yy=8.08-i*0.34
    fc='#D5EBDC' if lb=='图' else '#FFF3CD'
    ax.add_patch(Rectangle((11.90,yy),1.45,0.28,fc=fc,ec=C_NEW_B,lw=1.1))
    ax.text(12.62,yy+0.14,lb,ha='center',va='center',fontsize=10,color='#1F2937')
arrow(11.39,8.41,11.67,8.05)
arrow(11.39,6.76,11.67,7.12)

# ===== 两阶段训练：并排放进流程主线 =====
# S1
ax.add_patch(FancyBboxPatch((7.40,4.55),3.35,1.32,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#E8F0FA',ec=C_BORROW_B,lw=2.4))
ax.text(9.07,5.58,'训练阶段 S1：自回归',ha='center',va='center',fontsize=12.5,
        fontweight='bold',color='#2C4A73')
ax.text(9.07,5.24,'顺着往下写 · 学会生成表达',ha='center',va='center',fontsize=10.2,color='#3D5A80')
ax.text(9.07,4.90,'← 继承自变色龙',ha='center',va='center',fontsize=10,
        color=C_BORROW_B,fontweight='bold',style='italic')

arrow(12.62,6.18,12.62,5.90)
ax.plot([12.62,9.07],[5.90,5.90],color='#4B5563',lw=2.2)
arrow(9.07,5.90,9.07,5.89,color='#4B5563',lw=0.1)  # 触点
ax.add_patch(FancyArrowPatch((9.07,5.90),(9.07,5.89),arrowstyle='-',color='#4B5563',lw=2.2))

# S2
ax.add_patch(FancyBboxPatch((11.10,4.55),3.35,1.32,boxstyle="round,pad=0.02,rounding_size=0.12",
                            fc='#FFF4E5',ec=C_HOT_B,lw=2.8))
ax.text(12.78,5.58,'训练阶段 S2：掩码重建',ha='center',va='center',fontsize=12.5,
        fontweight='bold',color='#7E5109')
ax.text(12.78,5.24,'遮住 50% 再补回来 · 学会看细节',ha='center',va='center',fontsize=10.2,color='#8A6023')
ax.text(12.78,4.90,'← CheXmix 新增（原创）',ha='center',va='center',fontsize=10,
        color=C_HOT_B,fontweight='bold',style='italic')

arrow(10.78,5.21,11.07,5.21,color=C_HOT_B,lw=2.8)

# ===== 模型 =====
box(8.40,3.30,4.30,0.90,'一个 Transformer 就够了','',fc=C_NEW,ec=C_NEW_B,fs=13.5,lw=2.4)
arrow(12.78,4.53,12.78,4.30,color=C_HOT_B)
ax.plot([12.78,10.55],[4.30,4.30],color='#4B5563',lw=2.2)
arrow(10.55,4.30,10.55,4.22)

# ===== 输出 =====
box(8.40,2.05,1.95,0.80,'分类 / 判别','',fs=12.5)
box(10.75,2.05,1.95,0.80,'报告 / 补图','',fs=12.5)
arrow(9.37,3.28,9.37,2.87)
arrow(11.72,3.28,11.72,2.87)

# ✓ 不需要翻译
ax.text(14.85,4.35,'✓ 不需要\n投影层',ha='center',va='center',fontsize=12.5,color=C_NEW_B,
        fontweight='bold',linespacing=1.4)

ax.text(11.42,1.42,'S1 学会「写」  +  S2 逼它「真看懂」  =  判别和生成都会',
        ha='center',va='center',fontsize=12,color='#2E7D5B',fontweight='bold')

# 底部条
ax.add_patch(FancyBboxPatch((0.25,0.08),15.50,0.36,boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc='#2C3E50',ec='#2C3E50'))
ax.text(8.00,0.26,'架构：取消投影层（借自变色龙）    ｜    训练：多了一个掩码重建阶段（CheXmix 原创）',
        ha='center',va='center',fontsize=12.5,color='#fff',fontweight='bold')

plt.tight_layout(pad=0.3)
out='/root/.openclaw/workspace/figs/architecture_compare_v9.png'
plt.savefig(out,bbox_inches='tight',facecolor='white')
print('saved',out)
