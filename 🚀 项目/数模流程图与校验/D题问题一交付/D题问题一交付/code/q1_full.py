"""问题一 完整求解 (T1.2+T1.3)
- 每服务区 × 每机型: 组批(2D装箱+能量约束) -> 架次/能耗/时间
- 机型对比 + 多目标权衡(帕累托)
- 返航安全余量 rho 灵敏度
"""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import *
import pandas as pd

def sortie_energy(g,d,h_up,h_dn,q,rho=None):
    p=TRANSPORT[g]; rho=p['rho'] if rho is None else rho
    Ea=(1-rho)*p['Euse']; e0=Ea/p['L0']; eF=Ea/p['LF']
    w=float(np.clip(q/p['qmax'],0,1)); e_hor=e0+(eF-e0)*w
    return ((p['m_empty']+q)*G*h_up/(p['eta_up']*3.6e6) + e_hor*d
            + p['m_empty']*G*h_dn/(p['eta_up']*3.6e6) + e0*d)

def sortie_time(g,d,h_up,h_dn,nb):
    p=TRANSPORT[g]
    return (p['t_prep'] + p['t_load_per_box']*nb
            + h_up/p['vup'] + d/p['vc']
            + p['t_hand_base'] + p['t_hand_per_box']*nb
            + h_dn/p['vdn'] + d/p['vc'])

def max_q(g,d,h_up,h_dn,rho=None):
    p=TRANSPORT[g]; rho=p['rho'] if rho is None else rho
    Ea=(1-rho)*p['Euse']
    f=lambda q: sortie_energy(g,d,h_up,h_dn,q,rho)-Ea
    if f(0)>0: return 0.0
    if f(p['qmax'])<=0: return p['qmax']
    lo,hi=0.0,p['qmax']
    for _ in range(80):
        m=(lo+hi)/2
        if f(m)<=0: lo=m
        else: hi=m
    return lo

def batch(boxes,g,qcap,vol,d,h_up,h_dn,rho=None):
    """FFD: 先大体积后大质量; 质量+体积+能量三重约束"""
    cap_m=min(qcap,TRANSPORT[g]['qmax']); cap_v=vol
    items=sorted(boxes,key=lambda b:(-b['v'],-b['m']))
    S=[]
    for b in items:
        if b['m']>cap_m+1e-9 or b['v']>cap_v+1e-9: return None
        for s in S:
            nq=s['q']+b['m']; nv=s['v']+b['v']
            if nq<=cap_m+1e-9 and nv<=cap_v+1e-9:
                p=TRANSPORT[g]; rho_=p['rho'] if rho is None else rho
                if sortie_energy(g,d,h_up,h_dn,nq,rho_)<=(1-rho_)*p['Euse']+1e-9:
                    s['boxes'].append(b); s['q']=nq; s['v']=nv; break
        else:
            S.append(dict(boxes=[b],q=b['m'],v=b['v']))
    return S

def plan_metrics(S,g,d,h_up,h_dn,rho=None):
    return dict(n=len(S), E=sum(sortie_energy(g,d,h_up,h_dn,s['q'],rho) for s in S),
                T=sum(sortie_time(g,d,h_up,h_dn,len(s['boxes'])) for s in S))

def main():
    dem=DEM(); O,svcs=load_nodes(); boxes=load_boxes()
    geom=json.load(open(os.path.join(RES,'common_leg_geometry.json')))
    by={}
    for b in boxes: by.setdefault(b['svc'],[]).append(b)

    rows=[]; detail={}
    for s in svcs:
        sid=s['id']; gg=geom[sid]; bx=by[sid]
        per={}
        for g in 'ABC':
            qc=max_q(g,gg['d'],gg['h_up'],gg['h_dn'])
            S=batch(bx,g,qc,TRANSPORT[g]['vol'],gg['d'],gg['h_up'],gg['h_dn'])
            per[g]=(plan_metrics(S,g,gg['d'],gg['h_up'],gg['h_dn']) if S else None, qc, S)
        # 选"主观最优": 先最少架次, 再能耗, 再时间
        best=None
        for g in 'ABC':
            m,qc,S=per[g]
            if m is None: continue
            key=(m['n'],m['E'],m['T'])
            if best is None or key<best[0]: best=(key,g,m,qc,S)
        _,g,m,qc,S=best
        rows.append(dict(svc=sid,n_boxes=len(bx),best_model=g,
            n_A=per['A'][0]['n'] if per['A'][0] else None,
            n_B=per['B'][0]['n'] if per['B'][0] else None,
            n_C=per['C'][0]['n'] if per['C'][0] else None,
            E_A=round(per['A'][0]['E'],3) if per['A'][0] else None,
            E_B=round(per['B'][0]['E'],3) if per['B'][0] else None,
            E_C=round(per['C'][0]['E'],3) if per['C'][0] else None,
            T_A=round(per['A'][0]['T'],0) if per['A'][0] else None,
            T_B=round(per['B'][0]['T'],0) if per['B'][0] else None,
            T_C=round(per['C'][0]['T'],0) if per['C'][0] else None,
            qcap_A=round(per['A'][1],2), qcap_B=round(per['B'][1],2), qcap_C=round(per['C'][1],2),
            n_sortie=m['n'], E=round(m['E'],3), T=round(m['T'],0),
            total_m=round(sum(b['m'] for b in bx),1), total_v=round(sum(b['v'] for b in bx),4)))
        detail[sid]=dict(model=g,qcap=round(qc,2),
            sorties=[dict(boxes=[b['id'] for b in x['boxes']],q=round(x['q'],2),
                          v=round(x['v'],4),E=round(sortie_energy(g,gg['d'],gg['h_up'],gg['h_dn'],x['q']),3),
                          T=round(sortie_time(g,gg['d'],gg['h_up'],gg['h_dn'],len(x['boxes'])),0)) for x in S])
    df=pd.DataFrame(rows)
    df.to_csv(os.path.join(RES,'q1_grouping.csv'),index=False,encoding='utf-8-sig')
    json.dump(detail,open(os.path.join(RES,'q1_grouping_detail.json'),'w'),ensure_ascii=False,indent=1)

    # 载荷表
    cap=[]
    for s in svcs:
        gg=geom[s['id']]
        for g in 'ABC':
            cap.append(dict(svc=s['id'],model=g,d=round(gg['d'],1),h_up=round(gg['h_up'],1),
                q_energy=round(max_q(g,gg['d'],gg['h_up'],gg['h_dn']),2),qmax=TRANSPORT[g]['qmax'],
                vol=TRANSPORT[g]['vol'], q_effective=round(min(max_q(g,gg['d'],gg['h_up'],gg['h_dn']),TRANSPORT[g]['qmax']),2)))
    pd.DataFrame(cap).to_csv(os.path.join(RES,'q1_payload_cap.csv'),index=False,encoding='utf-8-sig')

    print('=== 全机型对比 (最优方案加粗★) ===')
    print(df[['svc','n_boxes','best_model','n_A','n_B','n_C','E_A','E_B','E_C','n_sortie','E','T']].to_string(index=False))
    print()
    print(f"最优方案合计: 架次={df['n_sortie'].sum()} 能耗={df['E'].sum():.3f}kWh 时间={df['T'].sum():.0f}s ({df['T'].sum()/3600:.2f}h)")
    print(f"若全用A: 架次={df['n_A'].sum()} 能耗={df['E_A'].sum():.3f}kWh")
    print(f"若全用B: 架次={df['n_B'].sum()} 能耗={df['E_B'].sum():.3f}kWh")
    print(f"若全用C: 架次={df['n_C'].sum()} 能耗={df['E_C'].sum():.3f}kWh")

    # ---- 灵敏度: rho ----
    sen=[]
    for rho in [0.10,0.15,0.20,0.25,0.30]:
        tn=0;te=0;tq={}
        for s in svcs:
            sid=s['id']; gg=geom[sid]; bx=by[sid]; best=None
            for g in 'ABC':
                qc=max_q(g,gg['d'],gg['h_up'],gg['h_dn'],rho)
                S=batch(bx,g,qc,TRANSPORT[g]['vol'],gg['d'],gg['h_up'],gg['h_dn'],rho)
                if S is None: continue
                m=plan_metrics(S,g,gg['d'],gg['h_up'],gg['h_dn'],rho)
                if best is None or (m['n'],m['E'])<(best[0],best[1]): best=(m['n'],m['E'],g)
            if best: tn+=best[0]; te+=best[1]; tq[best[2]]=tq.get(best[2],0)+1
        sen.append(dict(rho=rho,total_sorties=tn,total_energy=round(te,3),model_dist=str(tq)))
    sdf=pd.DataFrame(sen); sdf.to_csv(os.path.join(RES,'q1_sensitivity.csv'),index=False,encoding='utf-8-sig')
    print('\n=== rho 灵敏度 ===')
    print(sdf.to_string(index=False))

if __name__=='__main__': main()
