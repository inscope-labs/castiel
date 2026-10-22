# Scope, Self-Containment & Components

**Overview.**  
This module defines the self-contained nature of the Session Router, the boundary of its responsibility, and the responsibilities of its principal components: the router instance, the router factory, and the interface to an external Attestation Authority. The component does not prescribe how any external entity or the Attestation Authority operates internally; it only defines the interaction contract.

---

## 1. Scope and Self-Containment

- **RTR-1** This specification defines a standalone component. It does not depend on any particular larger system.
- **RTR-2** Within a session, every communication between registered entities that the session is intended to mediate MUST pass through the router instance. The component does not police paths that never touch it.
- **RTR-3** RTR-2 applies to every entity that registers with the instance, whatever its role or origin.
- **RTR-4** The Session Router governs addressing, transport, and confidentiality of the envelopes it carries. Payload semantics are defined by the entities themselves.
- **RTR-5** Out of scope: human-to-interface interaction, communication internal to a single entity, and traffic between an entity and a non-entity external system.
- **RTR-6** Exchanges that necessarily precede the existence of a router instance (Init Envelope creation, Binding Data exchange, Discovery Record delivery, and re-discovery) are outside the mediated data plane. Once a router instance is active, session traffic among registered entities uses it.

---

## 5. Components

- **RTR-16** The router instance MUST hold the LA to (role, session public key, endpoint) mapping, enforce the policy supplied in the Init Envelope, and be blind to payload contents and long-term identities.
- **RTR-17** An external Attestation Authority issues role attestations and holds long-term identity bindings. The router and factory verify attestations against it. The internal operation of the Attestation Authority is outside this specification.
- **RTR-18** Each entity MUST hold a session keypair and a current role attestation (or participate via an adapter that does).
- **RTR-19** The router factory and every router instance SHOULD run on infrastructure that is independent of the entities that use them. The degree of independence is strengthened by higher complexity profiles.
- **RTR-20** Classification of the factory and instances within any larger system is outside the scope of this specification.

### Attestation Authority Interface Requirements

The Session Router requires only the following interface properties from an Attestation Authority:

- **RTR-91** The Attestation Authority’s signing key SHOULD be protected according to the claimed profile (software for Basic/Standard, HSM or equivalent for High).
- **RTR-93** Requests to the Attestation Authority SHOULD be mutually authenticated.
- **RTR-94** An attestation MUST carry `valid_from` and `valid_to`. `valid_to` MUST NOT exceed the end of the epoch plus the grace window `G`.
- **RTR-95** The Attestation Authority SHOULD publish a signed revocation list. Routers, the factory, and entities MUST check it when available and MUST reject attestations when their copy is older than `R_MAX`.
- **RTR-96** Epoch-0 issuance order is the responsibility of the entities and the Attestation Authority. The factory and router require only that a valid attestation is presented at registration.
- **RTR-98** Entities MUST be able to verify attestations against a pinned public key of the Attestation Authority.
- **RTR-99** The Attestation Authority SHOULD reject non-monotonic epoch requests for the same (session handle, role) pair.

The Session Router treats the Attestation Authority as a black box that produces verifiable attestations.
