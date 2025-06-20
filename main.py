#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异步启动永磁同步电动机电磁计算程序
主程序入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from gui.main_window import MotorCalculatorGUI
    from utils.helpers import validate_motor_parameters
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有必要的文件都在正确的位置")
    sys.exit(1)

def setup_matplotlib():
    """设置matplotlib后端"""
    try:
        import matplotlib
        matplotlib.use('TkAgg')  # 使用Tkinter后端
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        print("警告: matplotlib未安装，图表功能将不可用")

def check_dependencies():
    """检查依赖库"""
    required_packages = ['numpy', 'matplotlib', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖库:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请使用以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """主函数"""
    print("异步启动永磁同步电动机电磁计算程序")
    print("版本: 6.0.0 - 模块化版本")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    # 设置matplotlib
    setup_matplotlib()
    
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            # root.iconbitmap('icon.ico')  # 如果有图标文件
            pass
        except:
            pass
        
        # 创建应用程序
        app = MotorCalculatorGUI(root)
        
        # 设置关闭事件
        def on_closing():
            if messagebox.askokcancel("退出", "确定要退出程序吗？"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("GUI界面已启动")
        print("详细计算过程将在此控制台显示")
        print("-" * 50)
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        print(f"程序运行错误: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main()