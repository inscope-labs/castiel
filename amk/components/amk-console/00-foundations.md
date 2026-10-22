# Foundations — Terms, Role, Trust & Invariants

**File number:** 1  
**Overview.**  
This module defines the core terminology, the console’s role as the sole human representation of the operator, the trust boundary, and the absolute invariants. All subsequent modules presuppose these definitions. The console is treated as a self-contained component that interacts solely via envelopes.

---

## Terms

| Term | Meaning |
|---|---|
| Console | The component defined by this specification. |
| Controller | External black-box component that receives console envelopes and performs enforcement. |
| Operator | The human whose authenticated intent the console represents. |
| Envelope | A structured, signed, nonced, sequenced message that is the sole external communication unit. |
| Session | A unit of work mediated by the controller and started by a console envelope. |
| Handoff | An expiring credential returned by the controller that allows a session to begin. |
| Work order | A task statement carrying its own quota and constraints. |
| Pre-authorization envelope | A reusable, operator-signed advance approval for a named scope. |
| Validation gate | A deterministic check the console MUST apply to any controller-proposed surface before acceptance. |
| Role / Runtime | External entities registered or included via envelopes; treated as black boxes. |
| Attestation / Signature | Cryptographic proof of origin and integrity; verification rules are defined in this specification. |

---

## Role

- **CNS-1:1** The console is the sole seat of operator authority and the sole interface through which authenticated human intent enters the system.
- **CNS-1:2** The controller has no independent notion of an operator; the console’s cryptographic identity is how the operator is present.
- **CNS-1:3** The console submits signed envelopes; the controller (or other receiving party) enforces.

## Trust Boundary

- **CNS-1:4** The console is trusted for capturing and transmitting authenticated operator intent.
- **CNS-1:5** The console is untrusted for enforcement.
- **CNS-1:6** The console MUST verify every signature and response it receives from external parties.
- **CNS-1:7** External parties MUST be able to verify every signature the console emits.
- **CNS-1:8** The console MUST NOT rely on the internal behaviour of any counterpart beyond the envelope contract.

## Invariants

- **CNS-1:9** No implicit authority. Every action that affects system state is an explicit signed envelope.
- **CNS-1:10** The console is the sole human representation.
- **CNS-1:11** Enforcement authority lies outside the console.
- **CNS-1:12** A failed validation gate is never overridden.
- **CNS-1:13** Long-term private keys never leave the console’s protected key store.
- **CNS-1:14** The console never accepts an envelope whose signature or freshness checks fail.
- **CNS-1:15** All external communication occurs through envelopes defined in this specification, subject to the exception in CNS-3:21.

**CNS-1:16** An implementation that violates any invariant listed above is non-conformant.
