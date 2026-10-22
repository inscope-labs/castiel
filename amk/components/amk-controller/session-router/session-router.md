# Session Router — Blind Ingress/Egress Router Specification

| Field | Value |
|---|---|
| Spec ID | `session-router` |
| Version | 0.5.0-draft |
| Status | Draft — general-purpose, self-contained, language-agnostic design with three complexity profiles. |
| Requirement IDs | RTR-1 to RTR-116 (stable where retained). Profile-specific obligations identified as PROF-*. |
| Scope | Standalone component. Defines only the interactions between the router/factory and external entities. |

---

## Holistic System Overview

The Session Router is a language-agnostic, role-addressed, capability-gated, end-to-end encrypted relay that functions as a minimal mixnet scoped to a single session. It is designed as a self-contained component for general public use. It does not require knowledge of the internal operation of any external component; it only defines the messages, cryptographic obligations, and verification rules that external entities must satisfy when interacting with it.

Every communication between registered entities within a session must pass exclusively through a per-session router instance. Direct, loopback, out-of-band, or third-party-forwarded paths between entities are outside the component’s responsibility and are simply not mediated by it.

**Identity is strictly separated from address.** Entities address one another solely by role or capability. The router alone holds the mapping from these addresses to opaque, epoch-scoped logical addresses (LAs). Session identity is an ephemeral keypair that rotates every epoch. Long-term identity never crosses the router; it is held only by an external Attestation Authority. Role attestations issued by that authority replace identity disclosure: each party learns only the counterparty’s role and the public key of its current session identity.

**Channels** are established by a three-message brokered ECDH handshake in which every message is signed by an attested session key and attestation is mutual. The router relays public values but never derives or holds the shared secret. Application payloads travel in fixed-size cells (or variable size under the Basic profile) under AEAD encryption whose keys the router cannot see. Replay protection is enforced by receivers via monotonic sequence numbers carried inside the AEAD plaintext.

**Policy** is defined exclusively over roles, message classes, and direction. It is epoch-scoped and auditable. The complete policy (including the set of permitted roles) is supplied in the Init Envelope that creates the instance; there are no hard-coded roles. Denials are opaque. The router’s residual knowledge is limited to traffic metadata (roles, cell sizes, timings, endpoints, membership, and policy outcomes). Padding, jitter, and per-session instance isolation bound that knowledge.

A **Router Factory** creates one isolated instance per session from a signed Init Envelope. The Init Envelope declares the set of roles for the session, the policy, and other parameters. Entities discover the instance solely through a factory-signed Discovery Record and register with single-use tickets. The factory and each instance are self-contained; they treat all external entities as black boxes that must present valid attestations and cryptographic material.

The system fails closed: when a router instance is unavailable, inter-entity traffic mediated by it ceases. Compromise of the router reveals only traffic metadata. Compromise of the Attestation Authority is mitigated by key protection (software or hardware according to profile), mutual authentication, and pinned verification keys. All invariants remain absolute.

The specification is language-agnostic. Implementations may be written in any language that supplies the necessary networking and cryptographic primitives. Three complexity profiles—Basic, Standard, and High—define substantive differences in code structure and infrastructure requirements while preserving the same core protocol and security invariants.

This document is the single source of truth. Normative requirements live in the module files listed below.

---

## Complexity Profiles

Three formal profiles provide progressive levels of implementation and infrastructure complexity. Higher profiles subsume all requirements of lower profiles. An implementation MUST declare the profile it claims.

### Basic Profile
- **Audience**: Hobbyists, students, educational prototypes, early experimentation.
- **Code complexity**: Single-process or single-threaded designs are acceptable. Cryptographic operations may use any convenient library. Fixed-size cells and timing jitter are optional. Soft isolation is permitted. Simplified error handling and state management.
- **Infrastructure complexity**: Ordinary developer machines, containers, or low-cost virtual machines. No HSM, TEE, or hardware root-of-trust required. Shared host for factory and instances is acceptable. Persistence of instance state may be relaxed for experimentation.
- **Language support**: Fully language-agnostic. May be implemented in PHP, Python, JavaScript/TypeScript, C++, Bash (with external cryptographic utilities), Go, Rust, Java, C#, Ruby, Lua, or any other language providing networking and basic cryptography.

### Standard Profile
- **Audience**: Production services, professional software teams.
- **Code complexity**: Mandatory multi-process or multi-container architecture; each router instance runs in its own isolated process or container with no shared memory. Full implementation of every normative requirement. Formal state machines and comprehensive non-leaking error handling.
- **Infrastructure complexity**: Dedicated process/container isolation for every instance. Software key storage (OS keyring, encrypted files, or cloud KMS) is acceptable. Network isolation between instances required. Automatic secure erasure of instance state.
- **Language support**: Language-agnostic in principle; practical implementations require languages with mature process/container support and audited cryptographic libraries.

### High Profile
- **Audience**: Enterprise, regulated, and high-assurance environments.
- **Code complexity**: All Standard requirements plus high-assurance practices (formal review or verification of security-critical paths, explicit side-channel resistance, memory scrubbing). Hardware-backed key lifecycle. Measured/attested boot integration.
- **Infrastructure complexity**: Mandatory HSMs, TPMs, secure elements, or equivalent for all long-term and instance private keys. Trusted Execution Environments (TEEs) or equivalent for each router instance and the factory. Measured boot / remote attestation. Dedicated isolated network segments. Hardware-enforced secure erasure and anti-rollback protections.
- **Language support**: Language-agnostic in principle; constrained by availability of HSM/TEE interfaces and high-assurance toolchains.

Profile selection is declared in the Init Envelope and Discovery Record.

---

## Module Index

| File | Scope | Primary Content |
|---|---|---|
| [00-conventions-terms-principles.md](00-conventions-terms-principles.md) | Conventions, terminology, core principles, identity model, invariants | Foundations |
| [01-scope-components.md](01-scope-components.md) | Scope, self-containment, component responsibilities, Attestation Authority interface | Boundaries |
| [02-addressing-registration-epochs.md](02-addressing-registration-epochs.md) | Address space, registration, epoch lifecycle | Addressing |
| [03-channel-envelope.md](03-channel-envelope.md) | Brokered channel establishment and envelope format | Channels |
| [04-routing-policy-admission.md](04-routing-policy-admission.md) | Routing policy, dynamic roles, entity admission | Policy |
| [05-adapters.md](05-adapters.md) | Optional adapters for entities that cannot hold session keypairs themselves | Adapters |
| [06-knowledge-failure.md](06-knowledge-failure.md) | Router knowledge boundary and failure/compromise behaviour | Security boundary |
| [07-instances-discovery.md](07-instances-discovery.md) | Per-session instances, factory, Init Envelope, discovery | Lifecycle |
| [08-conformance.md](08-conformance.md) | Conformance criteria and profile declarations | Conformance |
| [99-appendices.md](99-appendices.md) | Change log, open questions, summary | Non-normative |

---

## Parameter Reference

Policy parameters written in capitals remain open for concrete values:

`T_MAX`, `N_MAX`, `G`, `X`, `R_MAX`, `CELL_SIZE`, `TAG_MAX`, `HS_MAX`, `REG_WINDOW`.

Profile-specific recommended ranges may be supplied later.

---

## Normative Language

MUST / MUST NOT / SHOULD / MAY are used as defined in RFC 2119. Each normative statement carries a stable identifier of the form `RTR-n` or `PROF-n`. Identifiers are never reused or renumbered.
