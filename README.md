# 🔬 ROS Sensor Calibration Optimizer

**Advanced sensor calibration analysis tool for optimizing measurement accuracy through systematic calibration range testing**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![NumPy](https://img.shields.io/badge/NumPy-1.21+-orange.svg)](https://numpy.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-green.svg)](https://matplotlib.org)

## 🎯 Project Overview

This project performs comprehensive analysis of different calibration range configurations for ROS (Robotic Operating System) sensors to identify optimal calibration points that maximize measurement accuracy. Through systematic testing of 7 different calibration scenarios, the tool determines the best distance points for sensor calibration.

## 🚀 Purpose & Impact

**Objective**: Determine the optimal calibration range (distance measurement points) that provides the most accurate sensor readings in the target operating zone (1.5-3.0mm).

**Business Value**: 
- Reduces sensor measurement errors by up to 7.8x
- Improves manufacturing quality control
- Optimizes sensor performance for critical applications

## Key Files

### Core Analysis Scripts
- **`calibration_range_optimizer.py`** - Main analysis engine that tests 7 different calibration range scenarios
- **`range_analysis_main.py`** - Primary script to run the complete analysis
- **`results_summary.py`** - Simple summary of analysis results

### Reports and Documentation
- **`calibration_range_analysis_report.md`** - Comprehensive analysis report in Markdown format
- **`confluence_calibration_report.xml`** - XML formatted report for Confluence integration
- **`README.md`** - This documentation file

## 📊 Generated Visualizations

The analysis produces comprehensive visualizations in the `outputs/` folder:

### Core Analysis Charts
- **`calibration_comparison_plots.png`** - Side-by-side comparison of all 7 calibration scenarios
- **`comprehensive_calibration_analysis.png`** - Detailed statistical analysis across all sensors
- **`error_analysis_detailed.png`** - RMS error breakdown and confidence intervals

### Performance Summary  
- **`comprehensive_summary_table.png`** - Complete results table with rankings
- **`calibration_summary_table.png`** - Condensed performance metrics

### Data Quality Analysis
- **`raw_data_analysis.png`** - Original sensor measurements and data quality
- **`sensor_measurements_plot.png`** - Individual sensor response curves
- **`sensor_jumps_detection.png`** - Data anomaly detection and filtering

### Statistical Analysis
- **`bias_linearity_analysis.png`** - Sensor bias and linearity assessment  
- **`calibration_range_analysis_comprehensive.png`** - Range-specific performance analysis

> 💡 **Tip**: Browse the [`outputs/`](./outputs/) folder to view all generated charts and analysis results.

## Test Scenarios

The analysis tests 7 different calibration point configurations:

1. **Standard**: [1.0, 2.0, 3.0] mm - Traditional approach
2. **Wide-1**: [0.5, 2.0, 3.5] mm - Maximum range coverage
3. **Wide-2**: [0.5, 1.75, 3.0] mm - Wide with closer spacing
4. **Short**: [0.5, 1.5, 2.5] mm - Concentrated in lower range
5. **Far-1**: [1.5, 2.25, 3.0] mm - Focused on target range ⭐ **WINNER**
6. **Far-2**: [1.5, 2.5, 3.5] mm - Target range + extension
7. **Mid**: [1.5, 2.15, 2.8] mm - Tight spacing in target

## 📊 Key Results

🏆 **Optimal Configuration: Far-1 (1.5-2.25-3.0mm)**
- **Average RMS Error: 16.1 ± 3.7 μm**
- **7.8x improvement** over worst-performing configuration
- All calibration points within target operating range (1.5-3.0mm)
- Consistent performance across all sensor types

### Performance Comparison
| Configuration | Avg RMS Error (μm) | Performance Rank |
|--------------|-------------------|------------------|
| **Far-1** ⭐ | **16.1 ± 3.7** | **#1** |
| Far-2 | 21.8 ± 5.0 | #2 |
| Mid | 22.2 ± 8.6 | #3 |
| Standard | 23.2 ± 7.4 | #4 |
| Wide-2 | 53.8 ± 11.6 | #5 |
| Short | 35.8 ± 7.2 | #6 |
| Wide-1 | 126.9 ± 25.5 | #7 |

## 🔧 Sensors Analyzed

- **43220065 ROS1** and **ROS2** - High-precision proximity sensors
- **12220031 ROS1** and **ROS2** - Industrial measurement sensors

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ros-sensor-calibration-optimizer.git
   cd ros-sensor-calibration-optimizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis**:
   ```bash
   python range_calibration_analyzer.py
   ```

4. **View results**: Check generated visualizations and `updated_results_summary.py` output

## 📈 Sample Output

### Key Results Visualization
![Calibration Comparison](./outputs/calibration_comparison_plots.png)
*Comparison of all 7 calibration scenarios showing Far-1 as the optimal configuration*

![Comprehensive Analysis](./outputs/comprehensive_calibration_analysis.png)  
*Detailed statistical analysis demonstrating 7.8x improvement in sensor accuracy*

### Complete Analysis Suite
The tool generates comprehensive analysis including:
- 📊 **Performance comparison charts** - Visual ranking of all calibration methods
- 📋 **Statistical summary tables** - Quantitative results with confidence intervals
- 🎯 **Error analysis visualizations** - RMS error breakdown and trend analysis  
- 📝 **Detailed calibration recommendations** - Data-driven optimization guidance

> 🔍 **[View All Visualizations →](./outputs/)**

## Data Source

Analysis is performed on sensor measurement data from:
- Excel file containing distance vs. sensor reading measurements
- Distance range: 0.1-4.0mm with ~0.1mm spacing
- Target evaluation range: 1.5-3.0mm (optimal sensor operating zone)

## Calibration Model

Uses exponential decay function: **S = A × exp(-B × x) + C**
- S = Sensor reading
- x = Distance
- A, B, C = Calibration coefficients calculated for each scenario

## 🛠️ Technical Stack

- **Python 3.8+** - Core programming language
- **NumPy & Pandas** - Data analysis and numerical computations
- **Matplotlib & Seaborn** - Advanced data visualization
- **OpenPyXL** - Excel file processing
- **SciPy** - Statistical analysis and optimization

## 📁 Project Structure

```
ros-sensor-calibration-optimizer/
├── range_calibration_analyzer.py    # Main analysis engine
├── updated_results_summary.py       # Results summary and insights
├── README.md                       # Project documentation
├── requirements.txt               # Python dependencies
├── .gitignore                    # Git ignore rules
└── outputs/                      # Generated visualizations
    ├── calibration_comparison_plots.png
    ├── error_analysis_detailed.png
    ├── comprehensive_summary_table.png
    └── ...
```

## 🔍 Methodology

**Calibration Model**: Exponential decay function `S = A × exp(-B × x) + C`
- **S**: Sensor reading
- **x**: Distance measurement  
- **A, B, C**: Optimized calibration coefficients

**Evaluation Criteria**:
- RMS Error in target range (1.5-3.0mm)
- R² coefficient of determination
- Statistical consistency across sensors

## 📞 Contact & Portfolio

This project demonstrates expertise in:
- 📊 **Data Analysis & Visualization**
- 🔬 **Scientific Computing & Optimization** 
- 🤖 **Sensor Systems & Robotics**
- 📈 **Statistical Analysis & Modeling**

---

*Part of my data science and engineering portfolio - Available for opportunities in sensor systems, robotics, and data analysis*
