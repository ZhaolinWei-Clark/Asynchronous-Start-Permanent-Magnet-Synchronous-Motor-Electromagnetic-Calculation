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

## 🧭 User Guide

### 🔄 Basic Operation Flow

1. **Start Program**  
   Run the program with:
   ```bash
   python xxx.py
   ```
   The program will launch in full-screen mode.

2. **Input Parameters**  
   - Enter motor design parameters via the various tabs.  
   - Select the appropriate **silicon steel material** and **slot type**.  
   - All parameters have default values for quick calculation.

3. **Execute Calculation**  
   - Click **Start Calculation** at the top of the window.  
   - The program performs a complete electromagnetic simulation.  
   - The calculation process is visible in the console window.

4. **View Results**  
   - Navigate to the **Calculation Results** tab for detailed data.  
   - Switch to the **Chart Display** tab to view characteristic curves.  
   - All outputs are based on actual computations.

5. **Export Results**  
   - Click the **Export Results** button.  
   - Choose a save location and filename.  
   - Results will be saved as a `.txt` file.

---

## ⚙️ Parameter Description

### 📌 Basic Parameters

| Parameter             | Description                                      |
|-----------------------|--------------------------------------------------|
| **Rated Power PN (kW)** | Rated output power of the motor                  |
| **Rated Voltage UN (V)** | Operating voltage under rated conditions         |
| **Phase Number m**     | Number of motor phases (typically 3)             |
| **Frequency f (Hz)**   | Supply frequency                                 |
| **Pole Pairs p**       | Number of magnetic pole pairs                    |

### 🧲 Material Selection

| Material     | Features                                                                 |
|--------------|--------------------------------------------------------------------------|
| **DR510-50** | High permeability, low loss — suitable for high-efficiency motors        |
| **DR420-50** | Ultra-low loss — ideal for energy-saving designs                         |
| **DR490-50** | High magnetic flux density — suited for compact, high-power motors       |
| **DR550-50** | High saturation flux — suitable for heavy-duty industrial applications   |
| **DW315-50** | Standard type — versatile and cost-effective                             |

### 🪛 Slot Type Selection

| Slot Type              | Advantages                                                |
|------------------------|-----------------------------------------------------------|
| **Pear-shaped Slot**      | High starting torque — good for heavy-load startups       |
| **Semi-pear-shaped Slot** | Balanced start/run performance                           |
| **Circular Slot**         | Easy to manufacture and cost-effective                   |
| **Beveled Circular Slot** | Low noise and minimal vibration                          |

---

## 🧪 Technical Features

### ✅ Calculation Accuracy

- Uses real **silicon steel B-H curve data** (37 data points).
- Slot leakage reactance is calculated using **original Fortran-based formulas**.
- Magnetic circuit solved iteratively to ensure **accurate convergence**.
- Includes effects of **temperature**, **saturation**, **skin effect**, etc.

### ✅ Code Quality

- Adheres to **PEP 8** standards.
- Modular code with separation of logic and interface.
- Comprehensive comments and **docstrings** throughout.
- Robust **exception handling** and **error messaging**.

### ✅ User Experience

- **Tabbed interface** for intuitive navigation.
- Real-time **calculation progress** displayed.
- Friendly and informative **error prompts**.

---

---

## 📦 `requirements.txt`

```text
numpy>=1.19.0
matplotlib>=3.3.0
```

---

## 🧪 Example Usage


### 1. Select "Basic Parameters" tab
### 2. Enter motor specifications (default: 15kW motor)
### 3. Choose "Material and Slot Type" tab
### 4. Select appropriate steel material and slot type
### 5. Click "Start Calculation" button
### 6. View results in "Calculation Results" tab
### 7. Export results using "Export Results" button




## 🔁 Calculation Flow

The program follows a systematic calculation approach:

1. Basic parameter validation and computation  
2. Winding parameter analysis  
3. Geometric parameter calculation  
4. Permanent magnet parameter determination  
5. No-load magnetic circuit iterative solution  
6. Impedance parameter calculation  
7. Performance parameter analysis  
8. Material weight estimation  
9. Loss calculation  
10. Starting characteristic evaluation  
11. Actual performance parameter computation  

This comprehensive approach ensures accurate and reliable motor design calculations suitable for professional engineering applications.

