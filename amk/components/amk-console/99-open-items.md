# Open Items & Migration Notes

**File number:** 8  
**Overview.**  
Non-normative list of remaining open questions and notes on the migration from earlier drafts. This file contains no normative requirements.

---

## Open Questions

- **CNS-O-01** Concrete envelope schemas (field-level definitions, serialization format, mandatory vs optional fields) for each type listed in file 3.
- **CNS-O-02** Exact validation-gate set and versioning rules (companion specification).
- **CNS-O-03** Recovery protocol for Standard and High profiles after key loss or compromise.
- **CNS-O-04** Precise skew windows, nonce lifetime, and sequence-number storage requirements per profile.
- **CNS-O-05** How pre-authorization scope is expressed (single multi-scope envelope vs multiple single-scope envelopes).
- **CNS-O-06** Interaction of Auto Assist policy flags with anomaly levels reported by the controller.
- **CNS-O-07** Bootstrap / pinning mechanism for the controller’s public key and any other external verification keys. Partially resolved: the console build pins the Release Key fingerprint(s), controller URLs and Authority URLs (CNS-2:12). Remaining: see CNS-O-13.

- **CNS-O-08** Assignment of each envelope type to the administrative or session channel, and the encapsulation of envelopes as session-router payloads (CNS-3:19 to CNS-3:22).
- **CNS-O-09** `Genesis` and `TurnReceipt` envelopes: direction, fields and schema.
- **CNS-O-10** Whether `RuntimeInclusionDecision` is itself an envelope or the outcome of the console workflow is carried by another envelope, and the name of the runtime subtree intake envelope (shared with CTR-O-13).
- **CNS-O-11** `SessionPolicy` (level cap, Auto Assist, anomaly ceiling), `CheckIn` and `WorkOrderProposal` envelopes.
- **CNS-O-12** Behavioural rules for envelope types that currently have none: `StatusQuery` / `StatusResponse`, `Notification`, `ValidatorEvidence`, `HandoffReceipt`.
- **CNS-O-13** How the controller signing key and the Authority public key reach the console, and how a console enrolls with a controller over the administrative channel.

## Migration Notes

- All UI/UX, presentation, operator-load timing, deep-linking, first-run wizards, notification rendering, and platform-specific material has been removed.
- The console is defined solely by its envelope contracts and verification obligations.
- Three operational profiles (Basic / Standard / High) are defined in file 7.
- The specification is language-agnostic.
- Reference IDs now follow the single scheme `CNS-<file>:<rule>`.
- `RuntimeRegistration`, `RuntimeInclusionRequest` and `ClarificationAnswer` envelopes were removed. Runtime registration and inclusion handling are console workflows; `ClarificationAnswer` is discontinued. CNS-4:11 and CNS-5:1 are marked `RETIRED`.
- `Genesis` and `TurnReceipt` envelopes were added to the catalogue. Common envelope fields now include `contract_version` and `ttl`.
- Cross-spec open items are indexed in `specs/core/OPEN-ITEMS.md`.
