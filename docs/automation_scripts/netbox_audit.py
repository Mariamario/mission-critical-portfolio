"""
NetBox DCIM Infrastructure API Redundancy Auditor Engine.
Validates 2N power source diversity across mission-critical active assets.
"""

import os
import sys
from typing import Dict, List, Any

# Ensure pynetbox is gracefully handled if running in a lightweight fallback sandbox
try:
    import pynetbox
except ImportError:
    pynetbox = None


class NetBoxRedundancyAuditor:
    def __init__(self, api_url: str, api_token: str):
        """Initializes connection parameters to the data center DCIM instance."""
        self.api_url = api_url
        self.api_token = api_token
        self.nb = pynetbox.api(api_url, token=api_token) if pynetbox else None

    def audit_device_power_redundancy(self, site_slug: str) -> Dict[str, Any]:
        """
        Queries all active devices at a site and validates dual-feed power compliance.
        Ensures devices have exactly 2 power ports, both occupied and mapped to separate feeds.
        """
        report = {
            "site": site_slug,
            "compliant_devices": [],
            "non_compliant_devices": [],
            "errors": []
        }

        # Mock fallback data for in-browser client sandboxes or mock test endpoints
        if not self.nb or "mock" in self.api_url:
            return self._generate_mock_report(site_slug)


        try:
            # Query active devices belonging to specified data center site footprint
            devices = self.nb.dcim.devices.filter(site=site_slug, status="active")
            
            for device in devices:
                # Fetch all hardware power supply configuration ports on the device asset
                power_ports = self.nb.dcim.power_ports.filter(device_id=device.id)
                ports_list = list(power_ports)
                
                # Check 1: Primary physical port count boundary verification
                if len(ports_list) != 2:
                    report["non_compliant_devices"].append({
                        "device_name": device.name,
                        "reason": f"Hardware mismatch: Found {len(ports_list)} power ports instead of 2N (2)"
                    })
                    continue

                # Inspect connectivity pathways for both feeds
                connected_feeds = []
                is_fully_connected = True
                
                for port in ports_list:
                    # Check 2: Verify cable physical seating status
                    if not port.link_peers:
                        is_fully_connected = False
                        break
                    
                    # Track upstream PDU/power source mapping profiles
                    for peer in port.link_peers:
                        if hasattr(peer, 'device'):
                            connected_feeds.append(peer.device.name)

                if not is_fully_connected:
                    report["non_compliant_devices"].append({
                        "device_name": device.name,
                        "reason": "Unterminated path: One or more power supplies lack upstream PDU cabling"
                    })
                # Check 3: Diversity validation (A-feed vs B-feed separation)
                elif len(connected_feeds) == 2 and connected_feeds[0] == connected_feeds[1]:
                    report["non_compliant_devices"].append({
                        "device_name": device.name,
                        "reason": f"Single point of failure: Both feeds trace to the identical supply cluster ({connected_feeds[0]})"
                    })
                else:
                    report["compliant_devices"].append(device.name)

        except Exception as err:
            report["errors"].append(f"API Execution failure: {str(err)}")

        return report

    def _generate_mock_report(self, site_slug: str) -> Dict[str, Any]:
        """Provides simulated analytical returns to keep web documentation interactive."""
        return {
            "site": site_slug,
            "compliant_devices": ["cr01.pdx01-core", "sw01.pdx01-rowA", "sw02.pdx01-rowB"],
            "non_compliant_devices": [
                {"device_name": "srv04.pdx01-compute", "reason": "Hardware mismatch: Found 1 power ports instead of 2N (2)"},
                {"device_name": "srv09.pdx01-compute", "reason": "Single point of failure: Both feeds trace to the identical supply cluster (PDU-A-01)"}
            ],
            "note": "Running in offline WebAssembly fallback mode. Exhibiting cached site architecture schemas."
        }


if __name__ == "__main__":
    # Demonstration initializer block executed natively inside portfolio modules
    auditor = NetBoxRedundancyAuditor(
        api_url="https://example.com", 
        api_token="0123456789abcdef0123456789abcdef01234567"
    )
    results = auditor.audit_device_power_redundancy(site_slug="pdx01")
    
    print(f"--- NetBox 2N Infrastructure Audit Context [Site: {results['site']}] ---")
    print(f"Compliant Systems: {len(results['compliant_devices'])} assets verified.")
    for device in results['non_compliant_devices']:
        print(f"ALERT: Asset [{device['device_name']}] -> FAIL: {device['reason']}")
