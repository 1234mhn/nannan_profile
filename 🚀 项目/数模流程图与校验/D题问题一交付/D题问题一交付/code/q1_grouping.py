"""T1.2 货箱组批优化 + T1.3 多目标与灵敏度 (问题一完整求解)

流程:
 1) 载荷上限(能量约束) -> q_energy[g][s]
 2) 每服务区独立组批: 二维装箱(质量+体积) + 能量(架次往返)约束
 3) 三目标: 架次数 / 总能耗 / 累计作业时间
 4) rho 灵敏度
"""
import numpy as np, json, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import *
import pandas as pd
from fractions import Fraction

# ---------- 能量/时间模型 ----------
def leg_energy_load(g, d, h_up, h_dn, m_payload, m_takeoff):
    """航段能耗: 水平(按载荷锚定) + 爬升(mgh/eta)"""
    p = TRANSPORT[g]
    Ea = (1-p['rho'])*p['Euse']
    e0, eF = Ea/p['L0'], Ea/p['LF']
    w = float(np.clip(m_payload/p['qmax'], 0, 1))
    e_hor = e0 + (eF-e0)*w
    E_up = m_takeoff*G*h_up/(p['eta_up']*3.6e6) if h_up>0 else 0.0
    return e_hor*d + E_up

def sortie_energy(g, d, h_up, h_dn, q):
    """一个往返架次的总能耗: 去程带载 + 回程空载"""
    p = TRANSPORT[g]
    Ea=(1-p['rho'])*p['Euse']; e0=Ea/p['L0']; eF=Ea/p['LF']
    w=float(np.clip(q/p['qmax'],0,1)); e_hor=e0+(eF-e0)*w
    E_go = (p['m_empty']+q)*G*h_up/(p['eta_up']*3.6e6) + e_hor*d
    E_back = p['m_empty']*G*h_dn/(p['eta_up']*3.6e6) + e0*d
    return E_go+E_back

def sortie_time(g, d, h_up, h_dn, n_boxes):
    """架次累计作业时间: 工位准备 + 装载 + 去程飞行 + 交接 + 回程飞行"""
    p=TRANSPORT[g]
    t_go = h_up/p['vup'] + d/p['vc']
    t_back = h_dn/p['vdn'] + d/p['vc']
    t_load = p['t_load_per_box']*n_boxes
    t_hand = p['t_hand_base'] + p['t_hand_per_box']*n_boxes
    return p['t_prep'] + t_load + t_go + t_hand + t_back

def can_fly(g, d, h_up, h_dn, q):
    """能量可行性: 往返能耗 <= (1-rho)*Euse"""
    return sortie_energy(g,d,h_up,h_dn,q) <= (1-TRANSPORT[g]['rho'])*TRANSPORT[g]['Euse'] + 1e-9

def max_payload_energy(g, d, h_up, h_dn):
    p=TRANSPORT[g]
    if not can_fly(g,d,h_up,h_dn,0.0): return 0.0
    lo,hi=0.0,p['qmax']
    if can_fly(g,d,h_up,h_dn,hi): return hi
    for _ in range(80):
        mid=(lo+hi)/2
        if can_fly(g,d,h_up,h_dn,mid): lo=mid
        else: hi=mid
    return lo

# ---------- 组批: 单服务区, 固定机型 g ----------
def batch_single_svc(boxes, g, q_energy, vol, d, h_up, h_dn):
    """返回架次列表; 每架次 = {"boxes":[...], "q":总质量, "v":总体积, "E":..., "T":...}
    策略: 逐箱降序装入, 质量+体积双约束 + 能量约束; 超出则开新架次
    """
    p=TRANSPORT[g]
    cap_m = min(q_energy, p['qmax'])
    cap_v = p['vol']
    # 按体积降序(大件先装) 再按质量降序
    items = sorted(boxes, key=lambda b: (-b['v'], -b['m']))
    sorties=[]
    for b in items:
        placed=False
        # 尝试装入已有架次(首次适应)
        for s in sorties:
            if s['q']+b['m'] <= cap_m+1e-9 and s['v']+b['v'] <= cap_v+1e-9:
                # 能量复核(装入后总质量)
                if can_fly(g,d,h_up,h_dn,s['q']+b['m']):
                    s['boxes'].append(b); s['q']+=b['m']; s['v']+=b['v']; placed=True; break
        if not placed:
            if b['m']>cap_m+1e-9 or b['v']>cap_v+1e-9:
                return None  # 单箱不可行
            if not can_fly(g,d,h_up,h_dn,b['m']):
                return None
            sorties.append(dict(boxes=[b], q=b['m'], v=b['v']))
    # 计算能耗与时间
    for s in sorties:
        s['E']=sortie_energy(g,d,h_up,h_dn,s['q'])
        s['T']=sortie_time(g,d,h_up,h_dn,len(s['boxes']))
    return sorties

def eval_plan(sorties, g, d, h_up, h_dn):
    return dict(n_sortie=len(sorties),
                E=sum(s['E'] for s in sorties),
                T=sum(s['T'] for s in sorties))

def main():
    dem=DEM(); O,svcs=load_nodes(); boxes=load_boxes()
    geom=json.load(open(os.path.join(RES,'common_leg_geometry.json')))
    by_svc={}
    for b in boxes: by_svc.setdefault(b['svc'],[]).append(b)

    # ---- 1) 载荷上限表 ----
    cap_rows=[]
    qe={}
    for s in svcs:
        gg=geom[s['id']]; qe[s['id']]={}
        for g in ['A','B','C']:
            q=max_payload_energy(g,gg['d'],gg['h_up'],gg['h_dn'])
            qe[s['id']][g]=q
            # 体积折算上限: 用最轻物资密度折算(保守取各服务区实际箱型)
            cap_rows.append(dict(svc=s['id'],model=g,d=gg['d'],h_up=gg['h_up'],
                                 q_energy=round(q,3), vol_limit=TRANSPORT[g]['vol'],
                                 q_design=round(min(q,TRANSPORT[g]['qmax']),3)))
    pd.DataFrame(cap_rows).to_csv(os.path.join(RES,'q1_payload_cap.csv'),index=False,encoding='utf-8-sig')

    # ---- 2) 每服务区 × 每机型 组批, 选最优机型 ----
    all_rows=[]; detail={}
    for s in svcs:
        sid=s['id']; gg=geom[sid]
        bx=by_svc.get(sid,[])
        best=None
        cand={}
        for g in ['A','B','C']:
            so=batch_single_svc(bx,g,qe[sid][g],TRANSPORT[g]['vol'],gg['d'],gg['h_up'],gg['h_dn'])
            if so is None: 
                cand[g]=None; continue
            ev=eval_plan(so,g,gg['d'],gg['h_up'],gg['h_dn'])
            cand[g]=ev
            if best is None or (ev['n_sortie'],ev['E'],ev['T'])<(best[1]['n_sortie'],best[1]['E'],best[1]['T']):
                best=(g,ev,so)
        if best is None:
            all_rows.append(dict(svc=sid,n_boxes=len(bx),model='NONE',n_sortie=None,E=None,T=None,
                                 total_m=round(sum(b["m"] for b in bx),1),total_v=round(sum(b["v"] for b in bx),4)))
            continue
        g,ev,so=best
        all_rows.append(dict(svc=sid,n_boxes=len(bx),model=g,n_sortie=ev['n_sortie'],
                             E=round(ev['E'],4),T=round(ev['T'],1),
                             total_m=round(sum(b['m'] for b in bx),1),
                             total_v=round(sum(b['v'] for b in bx),4),
                             E_A=round(cand['A']['E'],4) if cand['A'] else None,
                             E_B=round(cand['B']['E'],4) if cand['B'] else None,
                             E_C=round(cand['C']['E'],4) if cand['C'] else None,
                             n_A=cand['A']['n_sortie'] if cand['A'] else None,
                             n_B=cand['B']['n_sortie'] if cand['B'] else None,
                             n_C=cand['C']['n_sortie'] if cand['C'] else None))
        detail[sid]=dict(model=g, sorties=[dict(boxes=[b['id'] for b in x['boxes']],
                        q=round(x['q'],2),v=round(x['v'],4),E=round(x['E'],4),T=round(x['T'],1)) for x in so])
    df=pd.DataFrame(all_rows)
    df.to_csv(os.path.join(RES,'q1_grouping.csv'),index=False,encoding='utf-8-sig')
    json.dump(detail,open(os.path.join(RES,'q1_grouping_detail.json'),'w'),ensure_ascii=False,indent=1)

    print('=== 问题一: 组批结果 ===')
    print(df.to_string(index=False))
    tot_s=df['n_sortie'].sum(); tot_E=df['E'].sum(); tot_T=df['T'].sum()
    print(f'\n合计: 架次={tot_s}, 总能耗={tot_E:.3f} kWh, 累计作业时间={tot_T:.0f} s ({tot_T/3600:.2f} h)')
    print('\n=== 机型选用统计 ===')
    print(df['model'].value_counts().to_dict())

if __name__=='__main__':
    main()
