"""T1.1 最大安全载荷反解"""
import numpy as np, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import *

def round_trip_energy(g, d, h_up, h_dn, q):
    """往返 O01->Si->O01 总能耗(kWh)
    去程载荷 q；回程空载(已交付)。
    采用【等效航程锚定】口径：由题面 L_g(q) 关系反推"该载荷下的单位距离能量"，
    使 q=0 时恰好可飞 L0、q=Qmax 时恰好可飞 LF（与题目给定航程口径自洽）。
    爬升项按 m*g*h/(eta_up) 单独计入（题目明示"下降能耗效率取0"）。
    """
    p = TRANSPORT[g]
    m_empty = p['m_empty']
    E_avail = (1 - p['rho']) * p['Euse']
    # 单位距离水平能耗 (kWh/m)，由等效航程锚定：
    #   q=0    -> L0  (空载可飞 L0)  => e0 = E_avail / L0
    #   q=Qmax -> LF  (满载可飞 LF)  => eF = E_avail / LF
    e0 = E_avail / p['L0']
    eF = E_avail / p['LF']
    w = float(np.clip(q / p['qmax'], 0, 1)) if p['qmax'] > 0 else 0.0
    e_hor_go = e0 + (eF - e0) * w          # 去程单位距离能耗(带载 q)
    # 去程: 爬升(带载) + 水平(带载)
    E_go_up = (m_empty + q) * G * h_up / (p['eta_up'] * 3.6e6)
    E_go_hor = e_hor_go * d
    # 回程: 空载 -> 从服务区作业高度(地面+30m)爬回巡航海拔，再水平飞回
    E_back_up = m_empty * G * h_dn / (p['eta_up'] * 3.6e6)
    E_back_hor = e0 * d
    return E_go_up + E_go_hor + E_back_up + E_back_hor

def max_payload(g, d, h_up, h_dn):
    p = TRANSPORT[g]
    E_avail = (1 - p['rho']) * p['Euse']
    lo, hi = 0.0, p['qmax']
    if round_trip_energy(g, d, h_up, h_dn, 0.0) > E_avail:
        return 0.0   # 空载都飞不到
    if round_trip_energy(g, d, h_up, h_dn, hi) <= E_avail:
        return hi    # 满载荷可行
    for _ in range(60):
        mid = (lo + hi) / 2
        if round_trip_energy(g, d, h_up, h_dn, mid) <= E_avail:
            lo = mid
        else:
            hi = mid
    return lo

if __name__ == '__main__':
    dem = DEM(); O, svcs = load_nodes()
    geom = json.load(open(os.path.join(RES, 'common_leg_geometry.json')))
    rows = []
    print(f"{'服务区':<7}{'机型':<5}{'d(m)':>9}{'h_up':>8}{'E_avail':>9}{'q_max(kg)':>11}{'体积限(kg)':>11}{'有效限':>9}")
    for s in svcs:
        gg = geom[s['id']]
        for g in ['A','B','C']:
            qe = max_payload(g, gg['d'], gg['h_up'], gg['h_dn'])
            p = TRANSPORT[g]
            # 体积约束折算为等价载重（按各箱最大密度估计，见后）
            rows.append(dict(svc=s['id'], model=g, d=gg['d'], h_up=gg['h_up'], h_dn=gg['h_dn'],
                             E_avail=(1-p['rho'])*p['Euse'], q_energy=qe, vol=p['vol'], qmax=p['qmax']))
    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RES,'q1_payload_cap.csv'), index=False, encoding='utf-8-sig')
    piv = df.pivot(index='svc', columns='model', values='q_energy').round(2)
    print(piv)
    print('\n✅ results/q1_payload_cap.csv')
