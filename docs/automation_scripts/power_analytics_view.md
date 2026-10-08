# 3-Phase Analytics & PUE Validation Engine

This production-grade core calculation module extracts 3-phase line current balances, tracks vector neutral unbalance return values, and logs datacenter PUE metrics.

### Interactive Calculation Sandbox

Click **LOAD** to spin up the WebAssembly runtime environment, alter the system metrics directly in the box below, and click **Run**.

```python { .python .pyscript }
--8<-- "automation_scripts/power_analytics.py"
```
