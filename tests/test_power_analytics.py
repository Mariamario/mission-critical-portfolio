import pytest
from docs.automation_scripts.power_analytics import calculate_facility_pue, analyze_three_phase_system

def test_pue_accuracy_metrics():
    """Validates data center PUE parameters against strict metric targets."""
    results = calculate_facility_pue(1450.0, 1100.0)
    assert results["pue"] == 1.318

def test_three_phase_balance_neutral():
    """Verifies perfectly balanced current vectors output a net 0.0A return loop."""
    results = analyze_three_phase_system(40.0, 40.0, 40.0, v_line_to_line=208.0)
    assert results["neutral_current_amps"] == 0.0
