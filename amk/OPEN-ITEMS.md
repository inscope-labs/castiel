# AMK Core — Open Items Index

This index links the open items of the core AMK specifications. The per-spec `99-open-items.md` files remain the normative lists; this file is the working view. IDs are never reassigned.

- [amk-console/99-open-items.md](amk-console/99-open-items.md) — `CNS-O-nn`
- [amk-controller/99-open-items.md](amk-controller/99-open-items.md) — `CTR-O-nn`
- [amk-authority/99-open-items.md](amk-authority/99-open-items.md) — `O-ATA-nn` (existing IDs retained)

Status values: `open`, `partially resolved`, `pending`. Owner: `unassigned` until assigned.

## Cross-spec items (`CORE-O-nn`)

| ID | Item | Affects | Status | Owner |
|---|---|---|---|---|
| CORE-O-01 | Naming of "epoch": release anti-rollback epoch (CTR-2:1), the epoch in CTR-2:12, and the Authority's in-session counter. Needs clarification before renaming. | controller, authority | open | unassigned |
| CORE-O-02 | Link the session-router specification (`specs/modules/session-router`) and reconcile the transport rules (CNS-3:19 to 3:22, CTR-3:12 to 3:14) with it. | console, controller, authority | pending | unassigned |
| CORE-O-03 | Add the `amk-prompt` and `amk-runtime` specifications to `specs/core` and complete their rows in `amk-ssot.md`. | all | pending | unassigned |
| CORE-O-04 | Distribute the content of the discontinued `amk-contracts`, `os10-lifecycle` and `amk-defaults-manifest` into the individual spec files (defaults, version rules, lifecycle). | all | open | unassigned |
| CORE-O-05 | Convert `amk-authority` to per-bullet ordinal IDs and remove main-file duplication of `00-foundations` (X-06, X-07). Pending the authority review resolution. | authority | pending | unassigned |
| CORE-O-06 | Resolve the remaining review decisions in the console, controller and authority review files (01, 02, 03). | console, controller, authority | pending | unassigned |
| CORE-O-07 | Specify the requirement that every session-router entity registers with `amk-authority` before being admitted as an approved router entity. | authority, session-router | open | unassigned |

## amk-console

| ID | Item | Status | Owner |
|---|---|---|---|
| CNS-O-01 | Concrete envelope schemas | open | unassigned |
| CNS-O-02 | Validation-gate set and versioning | open | unassigned |
| CNS-O-03 | Recovery protocol for Standard and High | open | unassigned |
| CNS-O-04 | Skew windows, nonce lifetime, sequence storage | open | unassigned |
| CNS-O-05 | Pre-authorization scope expression | open | unassigned |
| CNS-O-06 | Auto Assist flags vs anomaly levels | open | unassigned |
| CNS-O-07 | Bootstrap and pinning of verification keys | partially resolved (CNS-2:12) | unassigned |
| CNS-O-08 | Channel assignment per envelope; router payload encapsulation | open | unassigned |
| CNS-O-09 | `Genesis` and `TurnReceipt` schemas | open | unassigned |
| CNS-O-10 | Runtime inclusion decision envelope; subtree intake name | open | unassigned |
| CNS-O-11 | `SessionPolicy`, `CheckIn`, `WorkOrderProposal` envelopes | open | unassigned |
| CNS-O-12 | Behavioural rules for orphan envelope types | open | unassigned |
| CNS-O-13 | Key distribution and console enrollment | open | unassigned |

## amk-controller

| ID | Item | Status | Owner |
|---|---|---|---|
| CTR-O-01 | Concrete envelope schemas | open | unassigned |
| CTR-O-02 | Durable state that must survive restart | open | unassigned |
| CTR-O-03 | Console enrollment over the administrative channel | open | unassigned |
| CTR-O-04 | Provenance binding of runtime map and subtree | open | unassigned |
| CTR-O-05 | Capability tests and kernel-level matrix | open | unassigned |
| CTR-O-06 | Channels beyond HTSM and level gating | open | unassigned |
| CTR-O-07 | Recovery protocol for Standard and High | open | unassigned |
| CTR-O-08 | Skew windows, nonce lifetime, sequence storage | open | unassigned |
| CTR-O-09 | Work-order cost unit and concurrency limits | open | unassigned |
| CTR-O-10 | Gateway and export definitions | open | unassigned |
| CTR-O-11 | Channel assignment per envelope; router payload encapsulation | open | unassigned |
| CTR-O-12 | `Genesis` and `TurnReceipt` schemas | open | unassigned |
| CTR-O-13 | Subtree intake envelope name; inclusion decision | open | unassigned |
| CTR-O-14 | `SessionPolicy`, `CheckIn`, `WorkOrderProposal` envelopes | open | unassigned |
| CTR-O-15 | Behavioural rules for orphan envelope types | open | unassigned |
| CTR-O-16 | Key distribution and key rotation rules | open | unassigned |

## amk-authority

| ID | Item | Status | Owner |
|---|---|---|---|
| O-ATA-01 | Multiple simultaneous signing keys for rotation | open | unassigned |
| O-ATA-02 | Format of the declared role list and how it reaches the Authority | open | unassigned |
| O-ATA-03 | Identity binding per-role or per-session | open | unassigned |
| O-ATA-04 | Revocation list distribution mechanism | open | unassigned |
| O-ATA-05 | Enrollment of the Authority with the controller or router | open | unassigned |
| O-ATA-06 | Delegation of issuance to sub-authorities | open | unassigned |
| O-ATA-07 | PoP standardization | open | unassigned |
| O-ATA-08 | Metadata publication | open | unassigned |
| O-ATA-09 | Audit format and retention | open | unassigned |
| O-ATA-10 | Batch issuance | open | unassigned |
