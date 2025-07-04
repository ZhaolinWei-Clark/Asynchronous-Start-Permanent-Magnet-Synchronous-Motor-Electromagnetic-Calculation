#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硅钢片数据表模块
提供多种硅钢片的B-H曲线和损耗数据
"""

import numpy as np

class SteelDataTables:
    """多种硅钢片数据表类"""
    
    def __init__(self):
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