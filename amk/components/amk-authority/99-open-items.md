# 99-open-items.md

**File:** `99-open-items.md`
**Scope:** Open questions and their resolutions. This file is the single source for `O-ATA-nn` items and their blocking status.
**Reference prefix:** `ATA-99`

---

## ATA-99:01 Open Items

- **O-ATA-01** Multiple simultaneous signing keys for rotation. RESOLVED: a signed key set with `kid` and key statuses (`ATA-01:07`).
- **O-ATA-02** Format of the session's declared role list and how it reaches the Authority. RESOLVED: the controller supplies it in the session record (`ATA-02:02`).
- **O-ATA-03** Whether identity binding is per-role or per-session. RESOLVED: per-session (`ATA-05:04`).
- **O-ATA-04** Revocation list distribution mechanism. RESOLVED: pull-only by HTTPS GET (`ATA-04:01`).
- **O-ATA-05** How the Authority is enrolled with the controller at first use. RESOLVED: out-of-band pinning at deployment of the root key (`ATA-01:07`) and the controller identity (`ATA-02:02`); there is no online enrollment handshake.
- **O-ATA-06** Delegation of issuance to sub-authorities. CLOSED: not supported in this version; the Authority is the sole issuer (`ATA-00:01`).
- **O-ATA-07** PoP challenge format. RESOLVED: a deterministic signed value, with no challenge round-trip (`ATA-02:03`).
- **O-ATA-08** Metadata at a well-known endpoint. RESOLVED (`ATA-01:07`).
- **O-ATA-09** Audit format and retention per profile. RESOLVED (`ATA-06:10`, `DV-ATA-10`).
- **O-ATA-10** Batch issuance for multiple roles. CLOSED: not supported in this version; one request yields one attestation (`ATA-02:06`).
- **O-ATA-11** OPEN. The controller-to-Authority interface that carries the session record and revocation requests: channel, authentication of the controller, delivery and error semantics. Cross-spec with `amk-controller`; to be indexed in `specs/core/OPEN-ITEMS.md`.

## ATA-99:02 Blocking Items

- `O-ATA-11` is blocking for a 1.2.0 release.
- All other items are resolved or closed.

## ATA-99:03 Summary

- Ten of eleven open items are resolved or closed. The remaining item is the controller-to-Authority interface for the session record and revocation requests.

---

## Dependent files

Not yet updated: `amk-test-matrix`, `ssot-index`. Discontinued: `amk-contracts`, `os10-lifecycle`, `amk-defaults-manifest`.

## Cross-spec items

Cross-spec items that affect this specification are indexed in `specs/core/OPEN-ITEMS.md` (`CORE-O-nn`). Existing `O-ATA-nn` IDs are retained; IDs are never reassigned.
