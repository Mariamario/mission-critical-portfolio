# Mission Critical Engineering Portfolio

Welcome to my portfolio. Below is an interactive sandbox powered by WebAssembly. You can edit the kW figures directly in your browser and run the simulation.

### 3-Phase Analytics Sandbox

Click \*\*LOAD\*\* below to activate the isolated Python environment, change the values, and click \*\*Run\*\*.

```python

import math



# Editable parameters for portfolio review

voltage_ll = 415.0

phase_kw = (18.5, 11.2, 7.8)  # Edit these values to test unbalance!

power_factor = 0.95



voltage_ln = voltage_ll / math.sqrt(3)



# 3-Phase currents calculation

ia = (phase_kw[0] * 1000) / (voltage_ln * power_factor)

ib = (phase_kw[1] * 1000) / (voltage_ln * power_factor)

ic = (phase_kw[2] * 1000) / (voltage_ln * power_factor)



# Vectorial neutral calculations

inside_sqrt = (ia**2 + ib**2 + ic**2) - (ia * ib) - (ib * ic) - (ic * ia)

neutral_amps = math.sqrt(max(0.0, inside_sqrt))



print("--- Live Engine Analytics Output ---")

print(f"Phase A: {ia:.2f} A | Phase B: {ib:.2f} A | Phase C: {ic:.2f} A")

print(f"Calculated Unbalanced Neutral Load: {neutral_amps:.2f} Amps")

```
