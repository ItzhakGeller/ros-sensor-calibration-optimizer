"""
Range Calibration Analyzer
=========================

Focused analysis tool for testing different calibration ranges
English output only, statistical analysis across all sensors

Test Scenarios:
1. Standard: [1.0, 2.0, 3.0] mm - Reference
2. Wide-1: [0.5, 2.0, 3.5] mm
3. Wide-2: [0.5, 1.75, 3.0] mm
4. Short: [0.5, 1.5, 2.5] mm
5. Far-1: [1.5, 2.25, 3.0] mm
6. Far-2: [1.5, 2.5, 3.5] mm
7. Mid: [1.5, 2.15, 2.8] mm

Author: Advanced Analysis Tool
Date: September 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
import warnings

warnings.filterwarnings("ignore")

# Professional plotting style
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 11
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 10


@dataclass
class ScenarioResult:
    """Result for a single scenario"""

    scenario_name: str
    points: List[float]
    rms_error: float
    r_squared: float
    range_span: float
    sensor_name: str


@dataclass
class ScenarioSummary:
    """Statistical summary for a scenario across all sensors"""

    scenario_name: str
    points: List[float]
    rms_mean: float
    rms_std: float
    r2_mean: float
    r2_std: float
    improvement_vs_ref: float
    range_span: float


class RangeCalibrationAnalyzer:
    """Simple, focused calibration range analyzer"""

    def __init__(self, excel_file_path: str, sheet_name: str = "all raw"):
        """Initialize analyzer"""
        self.excel_file = excel_file_path
        self.sheet_name = sheet_name
        self.sensors = {}
        self.results = {}

        # Test scenarios
        self.scenarios = {
            "Standard": [1.0, 2.0, 3.0],  # Reference
            "Wide-1": [0.5, 2.0, 3.5],  # Wide range 1
            "Wide-2": [0.5, 1.75, 3.0],  # Wide range 2
            "Short": [0.5, 1.5, 2.5],  # Short range
            "Far-1": [1.5, 2.25, 3.0],  # Far range 1
            "Far-2": [1.5, 2.5, 3.5],  # Far range 2
            "Mid": [1.5, 2.15, 2.8],  # Mid range
        }

        print("🎯 Range Calibration Analyzer Initialized")
        print(f"📁 File: {excel_file_path}")
        print(f"📊 Scenarios: {len(self.scenarios)}")

    def load_sensor_data(self, column: str) -> Dict:
        """Load sensor data from Excel column using proven method from original code"""
        try:
            # Read the Excel file
            df_raw = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)

            # Get column index
            col_index = ord(column.upper()) - ord("A")  # Convert A,B,C,D,E to 0,1,2,3,4

            # Get sensor name from row 2 (index 1) - the actual header row
            if col_index < df_raw.shape[1] and len(df_raw) > 1:
                sensor_name = df_raw.iloc[1, col_index]  # Row 2 contains sensor names
                print(
                    f"   Sensor name from header (row 2, column {column}): {sensor_name}"
                )

                # Clean the sensor name
                if (
                    pd.isna(sensor_name)
                    or str(sensor_name).replace(".", "").replace(",", "").isdigit()
                ):
                    if len(df_raw) > 0:
                        sensor_name = df_raw.iloc[0, col_index]
                        print(f"   Trying row 1 instead: {sensor_name}")

                    if (
                        pd.isna(sensor_name)
                        or str(sensor_name).replace(".", "").replace(",", "").isdigit()
                    ):
                        sensor_name = f"Sensor_{column}"
                        print(f"   Using default name: {sensor_name}")

                sensor_name = str(sensor_name).strip()
            else:
                sensor_name = f"Sensor_{column}"
                print(f"   Could not read sensor name, using default: {sensor_name}")

            # Start reading data from row 3 (index 2) onwards - skip header rows
            data_start_row = 2

            # Extract distance (column A) and sensor data (specified column)
            distance_data = df_raw.iloc[data_start_row:, 0]  # Column A - distance
            sensor_data = df_raw.iloc[
                data_start_row:, col_index
            ]  # Specified column - sensor reading

            # Convert to numeric and remove NaN values
            distance_numeric = pd.to_numeric(distance_data, errors="coerce")
            sensor_numeric = pd.to_numeric(sensor_data, errors="coerce")

            # Create DataFrame and remove rows with NaN values
            df = pd.DataFrame(
                {"distance": distance_numeric, "sensor_reading": sensor_numeric}
            ).dropna()

            # Filter to distance <= 4
            df = df[df["distance"] <= 4].copy()

            print(f"   ✅ Loaded {len(df)} data points for {sensor_name}")
            if len(df) > 0:
                print(
                    f"      Distance range: {df['distance'].min():.3f} - {df['distance'].max():.3f} mm"
                )
                print(
                    f"      Reading range: {df['sensor_reading'].min():.0f} - {df['sensor_reading'].max():.0f}"
                )

            return {
                "name": sensor_name,
                "distances": df["distance"].values,
                "readings": df["sensor_reading"].values,
            }

        except Exception as e:
            print(f"   ❌ Error loading data from column {column}: {e}")
            return {}

    def load_all_sensors(self, columns: List[str] = ["B", "C", "D", "E"]) -> None:
        """Load all sensors"""
        print(f"\n📡 Loading sensors from columns: {columns}")

        for column in columns:
            sensor_data = self.load_sensor_data(column)
            self.sensors[sensor_data["name"]] = sensor_data
            print(
                f"   ✅ {sensor_data['name']}: {len(sensor_data['distances'])} points"
            )

        print(f"✅ Loaded {len(self.sensors)} sensors successfully")

    def calculate_exponential_calibration(
        self, sensor_readings: List[float], distances: List[float]
    ) -> Dict[str, float]:
        """Calculate exponential calibration parameters - EXACT copy from working original code"""
        S1, S2, S3 = sensor_readings
        X1, X2, X3 = distances

        # Check sensor behavior - for ROS, readings should decrease with distance
        if S1 < S2 or S2 < S3:
            print(
                f"   WARNING: Sensor readings should decrease with distance for ROS sensors!"
            )
            print(
                f"   S1={S1:.1f} at {X1}mm, S2={S2:.1f} at {X2}mm, S3={S3:.1f} at {X3}mm"
            )

        # Calculate terms
        term1 = S1 - S3
        term2 = S2 - S3
        term3 = S1 - S2

        # Calculate discriminant
        discriminant = term1**2 - 4 * term2 * term3

        if discriminant < 0:
            return {"A": 0, "B": 0, "C": 0}

        sqrt_discriminant = np.sqrt(discriminant)

        # Apply the correct formula from original code
        denominator = 2 * term2  # 2*(S2-S3)
        if abs(denominator) < 1e-10:
            return {"A": 0, "B": 0, "C": 0}

        # Calculate the two possible arguments for the natural logarithm
        numerator_plus = term1 + sqrt_discriminant  # (S1-S3) + SQRT(...)
        numerator_minus = term1 - sqrt_discriminant  # (S1-S3) - SQRT(...)

        # Calculate the arguments for ln() - this is the complete fraction inside ln()
        ln_arg_plus = numerator_plus / denominator
        ln_arg_minus = numerator_minus / denominator

        # Calculate B values using the natural logarithm - NO DIVISION BY (X1-X3)!
        B_plus = np.log(ln_arg_plus) if ln_arg_plus > 0 else np.nan
        B_minus = np.log(ln_arg_minus) if ln_arg_minus > 0 else np.nan

        # For decreasing ROS sensors, we want B > 0
        if not np.isnan(B_plus) and B_plus > 0:
            B = B_plus
        elif not np.isnan(B_minus) and B_minus > 0:
            B = B_minus
        else:
            return {"A": 0, "B": 0, "C": 0}

        # Calculate A using: A = (S1-S3)/(exp(-B*X1)-exp(-B*X3))
        exp_neg_BX1 = np.exp(-B * X1)
        exp_neg_BX3 = np.exp(-B * X3)

        denominator_A = exp_neg_BX1 - exp_neg_BX3

        if abs(denominator_A) < 1e-10:
            return {"A": 0, "B": 0, "C": 0}

        A = (S1 - S3) / denominator_A

        # Calculate C using: C = S2 - A*exp(-B*X2)
        exp_neg_BX2 = np.exp(-B * X2)
        C = S2 - A * exp_neg_BX2

        return {"A": A, "B": B, "C": C}

    def calculate_distance_from_reading(
        self, sensor_reading: float, params: Dict[str, float]
    ) -> float:
        """Calculate distance from sensor reading"""
        A, B, C = params["A"], params["B"], params["C"]

        if A == 0 or B == 0:
            return np.nan

        argument = (sensor_reading - C) / A
        if argument <= 0:
            return np.nan

        distance = -np.log(argument) / B
        return distance

    def evaluate_calibration_performance(
        self, sensor_data: Dict[str, np.ndarray], params: Dict[str, float]
    ) -> Tuple[float, float]:
        """Evaluate calibration performance"""
        predicted_distances = []

        # Calculate predicted distances
        for reading in sensor_data["readings"]:
            predicted = self.calculate_distance_from_reading(reading, params)
            predicted_distances.append(predicted)

        predicted_distances = np.array(predicted_distances)
        actual_distances = sensor_data["distances"]

        # Remove invalid values
        valid_mask = ~np.isnan(predicted_distances)
        valid_predicted = predicted_distances[valid_mask]
        valid_actual = actual_distances[valid_mask]

        if len(valid_predicted) == 0:
            return float("inf"), -1.0

        # Calculate errors (bias removed)
        errors = valid_predicted - valid_actual
        mean_error = np.mean(errors)
        bias_removed_errors = errors - mean_error
        rms_error = np.sqrt(np.mean(bias_removed_errors**2))

        # Calculate R²
        ss_res = np.sum(bias_removed_errors**2)
        ss_tot = np.sum((valid_actual - np.mean(valid_actual)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

        return float(rms_error), float(r_squared)

    def test_scenario(
        self, sensor_name: str, points: List[float], scenario_name: str
    ) -> ScenarioResult:
        """Test a single calibration scenario"""
        sensor_data = self.sensors[sensor_name]

        # Interpolate sensor readings at calibration points
        sensor_readings = np.interp(
            points, sensor_data["distances"], sensor_data["readings"]
        )

        print(f"         DEBUG: Points {points} -> Readings {sensor_readings}")

        # Calculate calibration parameters
        params = self.calculate_exponential_calibration(sensor_readings, points)

        print(
            f"         DEBUG: Params A={params['A']:.2e}, B={params['B']:.6f}, C={params['C']:.2e}"
        )

        # Evaluate performance
        rms_error, r_squared = self.evaluate_calibration_performance(
            sensor_data, params
        )

        return ScenarioResult(
            scenario_name=scenario_name,
            points=points,
            rms_error=rms_error,
            r_squared=r_squared,
            range_span=points[2] - points[0],
            sensor_name=sensor_name,
        )

    def run_all_scenarios(self) -> None:
        """Run all calibration scenarios for all sensors"""
        print(f"\n🔬 Running calibration range analysis...")
        print(f"   Sensors: {len(self.sensors)}")
        print(f"   Scenarios: {len(self.scenarios)}")

        all_results = []

        for sensor_name in self.sensors.keys():
            print(f"\n   📊 Testing {sensor_name}:")

            for scenario_name, points in self.scenarios.items():
                result = self.test_scenario(sensor_name, points, scenario_name)
                all_results.append(result)

                print(
                    f"     {scenario_name:8}: RMS={result.rms_error*1000:.1f}μm, R²={result.r_squared:.4f}"
                )

        self.results = all_results
        print(f"\n✅ Analysis complete! {len(all_results)} test results generated.")

    def calculate_scenario_statistics(self) -> List[ScenarioSummary]:
        """Calculate statistics for each scenario across all sensors"""
        summaries = []

        # Group results by scenario
        scenario_groups = {}
        for result in self.results:
            if result.scenario_name not in scenario_groups:
                scenario_groups[result.scenario_name] = []
            scenario_groups[result.scenario_name].append(result)

        # Find reference performance (Standard scenario)
        ref_rms_mean = np.mean([r.rms_error for r in scenario_groups["Standard"]])

        for scenario_name, scenario_points in self.scenarios.items():
            results = scenario_groups[scenario_name]

            rms_values = [r.rms_error for r in results if np.isfinite(r.rms_error)]
            r2_values = [r.r_squared for r in results if np.isfinite(r.r_squared)]

            if len(rms_values) == 0:
                continue

            rms_mean = np.mean(rms_values)
            rms_std = np.std(rms_values)
            r2_mean = np.mean(r2_values)
            r2_std = np.std(r2_values)

            # Calculate improvement vs reference
            improvement = ((ref_rms_mean - rms_mean) / ref_rms_mean) * 100

            summary = ScenarioSummary(
                scenario_name=scenario_name,
                points=scenario_points,
                rms_mean=float(rms_mean),
                rms_std=float(rms_std),
                r2_mean=float(r2_mean),
                r2_std=float(r2_std),
                improvement_vs_ref=float(improvement),
                range_span=scenario_points[2] - scenario_points[0],
            )

            summaries.append(summary)

        return summaries

    def create_summary_table(self) -> pd.DataFrame:
        """Create summary table with statistics"""
        summaries = self.calculate_scenario_statistics()

        # Create DataFrame
        data = []
        for summary in summaries:
            data.append(
                {
                    "Scenario": summary.scenario_name,
                    "Points (mm)": f"{summary.points[0]:.1f}, {summary.points[1]:.2f}, {summary.points[2]:.1f}",
                    "Range Span (mm)": f"{summary.range_span:.1f}",
                    "RMS Mean (μm)": f"{summary.rms_mean*1000:.1f}",
                    "RMS STD (μm)": f"{summary.rms_std*1000:.1f}",
                    "R² Mean": f"{summary.r2_mean:.4f}",
                    "R² STD": f"{summary.r2_std:.4f}",
                    "vs Reference (%)": f"{summary.improvement_vs_ref:+.1f}%",
                }
            )

        df = pd.DataFrame(data)
        return df

    def plot_summary_analysis(self) -> None:
        """Create comprehensive summary plots"""
        summaries = self.calculate_scenario_statistics()

        # Create figure with 3 subplots
        fig = plt.figure(figsize=(18, 12))

        # Plot 1: RMS Error Comparison with Error Bars
        ax1 = plt.subplot(2, 2, 1)

        scenario_names = [s.scenario_name for s in summaries]
        rms_means = [s.rms_mean * 1000 for s in summaries]  # Convert to μm
        rms_stds = [s.rms_std * 1000 for s in summaries]
        improvements = [s.improvement_vs_ref for s in summaries]

        # Color coding by improvement
        colors = [
            "red" if imp < 0 else "green" if imp > 5 else "orange"
            for imp in improvements
        ]

        bars = ax1.bar(
            scenario_names,
            rms_means,
            yerr=rms_stds,
            color=colors,
            alpha=0.7,
            capsize=5,
            edgecolor="black",
        )

        # Reference line
        ref_rms = next(
            s.rms_mean * 1000 for s in summaries if s.scenario_name == "Standard"
        )
        ax1.axhline(
            y=ref_rms,
            color="black",
            linestyle="--",
            linewidth=2,
            label="Reference (Standard)",
        )

        # Add improvement percentages on bars
        for i, (bar, imp) in enumerate(zip(bars, improvements)):
            height = bar.get_height() + rms_stds[i]
            ax1.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + max(rms_means) * 0.02,
                f"{imp:+.1f}%",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        ax1.set_ylabel("RMS Error (μm)")
        ax1.set_title("Calibration Accuracy by Range Scenario")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.get_xticklabels(), rotation=45)

        # Plot 2: R² Comparison
        ax2 = plt.subplot(2, 2, 2)

        r2_means = [s.r2_mean for s in summaries]
        r2_stds = [s.r2_std for s in summaries]

        bars2 = ax2.bar(
            scenario_names,
            r2_means,
            yerr=r2_stds,
            color=colors,
            alpha=0.7,
            capsize=5,
            edgecolor="black",
        )

        ax2.set_ylabel("R² Score")
        ax2.set_title("Calibration Quality (R²)")
        ax2.set_ylim(0.99, 1.0)
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.get_xticklabels(), rotation=45)

        # Plot 3: Range Span vs Performance
        ax3 = plt.subplot(2, 2, 3)

        range_spans = [s.range_span for s in summaries]

        scatter = ax3.scatter(
            range_spans,
            rms_means,
            c=improvements,
            s=100,
            cmap="RdYlGn",
            edgecolors="black",
        )

        # Add scenario labels
        for i, scenario in enumerate(scenario_names):
            ax3.annotate(
                scenario,
                (range_spans[i], rms_means[i]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
            )

        ax3.set_xlabel("Range Span (mm)")
        ax3.set_ylabel("RMS Error (μm)")
        ax3.set_title("Range Span vs Accuracy")
        ax3.grid(True, alpha=0.3)

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label("Improvement vs Reference (%)")

        # Plot 4: Performance Matrix Heatmap
        ax4 = plt.subplot(2, 2, 4)

        # Create matrix data
        sensor_names = list(self.sensors.keys())
        matrix_data = np.zeros((len(sensor_names), len(scenario_names)))

        for i, sensor_name in enumerate(sensor_names):
            for j, scenario_name in enumerate(scenario_names):
                sensor_results = [
                    r
                    for r in self.results
                    if r.sensor_name == sensor_name and r.scenario_name == scenario_name
                ]
                if sensor_results:
                    matrix_data[i, j] = sensor_results[0].rms_error * 1000

        # Create heatmap
        im = ax4.imshow(matrix_data, cmap="RdYlGn_r", aspect="auto")

        # Set ticks and labels
        ax4.set_xticks(range(len(scenario_names)))
        ax4.set_xticklabels(scenario_names, rotation=45)
        ax4.set_yticks(range(len(sensor_names)))
        ax4.set_yticklabels(sensor_names)

        # Add text annotations
        for i in range(len(sensor_names)):
            for j in range(len(scenario_names)):
                text = ax4.text(
                    j,
                    i,
                    f"{matrix_data[i, j]:.1f}",
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )

        ax4.set_title("Performance Matrix (RMS Error μm)")

        # Colorbar for heatmap
        cbar2 = plt.colorbar(im, ax=ax4)
        cbar2.set_label("RMS Error (μm)")

        plt.tight_layout()
        plt.show()

    def print_results(self) -> None:
        """Print comprehensive results"""
        summaries = self.calculate_scenario_statistics()

        print(f"\n📊 CALIBRATION RANGE ANALYSIS RESULTS")
        print("=" * 70)
        print(f"Sensors Analyzed: {len(self.sensors)}")
        print(f"Scenarios Tested: {len(self.scenarios)}")

        # Summary table
        df = self.create_summary_table()
        print(f"\n📋 SUMMARY TABLE:")
        print(df.to_string(index=False))

        # Best and worst scenarios
        valid_summaries = [s for s in summaries if np.isfinite(s.rms_mean)]
        best_scenario = min(valid_summaries, key=lambda x: x.rms_mean)
        worst_scenario = max(valid_summaries, key=lambda x: x.rms_mean)

        print(f"\n🏆 BEST CONFIGURATION:")
        print(f"   Scenario: {best_scenario.scenario_name}")
        print(f"   Points: {best_scenario.points} mm")
        print(f"   Range Span: {best_scenario.range_span:.1f} mm")
        print(
            f"   Average RMS: {best_scenario.rms_mean*1000:.1f} ± {best_scenario.rms_std*1000:.1f} μm"
        )
        print(
            f"   Average R²: {best_scenario.r2_mean:.4f} ± {best_scenario.r2_std:.4f}"
        )
        print(f"   Improvement: {best_scenario.improvement_vs_ref:+.1f}% vs Standard")

        print(f"\n❌ WORST CONFIGURATION:")
        print(f"   Scenario: {worst_scenario.scenario_name}")
        print(f"   Points: {worst_scenario.points} mm")
        print(
            f"   Average RMS: {worst_scenario.rms_mean*1000:.1f} ± {worst_scenario.rms_std*1000:.1f} μm"
        )
        print(f"   Degradation: {worst_scenario.improvement_vs_ref:+.1f}% vs Standard")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")

        wide_scenarios = [s for s in summaries if "Wide" in s.scenario_name]
        if wide_scenarios:
            best_wide = min(wide_scenarios, key=lambda x: x.rms_mean)
            print(
                f"   1. For maximum accuracy: Use {best_wide.scenario_name} configuration"
            )

        stable_scenarios = sorted(summaries, key=lambda x: x.rms_std)[:3]
        print(
            f"   2. For consistency: {stable_scenarios[0].scenario_name} has lowest variability"
        )

        if best_scenario.improvement_vs_ref > 5:
            print(
                f"   3. Significant improvement possible: {best_scenario.improvement_vs_ref:.1f}% better than standard"
            )
        else:
            print(f"   3. Standard configuration is competitive")


def main():
    """Main function for range calibration analysis"""

    # File path
    excel_file_path = r"C:\Users\geller\OneDrive - HP Inc\data\ROS\using ROS for cast iron\ROS vs PIP tsrget in Tamar104 press\summary.xlsx"

    print("🎯 Range Calibration Analysis")
    print("=" * 50)

    # Create analyzer
    analyzer = RangeCalibrationAnalyzer(excel_file_path)

    # Load sensors
    analyzer.load_all_sensors(["B", "C", "D", "E"])

    # Run analysis
    analyzer.run_all_scenarios()

    # Display results
    analyzer.print_results()

    # Create plots
    analyzer.plot_summary_analysis()

    print(f"\n✅ Analysis Complete!")


if __name__ == "__main__":
    main()
