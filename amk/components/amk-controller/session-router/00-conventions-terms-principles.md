# Conventions, Terms, Principles, Identity Model & Invariants

**Overview.**  
This module establishes the foundational language, normative conventions, core design principles, and absolute invariants of the Session Router. It defines the separation of long-term identity from session identity and from logical address, states the principle of role-addressed capability-gated E2E-encrypted relay, and enumerates the invariants that every conformant implementation must uphold. The specification is language-agnostic and self-contained. The three complexity profiles affect only implementation and infrastructure strength, not these core definitions.

---

## 0. Conventions

- **MUST / MUST NOT / SHOULD / MAY** are used as in RFC 2119.
- Each normative statement has one ID (`RTR-n` or `PROF-n`). IDs are never reused or renumbered.
- "Entity" means any participant that registers with a router instance under a role declared for that session.
- "Router" means a router instance unless stated otherwise.
- Parameters written in capitals (`T_MAX`, `N_MAX`, `G`, `X`, `R_MAX`, `CELL_SIZE`, `TAG_MAX`, `HS_MAX`, `REG_WINDOW`) are policy parameters. Their concrete values are not fixed by this specification.
- The specification is language-agnostic. Profile-specific obligations may relax or strengthen selected non-invariant requirements according to the declared profile.
- The component is self-contained: it defines only the messages, fields, cryptographic checks, and state transitions that occur at its own boundary. It does not prescribe the internal behaviour of any external entity or Attestation Authority beyond the interface required for interaction.

---

## 2. Terms

| Term | Meaning |
|---|---|
| Router instance | A router created for exactly one session. Holds the LA table, enforces policy, is blind to content and long-term identity. |
| Router factory | The component that creates router instances. |
| Attestation Authority | External service that issues role attestations and holds long-term identity bindings. The router verifies attestations against it but does not define its internal operation. |
| Role | Arbitrary string identifying a function an entity performs in a session. Roles are declared in the Init Envelope; there are no hard-coded roles. |
| Session handle | Identifier for the session. Appears in attestations, envelopes, and the Discovery Record. |
| Session identity | Ephemeral keypair held by an entity for one epoch. |
| Long-term identity | Persistent identity of an entity. Never crosses the router. |
| LA | Logical address. Opaque handle, known only to the router, scoped to an epoch. |
| Epoch | Period within a session over which LAs, session keys, channels, and policy are valid. |
| Attestation | Signed statement from the Attestation Authority binding a session public key to a role, session, and epoch for a validity window. |
| Capability | A token that encodes a right, not an identity. |
| Channel | An established E2E-encrypted path between two roles for one epoch. |
| Traffic metadata | The router’s residual knowledge (see Knowledge Boundary module). |
| Init Envelope | Signed request, sealed to the factory’s key, that creates a session router instance and declares roles, policy, and parameters. |
| Binding Data | Per-role data an entity supplies so it can be bound to the instance. |
| Discovery Record | Factory-signed record that tells bound entities how to reach and authenticate the instance. |
| Session Initiator | The external party that creates and signs the Init Envelope. |

---

## 3. Principle

Role-addressed, capability-gated, E2E-encrypted relay with brokered ECDH and role attestation. A minimal mixnet scoped to one session.

- **RTR-7** Identity MUST be separated from address.
- **RTR-8** Entities MUST address each other by role or capability, never by key or long-term name.
- **RTR-9** The router MUST be the sole holder of the role-to-endpoint mapping.
- **RTR-10** E2E encryption MUST be established through a brokered key agreement. The router relays public values and MUST NOT derive or hold the secret.
- **RTR-11** Role attestations MUST replace identity disclosure.

---

## 4. Identity Model

Two layers, never conflated.

| Layer | Known by | Rotates |
|---|---|---|
| Long-term identity | Never crosses the router. Held by the Attestation Authority only. | Rarely |
| Session identity (ephemeral keypair per entity) | Router and Attestation Authority. Counterparty learns the public key only. | Per epoch |
| Role | Router, Attestation Authority, and other entities, as a function. | Per session (declared in Init Envelope) |
| Logical address (LA) | Router only. | Per epoch |

- **RTR-12** Long-term identity MUST NOT cross the router.
- **RTR-13** An entity MUST know only: its own long-term identity, its own session key, its own role, and the roles it may address according to policy.
- **RTR-14** An entity MUST NOT learn any counterparty’s long-term identity or LA.
- **RTR-15** A session keypair MUST be generated fresh for each epoch.

---

## 15. Invariants

| ID | Invariant |
|---|---|
| INV-1 | No entity ever learns another’s long-term identity through the router. |
| INV-2 | No entity ever learns another’s LA. |
| INV-3 | The router never holds a derived shared secret. |
| INV-4 | The router cannot impersonate any entity. |
| INV-5 | Policy is role-based, epoch-scoped, and auditable. |
| INV-6 | Denial is opaque and indistinguishable from absence. |
| INV-7 | Channels are per-epoch and re-established on rotation. |
| INV-8 | LAs and session keys rotate per epoch. |
| INV-9 | The router’s control-plane authority (admission and role binding) derives from Attestation Authority attestations, never from the router itself. |
| INV-10 | The router’s residual knowledge is the traffic metadata defined in the Knowledge Boundary module, and nothing else. |
| INV-11 | One router instance serves exactly one session and shares no value with any other instance. |
| INV-12 | An entity registers only with an endpoint obtained from a verified Discovery Record. |

- **RTR-60** An implementation that violates any invariant is non-conformant, regardless of other requirements met.
