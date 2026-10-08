"""
3-Phase Electrical Load, Neutral Unbalance, and PUE Calculation Engine.
Provides calculation frameworks for mission-critical infrastructure metrics.
"""

import math
from typing import Dict, Tuple

class PowerAnalyticsEngine:
    def __init__(self, voltage_ll: float = 415.0):
        """
        Initializes engine with a standard Line-to-Line voltage.
        Default is 415V LL (yielding ~240V Line-to-Neutral).
        """
        self.voltage_ll = voltage_ll
        self.voltage_ln = voltage_ll / math.sqrt(3)

    def calculate_phase_currents(self, phase_kw: Tuple[float, float, float], power_factor: float = 0.95) -> Tuple[float, float, float]:
        """
        Calculates Line Currents (Amps) for Phase A, B, and C assuming a steady Power Factor.
        Formula: I = (kW * 1000) / (V_ln * PF)
        """
        if power_factor <= 0 or power_factor > 1.0:
            raise ValueError("Power factor must be strictly between 0 and 1.0")
            
        ia = (phase_kw[0] * 1000) / (self.voltage_ln * power_factor)
        ib = (phase_kw[1] * 1000) / (self.voltage_ln * power_factor)
        ic = (phase_kw[2] * 1000) / (self.voltage_ln * power_factor)
        return (round(ia, 2), round(ib, 2), round(ic, 2))

    def calculate_neutral_current(self, currents: Tuple[float, float, float]) -> float:
        """
        Calculates vector sum of neutral current resulting from unbalance.
        Formula: I_n = sqrt(Ia^2 + Ib^2 + Ic^2 - (Ia*Ib) - (Ib*Ic) - (Ic*Ia))
        """
        ia, ib, ic = currents
        inside_sqrt = (ia**2 + ib**2 + ic**2) - (ia * ib) - (ib * ic) - (ic * ia)
        # Account for precision boundaries close to 0
        return round(math.sqrt(max(0.0, inside_sqrt)), 2)

    @staticmethod
    def calculate_pue(total_facility_kw: float, it_equipment_kw: float) -> float:
        """
        Calculates Power Usage Effectiveness (PUE).
        Formula: Total Facility Energy / IT Equipment Energy
        """
        if it_equipment_kw <= 0:
            raise ValueError("IT Equipment Load must be greater than 0 kW to compute PUE.")
        return round(total_facility_kw / it_equipment_kw, 3)


if __name__ == "__main__":
    # Sample runtime demonstration for site visitors
    engine = PowerAnalyticsEngine(voltage_ll=415.0)
    
    # 15kW on Phase A, 12kW on Phase B, 10kW on Phase C
    sample_kw = (15.0, 12.0, 10.0)
    amps = engine.calculate_phase_currents(sample_kw, power_factor=0.95)
    neutral = engine.calculate_neutral_current(amps)
    pue = engine.calculate_pue(total_facility_kw=65.0, it_equipment_kw=37.0)
    
    print(f"Calculated Currents (A): Phase A: {amps[0]}, Phase B: {amps[1]}, Phase C: {amps[2]}")
    print(f"Resulting Vector Neutral Current: {neutral} A")
    print(f"Calculated Data Center PUE: {pue}")
