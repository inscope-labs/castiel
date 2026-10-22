# Capability Tokens, Audit, Revocation & Recovery

**File number:** 7  
**Overview.**  
This module defines capability-token issuance, the append-only audit chain, revocation behaviour, multi-runtime isolation, and the recovery posture.

---

## Capability Tokens

- **CTR-7:1** The controller issues short-lived, controller-signed capability tokens bound to session, runtime, scope, nonce, and lineage.
- **CTR-7:2** Tokens for destructive or irreversible operations MUST be single-use.
- **CTR-7:3** Duplicate of CTR-1:19. The requirement is defined only there.

## Audit

- **CTR-7:4** The audit log is append-only, hash-chained, and signed by the Controller Signing Key.
- **CTR-7:5** Under Standard and High profiles, Merkle checkpoints (or equivalent integrity anchors) MUST be produced and protected according to the claimed profile.
- **CTR-7:6** Audited events include genesis, handoff use, console turns and receipts, proposals and decisions, subtree revisions, surface proposals and approvals, envelope use and revocation, capability tests, anomaly changes, Auto Assist periods, forks, and every anomaly.

## Revocation

- **CTR-7:7** Revocation commits at the controller, is audited, and halts runtimes at the next operation boundary; authority also ends at token expiry.
- **CTR-7:8** The controller keeps a revocation registry for pre-authorization envelopes.
- **CTR-7:9** Duplicate of CTR-2:13. The requirement is defined only there.

## Multi-Runtime Isolation

- **CTR-7:10** Each runtime has an isolated execution context and independent authorization scope. No inherited state or authority.

## Recovery and Availability

- **CTR-7:11** The controller fails closed during outages or integrity drops.
- **CTR-7:12** Recovery of controller identity and key material after loss or compromise is profile-dependent and remains an open item. The Basic profile may permit simpler recovery; Standard and High profiles require protocols that preserve non-exportable and hardware-backed properties.
