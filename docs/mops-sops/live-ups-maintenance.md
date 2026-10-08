# Live Zero-Downtime UPS Bypass Method of Procedure (MOP)

This Method of Procedure (MOP) outlines the rigid, breaker-level switching sequence required to safely isolate a **500kVA UPS Module** and transition its downstream critical bus to external mechanical bypass.

This procedure must be executed without dropping the critical IT payload.

!!! danger "Critical Safety Thresholds"
_ **DO NOT** attempt manual transfers if the UPS internal static bypass fails to synchronize with the utility bypass source source.
_ Phase angle displacement between the inverter output and bypass input **MUST BE < 3 DEGREES**. \* Failure to strictly follow this sequence will trigger an out-of-phase cross-fault, causing catastrophic arc-flash destruction or total downstream data center load dropped blackout.

---

## Pre-Flight Automation Validation Checklist

Before throwing any physical handles, run the structural electrical analysis validation routines to ensure your distribution networks have stable capacity tolerances:

1. **Verify Source Phase Alignments:** Check that upstream source vectors match parameters.
2. **Execute System Health Verification:** Verify zero active active alarms exist on the target module control panel.

---

## Phase 1: Internal Static Bypass Sync Sequence

???+ info "Step 1: Command the Inverter to Synchronize"
_ Navigate to the liquid crystal touch interface panel on the front cabinet door of **UPS-A**.
_ Select **Operations Menu** -> **Transfer to Static Bypass**.
_ Verify via the mimic panel graphic that the load has transitioned seamlessly from the inverter components over to the internal static bypass circuit path.
_ _Inverter Output Amperage should drop to 0A; Static Bypass line current should rise proportionally._

---

## Phase 2: Physical Switchgear Isolation Sequence

???+ warning "Step 2: Activating the Mechanical Isolation Breakers"
Follow this absolute sequential path to transfer the load to the external wrap-around physical maintenance panel:

    1. **CLOSE Breaker MBB (Maintenance Bypass Breaker):**
       *Locate the external bypass panel cabinet. Throw breaker MBB into the full ON position. The system is now temporarily operating on a dual-feed parallel path between the static switch and the physical maintenance wrap-around link.*
    2. **OPEN Breaker MIB (Maintenance Isolation Breaker):**
       *Throw breaker MIB into the full OFF position. This safely drops out the downstream static bypass feed path, shifting 100% of the active critical IT power exclusively onto the isolated mechanical bypass breaker.*
    3. **OPEN Breaker UIO (UPS Input & Output Isolation Handles):**
       *Open the primary input and output isolation distribution breakers on the main power distribution boards to completely isolate the internal electronics framework of the UPS vault.*

---

## Phase 3: Lockout / Tagout (LOTO) & Safe Discharge State

???+ success "Step 3: Verification of Zero Energy State"
_ Apply structural padlocks and safety tags to all open input and output circuit breakers in accordance with standard OSHA requirements.
_ **WAIT 10 MINUTES** for internal link capacitor banks to completely discharge residual DC voltages down to < 50VDC before opening enclosure access panels. \* Use a calibrated digital multimeter to verify absolute zero electrical state across all raw terminal busses prior to touching internal components.
