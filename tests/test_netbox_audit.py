from docs.automation_scripts.netbox_audit import NetBoxRedundancyAuditor

def test_mock_fallback_audit_report():
    """Validates that auditor engine reports structural data format correctly under sandboxed modes."""
    auditor = NetBoxRedundancyAuditor(api_url="mock://local", api_token="dummy")
    results = auditor.audit_device_power_redundancy(site_slug="pdx01")
    
    assert results["site"] == "pdx01"
    assert "compliant_devices" in results
    assert "non_compliant_devices" in results
    assert len(results["non_compliant_devices"]) > 0
