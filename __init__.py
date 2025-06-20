#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步启动永磁同步电动机电磁计算程序
模块化版本
"""

__version__ = "6.0.0"
__author__ = "PMSM Calculator Team"
__description__ = "Asynchronous Start Permanent Magnet Synchronous Motor Electromagnetic Calculation Program"

# 导入主要类和函数
from config.parameters import MotorParameters
from calculation.motor import MotorCalculationEngine
from data.steel_tables import SteelDataTables
from calculation.slot_leakage import SlotLeakageCalculator

__all__ = [
    'MotorParameters',
    'MotorCalculationEngine', 
    'SteelDataTables',
    'SlotLeakageCalculator'
]