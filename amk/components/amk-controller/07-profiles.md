# Operational Profiles

**File number:** 8  
**Overview.**  
This module defines the three operational profiles. An implementation MUST declare exactly one profile. Higher profiles subsume all requirements of lower profiles. Higher profiles may exclude languages or platforms that cannot meet the required isolation, key protection, durability, or audit strength.

---

## Common Rules

- **CTR-8:1** Every conformant implementation MUST declare exactly one profile: `basic`, `standard`, or `high`.
- **CTR-8:2** The declared profile MUST be discoverable through a status or capability envelope.
- **CTR-8:3** An implementation claiming `standard` MUST satisfy every Basic requirement in addition to the Standard obligations.
- **CTR-8:4** An implementation claiming `high` MUST satisfy every Basic and Standard requirement in addition to the High obligations.
- **CTR-8:5** The invariants defined in file 1 apply at every profile.

## Basic Profile

- **CTR-8:6** Software-protected keys are permitted.
- **CTR-8:7** Soft isolation is acceptable.
- **CTR-8:8** Sequencing and replay protection MAY use simplified mechanisms.
- **CTR-8:9** Minimal durable state and audit retention are acceptable.
- **CTR-8:10** Suitable for any programming language and platform that can perform the required public-key operations and maintain basic monotonic state.

## Standard Profile

- **CTR-8:11** Private keys MUST be non-exportable and protected by an OS keystore or equivalent.
- **CTR-8:12** Process or container isolation is required.
- **CTR-8:13** Full envelope sequencing, freshness, and replay protection are mandatory.
- **CTR-8:14** Durable storage with point-in-time recovery (or equivalent) and a complete signed audit chain are required.
- **CTR-8:15** Languages and platforms must support mature cryptographic libraries and process/container isolation. Implementations that cannot meet these requirements are non-conformant for the Standard profile.

## High Profile

- **CTR-8:16** Private keys MUST be protected by an HSM, secure element, or TEE and MUST NOT exist in ordinary process memory in clear form.
- **CTR-8:17** Strong isolation (TEE or equivalent hardware security domain) is required.
- **CTR-8:18** Measured boot / remote attestation SHOULD be supported.
- **CTR-8:19** The audit trail MUST be protected against tampering (hardware-backed or equivalently strong integrity protection).
- **CTR-8:20** Side-channel resistance and high-assurance coding practices are expected for security-critical paths.
- **CTR-8:21** Languages and platforms that cannot provide HSM/TEE support, measured boot, or the required isolation and audit strength are excluded from the High profile.

## Profile Summary Table

| Requirement | Basic | Standard | High |
|---|---|---|---|
| Non-exportable keys | SHOULD | MUST | MUST |
| OS keystore / equivalent | MAY | MUST | MUST |
| HSM / TEE / secure element | — | MAY | MUST |
| Keys never in clear process memory | — | SHOULD | MUST |
| Process / container isolation | MAY | MUST | MUST |
| TEE-level isolation | — | — | MUST |
| Full sequencing + replay protection | MAY (simplified) | MUST | MUST |
| Durable state + signed audit | Minimal | Full | Hardware-protected |
| Remote attestation support | — | — | SHOULD |
| Language / platform exclusion | None (basic crypto) | Must support isolation + mature crypto | Must support HSM/TEE + measured environment |

## Peer Profile Rule

- **CTR-8:22** The controller MUST NOT accept a peer that declares a lower profile than its own unless the administrator has explicitly allowed it, and that allowance MUST be audited.
