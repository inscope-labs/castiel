# Open Items & Migration Notes

**File number:** 9  
**Overview.**  
Non-normative list of remaining open questions and notes on the migration from the previous draft. This file contains no normative requirements.

---

## Open Questions

- **CTR-O-01** Concrete envelope schemas (field-level definitions, serialization format) for each type listed in file 3.
- **CTR-O-02** Exact durable-state requirements that must survive a restart (profile-dependent).
- **CTR-O-03** Console enrollment / key-registration procedure with the controller, over the administrative channel.
- **CTR-O-04** Provenance binding between a provider-signed runtime map and the console-derived subtree.
- **CTR-O-05** Definition of the capability tests and the kernel-level matrix.
- **CTR-O-06** Channels beyond HTSM and how the kernel operating level gates them.
- **CTR-O-07** Recovery protocol for Standard and High profiles after key loss or compromise.
- **CTR-O-08** Precise skew windows, nonce lifetime, and sequence-number storage requirements per profile.
- **CTR-O-09** Work-order cost unit and concurrent work-order limits.
- **CTR-O-10** Gateway / export definitions.

- **CTR-O-11** Assignment of each envelope type to the administrative or session channel, the encapsulation of envelopes as session-router payloads, and the relationship between the session router and the HTSM Host AI channel (CTR-3:12 to CTR-3:14).
- **CTR-O-12** `Genesis` and `TurnReceipt` envelopes: direction, fields and schema.
- **CTR-O-13** The name of the runtime subtree intake envelope, and whether `RuntimeInclusionDecision` is itself an envelope or the outcome of the console workflow is carried by another envelope (shared with CNS-O-10).
- **CTR-O-14** `SessionPolicy` (level cap, Auto Assist, anomaly ceiling), `CheckIn` and `WorkOrderProposal` envelopes.
- **CTR-O-15** Behavioural rules for envelope types that currently have none: `StatusQuery` / `StatusResponse`, `Notification`, `ValidatorEvidence`, `CapabilityToken`.
- **CTR-O-16** How the controller signing key and the Authority public key are distributed to consoles, and rotation rules for the Release Key, Controller Signing Key and Token Signing Key (file 10).

## Migration Notes

- All references to Cloudflare (or any specific platform or vendor) have been removed.
- The specification is language- and platform-agnostic. Higher profiles may exclude languages or platforms that cannot meet the required isolation, key protection, or audit strength.
- All UI/UX and presentation material has been removed.
- Control-plane interaction with consoles is expressed solely through envelopes.
- Three operational profiles (Basic / Standard / High) are defined in file 8.
- Reference IDs follow the single scheme `CTR-<file>:<rule>`.
- `RuntimeRegistration` and `ClarificationAnswer` were removed from the catalogue. `Genesis` and `TurnReceipt` were added. Common envelope validation now includes `contract_version` and `ttl` (CTR-3:10, CTR-3:11).
- File 10 (`08-keys.md`) was added. File numbers are stable identifiers and need not follow file-name order.
- Cross-spec open items are indexed in `specs/core/OPEN-ITEMS.md`.
