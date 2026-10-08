"""
Data Center Power Analytics & Efficiency Engine
Calculates rack power budgets, 3-phase line currents, neutral conductor loading,  
and facility Power Usage Effectiveness (PUE) metrics.  
"""
import math
import sys
from typing import Dict, List, Any

def calculate_rack_power(devices: List[Dict[str, Any]]) -> Dict[str, float]:
    total_nameplate_watts = 0.0
    total_actual_measured_watts = 0.0
    for dev in devices:
        nameplate = float(dev.get("nameplate_watts", 0.0))
        actual = float(dev.get("actual_measured_watts", nameplate * 0.60))
        total_nameplate_watts += nameplate
        total_actual_measured_watts += actual
    static_derated_budget_watts = total_nameplate_watts * 0.60
    stranded_capacity_recovered_watts = static_derated_budget_watts - total_actual_measured_watts
    return {
        "total_nameplate_watts": total_nameplate_watts,
        "total_actual_measured_watts": total_actual_measured_watts,
        "static_derated_budget_watts": static_derated_budget_watts,
        "stranded_capacity_recovered_watts": stranded_capacity_recovered_watts,
    }

def analyze_three_phase_system(line_a_amps: float, line_b_amps: float, line_c_amps: float, v_line_to_line: float = 208.0, power_factor: float = 0.95) -> Dict[str, Any]:
    if any(i < 0 for i in (line_a_amps, line_b_amps, line_c_amps)):
        raise ValueError("Line currents must be non-negative values.")
    if v_line_to_line <= 0:
        raise ValueError("Line-to-Line voltage must be greater than zero.")
    if not (0.0 < power_factor <= 1.0):
        raise ValueError("Power factor must be strictly between 0.0 and 1.0.")
    avg_current_amps = (line_a_amps + line_b_amps + line_c_amps) / 3.0
    if avg_current_amps == 0.0:
        return {"status": "NO_LOAD", "apparent_power_kva": 0.0, "active_power_kw": 0.0, "neutral_current_amps": 0.0, "imbalance_percent": 0.0}
    apparent_power_kva = (math.sqrt(3) * v_line_to_line * avg_current_amps) / 1000.0
    active_power_kw = apparent_power_kva * power_factor
    neutral_current_amps = math.sqrt(line_a_amps**2 + line_b_amps**2 + line_c_amps**2 - (line_a_amps * line_b_amps + line_b_amps * line_c_amps + line_c_amps * line_a_amps))
    max_deviation = max(abs(line_a_amps - avg_current_amps), abs(line_b_amps - avg_current_amps), abs(line_c_amps - avg_current_amps))
    imbalance_percent = (max_deviation / avg_current_amps) * 100.0
    status = "CRITICAL_IMBALANCE" if (imbalance_percent > 20.0 or neutral_current_amps > (0.5 * avg_current_amps)) else "BALANCED"
    return {
        "line_a_amps": line_a_amps, "line_b_amps": line_b_amps, "line_c_amps": line_c_amps,
        "average_amps": round(avg_current_amps, 2), "neutral_current_amps": round(neutral_current_amps, 2),
        "apparent_power_kva": round(apparent_power_kva, 2), "active_power_kw": round(active_power_kw, 2),
        "imbalance_percent": round(imbalance_percent, 2), "status": status
    }

def calculate_facility_pue(total_facility_kw: float, it_equipment_kw: float) -> Dict[str, float]:
    if it_equipment_kw <= 0.0:
        raise ValueError("IT Equipment Power must be greater than zero.")
    if total_facility_kw < it_equipment_kw:
        raise ValueError("Total Facility Power cannot be less than IT Equipment Power.")
    pue = total_facility_kw / it_equipment_kw
    overhead_kw = total_facility_kw - it_equipment_kw
    overhead_percent = (overhead_kw / total_facility_kw) * 100.0
    return {"pue": round(pue, 3), "total_facility_kw": round(total_facility_kw, 2), "it_equipment_kw": round(it_equipment_kw, 2), "overhead_kw": round(overhead_kw, 2), "overhead_percent": round(overhead_percent, 2)}

# Execution handler for live web sandbox environments
rack_devices = [
    {"device_id": "srv-01", "nameplate_watts": 750, "actual_measured_watts": 420},
    {"device_id": "srv-02", "nameplate_watts": 750, "actual_measured_watts": 410},
    {"device_id": "srv-03", "nameplate_watts": 1200, "actual_measured_watts": 680},
]
rack_results = calculate_rack_power(rack_devices)
phase_results = analyze_three_phase_system(line_a_amps=42.5, line_b_amps=48.0, line_c_amps=39.0)
pue_results = calculate_facility_pue(total_facility_kw=1450.0, it_equipment_kw=1100.0)

print(f"--- Power Recovery Framework Metrics ---")
print(f"Recovered Stranded Power Capacity: {rack_results['stranded_capacity_recovered_watts']:.2f} W")
print(f"Calculated System Unbalanced Neutral Return Load: {phase_results['neutral_current_amps']} Amps")
print(f"Calculated Infrastructure Optimization PUE Target: {pue_results['pue']}")
