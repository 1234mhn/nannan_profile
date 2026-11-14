"""
D题 公共模块 (T0)
- DEM 读取与采样
- 节点坐标与距离计算
- 航段几何（巡航海拔、爬升/下降高度）
- 三机型/中继机参数
- 飞行时间与能耗模型
- 电池两阶段充电模型
"""
import numpy as np
import scipy.io as sio
import json, os
from math import radians, sin, cos, asin, sqrt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, '数据')
RES  = os.path.join(BASE, 'results')
os.makedirs(RES, exist_ok=True)

R_EARTH = 6371000.0
G = 9.80665  # m/s^2

# ---------------- DEM ----------------
class DEM:
    def __init__(self, path=None):
        path = path or os.path.join(DATA, '镇龙乡地理空间数据/镇龙乡及周边30米DEM.mat')
        d = sio.loadmat(path)
        self.dem = d['dem'].astype(np.float64)          # (1309, 1486)
        self.lat = d['latitude'].ravel().astype(np.float64)   # 递减
        self.lon = d['longitude'].ravel().astype(np.float64)  # 递增
        self.nodata = float(d['nodata'][0, 0])
        self.transform = d['transform'].ravel()
        self.valid = self.dem != self.nodata

    def _idx(self, lon, lat):
        """经纬度数组 -> (row, col) 索引（向量化）"""
        lon = np.atleast_1d(np.asarray(lon, dtype=float))
        lat = np.atleast_1d(np.asarray(lat, dtype=float))
        # lat 递减，用 -lat 做 searchsorted
        r = np.searchsorted(-self.lat, -lat, side='left')
        c = np.searchsorted(self.lon, lon, side='left')
        r = np.clip(r - 0, 0, self.dem.shape[0] - 1)
        c = np.clip(c - 0, 0, self.dem.shape[1] - 1)
        # searchsorted 'left' 给出插入点，取最近像元
        r2 = np.clip(r, 0, self.dem.shape[0] - 1)
        c2 = np.clip(c, 0, self.dem.shape[1] - 1)
        return r2, c2

    def sample(self, lon, lat):
        """采样单点高程"""
        r, c = self._idx(lon, lat)
        return self.dem[r, c].ravel()

    def profile(self, lon1, lat1, lon2, lat2, n=400):
        """沿线剖面（含两端点）"""
        lons = np.linspace(lon1, lon2, n)
        lats = np.linspace(lat1, lat2, n)
        return lons, lats, self.sample(lons, lats)

# ---------------- 坐标/距离 ----------------
def haversine(lon1, lat1, lon2, lat2):
    """水平大圆距离(m)，向量化"""
    lon1, lat1, lon2, lat2 = map(np.asarray, (lon1, lat1, lon2, lat2))
    dlon = np.radians(lon2 - lon1); dlat = np.radians(lat2 - lat1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dlon/2)**2
    return 2*R_EARTH*np.arcsin(np.sqrt(np.clip(a, 0, 1)))

# ---------------- 机型参数 ----------------
TRANSPORT = {
    'A': dict(name='中轻载标准测试多旋翼', m_empty=70.0, qmax=25.0, vol=0.06,
              vc=12.0, L0=25000.0, LF=20000.0, Euse=4.5, rho=0.20,
              t_prep=300.0, t_load_per_box=30.0, t_hand_base=150.0, t_hand_per_box=30.0,
              vup=3.0, vdn=2.5, eta_up=0.72, eta_dn=0.0),
    'B': dict(name='中载标准测试多旋翼', m_empty=65.0, qmax=30.0, vol=0.073,
              vc=15.0, L0=28000.0, LF=16000.0, Euse=4.0, rho=0.20,
              t_prep=300.0, t_load_per_box=30.0, t_hand_base=150.0, t_hand_per_box=30.0,
              vup=3.0, vdn=2.5, eta_up=0.72, eta_dn=0.0),
    'C': dict(name='重载标准测试多旋翼', m_empty=69.9, qmax=80.0, vol=0.25,
              vc=15.0, L0=26000.0, LF=12000.0, Euse=8.0, rho=0.20,
              t_prep=300.0, t_load_per_box=30.0, t_hand_base=180.0, t_hand_per_box=36.0,
              vup=2.5, vdn=2.0, eta_up=0.72, eta_dn=0.0),
}
RELAY = dict(name='中继标准测试多旋翼', m_empty=21.0, m_comm=2.5, m_takeoff=23.5,
             vc=15.0, Pc=1.15, Euse=3.2, rho=0.20,
             t_prep=180.0, t_link=30.0, t_turn=300.0, vup=4.0, vdn=3.0,
             eta_up=0.72, eta_dn=0.0, P_hover=1.05, P_comm=0.05, h_max=300.0)

UAV_FLEET = [('U01','A'),('U02','A'),('U03','A'),('U04','A'),
             ('U05','B'),('U06','B'),('U07','C'),('U08','C')]
BATTERY_STOCK = {'A': (6, 1800.0), 'B': (4, 2400.0), 'C': (4, 3000.0)}

COMM = dict(f=2400.0, Lsys=3.0, Lobs=10.0, Psens=-98.0, M=8.0,
            Pt_tuav=20.0, G_tuav=3.0,
            Pt_relay_in=20.0, G_relay_in=6.0,
            Pt_relay_back=19.0, G_relay_back=8.0,
            Pt_gw=27.0, G_gw=12.0, h_gw=20.0)

# ---------------- 飞行与能耗 ----------------
def equiv_range(g, q):
    """等效航程 L_g(q) = L0 - (L0-LF)*q^1.5/Q^1.5"""
    p = TRANSPORT[g]
    q = np.clip(q, 0, p['qmax'])
    return p['L0'] - (p['L0'] - p['LF']) * (q ** 1.5) / (p['qmax'] ** 1.5)

def status_height(g, ground_elev):
    """作业高度: O01=地面海拔；服务区=地面+30m"""
    return ground_elev

def leg_geometry(dem, lon1, lat1, e1, lon2, lat2, e2, h_op2_offset=0.0):
    """航段几何: 返回水平距离 d, 巡航海拔 h_cru, 爬升 h+, 下降 h-"""
    d = float(haversine(lon1, lat1, lon2, lat2))
    _, _, prof = dem.profile(lon1, lat1, lon2, lat2, n=max(50, int(d/30)))
    h_cru = float(np.max(prof)) + 50.0
    h_up = max(0.0, h_cru - e1)
    h_dn = max(0.0, h_cru - (e2 + h_op2_offset))
    return d, h_cru, h_up, h_dn

def leg_time(g, d, h_up, h_dn):
    p = TRANSPORT[g]
    return h_up/p['vup'] + d/p['vc'] + h_dn/p['vdn']

def leg_energy(g, d, h_up, q, m_takeoff=None):
    """
    航段能耗(kWh)
    水平: 由等效航程/巡航功率推广 -> 采用"单位距离能量"按载荷修正
          水平功率 P_hor(q) = E_hor_unit * vc ，E_hor_unit 由满载/空载航程标定
    爬升: m*g*h/(eta_up*3.6e6)
    """
    p = TRANSPORT[g]
    # 水平能耗系数：以空载标准航程为基准，载荷 q 使能耗线性放大（保守）
    # 空载: 单位距离能耗 e0 (kWh/m)；满载 q=Q 时等效航程 LF，能耗按 vc*t 计
    # 采用: E_hor = (P_hover_equiv(q)) * t_cruise, P 随 q 增
    # 标定: 设 Q 载荷下等效航程 LF -> 总能量 Euse*(1-rho) 可飞 LF
    P_cr_empty = 0.55 * p['Euse'] * p['vc'] / p['L0'] * 3.6e6 / 3.6e6  # 占位，见下
    # ---- 采用物理模型 ----
    # 巡航所需功率 ~ 与总质量成正比（旋翼机悬停/巡航诱导功率近似）
    m = (m_takeoff if m_takeoff is not None else p['m_empty']) + q
    m_ref = p['m_empty'] + p['qmax']
    # 用满载标准航程标定"满载巡航功率"
    P_full = p['Euse'] * (1 - p['rho']) * 3.6e6 / p['LF'] * p['vc']  # W  (满载可飞 LF)
    P_empty = p['Euse'] * (1 - p['rho']) * 3.6e6 / p['L0'] * p['vc'] # W
    # 质量插值
    w = (m - p['m_empty']) / p['qmax'] if p['qmax'] > 0 else 0.0
    w = float(np.clip(w, 0, 1))
    P_hor = P_empty + (P_full - P_empty) * w
    t_cru = d / p['vc']
    E_hor = P_hor * t_cru / 3.6e6  # kWh
    # 爬升附加
    E_up = 0.0
    if h_up > 0:
        E_up = m * G * h_up / (p['eta_up'] * 3.6e6)  # kWh
    return E_hor + E_up, E_hor, E_up

def charge_time(soc, T_full):
    """两阶段等效充电时间(s)"""
    s = float(np.clip(soc, 0, 1))
    if s < 0.90:
        return T_full * (0.65 * (0.90 - s) / 0.90 + 0.35)
    else:
        return T_full * 0.35 * (1 - s) / 0.10

# ---------------- 数据加载 ----------------
def load_nodes():
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(DATA, '无人机应急物资运输基础数据/调度中心与服务区.xlsx'), data_only=True)
    ws = wb['数据']
    rows = [r for r in ws.iter_rows(values_only=True)]
    O = dict(id=rows[2][0], name=rows[2][1], lon=rows[2][2], lat=rows[2][3], elev=rows[2][4])
    svcs = []
    for r in rows[6:]:
        if r[0] and str(r[0]).startswith('S'):
            svcs.append(dict(id=r[0], name=r[1], lon=r[2], lat=r[3], elev=r[4], pop=r[5]))
    return O, svcs

def load_boxes():
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(DATA, '无人机应急物资运输基础数据/物资需求与配送时限.xlsx'), data_only=True)
    ws = wb['逐箱货箱清单']
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    boxes = []
    for r in rows:
        if r[0]:
            boxes.append(dict(id=r[0], svc=r[1], type=r[2], m=r[3], v=r[4],
                              first=(r[5]=='是'), t_first=r[6], t_exp=r[7], prio=r[8]))
    return boxes

if __name__ == '__main__':
    dem = DEM()
    O, svcs = load_nodes()
    boxes = load_boxes()
    print('DEM', dem.dem.shape, '| O01', O['id'], '| 服务区', len(svcs), '| 货箱', len(boxes))
    # 验证：重算 15 服务区巡航海拔，与报告中 §4 表比对
    out = {}
    print(f"{'服务区':<7}{'d(m)':>9}{'h_max':>9}{'h_cru':>9}{'h_up':>8}")
    for s in svcs:
        d, hc, hu, hd = leg_geometry(dem, O['lon'], O['lat'], O['elev'],
                                     s['lon'], s['lat'], s['elev'], h_op2_offset=30.0)
        out[s['id']] = dict(d=d, h_cru=hc, h_up=hu, h_dn=hd)
        print(f"{s['id']:<7}{d:>9.1f}{hc-50:>9.1f}{hc:>9.1f}{hu:>8.1f}")
    json.dump(out, open(os.path.join(RES, 'common_leg_geometry.json'), 'w'), ensure_ascii=False, indent=1)
    print('\n✅ 已存 results/common_leg_geometry.json')
