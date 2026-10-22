# Operational Profiles

**File number:** 8  
**Overview.**  
This module defines the three operational profiles—Basic, Standard, and High—that govern verification strength, isolation and audit for the loader and package authority. An implementation MUST declare exactly one profile. Higher profiles subsume all requirements of lower profiles.

---

## Common Rules

- **RTM-8:1** Every conformant implementation MUST declare exactly one profile: `basic`, `standard`, or `high`.
- **RTM-8:2** The declared profile MUST be discoverable through a status or capability envelope.
- **RTM-8:3** An implementation claiming `standard` MUST satisfy every Basic requirement in addition to the Standard obligations.
- **RTM-8:4** An implementation claiming `high` MUST satisfy every Basic and Standard requirement in addition to the High obligations.
- **RTM-8:5** The invariants in file 1 apply at every profile. Signature, hash and contract-version verification are mandatory at every profile.

---

## Basic Profile

**Target:** Hobbyists, educational use, rapid prototypes.

- **RTM-8:6** Software-protected verification keys are permitted.
- **RTM-8:7** Soft isolation between runtime contexts is acceptable.
- **RTM-8:8** Egress control MAY be advisory, but undeclared egress MUST still be refused.
- **RTM-8:9** Resource limits MUST be enforced, with simplified mechanisms permitted.
- **RTM-8:10** Minimal audit retention is acceptable.

## Standard Profile

**Target:** Production services and professional deployments.

- **RTM-8:11** Verification keys MUST be non-exportable and protected by an OS keystore or equivalent.
- **RTM-8:12** Each runtime MUST run in its own process, container or isolate with no shared memory.
- **RTM-8:13** Egress MUST be denied by default and enforced by the platform, not by the runtime.
- **RTM-8:14** A complete signed audit of verification, load, include, remove, fault and rejection events MUST be maintained.
- **RTM-8:15** Cached packages MUST be stored keyed by package hash with integrity protection.

## High Profile

**Target:** Enterprise, regulated and high-assurance environments.

- **RTM-8:16** Verification keys MUST be protected by an HSM, secure element or TEE.
- **RTM-8:17** Runtime contexts MUST be isolated by a hardware-backed security domain or equivalent.
- **RTM-8:18** Measured load and remote attestation of the loader SHOULD be supported.
- **RTM-8:19** The audit trail MUST be protected against tampering by hardware-backed or equivalently strong integrity protection.
- **RTM-8:20** System packages SHOULD be reproducibly built so their package hash can be independently reproduced.

---

## Profile Summary Table

| Requirement | Basic | Standard | High |
|---|---|---|---|
| Signature, hash, contract-version verification | MUST | MUST | MUST |
| Verification key protection | Software | OS keystore | HSM / TEE |
| Runtime isolation | Soft | Process / container / isolate | Hardware-backed |
| Undeclared egress refused | MUST | MUST | MUST |
| Egress denied by default, platform-enforced | MAY (advisory) | MUST | MUST |
| Resource limits | MUST (simplified) | MUST | MUST |
| Signed lifecycle audit | Minimal | Full | Hardware-protected |
| Package cache keyed by hash with integrity | SHOULD | MUST | MUST |
| Loader attestation | — | — | SHOULD |
| Reproducible system packages | — | — | SHOULD |
