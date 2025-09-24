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

## 📊 Analysis Process & Visualizations

The analysis follows a systematic approach from raw data processing to optimal calibration identification:

### 1. Data Preprocessing & Quality Control
**`sensor_jumps_detection.png`** - **Step Detection Algorithm**  
From continuous sensor measurements, automated detection identifies discrete ROS position changes during data collection. This critical preprocessing step ensures each measurement corresponds to a known distance position, enabling accurate calibration point extraction.

### 2. Raw Data Analysis & Interpolation  
**`raw_data_analysis.png`** - **Sensor Response Curves**  
**`sensor_measurements_plot.png`** - **Individual Sensor Characteristics**  
Display original sensor measurements across the full distance range (0.1-4.0mm) with mathematical interpolation. Shows the exponential decay behavior that characterizes ROS sensor response.

### 3. Mathematical Model Selection
Multiple calibration functions were tested (linear, polynomial, logarithmic, exponential). **The exponential decay model (`S = A × exp(-B × x) + C`) demonstrated superior performance** across all sensors and was selected for the optimization study.

### 4. Calibration Scenario Comparison
**`comprehensive_summary_table.png`** - **Complete Results Matrix**  
**`calibration_summary_table.png`** - **Performance Rankings**  
Comprehensive comparison of all 7 calibration point configurations showing both raw statistical data and performance scores. Clear identification of Far-1 as the optimal configuration.

### 5. Target Range Error Analysis
**`error_analysis_detailed.png`** - **Calibration Accuracy in Operating Zone (1.5-3.0mm)**  
Detailed RMS error analysis focused on the sensors' intended operating range. Demonstrates why Far-1 configuration achieves superior performance where accuracy matters most.

### 6. Performance Metrics & Validation
**`calibration_range_analysis_comprehensive.png`** - **RMS Error and R² Correlation Analysis**  
Final validation showing both RMS error (measurement accuracy) and R² values (model fit quality) across all calibration scenarios.

> 🔍 **[View All Analysis Results →](./outputs/)**

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

![Step Detection](./outputs/sensor_jumps_detection.png)
*Automated detection of ROS position changes from continuous sensor data - enabling precise calibration point identification*

![Raw Data Analysis](./outputs/raw_data_analysis.png)
*Original sensor measurements showing exponential decay characteristics with mathematical interpolation*

![Results Summary](./outputs/comprehensive_summary_table.png)
*Complete performance comparison showing Far-1 configuration achieving optimal accuracy*

![Error Analysis](./outputs/error_analysis_detailed.png)  
*RMS error analysis in target operating range (1.5-3.0mm) demonstrating 7.8x improvement*

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
├── README.md                    # Main project documentation
├── PORTFOLIO.md                 # Portfolio showcase  
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── range_calibration_analyzer.py # Main analysis engine
├── updated_results_summary.py   # Results summary and insights
└── outputs/                     # Generated analysis visualizations
    ├── sensor_jumps_detection.png      # Step detection preprocessing
    ├── raw_data_analysis.png           # Original sensor data
    ├── sensor_measurements_plot.png    # Individual sensor curves
    ├── comprehensive_summary_table.png # Complete results matrix
    ├── calibration_summary_table.png   # Performance rankings
    ├── error_analysis_detailed.png     # Target range accuracy
    └── calibration_range_analysis_comprehensive.png # RMS & R² metrics
```

## 🔍 Methodology

### Mathematical Model
**Calibration Function**: Exponential decay `S = A × exp(-B × x) + C`
- **S**: Sensor reading
- **x**: Distance measurement  
- **A, B, C**: Optimized calibration coefficients

*Multiple function types were tested (linear, polynomial, logarithmic, exponential). The exponential model provided the best fit for ROS sensor physics.*

### Evaluation Metrics & Rationale

**Primary Metric: RMS Error in Target Range (1.5-3.0mm)**
- **Why**: Sensors must perform optimally in their intended operating zone
- **Calculation**: √(Σ(predicted - actual)²/n) for measurements within 1.5-3.0mm only
- **Advantage**: Eliminates bias from extrapolation errors outside working range

**Secondary Metric: R² Coefficient of Determination**  
- **Purpose**: Validates mathematical model quality and fit consistency
- **Range**: 0-1 (higher = better correlation between model and measurements)
- **Use**: Ensures calibration reliability across full measurement range

**Statistical Validation**: Cross-sensor consistency analysis
- Tests performance across multiple sensor units (4 total)
- Validates that optimal configuration works universally, not just for specific sensors

## 📞 Contact & Portfolio

This project demonstrates expertise in:
- 📊 **Data Analysis & Visualization**
- 🔬 **Scientific Computing & Optimization** 
- 🤖 **Sensor Systems & Robotics**
- 📈 **Statistical Analysis & Modeling**

---

*Part of my data science and engineering portfolio - Available for opportunities in sensor systems, robotics, and data analysis*
