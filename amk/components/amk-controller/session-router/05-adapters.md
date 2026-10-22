# Adapters for Constrained Entities

**Overview.**  
Some entities cannot hold a session keypair or perform the cryptographic operations required by the protocol (for example, certain hardware devices, legacy systems, or sandboxed agents). This module defines the optional adapter pattern that allows such entities to participate. The adapter is a compliant entity that holds the session key material and performs handshake, encryption, and padding on behalf of the constrained principal. The Session Router itself treats the adapter as an ordinary registered entity; it has no special knowledge of the constrained principal.

---

## Adapter Requirements

- **RTR-53** An adapter MUST register under a role declared in the Init Envelope and MUST present a valid attestation for that role.
- **RTR-54** The adapter MUST hold the session keypair and perform all cryptographic operations (handshake, AEAD, proof-of-possession) itself.
- **RTR-63** Any relay or transport function that carries envelopes between the adapter and the constrained principal MUST carry them opaquely. It MUST NOT originate, alter, decrypt, or inject content outside the adapter.
- **RTR-64** Under Standard and High profiles the adapter MUST run in an isolate separate from any other component that should not have access to its key material. Under the Basic profile, shared address space is permitted.
- **RTR-65** The constrained principal MUST NOT learn the router endpoint, the Discovery Record, any registration ticket, any LA, or any `from_tag` unless the adapter explicitly and intentionally reveals them.
- **RTR-66** Under Standard and High profiles the adapter MUST apply fixed-size cells and bounded timing jitter before envelopes leave its control. The Basic profile may omit these protections.

The Session Router never interacts directly with the constrained principal; it only sees the adapter as a normal entity.
