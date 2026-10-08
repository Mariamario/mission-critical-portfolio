# 3-Phase Analytics & PUE Validation Engine

This production-grade core calculation module extracts 3-phase line current balances, tracks vector neutral unbalance return values, and logs datacenter PUE metrics.

### Interactive Calculation Sandbox

Click **LOAD** to spin up the WebAssembly runtime environment, alter the system metrics directly in the box below, and click **Run**.

```python { .python .pyscript }
import math

# System Configuration Metrics
voltage_ll = 415.0
phase_kw = (18.5, 11.2, 7.8)
power_factor = 0.95

# Derivation calculation engines
voltage_ln = voltage_ll / math.sqrt(3)

ia = (phase_kw[0] * 1000) / (voltage_ln * power_factor)
ib = (phase_kw[1] * 1000) / (voltage_ln * power_factor)
ic = (phase_kw[2] * 1000) / (voltage_ln * power_factor)

# Vectorial calculations for neutral tracking
inside_sqrt = (ia**2 + ib**2 + ic**2) - (ia * ib) - (ib * ic) - (ic * ia)
neutral_amps = math.sqrt(max(0.0, inside_sqrt))

print("--- Live Engine Analytics Output ---")
print(f"Phase A: {ia:.2f} A | Phase B: {ib:.2f} A | Phase C: {ic:.2f} A")
print(f"Calculated Unbalanced Neutral Load: {neutral_amps:.2f} Amps")
```
