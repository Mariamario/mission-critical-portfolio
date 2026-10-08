# 2N Redundant Single-Line Diagram Specifications

This specification delineates the electrical topology, physical switchgear separation, and automated interlocking logic for the **2N Redundant Power Distribution Architecture**. The design guarantees concurrent maintainability and fault isolation down to the component level without interrupting the critical IT load.

## 1. System Topology & Dual-Feed Architecture

The facility maintains two completely independent, mirrored power paths (**Side A** and **Side B**). There are no electrical cross-ties or common busses on the downstream output side of the Uninterruptible Power Supply (UPS) systems, eliminating all systemic single points of failure (SPOF).

```mermaid
graph TD
    %% Utility Infeeds
    subgraph Utility Grid Sources
        UtilA[Utility Feed A: 13.8kV]
        UtilB[Utility Feed B: 13.8kV]
    end

    %% Side A Infrastructure
    subgraph Power Path A - Alpha Train
        UtilA --> XFMR_A[XFMR-A: 13.8kV to 415V]
        XFMR_A --> SWG_A[Main Switchgear SWG-A]
        SWG_A --> UPS_A[UPS System A: 500kVA N+1]
        UPS_A --> PDU_A[Floor PDU-A]
    end

    %% Side B Infrastructure
    subgraph Power Path B - Beta Train
        UtilB --> XFMR_B[XFMR-B: 13.8kV to 415V]
        XFMR_B --> SWG_B[Main Switchgear SWG-B]
        SWG_B --> UPS_B[UPS System B: 500kVA N+1]
        UPS_B --> PDU_B[Floor PDU-B]
    end

    %% Critical IT Dual-Corded Assets
    subgraph Critical IT Load
        PDU_A --> Server[Dual-Corded Production Rack Server]
        PDU_B --> Server
    end

    style Power Path A - Alpha Train fill:#f5faff,stroke:#005dc0,stroke-width:2px
    style Power Path B - Beta Train fill:#fff5f5,stroke:#c00000,stroke-width:2px
    style Critical IT Load fill:#f5fff5,stroke:#008000,stroke-width:2px
```

## 2. Component System Specifications

### Main Medium-Voltage Switchgear (SWG-A & SWG-B)

- **Voltage Rating:** 13.8 kV Nominal, 3-Phase, 3-Wire, 60Hz.
- **Interrupting Rating:** 40kA Symmetrical Short Circuit current.
- **Interlocking Scheme:** Keyed-exchange system (Kirk Key) configured to prevent concurrent closing of the main utility breaker and the emergency generator breaker during un-synchronized manual transfers.

### Power Distribution Units (PDU-A & PDU-B)

- **Voltage Configuration:** 415V Line-to-Line (240V Line-to-Neutral), 3-Phase, 4-Wire + Ground.
- **Isolation Transformer:** K-Factor K-13 rated for harmonic mitigation arising from non-linear IT switch-mode power supplies.
- **Monitoring Matrix:** Real-time branch circuit monitoring capturing Phase Current (A), Neutral Current Vector (A), Voltage Balance (%), and active Power Factor tracking.

!!! note "Neutral Balancing Metric Link"
The line currents and unbalance return tracking models parsed by this PDU hardware map directly to the calculation engines exposed inside our **[3-Phase Analytics Framework](../automation_scripts/power_analytics_view.md)**.
