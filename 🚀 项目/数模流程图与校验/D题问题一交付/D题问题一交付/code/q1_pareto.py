"""T1.3 多目标帕累托分析 + 图表"""
import numpy as np, json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['WenQuanYi Zen Hei','Noto Sans CJK SC','DejaVu Sans']
plt.rcParams['axes.unicode_minus']=False

dem=DEM(); O,svcs=load_nodes(); boxes=load_boxes()
geom=json.load(open(os.path.join(RES,'common_leg_geometry.json')))
by={}
for b in boxes: by.setdefault(b['svc'],[]).append(b)

# 复用 q1_full 的函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q1_full import max_q, batch, plan_metrics, sortie_energy, sortie_time

# ---- 帕累托: 每服务区选机型(3选项) -> 全局组合作战空间 ----
# 简化: 逐服务区枚举机型, 统计不同"机型组合"的全局 (架次, 能耗, 时间)
opts={}
for s in svcs:
    sid=s['id']; gg=geom[sid]; bx=by[sid]
    o=[]
    for g in 'ABC':
        qc=max_q(g,gg['d'],gg['h_up'],gg['h_dn'])
        S=batch(bx,g,qc,TRANSPORT[g]['vol'],gg['d'],gg['h_up'],gg['h_dn'])
        if S is None: continue
        m=plan_metrics(S,g,gg['d'],gg['h_up'],gg['h_dn'])
        o.append((g,m['n'],m['E'],m['T']))
    opts[sid]=o

# 逐服务区独立选 -> 全组合太大(3^15), 改为"逐服务区帕累托 + 全局代表性方案"
rep=[]
# 方案1: 架次优先
# 方案2: 能耗优先
# 方案3: 时间优先
for crit,name in [(0,'架次优先'),(1,'能耗优先'),(2,'时间优先')]:
    tn=te=tt=0; dist={}
    for sid,o in opts.items():
        best=min(o,key=lambda x:(x[1+crit],x[1],x[2],x[3]))
        tn+=best[1];te+=best[2];tt+=best[3]
        dist[best[0]]=dist.get(best[0],0)+1
    rep.append(dict(scheme=name,sorties=tn,energy=round(te,3),time=round(tt,0),model_dist=str(dist)))
rdf=pd.DataFrame(rep)
rdf.to_csv(os.path.join(RES,'q1_pareto.csv'),index=False,encoding='utf-8-sig')
print('=== 三种优先策略 ===')
print(rdf.to_string(index=False))

# ---- 图1: 载荷上限热力图 ----
cap=pd.read_csv(os.path.join(RES,'q1_payload_cap.csv'))
piv=cap.pivot(index='svc',columns='model',values='q_effective')
fig,ax=plt.subplots(figsize=(6,7))
im=ax.imshow(piv.values,cmap='YlOrRd',aspect='auto')
ax.set_xticks(range(3)); ax.set_xticklabels(['A型','B型','C型'])
ax.set_yticks(range(len(piv))); ax.set_yticklabels(piv.index,fontsize=8)
for i in range(len(piv)):
    for j in range(3):
        ax.text(j,i,f'{piv.values[i,j]:.0f}',ha='center',va='center',fontsize=7)
plt.colorbar(im,label='最大安全载荷 (kg)')
plt.tight_layout(); plt.savefig(os.path.join(BASE,'figures','q1_payload_heatmap.pdf')); plt.close()

# ---- 图2: 机型综合对比 (架次/能耗/时间) ----
df=pd.read_csv(os.path.join(RES,'q1_grouping.csv'))
fig,axes=plt.subplots(1,3,figsize=(14,4))
for ax,col,lab in zip(axes,['n_A','n_B','n_C'],['A型','B型','C型']):
    ax.bar(df['svc'],df[col],label=lab,color='steelblue')
    ax.set_title(f'{lab} 架次数'); ax.tick_params(axis='x',rotation=90,labelsize=7)
plt.tight_layout(); plt.savefig(os.path.join(BASE,'figures','q1_model_compare.pdf')); plt.close()

# ---- 图3: 三目标权衡散点 ----
fig,ax=plt.subplots(figsize=(7,5))
ax.scatter(rdf['energy'],rdf['sorties'],s=120,c=['#d62728','#2ca02c','#1f77b4'])
for _,r in rdf.iterrows():
    ax.annotate(r['scheme'],(r['energy'],r['sorties']),fontsize=9,xytext=(5,5),textcoords='offset points')
ax.set_xlabel('总能耗 (kWh)'); ax.set_ylabel('总架次数'); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(BASE,'figures','q1_tradeoff.pdf')); plt.close()

# ---- 图4: rho 灵敏度 ----
sen=pd.read_csv(os.path.join(RES,'q1_sensitivity.csv'))
fig,ax1=plt.subplots(figsize=(7,4.5))
ax1.plot(sen['rho'],sen['total_energy'],'o-',color='#d62728',label='总能耗')
ax1.set_xlabel('返航安全余量 ρ'); ax1.set_ylabel('总能耗 (kWh)',color='#d62728')
ax2=ax1.twinx(); ax2.plot(sen['rho'],sen['total_sorties'],'s--',color='#1f77b4',label='总架次')
ax2.set_ylabel('总架次数',color='#1f77b4')
ax1.grid(alpha=.3); plt.tight_layout()
plt.savefig(os.path.join(BASE,'figures','q1_sensitivity.pdf')); plt.close()

# ---- 图5: 组批方案堆叠图 ----
fig,ax=plt.subplots(figsize=(11,4.5))
x=np.arange(len(df)); bot=np.zeros(len(df))
cmap=plt.cm.Set3
det=json.load(open(os.path.join(RES,'q1_grouping_detail.json')))
maxs=max(len(det[s]['sorties']) for s in det)
for k in range(maxs):
    vals=[det[s]['sorties'][k]['q'] if k<len(det[s]['sorties']) else 0 for s in df['svc']]
    ax.bar(x,vals,bottom=bot,label=f'第{k+1}架次',color=cmap(k%12)); bot+=np.array(vals)
ax.set_xticks(x); ax.set_xticklabels(df['svc'],rotation=90,fontsize=8)
ax.set_ylabel('装载质量 (kg)')
for i,(sid,m) in enumerate(zip(df['svc'],df['best_model'])):
    ax.text(i,bot[i]+2,m,ha='center',fontsize=8,fontweight='bold')
ax.legend(fontsize=7,ncol=4)
plt.tight_layout(); plt.savefig(os.path.join(BASE,'figures','q1_grouping.pdf')); plt.close()

print('\n✅ 图已生成:', os.listdir(os.path.join(BASE,'figures')))
