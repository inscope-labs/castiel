# Operational Profiles

**File number:** 7  
**Overview.**  
This module defines the three operational profiles—Basic, Standard, and High—that govern privacy, security, and implementation complexity. An implementation MUST declare exactly one profile. Higher profiles subsume all requirements of lower profiles.

---

## Common Rules

- **CNS-7:1** Every conformant implementation MUST declare exactly one profile: `basic`, `standard`, or `high`.
- **CNS-7:2** The declared profile MUST be discoverable through a status or capability envelope.
- **CNS-7:3** An implementation claiming `standard` MUST satisfy every Basic requirement in addition to the Standard obligations.
- **CNS-7:4** An implementation claiming `high` MUST satisfy every Basic and Standard requirement in addition to the High obligations.
- **CNS-7:5** The invariants defined in file 1 apply at every profile.

---

## Basic Profile

**Target:** Hobbyists, educational use, rapid prototypes, early experimentation.

- **CNS-7:6** Software-protected keys are permitted.
- **CNS-7:7** Soft isolation is acceptable.
- **CNS-7:8** Sequencing and replay protection MAY use simplified mechanisms.
- **CNS-7:9** Fresh confirmation MAY be relaxed for some high-impact actions.
- **CNS-7:10** Minimal audit retention is acceptable.
- **CNS-7:11** The Basic profile is suitable for any programming language that can perform the required public-key operations and maintain basic monotonic state.

## Standard Profile

**Target:** Production services and professional deployments.

- **CNS-7:12** Private keys MUST be non-exportable and protected by an OS keystore or equivalent.
- **CNS-7:13** Process or container isolation between the console and any less-trusted components is required.
- **CNS-7:14** Full envelope sequencing, freshness, and replay protection are mandatory.
- **CNS-7:15** Fresh confirmation is required for session start, pre-authorization creation/change, key changes, and active-session revocation.
- **CNS-7:16** A complete audit trail of emitted and accepted envelopes MUST be maintained for the retention period defined by policy.

## High Profile

**Target:** Enterprise, regulated, and high-assurance environments.

- **CNS-7:17** Private keys MUST be protected by an HSM, secure element, or TEE and MUST NOT exist in ordinary process memory in clear form.
- **CNS-7:18** Strong isolation (TEE or equivalent hardware security domain) is required.
- **CNS-7:19** Measured boot / remote attestation of the console’s key environment SHOULD be supported.
- **CNS-7:20** Strict fresh confirmation for all high-impact actions is required; additional environmental checks may be required.
- **CNS-7:21** The audit trail MUST be protected against tampering (hardware-backed or equivalently strong integrity protection).
- **CNS-7:22** Side-channel resistance and high-assurance coding practices are expected for the security-critical paths.

---

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
| Fresh confirmation for high-impact actions | MAY relax | MUST | MUST |
| Tamper-protected audit trail | Minimal | Full | Hardware-protected |
| Remote attestation support | — | — | SHOULD |

## Peer Profile Rule

- **CNS-7:23** The console MUST NOT accept a peer that declares a lower profile than its own unless the operator has explicitly allowed it, and that allowance MUST be audited.
