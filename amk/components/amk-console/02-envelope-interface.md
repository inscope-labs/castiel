# Envelope Interface

**File number:** 3  
**Overview.**  
This module defines the sole external communication mechanism of the console: signed envelopes. Every interaction with the controller or any other external party occurs through envelopes. Common fields, sequencing, freshness, and verification rules are specified here.

---

## Common Envelope Rules

- **CNS-3:1** Every envelope MUST contain a unique nonce of at least 128 bits.
- **CNS-3:2** Every envelope MUST contain a timestamp.
- **CNS-3:3** Every envelope MUST contain a monotonic sequence number scoped to the sender identity.
- **CNS-3:4** Every envelope MUST contain an explicit type identifier and the sender’s identity.
- **CNS-3:5** Every envelope MUST be signed over its canonical serialization by the sender’s appropriate key.
- **CNS-3:6** The console MUST reject any envelope whose signature fails verification against a pinned public key.
- **CNS-3:7** The console MUST reject any envelope whose timestamp falls outside the allowed skew window.
- **CNS-3:8** The console MUST reject any envelope whose nonce has been seen before.
- **CNS-3:9** Under the Standard and High profiles the console MUST reject any envelope whose sequence number is not strictly greater than the last accepted sequence number from that sender. The Basic profile MAY use weaker sequencing.
- **CNS-3:10** The console MUST produce envelopes that satisfy the same rules so that external parties can apply identical verification.

## Envelope Catalogue

- **CNS-3:11** The following envelope types are defined by this specification. Additional types may be added by companion specifications provided they obey the common rules above.

| Type | Direction | Purpose |
|---|---|---|
| `SessionStart` | Console → Controller | Initiate a new session |
| `ExecutionProfile` | Console → Controller | Supply work orders, runtime selections, context |
| `SurfaceProposal` | Controller → Console | Proposed surface for validation |
| `SurfaceAcceptance` / `SurfaceRejection` | Console → Controller | Result of validation gates |
| `Handoff` | Controller → Console | Session start credential |
| `HandoffDelivery` / `HandoffReceipt` | Console ↔ external | Delivery and acknowledgement of handoff |
| `RuntimeInclusionDecision` | Console → Controller | Approve or deny inclusion of an already-registered runtime in a running session (see CNS-O-10) |
| `WorkOrder` / `WorkOrderUpdate` | Console → Controller | Create, extend, renew, cancel |
| `PreAuthorization` | Console → Controller | Create, change, or revoke a pre-authorization |
| `Revocation` | Console → Controller | Immediate revocation of session, runtime, or pre-auth |
| `StatusQuery` / `StatusResponse` | Console ↔ Controller | Request and receive state or audit information |
| `Notification` | Controller → Console | Pending decision or event |
| `ValidatorEvidence` | Console → Controller | Optional session-validator observation |
| `Genesis` | Console → Controller | Console-signed anchor that locks console, Host AI, controller and gateways into one session; the genesis value MUST be 0 at handoff (see CNS-O-09) |
| `TurnReceipt` | Console → Controller | Console-signed receipt for a turn (see CNS-O-09) |

- **CNS-3:12** All of the above are ordinary envelopes subject to the common rules. No transport other than the channels defined in CNS-3:19 and the delivery exception in CNS-3:21 is permitted for control-plane actions.

## Sequencing and Sessions

- **CNS-3:13** Duplicate of CNS-3:3. The requirement is defined only there.
- **CNS-3:14** Session-related envelopes carry a session handle once one has been allocated.
- **CNS-3:15** The console MUST maintain sufficient state to enforce monotonicity and replay protection for the lifetime required by the claimed profile.

## Contract Version and TTL

- **CNS-3:16** Every envelope MUST contain a `contract_version` equal to the suite major.minor to which the sender conforms (`amk-ssot.md`, SSOT-1:3).
- **CNS-3:17** Every envelope MUST contain a `ttl` after which the envelope MUST be rejected.
- **CNS-3:18** The console MUST reject any envelope whose `contract_version` it does not support or whose `ttl` has expired. It MUST NOT silently downgrade.

## Channels

- **CNS-3:19** The console and the controller communicate over two distinct channels. The **administrative channel** is direct, its trust is rooted in the Release Key, and it is required to initiate a session. The **session channel** carries all session-based communication through the session router; envelopes are router payloads.
- **CNS-3:20** `SessionStart` is sent on the administrative channel. Once a session handle has been allocated, every session-related envelope MUST use the session channel. The assignment of the remaining envelope types to channels is not yet defined (see CNS-O-08).
- **CNS-3:21** Delivery of the handoff to a Host AI by manual, loopback or gateway means is the only permitted transport that is not an envelope exchange.
- **CNS-3:22** The encapsulation of envelopes as router payloads is defined by the session-router specification (see CNS-O-08).
