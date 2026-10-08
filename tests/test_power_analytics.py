import pytest
from docs.automation_scripts.power_analytics import PowerAnalyticsEngine

def test_balanced_load_neutral_zero():
    """Verifies that perfectly balanced phase currents yield a net 0 Neutral Amperage."""
    engine = PowerAnalyticsEngine(voltage_ll=415.0)
    
    # Balanced 10kW per phase
    currents = engine.calculate_phase_currents((10.0, 10.0, 10.0), power_factor=1.0)
    neutral = engine.calculate_neutral_current(currents)
    
    assert currents[0] == currents[1] == currents[2]
    assert neutral == 0.0

def test_unbalanced_load_neutral_calculation():
    """Tests neutral calculation vectors using non-trivial unbalanced entries."""
    engine = PowerAnalyticsEngine(voltage_ll=415.0)
    
    # Intentionally unbalanced loads
    currents = engine.calculate_phase_currents((20.0, 10.0, 5.0), power_factor=0.95)
    neutral = engine.calculate_neutral_current(currents)
    
    # Neutral current must be greater than zero when unbalance is high
    assert neutral > 0.0
    assert isinstance(neutral, float)

def test_pue_calculation():
    """Validates baseline and typical efficiency values for tracking software operations."""
    assert PowerAnalyticsEngine.calculate_pue(150.0, 100.0) == 1.50
    assert PowerAnalyticsEngine.calculate_pue(115.0, 100.0) == 1.15

def test_pue_division_by_zero():
    """Ensures improper infrastructure parameters raise correct errors."""
    with pytest.raises(ValueError):
        PowerAnalyticsEngine.calculate_pue(100.0, 0.0)
