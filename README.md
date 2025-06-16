# Asynchronous Start Permanent Magnet Synchronous Motor Electromagnetic Calculation Program

A comprehensive Python GUI application for calculating electromagnetic parameters of asynchronous start permanent magnet synchronous motors. This program supports multiple steel materials and rotor slot types, providing precise motor design calculations.

## Features

### 🔧 Core Functionality
- **Multi-Material Support**: Supports 5 types of silicon steel materials (DR510-50, DR420-50, DR490-50, DR550-50, DW315-50)
- **Multi-Slot Type Calculation**: Supports 4 rotor slot types (pear-shaped, semi-pear-shaped, circular, beveled circular)
- **Precise Calculations**: Iterative calculations based on actual B-H curves and loss data
- **Complete Parameters**: Calculates basic parameters, winding parameters, magnetic circuit parameters, impedance parameters, etc.
- **Real-time Results**: All parameters are actual calculated values, not typical values

### 🎨 Interface Features
- **Large Font Design**: Suitable for users of all ages
- **Responsive Design**: Automatically adapts to different screen sizes
- **Scroll Support**: Each page supports scroll browsing
- **Convenient Operation**: Top operation panel with one-click calculate, export, and clear functions

### 📊 Output Capabilities
- **Detailed Reports**: Generates complete motor design specification sheets
- **Chart Display**: Torque characteristics, magnetic flux density distribution, loss analysis, impedance parameter charts
- **Result Export**: Supports exporting calculation results to text files

## Installation Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
```bash
pip install numpy matplotlib tkinter
