#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电机参数配置模块
定义电机的所有输入参数和默认值
"""

from dataclasses import dataclass

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
    steel_type: int = 5 # 硅钢片类型
    
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