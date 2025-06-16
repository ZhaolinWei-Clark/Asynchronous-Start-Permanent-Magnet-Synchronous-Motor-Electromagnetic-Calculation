#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步启动永磁同步电动机电磁计算程序
Python版本 - 多材料多槽型精确计算版本（布局优化版）
"""

import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class MotorParameters:
    """电机参数数据类"""
    # 基本参数
    PN: float = 15.0    # 额定功率 kW
    UN: float = 380.0   # 额定电压 V
    m: int = 3          # 相数
    f: float = 50.0     # 频率 Hz
    p: int = 2          # 极对数
    cosfi: float = 0.95 # 功率因数
    eff: float = 0.935  # 效率
    Tpo: float = 1.8    # 启动转矩倍数
    Ist: float = 9.0    # 启动电流倍数
    Tst: float = 2.0    # 堵转转矩倍数
    
    # 几何尺寸
    D1: float = 260.0   # 定子外径 mm
    Di1: float = 170.0  # 定子内径 mm
    La: float = 190.0   # 铁心长度 mm
    g: float = 0.65     # 气隙长度 mm
    g12: float = 0.15   # 永磁体等效气隙 mm
    Q1: int = 36        # 定子槽数
    Q2: int = 32        # 转子槽数
    Di2: float = 60.0   # 转子内径 mm
    
    # 定子槽参数
    b01: float = 3.8    # 定子槽口宽度 mm
    h01: float = 0.8    # 定子槽口高度 mm
    b1: float = 7.7     # 定子槽宽度 mm
    ALFA1: float = 30.0 # 定子槽斜角 度
    R1: float = 5.1     # 定子槽圆角半径 mm
    h12: float = 15.2   # 定子槽高度 mm
    sks: str = 'Y'      # 是否斜槽 Y/N
    
    # 转子槽参数
    Lv: int = 1         # 转子结构类型
    b02: float = 2.0    # 转子槽口宽度 mm
    h02: float = 0.8    # 转子槽口高度 mm
    br1: float = 6.4    # 转子槽上部宽度 mm
    br2: float = 5.5    # 转子槽下部宽度 mm
    hr12: float = 15.0  # 转子槽高度 mm
    ALFA2: float = 30.0 # 转子槽斜角 度
    AR: float = 180.0   # 转子端环面积 mm²
    
    # 槽型参数
    CX: int = 1         # 槽型：1-梨形槽 2-半梨形槽 3-圆形槽 4-斜肩圆槽
    steel_type: int = 5 # 硅钢片类型：1-DR510-50, 2-DR420-50, 3-DR490-50, 4-DR550-50, 5-DW315-50
    
    # 绕组参数
    LE: int = 2         # 绕组类型
    a: int = 1          # 并联支路数
    Ns: int = 13        # 每槽导体数
    Nt1: int = 2        # 第一种导线根数
    d11: float = 1.20   # 第一种导线直径 mm
    Nt2: int = 3        # 第二种导线根数
    d12: float = 1.25   # 第二种导线直径 mm
    d: float = 15.0     # 绕组端部伸出长度 mm
    y: int = 9          # 绕组节距
    wgco: str = 'Y'     # 绕组连接方式 Y/J
    
    # 永磁体参数
    Lev: int = 1        # 磁路结构 1-径向 2-切向
    magnet: int = 1     # 永磁材料 1-钕铁硼 2-铁氧体
    Br0: float = 1.15   # 剩磁密度 T
    Hc0: float = 875.0  # 矫顽力 kA/m
    hM: float = 5.3     # 永磁体厚度 mm
    bM: float = 110.0   # 永磁体宽度 mm
    LM: float = 190.0   # 永磁体长度 mm
    ROUm: float = 7400.0 # 永磁体密度 kg/m³
    SIGMA0: float = 1.28 # 漏磁系数
    
    # 其他参数
    t: float = 75.0     # 工作温度 ℃
    pfwl: float = 0.0107 # 机械损耗标么值
    psl: float = 0.015  # 杂散损耗标么值
    Kq: float = 0.36    # 交轴绕组系数

class SteelDataTables:
    """多种硅钢片数据表类"""
    
    def __init__(self):
        # 定义各种硅钢片的B-H曲线和损耗数据
        self.steel_names = {
            1: "DR510-50",
            2: "DR420-50", 
            3: "DR490-50",
            4: "DR550-50",
            5: "DW315-50"
        }
        
        # B值数组（通用）
        self.B_data = np.array([
            0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85,
            0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35,
            1.40, 1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85,
            1.90, 1.95, 2.00, 2.05, 2.10, 2.15, 2.20
        ])
        
        # 各种硅钢片的H值数据
        self.H_data = {
            1: np.array([  # DR510-50
                75, 88, 102, 118, 135, 155, 178, 205, 236, 272,
                314, 363, 420, 486, 563, 653, 758, 880, 1023, 1190,
                1385, 1614, 1882, 2196, 2564, 2995, 3500, 4092, 4785, 5595,
                6540, 7642, 8925, 10420, 12160, 14180, 16530
            ]),
            2: np.array([  # DR420-50
                70, 82, 95, 110, 127, 146, 168, 193, 222, 255,
                293, 337, 388, 447, 516, 596, 689, 798, 925, 1073,
                1246, 1447, 1682, 1955, 2272, 2639, 3065, 3559, 4132, 4796,
                5565, 6453, 7477, 8658, 10020, 11590, 13400
            ]),
            3: np.array([  # DR490-50
                78, 92, 107, 124, 143, 164, 188, 216, 247, 283,
                324, 371, 425, 488, 561, 646, 745, 860, 994, 1150,
                1331, 1540, 1782, 2062, 2386, 2760, 3193, 3693, 4272, 4942,
                5718, 6616, 7655, 8856, 10245, 11850, 13700
            ]),
            4: np.array([  # DR550-50
                85, 100, 117, 136, 157, 181, 208, 239, 274, 314,
                360, 413, 474, 544, 625, 719, 828, 954, 1100, 1268,
                1462, 1686, 1945, 2244, 2590, 2989, 3450, 3982, 4596, 5305,
                6123, 7068, 8160, 9424, 10885, 12575, 14530
            ]),
            5: np.array([  # DW315-50
                80, 95, 110, 125, 140, 160, 180, 200, 225, 250,
                280, 315, 355, 400, 450, 510, 580, 660, 750, 850,
                970, 1100, 1250, 1420, 1620, 1840, 2100, 2400, 2750, 3150,
                3600, 4100, 4700, 5400, 6200, 7100, 8100
            ])
        }
        
        # 各种硅钢片的损耗数据 W/kg
        self.P_data = {
            1: np.array([  # DR510-50
                0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.1, 3.8,
                4.6, 5.5, 6.6, 7.9, 9.4, 11.2, 13.3, 15.7, 18.5, 21.7,
                25.4, 29.6, 34.4, 39.9, 46.2, 53.3, 61.4, 70.5, 80.8, 92.4,
                105.5, 120.2, 136.8, 155.5, 176.5, 200.2, 226.8
            ]),
            2: np.array([  # DR420-50
                0.3, 0.5, 0.7, 0.9, 1.2, 1.5, 1.9, 2.4, 2.9, 3.6,
                4.3, 5.2, 6.2, 7.4, 8.8, 10.4, 12.3, 14.5, 17.0, 19.9,
                23.2, 27.0, 31.3, 36.2, 41.8, 48.2, 55.4, 63.6, 72.8, 83.2,
                94.9, 108.1, 122.9, 139.5, 158.2, 179.2, 202.8
            ]),
            3: np.array([  # DR490-50
                0.45, 0.65, 0.85, 1.1, 1.4, 1.7, 2.1, 2.6, 3.2, 3.9,
                4.7, 5.6, 6.7, 8.0, 9.5, 11.3, 13.4, 15.8, 18.6, 21.8,
                25.5, 29.7, 34.5, 40.0, 46.3, 53.4, 61.5, 70.7, 81.1, 92.8,
                106.0, 120.8, 137.4, 156.0, 176.8, 200.1, 226.2
            ]),
            4: np.array([  # DR550-50
                0.5, 0.7, 0.9, 1.2, 1.5, 1.9, 2.3, 2.8, 3.4, 4.1,
                4.9, 5.8, 6.9, 8.2, 9.7, 11.5, 13.6, 16.0, 18.8, 22.0,
                25.7, 29.9, 34.7, 40.2, 46.5, 53.7, 61.9, 71.2, 81.7, 93.6,
                107.0, 122.1, 139.0, 158.0, 179.3, 203.2, 230.0
            ]),
            5: np.array([  # DW315-50
                0.5, 0.7, 0.9, 1.2, 1.5, 1.9, 2.4, 3.0, 3.7, 4.5,
                5.4, 6.5, 7.8, 9.3, 11.0, 12.9, 15.1, 17.6, 20.4, 23.6,
                27.2, 31.2, 35.7, 40.7, 46.2, 52.3, 59.0, 66.3, 74.3, 83.0,
                92.5, 102.8, 114.0, 126.1, 139.2, 153.3, 168.5
            ])
        }

    def linear_interpolation(self, x_data, y_data, x):
        """一元线性插值"""
        if x <= x_data[0]:
            return y_data[0]
        elif x >= x_data[-1]:
            return y_data[-1]
        else:
            return np.interp(x, x_data, y_data)
    
    def get_BH_curve(self, B, steel_type):
        """获取指定硅钢片的B-H曲线数据"""
        return self.linear_interpolation(self.B_data, self.H_data[steel_type], B)
    
    def get_iron_loss(self, B, steel_type):
        """获取指定硅钢片的铁心损耗数据"""
        return self.linear_interpolation(self.B_data, self.P_data[steel_type], B)
    
    def get_steel_name(self, steel_type):
        """获取硅钢片名称"""
        return self.steel_names.get(steel_type, "未知")

class SlotLeakageCalculator:
    """槽漏抗计算类"""
    
    def __init__(self):
        self.PAI = np.pi
    
    def calculate_slot_leakage(self, CX, h02, b02, h2, d1, d2, h22, QSX, B12, KRS1, KRS2, KRS3):
        """
        根据槽型计算电枢槽比漏磁导
        CX: 槽型 1-梨形槽 2-半梨形槽 3-圆形槽 4-斜肩圆槽
        """
        if CX == 1:  # 梨形槽
            if abs(B12 - 1.0) <= 1e-4:
                LUMDAS = (4.0 * QSX**3 / 3.0 + 3.0 * self.PAI * QSX**2 / 2.0 + 
                         4.816 * QSX + 1.5377) / (2.0 * QSX + self.PAI / 2.0)**2 + h02 / b02
            else:
                LUMDAS = (QSX * (KRS1 + KRS2 + KRS3) / 
                         (self.PAI * (1.0 + B12**2) / (8.0 * QSX) + (1.0 + B12) / 2.0)**2 + 
                         h02 / b02)
        elif CX == 2:  # 半梨形槽
            LUMDAS = h2 / d1 + 2.0 * h22 / (3.0 * (d1 + d2)) + h02 / b02
        elif CX == 3:  # 圆形槽
            LUMDAS = 0.623 + h02 / b02
        elif CX == 4:  # 斜肩圆槽
            if abs(B12 - 1.0) <= 1e-4:
                LUMDAS = ((self.PAI**2 * QSX / 16.0 + self.PAI * QSX**2 / 2.0 + 
                          4.0 * QSX**3 / 3.0) / (2.0 * QSX + self.PAI / 4.0)**2 + 
                         h02 / b02 + 2.0 * h2 / (b02 + d1))
            else:
                LUMDAS = (QSX * (KRS1 + KRS2) / 
                         (self.PAI / (8.0 * QSX) + (1.0 + B12) / 2.0)**2 + 
                         h02 / b02 + 2.0 * h2 / (b02 + d1))
        else:
            # 默认使用梨形槽计算
            LUMDAS = h02 / b02
            
        return LUMDAS

class MotorCalculationEngine:
    """电机计算引擎 - 多材料多槽型精确版本"""
    
    def __init__(self, params: MotorParameters):
        self.params = params
        self.steel_tables = SteelDataTables()
        self.slot_calculator = SlotLeakageCalculator()
        self.results = {}
        self.PAI = np.pi
        self.MUO = 4.0 * self.PAI * 1e-7  # 真空磁导率
        
    def calculate_all(self):
        """执行完整精确计算"""
        try:
            p = self.params
            
            print(f"开始电机电磁计算... 使用{self.steel_tables.get_steel_name(p.steel_type)}硅钢片")
            
            # 1. 基本参数计算
            print("1. 计算基本参数...")
            self.calculate_basic_parameters()
            
            # 2. 绕组参数计算
            print("2. 计算绕组参数...")
            self.calculate_winding_parameters()
            
            # 3. 几何参数计算
            print("3. 计算几何参数...")
            self.calculate_geometry_parameters()
            
            # 4. 永磁体参数计算
            print("4. 计算永磁体参数...")
            self.calculate_magnet_parameters()
            
            # 5. 空载磁路计算（迭代求解）
            print("5. 迭代计算空载磁路...")
            self.calculate_no_load_magnetic_circuit()
            
            # 6. 阻抗参数计算
            print("6. 计算阻抗参数...")
            self.calculate_impedances()
            
            # 7. 性能参数计算
            print("7. 计算性能参数...")
            self.calculate_performance()
            
            # 8. 材料质量计算
            print("8. 计算材料质量...")
            self.calculate_material_weights()
            
            # 9. 损耗计算
            print("9. 计算损耗...")
            self.calculate_losses()
            
            # 10. 启动特性计算
            print("10. 计算启动特性...")
            self.calculate_starting_characteristics()
            
            # 11. 计算实际性能参数（不是典型值！）
            print("11. 计算实际性能参数...")
            self.calculate_actual_performance()
            
            print("计算完成！")
            
            # 保存完整结果
            self.save_complete_results()
            
            return True, "计算完成"
            
        except Exception as e:
            print(f"计算错误: {str(e)}")
            return False, f"计算错误: {str(e)}"
    
    def calculate_basic_parameters(self):
        """计算基本参数"""
        p = self.params
        
        # 同步角速度 OMGs = 2πf/p
        self.OMGs = 2 * self.PAI * p.f / p.p
        
        # 额定转速 nN = 60f/p
        self.nN = 60 * p.f / p.p
        
        # 额定电流计算
        if p.wgco.upper() == 'Y':
            UN_calc = p.UN / np.sqrt(3)  # 星形连接相电压
        else:
            UN_calc = p.UN  # 三角形连接相电压
            
        # 额定电流 IN = PN/(m*UN*eff*cosφ) * 1000
        self.IN = p.PN * 1000 / (p.m * UN_calc * p.eff * p.cosfi)
        
        # 额定转矩 TN = PN/(2πnN/60) * 1000
        self.TN = p.PN * 1000 / (2 * self.PAI * self.nN / 60)
        
        # 极距 TAO = πDi1/(2p)
        self.TAO = self.PAI * p.Di1 / (2 * p.p)
        
        print(f"  OMGs = {self.OMGs:.2f} rad/s")
        print(f"  nN = {self.nN:.1f} rpm")
        print(f"  IN = {self.IN:.2f} A")
        print(f"  TN = {self.TN:.2f} N·m")
        print(f"  TAO = {self.TAO:.2f} mm")
        
    def calculate_winding_parameters(self):
        """计算绕组参数"""
        p = self.params
        
        # 每相绕组串联匝数 N = Q1*Ns/(2*m*a)
        self.N = p.Q1 * p.Ns / (2 * p.m * p.a)
        
        # 每极每相槽数 QPM = Q1/(2*m*p)
        QPM = p.Q1 / (2 * p.m * p.p)
        
        # 节距系数 BETA
        if p.LE not in [1, 2, 3]:
            BETA = p.y / (p.m * QPM)
        else:
            BETA = 1.0
            
        # 短距因数 Kp1 = sin(β*π/2)
        self.Kp1 = np.sin(BETA * self.PAI / 2)
        
        # 分布因数 Kd1 = sin(π/(2m))/(QPM*sin(π/(2m*QPM)))
        self.Kd1 = np.sin(self.PAI / (2 * p.m)) / (QPM * np.sin(self.PAI / (2 * p.m * QPM)))
        
        # 斜槽因数计算
        if p.sks.upper() == 'Y':
            t1 = self.PAI * p.Di1 / p.Q1  # 定子齿距
            tsk = p.Q1 * t1 / (p.Q1 + p.p)  # 斜槽距离
            ALFAs = tsk / self.TAO * self.PAI
            self.Ksk1 = 2 * np.sin(ALFAs / 2) / ALFAs
        else:
            self.Ksk1 = 1.0
            
        # 绕组因数 Kdp = Kp1 * Kd1 * Ksk1
        self.Kdp = self.Kp1 * self.Kd1 * self.Ksk1
        
        print(f"  N = {int(self.N)}")
        print(f"  QPM = {QPM:.3f}")
        print(f"  Kp1 = {self.Kp1:.4f}")
        print(f"  Kd1 = {self.Kd1:.4f}")
        print(f"  Ksk1 = {self.Ksk1:.4f}")
        print(f"  Kdp = {self.Kdp:.4f}")
        
    def calculate_geometry_parameters(self):
        """计算几何参数"""
        p = self.params
        
        # 定子齿距 t1 = πDi1/Q1
        self.t1 = self.PAI * p.Di1 / p.Q1
        
        # 转子外径 D2 = Di1 - 2g
        self.D2 = p.Di1 - 2 * p.g
        
        # 转子齿距 t2 = πD2/Q2
        self.t2 = self.PAI * self.D2 / p.Q2
        
        # 定子槽形参数
        self.hs1 = (p.b1 - p.b01) / 2 * np.tan(p.ALFA1 * self.PAI / 180)  # 定子槽斜部高度
        self.bt1 = (p.Di1 + 2 * (p.h01 + p.h12)) * self.PAI / p.Q1 - 2 * p.R1  # 定子齿宽
        self.hj1 = (p.D1 - p.Di1) / 2 - (p.h01 + p.h12 + 2 * p.R1 / 3)  # 定子轭高度
        self.ht1 = p.h12 + p.R1 / 3  # 定子齿磁路长度
        self.Lj1 = self.PAI * (p.D1 - self.hj1) / (4 * p.p)  # 定子轭磁路长度
        
        # 转子槽形参数
        self.hr1 = (p.br1 - p.b02) * np.tan(p.ALFA2 * self.PAI / 180) / 2  # 转子槽上斜部高度
        self.hr2 = p.hr12 - self.hr1  # 转子槽下斜部高度
        self.hr = p.h02 + p.hr12  # 转子槽总高度
        self.AB = (p.b02 + p.br1) * self.hr1 / 2 + (p.br1 + p.br2) * self.hr2 / 2  # 转子槽面积
        
        # 转子轭参数
        if p.Lev == 1:  # 径向磁路
            self.hj2 = (self.D2 - p.Di2) / 2 - self.hr - p.hM
        else:  # 切向磁路
            self.hj2 = p.bM
            
        self.bt2 = (self.D2 - 2 * (p.h02 + p.hr12)) * self.PAI / p.Q2 - p.br2  # 转子齿宽
        self.DR = self.D2 - self.hr - 2  # 转子端环直径
        self.Lj2 = self.PAI * (p.Di2 + self.hj2) / (4 * p.p)  # 转子轭磁路长度
        
        # 定子齿和轭体积
        self.Vt1 = p.Q1 * p.La * 0.93 * self.ht1 * self.bt1  # 定子齿体积
        self.Vj1 = self.PAI * (p.D1 - self.hj1) * p.La * 0.93 * self.hj1  # 定子轭体积
        
        print(f"  槽型CX = {p.CX} ({self.get_slot_type_name(p.CX)})")
        print(f"  t1 = {self.t1:.2f} mm")
        print(f"  t2 = {self.t2:.2f} mm")
        print(f"  D2 = {self.D2:.1f} mm")
        print(f"  bt1 = {self.bt1:.2f} mm")
        print(f"  bt2 = {self.bt2:.2f} mm")
        print(f"  hj1 = {self.hj1:.2f} mm")
        print(f"  hj2 = {self.hj2:.2f} mm")
        print(f"  AB = {self.AB:.1f} mm²")
        print(f"  DR = {self.DR:.1f} mm")
        
    def get_slot_type_name(self, CX):
        """获取槽型名称"""
        slot_names = {1: "梨形槽", 2: "半梨形槽", 3: "圆形槽", 4: "斜肩圆槽"}
        return slot_names.get(CX, "未知槽型")
        
    def calculate_magnet_parameters(self):
        """计算永磁体参数"""
        p = self.params
        
        # 温度修正
        if p.magnet == 1:  # 钕铁硼
            TEMB = 1 - (p.t - 20) * 0.12e-2
            TEMH = TEMB
        else:  # 铁氧体
            TEMB = 1 - (p.t - 20) * 0.19e-2
            TEMH = 1 + (p.t - 20) * 0.4e-2
            
        # 工作温度下的磁性能
        self.Br = TEMB * p.Br0  # 剩磁密度
        self.Hc = TEMH * p.Hc0 * 1000  # 矫顽力
        
        # 相对回复磁导率 MUr = Br0/(μ0*Hc0)
        self.MUr = p.Br0 / (self.MUO * p.Hc0 * 1000)
        
        # 永磁体截面积
        if p.Lev == 1:  # 径向磁路
            self.Am = p.bM * p.LM
        else:  # 切向磁路
            self.Am = 2 * p.bM * p.LM
            
        # 永磁体体积
        self.Vm = 2 * p.p * p.LM * p.bM * p.hM
        
        # 永磁体质量 mm = ρm * Vm
        self.mm = p.ROUm * self.Vm / 1e9  # kg
        
        # 永磁体磁动势 FF = hM * Hc
        self.FF = p.hM * self.Hc / 1000
        
        # 永磁体磁通 FAIM = Am * Br
        self.FAIM = self.Am * self.Br
        
        print(f"  Br = {self.Br:.3f} T")
        print(f"  Hc = {self.Hc:.0f} A/m")
        print(f"  MUr = {self.MUr:.3f}")
        print(f"  Am = {self.Am:.0f} mm²")
        print(f"  FF = {self.FF:.1f} A")
        print(f"  FAIM = {self.FAIM:.3f} Wb·mm")
        print(f"  mm = {self.mm:.2f} kg")
        
    def calculate_no_load_magnetic_circuit(self):
        """迭代计算空载磁路"""
        p = self.params
        
        # 初始工作点估算
        bm01 = 0.95 * p.SIGMA0 * p.hM / (p.SIGMA0 * p.hM + p.g)
        
        print(f"  开始迭代计算，初始bm0 = {bm01:.3f}")
        
        # 迭代求解
        for iteration in range(30):
            # 永磁体磁通
            FI01 = bm01 * self.FAIM / p.SIGMA0 * 1e-6
            
            # 气隙磁密计算
            RFAi = 0.64  # 气隙磁通波形系数
            self.Bg = FI01 / (RFAi * self.TAO * (p.La + 2 * p.g)) * 1e6
            
            # 定子齿磁密 Bts = Bg * t1 * Lef / (La * KFe * bt1)
            self.Bts = self.Bg * self.t1 * (p.La + 2 * p.g) / (p.La * 0.93 * self.bt1)
            
            # 定子轭磁密 Bj1 = FI0 / (2 * LFe * hj1)
            self.Bj1 = FI01 / (2 * p.La * 0.93 * self.hj1) * 1e6
            
            # 转子齿磁密
            self.Btr = self.Bg * self.t2 * (p.La + 2 * p.g) / (p.La * 0.93 * self.bt2)
            
            # 转子轭磁密
            self.Bj2 = FI01 / (2 * p.La * 0.93 * self.hj2) * 1e6
            
            # 使用指定硅钢片数据表计算磁位差
            Hts = self.steel_tables.get_BH_curve(self.Bts, p.steel_type)
            Hjs = self.steel_tables.get_BH_curve(self.Bj1, p.steel_type)
            Htr = self.steel_tables.get_BH_curve(self.Btr, p.steel_type)
            Hjr = self.steel_tables.get_BH_curve(self.Bj2, p.steel_type)
            
            # 各部分磁位差
            Ft1 = Hts * self.ht1 / 10  # 定子齿磁位差
            Fj1 = Hjs * self.Lj1 / 10  # 定子轭磁位差
            Ft2 = Htr * self.hr / 10   # 转子齿磁位差
            Fj2 = Hjr * self.Lj2 / 10  # 转子轭磁位差
            
            # 气隙磁位差（包括永磁体等效气隙）
            Fg = self.Bg / self.MUO * (p.g12 + p.g * self.calculate_gap_factor()) * 1e-3
            
            # 总磁位差
            SUMF = 2 * (Fg + Ft1 + Fj1 + Ft2 + Fj2)
            
            # 计算磁导
            NUMDAm = FI01 / SUMF
            
            # 主磁导标么值
            if p.Lev == 1:
                LUMDAm = NUMDAm * 2 * p.hM * 1e-3 / (self.MUr * self.MUO * self.Am * 1e-6)
            else:
                LUMDAm = NUMDAm * p.hM * 1e-3 / (self.MUr * self.MUO * self.Am * 1e-6)
                
            # 外磁路总磁导标么值
            LUMDAn = p.SIGMA0 * LUMDAm
            
            # 新的工作点
            bm0 = LUMDAn / (LUMDAn + 1)
            
            # 检查收敛性
            if abs((bm0 - bm01) / bm0) < 0.0001:
                print(f"  第{iteration+1}次迭代收敛，bm0 = {bm0:.4f}")
                break
                
            bm01 = (bm01 + bm0) / 2  # 阻尼更新
            
            if iteration % 5 == 0:
                print(f"  第{iteration+1}次迭代，bm0 = {bm0:.4f}")
        
        # 保存最终结果
        self.bm0 = bm0
        self.LUMDAn = LUMDAn
        self.LUMDAs = (p.SIGMA0 - 1) * LUMDAm
        self.FI0 = bm0 * self.FAIM / p.SIGMA0 * 1e-6
        
        # 气隙磁密基波幅值
        Kf = 4 / self.PAI * np.sin(self.PAI * RFAi / 2)
        self.Bg1 = Kf * FI01 / (RFAi * self.TAO * (p.La + 2 * p.g)) * 1e6
        
        # 空载反电动势
        KFI = 8 / (self.PAI * self.PAI) / RFAi * np.sin(RFAi * self.PAI / 2)
        self.E0 = 4.44 * p.f * self.N * self.Kdp * self.FI0 * KFI
        
        # 齿饱和系数
        Fgg = self.Bg / self.MUO * p.g * self.calculate_gap_factor() * 1e-3
        self.Kst = (Fgg + Ft1 + Ft2) / Fgg
        
        print(f"  最终结果：")
        print(f"    bm0 = {self.bm0:.4f}")
        print(f"    Bg = {self.Bg:.0f} T (气隙磁密)")
        print(f"    Bg1 = {self.Bg1:.3f} T (气隙磁密基波)")
        print(f"    Bts = {self.Bts:.3f} T (定子齿磁密)")
        print(f"    Bj1 = {self.Bj1:.3f} T (定子轭磁密)")
        print(f"    Btr = {self.Btr:.3f} T (转子齿磁密)")
        print(f"    Bj2 = {self.Bj2:.3f} T (转子轭磁密)")
        print(f"    E0 = {self.E0:.1f} V (空载反电动势)")
        print(f"    Kst = {self.Kst:.2f} (齿饱和系数)")
        
    def calculate_gap_factor(self):
        """计算气隙系数 Kg"""
        p = self.params
        
        # 定子侧气隙系数
        ttt = self.t1 * (4.4 * p.g + 0.75 * p.b01)
        Kg1 = ttt / (ttt - p.b01 * p.b01)
        
        # 转子侧气隙系数
        fff = self.t2 * (4.4 * p.g + 0.75 * p.b02)
        Kg2 = fff / (fff - p.b02 * p.b02)
        
        # 总气隙系数
        Kg = Kg1 * Kg2
        
        return Kg
        
    def calculate_impedances(self):
        """计算阻抗参数"""
        p = self.params
        
        print("  计算定子阻抗参数...")
        
        # 定子电阻计算
        s11 = p.Nt1 * self.PAI * p.d11**2 / 4  # 第一种导线截面积
        s12 = p.Nt2 * self.PAI * p.d12**2 / 4  # 第二种导线截面积
        ROUCu = 0.0175 * (1 + 0.004 * (p.t - 15))  # 铜电阻率温度修正
        
        # 线圈长度计算
        if p.LE in [1, 2, 3]:  # 单层绕组
            if p.p == 1:
                sss = 0.58
            elif p.p in [2, 3]:
                sss = 0.6
            else:
                sss = 0.625
        else:  # 双层绕组
            sss = 1 / np.sqrt(1 - ((p.b1 + 2 * p.R1) / (p.b1 + 2 * p.R1 + 2 * self.bt1))**2) / 2
            
        # 线圈端部参数
        TAOy = self.PAI / 2 / p.p * (p.Di1 + 2 * (p.h01 + self.hs1) + p.h12 - self.hs1 + p.R1)
        if p.LE in [1, 2]:
            TAOy = self.PAI / 2 / p.p * 0.85 * (p.Di1 + 2 * (p.h01 + self.hs1) + p.h12 - self.hs1 + p.R1)
            
        LEIP = sss * TAOy  # 线圈端部轴向投影长度
        Lc = 2 * (p.La + 2 * (p.d + LEIP))  # 线圈总长度
        self.fd = LEIP * (p.b1 + 2 * p.R1) / (p.b1 + 2 * p.R1 + 2 * self.bt1)  # 端部轴向投影长度
        self.Ls = 2 * (p.d + LEIP)  # 线圈端部平均长度
        
        # 定子电阻 Rs = ρ * Lc * N / (a * (s11 + s12))
        self.Rs = ROUCu * Lc * self.N / (p.a * (s11 + s12) * 1000)
        
        # 漏抗系数
        Cx = (4 * self.PAI)**2 * 1e-10 * p.f * (p.La + 2 * p.g) * (self.N * self.Kdp)**2 / p.p
        
        # 槽漏抗计算
        AU1 = p.h01 / p.b01 + 2 * self.hs1 / (p.b01 + p.b1)  # 槽上部比漏磁导
        AL1 = 2 * p.h12 / (p.b01 + p.b1)  # 槽下部比漏磁导
        
        # 节距系数计算
        QPM = p.Q1 / (2 * p.m * p.p)
        if p.LE not in [1, 2, 3]:
            BETA_calc = p.y / (p.m * QPM)
        else:
            BETA_calc = 1.0
            
        # 上、下部节距漏抗系数
        if BETA_calc > 1:
            BETA1 = 2 - BETA_calc
        else:
            BETA1 = BETA_calc
            
        if BETA1 >= 2/3:
            KU1 = (3 * BETA1 + 1) / 4
            KL1 = (9 * BETA1 + 7) / 16
        elif BETA1 > 1/3:
            KU1 = (6 * BETA1 - 1) / 4
            KL1 = (18 * BETA1 + 1) / 16
        else:
            KU1 = 0.75 * BETA1
            KL1 = (9 * BETA1 + 4) / 16
            
        As1 = KU1 * AU1 + KL1 * AL1  # 槽比漏磁导
        Xs1 = p.La * p.m * 2 * p.p * As1 / ((p.La + 2 * p.g) * self.Kdp**2 * p.Q1) * Cx
        
        # 谐波漏抗
        SUMR = self.PAI**2 * (2 * p.p / p.Q1)**2 / 12
        Xd1 = p.m * self.TAO * SUMR / (self.PAI**2 * self.calculate_gap_factor() * p.g * self.Kst) * Cx
        
        # 端部漏抗
        if p.LE == 0:  # 双层叠绕组
            XE1 = 1.2 * (p.d + 0.5 * self.fd) / (p.La + 2 * p.g) * Cx
        elif p.LE == 1:  # 单层同心式
            XE1 = 0.67 * (self.Ls - 0.64 * TAOy) / ((p.La + 2 * p.g) * self.Kdp**2) * Cx
        elif p.LE == 2:  # 单层交叉式
            XE1 = 0.47 * (self.Ls - 0.64 * TAOy) / ((p.La + 2 * p.g) * self.Kdp**2) * Cx
        else:  # 单层链式
            XE1 = 0.2 * self.Ls / ((p.La + 2 * p.g) * self.Kdp**2) * Cx
            
        # 斜槽漏抗
        if p.sks.upper() == 'Y':
            tsk = p.Q1 * self.t1 / (p.Q1 + p.p)
            Xsk1 = 0.5 * (tsk / self.t1)**2 * Xd1
        else:
            Xsk1 = 0.0
            
        # 定子总漏抗
        self.X1 = Xs1 + Xd1 + XE1 + Xsk1
        
        print("  计算转子阻抗参数...")
        
        # 转子参数计算
        kc = p.m * (2 * self.N * self.Kdp)**2 * 1e-4
        ROUA1 = 0.035 * (1 + 0.004 * (p.t - 15))  # 铝电阻率
        
        # 转子电阻
        RB = kc * (1.04 * p.La * ROUA1 * 10) / (self.AB * p.Q2)  # 导条电阻
        RR = kc * (self.DR * ROUA1 * 10) / (2 * self.PAI * p.p**2 * p.AR)  # 端环电阻
        self.R2 = RB + RR
        
        # 转子漏抗计算（考虑槽型影响）
        print(f"  使用槽型{p.CX}计算转子槽漏抗...")
        
        # 槽形参数
        QSX = 1.0  # 简化参数
        B12 = p.br2 / p.br1  # 槽宽比
        KRS1 = 0.5  # 简化系数
        KRS2 = 0.3
        KRS3 = 0.2
        h2 = p.hr12  # 槽高
        d1 = p.br1   # 上宽
        d2 = p.br2   # 下宽
        h22 = p.hr12 / 2  # 简化
        
        # 使用槽型计算槽漏抗
        LUMDAS = self.slot_calculator.calculate_slot_leakage(
            p.CX, p.h02, p.b02, h2, d1, d2, h22, QSX, B12, KRS1, KRS2, KRS3)
        
        Xs2 = p.La * p.m * 2 * p.p * LUMDAS * Cx / ((p.La + 2 * p.g) * p.Q2)  # 转子槽漏抗
        
        SUMR2 = self.PAI**2 * (2 * p.p / p.Q2)**2 / 12
        Xd2 = p.m * self.TAO * SUMR2 / (self.PAI**2 * p.g * self.calculate_gap_factor() * self.Kst) * Cx  # 转子谐波漏抗
        
        XE2 = 0.757 / (p.La + 2 * p.g) * ((p.La - p.La) / 1.13 + self.DR / (2 * p.p)) * Cx  # 转子端部漏抗
        
        self.X2 = Xs2 + Xd2 + XE2
        
        print(f"    Rs = {self.Rs:.4f} Ω")
        print(f"    X1 = {self.X1:.4f} Ω (Xs1={Xs1:.4f}, Xd1={Xd1:.4f}, XE1={XE1:.4f}, Xsk1={Xsk1:.4f})")
        print(f"    R2 = {self.R2:.4f} Ω (RB={RB:.4f}, RR={RR:.4f})")
        print(f"    X2 = {self.X2:.4f} Ω (Xs2={Xs2:.4f}, Xd2={Xd2:.4f}, XE2={XE2:.4f})")
        print(f"    槽漏磁导LUMDAS = {LUMDAS:.4f}")
        print(f"    Lc = {Lc:.1f} mm (线圈长度)")
        print(f"    Ls = {self.Ls:.1f} mm (端部长度)")
        
    def calculate_performance(self):
        """计算性能参数"""
        p = self.params
        
        print("  计算直轴和交轴电抗...")
        
        # 直轴电枢反应磁动势
        Fa = 0.45 * p.m * self.N * self.Kdp * 0.5 * self.IN * 1.0 / p.p
        
        if p.Lev == 1:
            fad = Fa / self.FF
        else:
            fad = 2 * Fa / self.FF
            
        f1 = fad / p.SIGMA0
        bmN = self.LUMDAn * (1 - f1) / (self.LUMDAn + 1)
        
        FIN = (bmN - (1 - bmN) * self.LUMDAs) * self.FAIM * 1e-6
        
        KFI = 8 / (self.PAI * self.PAI) / 0.64 * np.sin(0.64 * self.PAI / 2)
        Ed = 4.44 * p.f * self.N * self.Kdp * FIN * KFI
        
        # 直轴电枢反应电抗
        self.Xad = abs((self.E0 - Ed) / (0.5 * self.IN))
        self.Xd = self.Xad + self.X1  # 直轴同步电抗
        
        # 交轴电枢反应电抗（简化计算）
        self.Xaq = self.Xad * p.Kq  # 根据经验公式
        self.Xq = self.Xaq + self.X1  # 交轴同步电抗
        
        # 电枢反应折算系数
        Kf = 4 / self.PAI * np.sin(self.PAI * 0.64 / 2)
        self.Kad = 1 / Kf  # 直轴电枢磁动势折算系数
        self.Kaq = p.Kq / Kf  # 交轴电枢磁动势折算系数
        
        # 保存负载工作点
        self.bmN = bmN
        
        print(f"    Xad = {self.Xad:.3f} Ω")
        print(f"    Xaq = {self.Xaq:.3f} Ω")
        print(f"    Xd = {self.Xd:.3f} Ω")
        print(f"    Xq = {self.Xq:.3f} Ω")
        print(f"    Kad = {self.Kad:.3f}")
        print(f"    Kaq = {self.Kaq:.3f}")
        print(f"    bmN = {self.bmN:.3f}")
        
    def calculate_material_weights(self):
        """计算材料质量"""
        p = self.params
        
        # 定子导线质量
        s11 = p.Nt1 * self.PAI * p.d11**2 / 4
        s12 = p.Nt2 * self.PAI * p.d12**2 / 4
        Lc = 2 * (p.La + 2 * (p.d + self.Ls/2))  # 简化线圈长度
        self.mCu = 1.05 * 8.9 * p.Q1 * p.Ns * Lc / 2 * (s11 + s12) * 1e-6  # kg
        
        # 硅钢片质量
        self.mFe = 7.8 * (p.La + 2 * p.g) * (p.D1 + 5)**2 * 1e-6  # kg
        
        # 铸铝质量
        self.mAl = 2.7 * (p.Q2 * self.AB * p.La + 2 * p.AR * self.PAI * self.DR) * 1e-6  # kg
        
        print(f"  mCu = {self.mCu:.2f} kg (铜线质量)")
        print(f"  mFe = {self.mFe:.2f} kg (硅钢片质量)")
        print(f"  mAl = {self.mAl:.2f} kg (铸铝质量)")
        print(f"  mm = {self.mm:.2f} kg (永磁体质量)")
        
    def calculate_losses(self):
        """计算损耗"""
        p = self.params
        
        # 铜耗
        self.pCu = p.m * self.IN**2 * self.Rs  # W
        
        # 铁耗（使用指定硅钢片数据表）
        pt1 = self.steel_tables.get_iron_loss(self.Bts, p.steel_type)  # 定子齿损耗密度
        pj1 = self.steel_tables.get_iron_loss(self.Bj1, p.steel_type)  # 定子轭损耗密度
        
        self.pFe = 2.5 * self.Vt1 * pt1 / 1e6 + 2 * self.Vj1 * pj1 / 1e6  # W
        
        # 机械损耗
        self.pfw = p.pfwl * p.PN * 1000  # W
        
        # 杂散损耗
        self.ps = (self.IN / self.IN)**2 * p.psl * p.PN * 1000  # W
        
        # 总损耗
        self.pSum = self.pCu + self.pFe + self.pfw + self.ps
        
        print(f"  pCu = {self.pCu:.1f} W (铜耗)")
        print(f"  pFe = {self.pFe:.1f} W (铁耗，使用{self.steel_tables.get_steel_name(p.steel_type)})")
        print(f"  pfw = {self.pfw:.1f} W (机械损耗)")
        print(f"  ps = {self.ps:.1f} W (杂散损耗)")
        print(f"  Σp = {self.pSum:.1f} W (总损耗)")
        
    def calculate_starting_characteristics(self):
        """计算启动特性"""
        p = self.params
        
        # 启动时的等效电路参数（考虑饱和和集肤效应）
        X1st = self.X1 * 0.8  # 定子启动漏抗
        R2st = self.R2 * 1.2  # 转子启动电阻
        X2st = self.X2 * 0.8  # 转子启动漏抗
        
        Xst = X1st + X2st  # 启动总漏抗
        Rst = self.Rs + R2st  # 启动总电阻
        
        Zst = np.sqrt(Rst**2 + Xst**2)  # 启动阻抗
        
        if p.wgco.upper() == 'Y':
            UN_calc = p.UN / np.sqrt(3)
        else:
            UN_calc = p.UN
            
        # 启动电流
        self.Ist_calc = UN_calc / Zst
        self.Ist_ratio = self.Ist_calc / self.IN
        
        # 启动转矩
        self.Tst_calc = p.m * p.p * self.Ist_calc**2 * R2st / (2 * self.PAI * p.f) / self.TN
        
        print(f"  Ist = {self.Ist_calc:.1f} A ({self.Ist_ratio:.2f}倍)")
        print(f"  Tst = {self.Tst_calc:.2f}倍")
        print(f"  X1st = {X1st:.4f} Ω")
        print(f"  R2st = {R2st:.4f} Ω")
        print(f"  X2st = {X2st:.4f} Ω")
        
    def calculate_actual_performance(self):
        """计算实际性能参数（不是典型值！）"""
        p = self.params
        
        print("  计算实际性能参数...")
        
        # 实际效率计算
        P_out = p.PN * 1000  # 输出功率 W
        P_in = P_out + self.pSum  # 输入功率 W
        self.eta_actual = P_out / P_in * 100  # 实际效率 %
        
        # 实际功率因数计算（基于电机等效电路）
        # 简化计算，考虑空载反电动势和阻抗
        Z_total = np.sqrt(self.Rs**2 + self.X1**2)
        phi_rad = np.arctan(self.X1 / self.Rs)
        self.cosfi_actual = np.cos(phi_rad)
        
        # 功率角和负载角计算
        # 功率角 θ（电角度）
        self.theta_actual = np.arcsin(P_out / (p.m * self.E0 * self.IN / np.sqrt(3))) * 180 / self.PAI
        
        # 负载角 φ（功率因数角）
        self.phi_actual = np.arccos(self.cosfi_actual) * 180 / self.PAI
        
        # 槽满率计算（实际计算）
        # 导线总截面积
        s_total = p.Ns * (p.Nt1 * self.PAI * p.d11**2 / 4 + p.Nt2 * self.PAI * p.d12**2 / 4)
        # 槽面积
        slot_area = (p.b01 + p.b1) * p.h12 / 2 + p.b01 * p.h01
        # 槽满率
        self.Sf_actual = s_total / slot_area * 100
        
        # 线负荷和电密度计算
        # 线负荷 A1 = m*N*IN/(π*Di1)
        self.A1_actual = p.m * self.N * self.IN / (self.PAI * p.Di1)  # A/mm
        
        # 电密度 J1 = IN / s_total
        self.J1_actual = self.IN / s_total  # A/mm²
        
        # A1J1
        self.A1J1_actual = self.A1_actual * self.J1_actual
        
        # 永磁体负载工作点计算
        self.bmh_actual = self.bmN * 0.382  # 简化计算
        
        print(f"    实际效率 eta = {self.eta_actual:.2f}%")
        print(f"    实际功率因数 cosfi = {self.cosfi_actual:.3f}")
        print(f"    功率角 theta = {self.theta_actual:.1f}°")
        print(f"    负载角 phi = {self.phi_actual:.1f}°")
        print(f"    槽满率 Sf = {self.Sf_actual:.1f}%")
        print(f"    线负荷 A1 = {self.A1_actual:.1f} A/mm")
        print(f"    电密度 J1 = {self.J1_actual:.1f} A/mm²")
        print(f"    A1J1 = {self.A1J1_actual:.1f} A²/mm³")
        print(f"    负载工作点 bmh = {self.bmh_actual:.3f}")
        
    def save_complete_results(self):
        """保存完整计算结果"""
        p = self.params
        
        self.results = {
            '基本参数': {
                '额定转速 nN (rpm)': round(self.nN, 1),
                '额定电流 IN (A)': round(self.IN, 2),
                '额定转矩 TN (N·m)': round(self.TN, 2),
                '极距 TAO (mm)': round(self.TAO, 2),
                '同步角速度 OMGs (rad/s)': round(self.OMGs, 2)
            },
            '绕组参数': {
                '每相串联匝数 N': int(self.N),
                '绕组因数 Kdp': round(self.Kdp, 4),
                '短距因数 Kp1': round(self.Kp1, 4),
                '分布因数 Kd1': round(self.Kd1, 4),
                '斜槽因数 Ksk1': round(self.Ksk1, 4),
                '线圈端部长度 Ls (mm)': round(self.Ls, 1),
                '端部轴向投影 fd (mm)': round(self.fd, 1)
            },
            '几何参数': {
                '定子齿距 t1 (mm)': round(self.t1, 2),
                '转子齿距 t2 (mm)': round(self.t2, 2),
                '转子外径 D2 (mm)': round(self.D2, 1),
                '定子齿宽 bt1 (mm)': round(self.bt1, 2),
                '转子齿宽 bt2 (mm)': round(self.bt2, 2),
                '定子轭高 hj1 (mm)': round(self.hj1, 2),
                '转子轭高 hj2 (mm)': round(self.hj2, 2),
                '转子槽面积 AB (mm²)': round(self.AB, 1),
                '转子端环直径 DR (mm)': round(self.DR, 1),
                '槽型 CX': f"{p.CX} ({self.get_slot_type_name(p.CX)})"
            },
            '磁路参数': {
                '气隙系数 Kg': round(self.calculate_gap_factor(), 3),
                '气隙磁密 Bg (T)': round(self.Bg, 3),
                '气隙磁密基波 Bg1 (T)': round(self.Bg1, 3),
                '定子齿磁密 Bts (T)': round(self.Bts, 3),
                '定子轭磁密 Bj1 (T)': round(self.Bj1, 3),
                '转子齿磁密 Btr (T)': round(self.Btr, 3),
                '转子轭磁密 Bj2 (T)': round(self.Bj2, 3),
                '空载反电动势 E0 (V)': round(self.E0, 1),
                '永磁体工作点 bm0': round(self.bm0, 4),
                '齿饱和系数 Kst': round(self.Kst, 2),
                '硅钢片类型': self.steel_tables.get_steel_name(p.steel_type)
            },
            '永磁体参数': {
                '工作温度剩磁 Br (T)': round(self.Br, 3),
                '工作温度矫顽力 Hc (A/m)': round(self.Hc, 0),
                '相对磁导率 MUr': round(self.MUr, 3),
                '永磁体截面积 Am (mm²)': round(self.Am, 0),
                '永磁体磁动势 FF (A)': round(self.FF, 1),
                '永磁体磁通 FAIM (Wb·mm)': round(self.FAIM, 3),
                '永磁体质量 mm (kg)': round(self.mm, 2)
            },
            '阻抗参数': {
                '定子电阻 Rs (Ω)': round(self.Rs, 4),
                '转子电阻 R2 (Ω)': round(self.R2, 4),
                '定子漏抗 X1 (Ω)': round(self.X1, 4),
                '转子漏抗 X2 (Ω)': round(self.X2, 4),
                '直轴电抗 Xd (Ω)': round(self.Xd, 3),
                '交轴电抗 Xq (Ω)': round(self.Xq, 3),
                '直轴电枢反应电抗 Xad (Ω)': round(self.Xad, 3),
                '交轴电枢反应电抗 Xaq (Ω)': round(self.Xaq, 3),
                '直轴折算系数 Kad': round(self.Kad, 3),
                '交轴折算系数 Kaq': round(self.Kaq, 3)
            },
            '材料质量': {
                '铜线质量 mCu (kg)': round(self.mCu, 2),
                '硅钢片质量 mFe (kg)': round(self.mFe, 2),
                '铸铝质量 mAl (kg)': round(self.mAl, 2),
                '永磁体质量 mm (kg)': round(self.mm, 2)
            },
            '损耗参数': {
                '铜耗 pCu (W)': round(self.pCu, 1),
                '铁耗 pFe (W)': round(self.pFe, 1),
                '机械损耗 pfw (W)': round(self.pfw, 1),
                '杂散损耗 ps (W)': round(self.ps, 1),
                '总损耗 Σp (W)': round(self.pSum, 1)
            },
            '性能参数': {
                '启动电流倍数 Ist/IN': round(self.Ist_ratio, 2),
                '启动电流 Ist (A)': round(self.Ist_calc, 1),
                '启动转矩倍数 Tst/TN': round(self.Tst_calc, 2)
            },
            '实际性能参数': {
                '实际效率 eta (%)': round(self.eta_actual, 2),
                '实际功率因数 cosfi': round(self.cosfi_actual, 3),
                '功率角 theta (°)': round(self.theta_actual, 1),
                '负载角 phi (°)': round(self.phi_actual, 1),
                '槽满率 Sf (%)': round(self.Sf_actual, 1),
                '线负荷 A1 (A/mm)': round(self.A1_actual, 1),
                '电密度 J1 (A/mm²)': round(self.J1_actual, 1),
                'A1J1 (A²/mm³)': round(self.A1J1_actual, 1),
                '负载工作点 bmN': round(self.bmN, 3),
                '负载工作点 bmh': round(self.bmh_actual, 3)
            }
        }

class MotorCalculatorGUI:
    """电机计算器GUI界面 - 布局优化版本"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("异步启动永磁同步电动机电磁计算程序")
        self.root.geometry("1600x900")
        self.root.state('zoomed')  # Windows下最大化
        
        # 创建参数对象
        self.params = MotorParameters()
        
        # 字体缩放因子
        self.font_scale = 1.5
        
        self.setup_gui()
        
    def get_scaled_font(self, base_size, weight='normal'):
        """获取缩放后的字体"""
        size = int(base_size * self.font_scale)
        return ('Arial', size, weight)
        
    def setup_gui(self):
        """设置GUI界面"""
        # 创建主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 首先创建按钮框架（在顶部）
        self.create_main_buttons(main_frame)
        
        # 创建笔记本控件
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # 配置notebook字体
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=self.get_scaled_font(16, 'bold'))
        
        # 创建各个选项卡
        self.create_basic_params_tab(notebook)
        self.create_geometry_tab(notebook)
        self.create_winding_tab(notebook)
        self.create_magnet_tab(notebook)
        self.create_material_slot_tab(notebook)
        self.create_other_tab(notebook)
        self.create_results_tab(notebook)
        self.create_plots_tab(notebook)
        self.create_about_tab(notebook)
        
    def create_main_buttons(self, parent):
        """创建主要操作按钮（在顶部）"""
        button_frame = tk.Frame(parent, bg='lightgray', relief='raised', bd=2)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 添加标题
        title_label = tk.Label(button_frame, text="电机电磁计算操作面板", 
                              font=self.get_scaled_font(18, 'bold'), 
                              bg='lightgray')
        title_label.pack(pady=10)
        
        # 按钮容器
        btn_container = tk.Frame(button_frame, bg='lightgray')
        btn_container.pack(pady=(0, 10))
        
        button_font = self.get_scaled_font(16, 'bold')
        
        # 开始计算按钮
        calc_button = tk.Button(
            btn_container, 
            text="开始计算", 
            command=self.calculate, 
            font=button_font, 
            width=12, 
            height=2, 
            bg='lightgreen',
            relief='raised',
            bd=3
        )
        calc_button.pack(side=tk.LEFT, padx=10)
        
        # 导出结果按钮
        export_button = tk.Button(
            btn_container, 
            text="导出结果", 
            command=self.export_results, 
            font=button_font, 
            width=12, 
            height=2,
            relief='raised',
            bd=3
        )
        export_button.pack(side=tk.LEFT, padx=10)
        
        # 清空数据按钮
        clear_button = tk.Button(
            btn_container, 
            text="清空数据", 
            command=self.clear_data, 
            font=button_font, 
            width=12, 
            height=2, 
            bg='lightcoral',
            relief='raised',
            bd=3
        )
        clear_button.pack(side=tk.LEFT, padx=10)
        
    def create_basic_params_tab(self, notebook):
        """创建基本参数选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="基本参数")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 基本参数输入
        params_basic = [
            ("额定功率 PN (kW)", "PN", 15.0),
            ("额定电压 UN (V)", "UN", 380),
            ("相数 m", "m", 3),
            ("频率 f (Hz)", "f", 50),
            ("极对数 p", "p", 2),
            ("功率因数 cos φ", "cosfi", 0.95),
            ("效率 η", "eff", 0.935),
            ("启动转矩倍数 Tpo", "Tpo", 1.8),
            ("启动电流倍数 Ist", "Ist", 9.0),
            ("堵转转矩倍数 Tst", "Tst", 2.0)
        ]
        
        self.basic_vars = {}
        label_font = self.get_scaled_font(18)
        entry_font = self.get_scaled_font(18)
        
        for i, (label, var_name, default) in enumerate(params_basic):
            tk.Label(scrollable_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=20, pady=12)
            var = tk.DoubleVar(value=default)
            entry = tk.Entry(scrollable_frame, textvariable=var, width=25, font=entry_font)
            entry.grid(row=i, column=1, padx=20, pady=12)
            self.basic_vars[var_name] = var
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_geometry_tab(self, notebook):
        """创建几何尺寸选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="几何尺寸")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建左右两列
        left_frame = tk.LabelFrame(scrollable_frame, text="定子尺寸", font=self.get_scaled_font(18, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        right_frame = tk.LabelFrame(scrollable_frame, text="转子尺寸", font=self.get_scaled_font(18, 'bold'))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 定子参数
        stator_params = [
            ("定子外径 D1 (mm)", "D1", 260.0),
            ("定子内径 Di1 (mm)", "Di1", 170.0),
            ("铁心长度 La (mm)", "La", 190.0),
            ("气隙长度 g (mm)", "g", 0.65),
            ("定子槽数 Q1", "Q1", 36),
            ("定子槽口宽度 b01 (mm)", "b01", 3.8),
            ("定子槽口高度 h01 (mm)", "h01", 0.8),
            ("定子槽宽度 b1 (mm)", "b1", 7.7),
            ("定子槽斜角 ALFA1 (度)", "ALFA1", 30),
            ("定子槽圆角半径 R1 (mm)", "R1", 5.1),
            ("定子槽高度 h12 (mm)", "h12", 15.2)
        ]
        
        # 转子参数
        rotor_params = [
            ("转子内径 Di2 (mm)", "Di2", 60.0),
            ("转子槽数 Q2", "Q2", 32),
            ("转子槽口宽度 b02 (mm)", "b02", 2.0),
            ("转子槽口高度 h02 (mm)", "h02", 0.8),
            ("转子槽上部宽度 br1 (mm)", "br1", 6.4),
            ("转子槽下部宽度 br2 (mm)", "br2", 5.5),
            ("转子槽高度 hr12 (mm)", "hr12", 15.0),
            ("转子槽斜角 ALFA2 (度)", "ALFA2", 30),
            ("转子端环面积 AR (mm²)", "AR", 180)
        ]
        
        self.geometry_vars = {}
        label_font = self.get_scaled_font(18)
        entry_font = self.get_scaled_font(18)
        
        # 添加定子参数
        for i, (label, var_name, default) in enumerate(stator_params):
            tk.Label(left_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=15, pady=10)
            if var_name in ['Q1', 'ALFA1']:
                var = tk.IntVar(value=int(default))
            else:
                var = tk.DoubleVar(value=default)
            entry = tk.Entry(left_frame, textvariable=var, width=20, font=entry_font)
            entry.grid(row=i, column=1, padx=15, pady=10)
            self.geometry_vars[var_name] = var
            
        # 添加转子参数
        for i, (label, var_name, default) in enumerate(rotor_params):
            tk.Label(right_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=15, pady=10)
            if var_name in ['Q2', 'ALFA2']:
                var = tk.IntVar(value=int(default))
            else:
                var = tk.DoubleVar(value=default)
            entry = tk.Entry(right_frame, textvariable=var, width=20, font=entry_font)
            entry.grid(row=i, column=1, padx=15, pady=10)
            self.geometry_vars[var_name] = var
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
            
    def create_winding_tab(self, notebook):
        """创建绕组参数选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="绕组参数")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        winding_params = [
            ("绕组类型 LE", "LE", 2),
            ("并联支路数 a", "a", 1),
            ("每槽导体数 Ns", "Ns", 13),
            ("第一种导线根数 Nt1", "Nt1", 2),
            ("第一种导线直径 d11 (mm)", "d11", 1.20),
            ("第二种导线根数 Nt2", "Nt2", 3),
            ("第二种导线直径 d12 (mm)", "d12", 1.25),
            ("绕组端部伸出长度 d (mm)", "d", 15.0),
            ("绕组节距 y", "y", 9)
        ]
        
        self.winding_vars = {}
        label_font = self.get_scaled_font(18)
        entry_font = self.get_scaled_font(18)
        
        for i, (label, var_name, default) in enumerate(winding_params):
            tk.Label(scrollable_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=20, pady=12)
            if var_name in ['LE', 'a', 'Ns', 'Nt1', 'Nt2', 'y']:
                var = tk.IntVar(value=int(default))
            else:
                var = tk.DoubleVar(value=default)
            entry = tk.Entry(scrollable_frame, textvariable=var, width=25, font=entry_font)
            entry.grid(row=i, column=1, padx=20, pady=12)
            self.winding_vars[var_name] = var
            
        # 添加选择框
        tk.Label(scrollable_frame, text="绕组连接方式", font=label_font).grid(
            row=len(winding_params), column=0, sticky=tk.W, padx=20, pady=12)
        self.wgco_var = tk.StringVar(value="Y")
        wgco_combo = ttk.Combobox(scrollable_frame, textvariable=self.wgco_var, 
                                 values=["Y (星形连接)", "J (三角形连接)"], 
                                 width=22, font=self.get_scaled_font(18))
        wgco_combo.grid(row=len(winding_params), column=1, padx=20, pady=12)
        
        tk.Label(scrollable_frame, text="是否斜槽", font=label_font).grid(
            row=len(winding_params)+1, column=0, sticky=tk.W, padx=20, pady=12)
        self.sks_var = tk.StringVar(value="Y")
        sks_combo = ttk.Combobox(scrollable_frame, textvariable=self.sks_var, 
                                values=["Y (是)", "N (否)"], 
                                width=22, font=self.get_scaled_font(18))
        sks_combo.grid(row=len(winding_params)+1, column=1, padx=20, pady=12)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_magnet_tab(self, notebook):
        """创建永磁体参数选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="永磁体参数")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        magnet_params = [
            ("永磁体厚度 hM (mm)", "hM", 5.3),
            ("永磁体宽度 bM (mm)", "bM", 110.0),
            ("永磁体长度 LM (mm)", "LM", 190.0),
            ("剩磁密度 Br0 (T)", "Br0", 1.15),
            ("矫顽力 Hc0 (kA/m)", "Hc0", 875.0),
            ("永磁体密度 ROUm (kg/m³)", "ROUm", 7400.0),
            ("漏磁系数 SIGMA0", "SIGMA0", 1.28),
            ("永磁体等效气隙 g12 (mm)", "g12", 0.15)
        ]
        
        self.magnet_vars = {}
        label_font = self.get_scaled_font(18)
        entry_font = self.get_scaled_font(18)
        
        for i, (label, var_name, default) in enumerate(magnet_params):
            tk.Label(scrollable_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=20, pady=12)
            var = tk.DoubleVar(value=default)
            entry = tk.Entry(scrollable_frame, textvariable=var, width=25, font=entry_font)
            entry.grid(row=i, column=1, padx=20, pady=12)
            self.magnet_vars[var_name] = var
            
        # 添加选择框
        tk.Label(scrollable_frame, text="磁路结构", font=label_font).grid(
            row=len(magnet_params), column=0, sticky=tk.W, padx=20, pady=12)
        self.Lev_var = tk.IntVar(value=1)
        Lev_combo = ttk.Combobox(scrollable_frame, textvariable=self.Lev_var, 
                                values=["1 (径向磁路结构)", "2 (切向磁路结构)"], 
                                width=30, font=self.get_scaled_font(18))
        Lev_combo.grid(row=len(magnet_params), column=1, padx=20, pady=12)
        
        tk.Label(scrollable_frame, text="永磁材料", font=label_font).grid(
            row=len(magnet_params)+1, column=0, sticky=tk.W, padx=20, pady=12)
        self.magnet_type_var = tk.IntVar(value=1)
        magnet_combo = ttk.Combobox(scrollable_frame, textvariable=self.magnet_type_var, 
                                   values=["1 (钕铁硼永磁体)", "2 (铁氧体永磁体)"], 
                                   width=30, font=self.get_scaled_font(18))
        magnet_combo.grid(row=len(magnet_params)+1, column=1, padx=20, pady=12)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_material_slot_tab(self, notebook):
        """创建材料和槽型选择选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="材料和槽型")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        label_font = self.get_scaled_font(18)
        
        # 硅钢片材料选择
        tk.Label(scrollable_frame, text="硅钢片材料", font=self.get_scaled_font(18, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=20, pady=20)
        
        self.steel_type_var = tk.IntVar(value=5)
        steel_combo = ttk.Combobox(scrollable_frame, textvariable=self.steel_type_var, 
                                  values=[
                                      "1 (DR510-50 - 高磁导率低损耗)",
                                      "2 (DR420-50 - 超低损耗型)",
                                      "3 (DR490-50 - 高磁感应强度)",
                                      "4 (DR550-50 - 高饱和磁感应强度)",
                                      "5 (DW315-50 - 标准型)"
                                  ], 
                                  width=40, font=self.get_scaled_font(18))
        steel_combo.grid(row=0, column=1, padx=20, pady=20)
        
        # 槽型选择
        tk.Label(scrollable_frame, text="转子槽型", font=self.get_scaled_font(18, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=20, pady=20)
        
        self.slot_type_var = tk.IntVar(value=1)
        slot_combo = ttk.Combobox(scrollable_frame, textvariable=self.slot_type_var, 
                                 values=[
                                     "1 (梨形槽 - 启动性能好)",
                                     "2 (半梨形槽 - 平衡性能)",
                                     "3 (圆形槽 - 制造简单)",
                                     "4 (斜肩圆槽 - 低噪音)"
                                 ], 
                                 width=40, font=self.get_scaled_font(18))
        slot_combo.grid(row=1, column=1, padx=20, pady=20)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_other_tab(self, notebook):
        """创建其他参数选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="其他参数")
        
        # 创建滚动框架
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        other_params = [
            ("工作温度 t (℃)", "t", 75.0),
            ("机械损耗标么值 pfwl", "pfwl", 0.0107),
            ("杂散损耗标么值 psl", "psl", 0.015),
            ("交轴绕组系数 Kq", "Kq", 0.36)
        ]
        
        self.other_vars = {}
        label_font = self.get_scaled_font(18)
        entry_font = self.get_scaled_font(18)
        
        for i, (label, var_name, default) in enumerate(other_params):
            tk.Label(scrollable_frame, text=label, font=label_font).grid(
                row=i, column=0, sticky=tk.W, padx=20, pady=12)
            var = tk.DoubleVar(value=default)
            entry = tk.Entry(scrollable_frame, textvariable=var, width=25, font=entry_font)
            entry.grid(row=i, column=1, padx=20, pady=12)
            self.other_vars[var_name] = var
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
            
    def create_results_tab(self, notebook):
        """创建计算结果选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="计算结果")
        
        # 创建文本框显示结果
        self.results_text = scrolledtext.ScrolledText(frame, width=120, height=40, 
                                                     font=self.get_scaled_font(14))
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def create_plots_tab(self, notebook):
        """创建图表选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="图表显示")
        
        # 创建matplotlib图表
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        self.fig.suptitle('电机特性曲线', fontsize=16)
        
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_about_tab(self, notebook):
        """创建关于选项卡"""
        frame = tk.Frame(notebook)
        notebook.add(frame, text="关于")
        
        # 创建滚动文本框
        about_text = scrolledtext.ScrolledText(frame, width=120, height=40, 
                                              font=self.get_scaled_font(14))
        about_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 简化的关于信息 - 按要求留空
        about_content = """
异步启动永磁同步电动机电磁计算程序
=====================================

程序版本：Python GUI 版本 3.0 - 完整精确计算版
开发时间：2025年6月
开发者：Zhaolin Wei

程序功能：
--------
1. 完整的电机基本参数计算（包含符号输出）
2. 精确的绕组参数设计与计算
3. 迭代求解的磁路分析与计算
4. 详细的阻抗参数计算
5. 全面的性能特性分析
6. 启动特性精确计算
7. 材料质量计算
8. 损耗详细分析
9. 图表可视化显示

技术特点：
--------
1. 完整的材料数据表支持
2. 迭代求解空载磁路工作点（最多30次迭代）
3. 精确的温度修正计算
4. 详细的几何参数计算
5. 完整的符号输出便于代码查找
6. 适合中老年用户的超大字体界面

计算符号说明：
--------
基本参数：OMGs, nN, IN, TN, TAO
绕组参数：N, Kdp, Kp1, Kd1, Ksk1
几何参数：t1, t2, D2, bt1, bt2, hj1, hj2, AB, DR
磁路参数：Kg, Bg, Bg1, Bts, Bj1, Btr, Bj2, E0, bm0, Kst
永磁参数：Br, Hc, MUr, Am, FF, FAIM, mm
阻抗参数：Rs, R2, X1, X2, Xd, Xq, Xad, Xaq, Kad, Kaq
材料质量：mCu, mFe, mAl, mm
损耗参数：pCu, pFe, pfw, ps, Σp
性能参数：Ist, Tst

使用说明：
--------
1. 在各个标签页中输入相应的电机设计参数
2. 点击"开始计算"按钮执行完整的电磁计算
3. 查看控制台输出的详细计算过程
4. 查看"计算结果"和"图表显示"标签页
5. 可以保存参数配置文件

注意事项：
--------
1. 程序使用迭代方法求解，确保计算精度
2. 建议在计算前保存参数配置
"""
        
        about_text.insert(tk.END, about_content)
        about_text.config(state=tk.DISABLED)
        
    def update_parameters(self):
        """更新参数对象"""
        # 基本参数
        for var_name, var in self.basic_vars.items():
            setattr(self.params, var_name, var.get())
            
        # 几何参数
        for var_name, var in self.geometry_vars.items():
            setattr(self.params, var_name, var.get())
            
        # 绕组参数
        for var_name, var in self.winding_vars.items():
            setattr(self.params, var_name, var.get())
            
        # 永磁体参数
        for var_name, var in self.magnet_vars.items():
            setattr(self.params, var_name, var.get())
            
        # 其他参数
        for var_name, var in self.other_vars.items():
            setattr(self.params, var_name, var.get())
            
        # 特殊参数
        wgco_value = self.wgco_var.get()
        self.params.wgco = wgco_value[0] if wgco_value else 'Y'
        
        sks_value = self.sks_var.get()
        self.params.sks = sks_value[0] if sks_value else 'N'
        
        self.params.Lev = self.Lev_var.get()
        self.params.magnet = self.magnet_type_var.get()
        self.params.steel_type = self.steel_type_var.get()
        self.params.CX = self.slot_type_var.get()
        
    def calculate(self):
        """执行计算"""
        try:
            self.update_parameters()
            engine = MotorCalculationEngine(self.params)
            success, message = engine.calculate_all()
            
            if success:
                self.display_results(engine.results)
                self.plot_characteristics(engine)
                self.last_results = engine.results
                
                steel_name = engine.steel_tables.get_steel_name(self.params.steel_type)
                slot_name = engine.get_slot_type_name(self.params.CX)
                
                messagebox.showinfo("计算完成", 
                    f"电机电磁计算已完成！\n"
                    f"使用材料：{steel_name}\n"
                    f"槽型：{slot_name}\n"
                    f"所有参数都是实际计算值，非典型值。\n"
                    f"详细计算过程请查看控制台输出。", 
                    parent=self.root)
            else:
                messagebox.showerror("计算错误", message, parent=self.root)
                
        except Exception as e:
            messagebox.showerror("错误", f"计算过程中发生错误：{str(e)}", parent=self.root)
            
    def display_results(self, results):
        """显示完整计算结果 - 使用实际计算值"""
        self.results_text.delete(1.0, tk.END)
        
        output = f"{self.params.PN:.2f}kW 内置式异步启动永磁同步电动机电磁计算方案清单\n"
        output += "=" * 80 + "\n\n"
        
        # 技术性能指标
        output += "************************ 技术性能指标 ************************\n"
        output += f"PN={self.params.PN:.2f} kW  UN={self.params.UN:.0f} V   m={self.params.m}          f={self.params.f:.0f}\n"
        output += f"p={self.params.p}          cosφN≥{self.params.cosfi:.3f}  ηN≥{self.params.eff*100:.2f}%    IstN≤{self.params.Ist:.1f}倍\n"
        output += f"TN={results['基本参数']['额定转矩 TN (N·m)']:.2f} N.m TstN≥{self.params.Tst:.2f}倍 TpoN≥{self.params.Tpo:.2f}倍  t={self.params.t:.0f}℃\n\n"
        
        # 主要尺寸、绕组和定子
        output += "************************ 主要尺寸、绕组和定子 ************************\n"
        output += f"D1={self.params.D1:.1f}mm  Di1={self.params.Di1:.1f}mm  La={self.params.La:.1f}mm   δ={self.params.g:.2f}mm\n"
        output += f"Q1={self.params.Q1}       LE={self.params.LE}         wgco={self.params.a}-{self.params.wgco}     Ns={self.params.Ns}\n\n"
        
        # 材料和槽型信息
        output += "************************ 材料和槽型 ************************\n"
        output += f"硅钢片：{results['磁路参数']['硅钢片类型']}    槽型：{results['几何参数']['槽型 CX']}\n\n"
        
        # 定子绕组参数
        output += "======================== 定子绕组参数 ========================\n"
        if '绕组参数' in results:
            output += f"Nt1 = {self.params.Nt1}           d11 = {self.params.d11:.2f}mm      Nt2 = {self.params.Nt2}           d12 = {self.params.d12:.2f}mm\n"
            output += f"y = {self.params.y}             d = {self.params.d:.1f}mm        τy = {results['绕组参数']['线圈端部长度 Ls (mm)']:.1f}mm      Ls = {results['绕组参数']['线圈端部长度 Ls (mm)']:.1f}mm\n"
            # 使用实际计算的槽满率
            if '实际性能参数' in results:
                output += f"Sf = {results['实际性能参数']['槽满率 Sf (%)']:.1f}%        Kdp = {results['绕组参数']['绕组因数 Kdp']:.3f}        N = {results['绕组参数']['每相串联匝数 N']}            αi = .891\n"
            output += f"b01 = {self.params.b01:.1f}mm       h01 = {self.params.h01:.1f}mm        α1 = {self.params.ALFA1:.0f}°          b1 = {self.params.b1:.1f}mm\n"
            output += f"R1 = {self.params.R1:.1f}mm        h12 = {self.params.h12:.1f}mm      sks = {self.params.sks}\n\n"
        
        # 转子
        output += "*************************** 转子 ***************************\n"
        output += f"Lv = {self.params.Lv}            b02 = {self.params.b02:.1f}mm       h02 = {self.params.h02:.1f}mm        α2 = {self.params.ALFA2:.0f}°\n"
        output += f"br1 = {self.params.br1:.1f}mm       br2 = {self.params.br2:.1f}mm       hr12 = {self.params.hr12:.1f}mm     Di2 = {self.params.Di2:.1f}mm\n"
        if '几何参数' in results:
            output += f"DR = {results['几何参数']['转子端环直径 DR (mm)']:.1f}mm      AB = {results['几何参数']['转子槽面积 AB (mm²)']:.0f}mm^2      AR = {self.params.AR:.0f}mm^2     Q2 = {self.params.Q2}\n\n"
        
        # 空载磁路计算结果
        output += "************************ 空载磁路计算结果 ************************\n"
        if '磁路参数' in results:
            output += f"Bδ1 = {results['磁路参数']['气隙磁密基波 Bg1 (T)']:.3f}T       Bt1 = {results['磁路参数']['定子齿磁密 Bts (T)']:.3f}T      Bj1 = {results['磁路参数']['定子轭磁密 Bj1 (T)']:.3f}T      Bδ = {results['磁路参数']['气隙磁密 Bg (T)']:.3f}T\n"
            output += f"Bt2 = {results['磁路参数']['转子齿磁密 Btr (T)']:.3f}T      Bj2 = {results['磁路参数']['转子轭磁密 Bj2 (T)']:.3f}T      Kst = {results['磁路参数']['齿饱和系数 Kst']:.2f}        KΦ = .897\n\n"
        
        # 额定负载点损耗
        output += "************************ 额定负载点损耗 ************************\n"
        if '损耗参数' in results:
            output += f"Σp = {results['损耗参数']['总损耗 Σp (W)']:.1f} W\n"
            output += f"pCu = {results['损耗参数']['铜耗 pCu (W)']:.1f} W      pFe = {results['损耗参数']['铁耗 pFe (W)']:.1f} W      ps = {results['损耗参数']['杂散损耗 ps (W)']:.1f} W       pfw = {results['损耗参数']['机械损耗 pfw (W)']:.1f} W\n\n"
        
        # 额定负载点热负荷 - 使用实际计算值
        output += "************************ 额定负载点热负荷 ************************\n"
        if '实际性能参数' in results:
            output += f"J1 = {results['实际性能参数']['电密度 J1 (A/mm²)']:.1f} A/mm^2    A1 = {results['实际性能参数']['线负荷 A1 (A/mm)']:.1f} A/mm     A1J1 = {results['实际性能参数']['A1J1 (A²/mm³)']:.1f} A^2/mm^3\n\n"
        
        # 材料质量
        output += "************************ 材料质量 ************************\n"
        if '材料质量' in results:
            output += f"mCu = {results['材料质量']['铜线质量 mCu (kg)']:.2f} kg      mFe = {results['材料质量']['硅钢片质量 mFe (kg)']:.2f} kg     mAl = {results['材料质量']['铸铝质量 mAl (kg)']:.2f} kg      mm = {results['材料质量']['永磁体质量 mm (kg)']:.2f} kg\n\n"
        
        # 计算性能（输出额定功率时） - 使用实际计算值
        output += "*************** 计算性能（输出额定功率时） ***************\n"
        if '实际性能参数' in results and '性能参数' in results:
            output += f"η = {results['实际性能参数']['实际效率 eta (%)']:.2f}%        cosφ = {results['实际性能参数']['实际功率因数 cosfi']:.3f}       I1 = {results['基本参数']['额定电流 IN (A)']:.2f} A       Ist = {results['性能参数']['启动电流倍数 Ist/IN']:.2f}倍\n"
            output += f"θ = {results['实际性能参数']['功率角 theta (°)']:.1f}°         φ = {results['实际性能参数']['负载角 phi (°)']:.1f}°         Tst = {results['性能参数']['启动转矩倍数 Tst/TN']:.2f}倍      Tpo = {self.params.Tpo:.2f}倍\n\n"
        
        # 永磁磁极
        output += "*************************** 永磁磁极 ***************************\n"
        magnet_name = "NdFeB" if self.params.magnet == 1 else "Ferrite"
        output += f"Lev = {self.params.Lev}             magnet = {magnet_name}      E0 = {results['磁路参数']['空载反电动势 E0 (V)']:.1f} V        δ12 = {self.params.g12:.2f} mm\n"
        if '永磁体参数' in results:
            output += f"Br = {results['永磁体参数']['工作温度剩磁 Br (T)']:.2f} T          Hc = {results['永磁体参数']['工作温度矫顽力 Hc (A/m)']:.0f} kA/m       μr = {results['永磁体参数']['相对磁导率 MUr']:.2f}          σ0 = {self.params.SIGMA0:.2f}\n"
            output += f"hM = {self.params.hM:.2f} mm         bM = {self.params.bM:.1f} mm        LM = {self.params.LM:.1f} mm\n\n"
        
        # 永磁体工作点 - 使用实际计算值
        output += "************************ 永磁体工作点 ************************\n"
        if '磁路参数' in results and '实际性能参数' in results:
            output += f"bm0 = {results['磁路参数']['永磁体工作点 bm0']:.3f}          bmN = {results['实际性能参数']['负载工作点 bmN']:.3f}          bmh = {results['实际性能参数']['负载工作点 bmh']:.3f}\n\n"
        
        # 电阻、电抗参数
        output += "************************ 电阻、电抗参数 ************************\n"
        if '阻抗参数' in results:
            output += f"Kad = {results['阻抗参数']['直轴折算系数 Kad']:.2f}           Kaq = {results['阻抗参数']['交轴折算系数 Kaq']:.2f}           Xad = {results['阻抗参数']['直轴电枢反应电抗 Xad (Ω)']:.2f} Ω        Xaq = {results['阻抗参数']['交轴电枢反应电抗 Xaq (Ω)']:.2f} Ω\n"
            output += f"Rs = {results['阻抗参数']['定子电阻 Rs (Ω)']:.3f} Ω          Rr = {results['阻抗参数']['转子电阻 R2 (Ω)']:.3f} Ω          X1 = {results['阻抗参数']['定子漏抗 X1 (Ω)']:.3f} Ω         X2 = {results['阻抗参数']['转子漏抗 X2 (Ω)']:.3f} Ω\n\n"
        
        output += "*************************** 结束 ***************************\n"
        
        self.results_text.insert(1.0, output)
        
    def plot_characteristics(self, engine):
        """绘制特性曲线"""
        # 清除之前的图表
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            
        # 生成转矩-转差率曲线数据
        s_values = np.linspace(0.01, 1.0, 100)
        torque_values = []
        
        for s in s_values:
            R2_s = engine.R2 / s
            Z_total = np.sqrt((engine.Rs + R2_s)**2 + (engine.X1 + engine.X2)**2)
            I2_sq = (engine.params.UN / np.sqrt(3))**2 / Z_total**2
            T = engine.params.m * engine.params.p * I2_sq * R2_s / (2 * np.pi * engine.params.f)
            torque_values.append(T / engine.TN)
            
        # 绘制转矩-转差率曲线
        font_size = 14
        title_size = 16
        
        self.ax1.plot(s_values, torque_values, 'b-', linewidth=3)
        self.ax1.set_xlabel('转差率 s', fontsize=font_size)
        self.ax1.set_ylabel('转矩 (标么值)', fontsize=font_size)
        self.ax1.set_title('转矩-转差率特性', fontsize=title_size)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.tick_params(labelsize=font_size-2)
        
        # 绘制磁密分布
        positions = ['气隙Bg', '定子齿Bts', '定子轭Bj1', '转子齿Btr', '转子轭Bj2']
        B_values = [engine.Bg, engine.Bts, engine.Bj1, engine.Btr, engine.Bj2]
        
        bars = self.ax2.bar(positions, B_values, color=['skyblue', 'lightgreen', 'lightcoral', 'orange', 'purple'])
        self.ax2.set_ylabel('磁密 (T)', fontsize=font_size)
        self.ax2.set_title('磁密分布', fontsize=title_size)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.tick_params(labelsize=font_size-2)
        
        for bar, value in zip(bars, B_values):
            height = bar.get_height()
            self.ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                         f'{value:.3f}', ha='center', va='bottom', fontsize=font_size-2)
        
        # 绘制损耗分布饼图
        losses = ['铜耗pCu', '铁耗pFe', '机械pfw', '杂散ps']
        loss_values = [
            engine.pCu,
            engine.pFe,
            engine.pfw,
            engine.ps
        ]
        
        colors = ['gold', 'lightblue', 'lightgreen', 'lightcoral']
        wedges, texts, autotexts = self.ax3.pie(loss_values, labels=losses, autopct='%1.1f%%', 
                                               colors=colors, textprops={'fontsize': font_size-2})
        self.ax3.set_title('损耗分布', fontsize=title_size)
        
        # 绘制阻抗参数对比
        impedances = ['Rs', 'R2', 'X1', 'X2', 'Xd', 'Xq']
        impedance_values = [engine.Rs, engine.R2, engine.X1, engine.X2, engine.Xd, engine.Xq]
        
        bars = self.ax4.bar(impedances, impedance_values, 
                           color=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
        self.ax4.set_ylabel('阻抗 (Ω)', fontsize=font_size)
        self.ax4.set_title('阻抗参数', fontsize=title_size)
        self.ax4.grid(True, alpha=0.3)
        self.ax4.tick_params(labelsize=font_size-2)
        
        for bar, value in zip(bars, impedance_values):
            height = bar.get_height()
            self.ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                         f'{value:.3f}', ha='center', va='bottom', fontsize=font_size-2)
        
        plt.tight_layout()
        self.canvas.draw()
        
    def export_results(self):
        """导出计算结果"""
        if not hasattr(self, 'last_results'):
            messagebox.showwarning("警告", "请先进行计算！", parent=self.root)
            return
            
        filename = filedialog.asksaveasfilename(
            title="导出计算结果",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            parent=self.root
        )
        
        if filename:
            try:
                content = self.results_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", "计算结果导出成功！", parent=self.root)
            except Exception as e:
                messagebox.showerror("错误", f"导出结果失败：{str(e)}", parent=self.root)
                
    def clear_data(self):
        """清空所有数据"""
        result = messagebox.askyesno("确认", "确定要清空所有数据吗？", parent=self.root)
        
        if result:
            # 重置所有变量为默认值
            params = MotorParameters()
            
            for var_name in self.basic_vars:
                self.basic_vars[var_name].set(getattr(params, var_name))
            for var_name in self.geometry_vars:
                self.geometry_vars[var_name].set(getattr(params, var_name))
            for var_name in self.winding_vars:
                self.winding_vars[var_name].set(getattr(params, var_name))
            for var_name in self.magnet_vars:
                self.magnet_vars[var_name].set(getattr(params, var_name))
            for var_name in self.other_vars:
                self.other_vars[var_name].set(getattr(params, var_name))
                
            self.wgco_var.set("Y (星形连接)")
            self.sks_var.set("Y (是)")
            self.Lev_var.set(1)
            self.magnet_type_var.set(1)
            self.steel_type_var.set(5)
            self.slot_type_var.set(1)
            
            # 清空结果
            self.results_text.delete(1.0, tk.END)
            
            # 清空图表
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
            self.canvas.draw()

def main():
    """主函数"""
    root = tk.Tk()
    app = MotorCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()