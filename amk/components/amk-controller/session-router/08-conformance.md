# Conformance

**Overview.**  
This module states the precise criteria that an implementation must satisfy in order to claim conformance to the Session Router specification. Conformance requires correct implementation of the core protocol and invariants plus explicit declaration and correct implementation of one of the three complexity profiles. Higher profiles subsume all requirements of lower profiles. The core security invariants remain identical across all profiles; only isolation strength, cryptographic implementation, and infrastructure differ.

---

## 18. Conformance

- **RTR-61** A component is conformant when it satisfies every RTR requirement applicable to its role and when it correctly declares and implements one of the three complexity profiles.
- **RTR-62** A deployment is conformant only if the mediated inter-entity traffic of each session passes exclusively through the corresponding router instance.

### Profile Declaration and Requirements

- **PROF-1** Every conformant implementation MUST declare exactly one profile: `basic`, `standard`, or `high`. The declared profile MUST be present in the Init Envelope and in the Discovery Record.
- **PROF-2** An implementation that claims `standard` MUST satisfy every requirement of the Basic profile in addition to the Standard obligations.
- **PROF-3** An implementation that claims `high` MUST satisfy every requirement of the Basic and Standard profiles in addition to the High obligations.
- **PROF-4** The core security invariants (INV-1 through INV-12) and all RTR requirements that are not explicitly relaxed by a lower profile remain mandatory at every level.

#### Basic Profile Obligations
- Single-process or single-threaded designs are permitted.
- Fixed-size cells and bounded timing jitter MAY be omitted.
- Adapters MAY share address space with other components.
- Ordinary software cryptographic libraries are sufficient.
- No HSM, TEE, or hardware root-of-trust is required.
- Shared host for factory and instances is acceptable.
- Instance state persistence may be relaxed for experimentation.

#### Standard Profile Obligations
- Each router instance MUST run in its own isolated process or container with no shared memory.
- All normative requirements, including fixed-size cells, AEAD sequence numbers, mutual attestation, opaque denials, registration tickets, complete epoch lifecycle, and the supplied policy, MUST be implemented.
- Adapters MUST run in a separate isolate with their own key store when key isolation is required.
- Software key storage is acceptable.
- Network isolation between instances is required.
- Automatic destruction and secure erasure of instance state is mandatory.

#### High Profile Obligations
- All Standard obligations plus:
- Private keys MUST be protected by an HSM, TPM, secure element, or equivalent and MUST NOT exist in ordinary process memory in clear form.
- Each router instance and the factory MUST execute inside a Trusted Execution Environment or equivalent hardware security domain.
- Measured boot / remote attestation MUST be supported.
- Adapters MUST be isolated in a separate TEE or hardware domain when used.
- Explicit side-channel resistance, memory scrubbing, and high-assurance review of security-critical paths are required.
- Dedicated isolated network segments for the factory/instance plane are required.
- Hardware-enforced secure erasure and anti-rollback protections are mandatory.

- **PROF-5** An implementation that fails to meet the obligations of its declared profile is non-conformant for that profile, even if it satisfies the core RTR requirements.
