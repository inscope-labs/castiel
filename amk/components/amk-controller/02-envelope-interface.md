# Envelope Interface

**File number:** 3  
**Overview.**  
This module defines the common validation rules the controller applies to every request envelope and the catalogue of envelope types it exchanges with consoles and other parties. All control-plane interaction with consoles occurs through these envelopes.

---

## Common Validation Rules

- **CTR-3:1** The controller MUST validate every request envelope against CTR-3:2 to CTR-3:5, CTR-3:9 to CTR-3:11, and CTR-3:15.
- **CTR-3:2** The controller MUST reject any envelope whose signature fails verification against a registered console key (or other expected sender key).
- **CTR-3:3** The controller MUST reject any envelope whose timestamp falls outside the allowed skew window.
- **CTR-3:4** The controller MUST reject any envelope whose nonce has been seen before.
- **CTR-3:5** Under Standard and High profiles the controller MUST enforce strict monotonic sequence numbers per sender identity. The Basic profile MAY use weaker sequencing.
- **CTR-3:6** Unknown commands MUST be rejected; existence confers no authority.

## Envelope Catalogue (Core Types)

- **CTR-3:7** The following envelope types are recognized. Additional types may be defined by companion specifications provided they obey the common rules.

| Type | Direction | Purpose |
|---|---|---|
| `SessionStart` / `ExecutionProfile` | Console → Controller | Initiate session and supply work orders, runtimes, context |
| `SurfaceProposal` | Controller → Console | Proposed surface for validation |
| `SurfaceAcceptance` / `SurfaceRejection` | Console → Controller | Result of console validation gates |
| `Handoff` | Controller → Console | Session start credential |
| Runtime subtree intake (type name open, see CTR-O-13) | Console → Controller | Supply a console-scoped runtime subtree |
| `RuntimeInclusionDecision` | Console → Controller | Approve or deny inclusion of an already-registered runtime in a running session (see CTR-O-13) |
| `WorkOrder` / `WorkOrderUpdate` | Console → Controller | Create, extend, renew, cancel |
| `PreAuthorization` | Console → Controller | Create, change, or revoke a pre-authorization |
| `Revocation` | Console → Controller | Immediate revocation |
| `StatusQuery` / `StatusResponse` | Console ↔ Controller | State, audit, or risk information |
| `Notification` | Controller → Console | Pending decision or event |
| `CapabilityToken` | Controller → authorized party | Short-lived capability token |
| `ValidatorEvidence` | Console → Controller | Optional session-validator evidence |
| `Genesis` | Console → Controller | Console-signed anchor that locks console, Host AI, controller and gateways into one session; the genesis value MUST be 0 at handoff (see CTR-O-12) |
| `TurnReceipt` | Console → Controller | Console-signed receipt for a turn (see CTR-O-12) |

- **CTR-3:8** All of the above are ordinary envelopes subject to the common rules. No transport other than the channels defined in CTR-3:12 is permitted for control-plane actions between console and controller.

## Additional Validation Rules

- **CTR-3:9** The controller MUST reject any envelope that does not use the canonical serialization defined for its type.
- **CTR-3:10** Every envelope MUST contain a `contract_version` equal to the suite major.minor to which the sender conforms (`amk-ssot.md`, SSOT-1:3). The controller MUST reject any envelope whose `contract_version` it does not support, and MUST NOT silently downgrade.
- **CTR-3:11** Every envelope MUST contain a `ttl`. The controller MUST reject any envelope whose `ttl` has expired.

## Channels

- **CTR-3:12** The controller and a console communicate over two distinct channels. The **administrative channel** is direct, its trust is rooted in the Release Key, and it is required to initiate a session. The **session channel** carries all session-based communication through the session router; envelopes are router payloads.
- **CTR-3:13** `SessionStart` is received on the administrative channel. Once a session handle has been allocated, every session-related envelope MUST use the session channel. The assignment of the remaining envelope types to channels is not yet defined (see CTR-O-11).
- **CTR-3:14** The encapsulation of envelopes as router payloads, and the relationship between the session router and the HTSM Host AI channel, are defined by the session-router specification (see CTR-O-11).

## Nonce Length

- **CTR-3:15** Every nonce MUST be at least 128 bits.
