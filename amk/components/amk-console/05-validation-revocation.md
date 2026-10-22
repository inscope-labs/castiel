# Validation, State Rules, Revocation & Recovery

**File number:** 6  
**Overview.**  
This module defines the validation obligations the console must discharge before accepting a surface, the rules for relying on external state, the revocation interface, and the recovery posture. All behaviour is expressed as envelope verification and emission rules.

---

## Validation Gates

- **CNS-6:1** Before emitting a `SurfaceAcceptance` envelope the console MUST apply every validation gate defined by the referenced gate set.
- **CNS-6:2** A failed gate MUST produce a `SurfaceRejection` envelope.
- **CNS-6:3** A failed gate MUST NOT be overridden by the operator or by a pre-authorization (see CNS-1:12).
- **CNS-6:4** The console MUST record the gate-set version in the acceptance or rejection envelope.

## State Rules

- **CNS-6:5** The console treats the controller as the sole authority for session state.
- **CNS-6:6** Any locally cached state MUST be treated as unverified until confirmed by a freshly verified envelope from the controller.
- **CNS-6:7** Under the Standard and High profiles the console MUST enforce strict freshness and sequencing on all state-bearing envelopes.

## Revocation

- **CNS-6:8** The console MAY emit a `Revocation` envelope targeting an entire session, a runtime within a session, or a previously issued pre-authorization.
- **CNS-6:9** When the controller is unreachable the console relies on the natural expiry of credentials and pre-authorizations as the backstop.

## Recovery

- **CNS-6:10** Recovery of console identity and key material after loss or compromise is profile-dependent and remains an open item.
- **CNS-6:11** The Basic profile MAY permit simple re-keying; Standard and High profiles require a defined recovery protocol that preserves the non-exportable and hardware-backed properties of the keys.
