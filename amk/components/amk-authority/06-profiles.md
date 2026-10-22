# 06-profiles.md

**File:** `06-profiles.md`
**Scope:** Basic / Standard / High requirements.
**Reference prefix:** `ATA-06`

---

## ATA-06:01 Profile Overview

- The Authority supports three operational profiles:
  - **Basic:** software keys allowed, signed revocation list, suitable for any language.
  - **Standard:** non-exportable keys, full revocation list, process isolation.
  - **High:** HSM/TEE-protected signing keys with published attestation evidence, real-time revocation, hardware-protected audit of issuance.
- The profile in use MUST be documented and published as `profile` in the signed metadata (`ATA-01:07`).

## ATA-06:02 Basic Profile

- Signing keys MAY be software-protected.
- A signed revocation list is required; real-time revocation is not offered.
- Identity binding is not required.
- Process isolation is not required.
- Suitable for development, testing, or low-risk deployments.

## ATA-06:03 Standard Profile

- Signing keys MUST be non-exportable: held by an OS keystore, a key-management service in which the key never leaves the service, or a hardware token. Keys in process memory, files, or environment secrets do not qualify.
- Revocation list is required.
- Real-time revocation endpoint MAY be provided.
- Identity binding MAY be required.
- Process isolation MUST be enforced.
- Suitable for production deployments with moderate security requirements.

## ATA-06:04 High Profile

- Signing keys MUST be HSM- or TEE-protected.
- The metadata MUST include `evidence`: an attestation of the signing-key protection domain, as an Entity Attestation Token (RFC 9711) produced under the RATS architecture (RFC 9334).
- Measured boot of the Authority SHOULD be supported.
- Hardware-protected audit of issuance MUST be enabled.
- Revocation list is required.
- Real-time revocation endpoint MUST be provided.
- Identity binding SHOULD be required.
- Process isolation MUST be enforced.
- Suitable for high-security deployments.

## ATA-06:05 Profile Selection

- The profile MUST be selected at deployment time.
- The profile MUST NOT be changed without re-provisioning.
- Clients MUST read the profile from the signed metadata and verify that it matches their requirements before trusting attestations. If the metadata is unavailable or invalid, the client MUST reject.
- A High claim is accepted only if the client verifies the metadata's `evidence` against a trust anchor provisioned out of band. Otherwise the Authority is treated as no higher than Standard, and a client that requires High MUST reject.
- Basic and Standard claims are assertions by the Authority, not independently verified.

## ATA-06:06 Profile Summary

| Requirement | Basic | Standard | High |
|-------------|-------|----------|------|
| Signing key protection | Software | Non-exportable | HSM/TEE |
| Key-protection evidence in metadata | No | No | Required |
| Revocation list | Required | Required | Required |
| Real-time revocation | No | Optional | Required |
| Identity binding | No | Optional | Should |
| Process isolation | No | Required | Required |
| Measured boot | No | No | Should |
| Hardware audit | No | No | Required |

## ATA-06:07 Peer Profile Rule

- A verifying client or controller MUST NOT accept attestations from an Authority whose profile is lower than the profile the client requires, unless the operator or administrator has explicitly allowed it, and that allowance MUST be audited.
- An Authority whose profile cannot be determined from verified metadata is treated as Basic.

## ATA-06:08 Summary

- Three profiles define the security requirements for the Authority. A signed revocation list is required under all of them. Standard requires non-exportable keys; High adds hardware-protected keys, published attestation evidence, mandatory real-time revocation, and hardware-protected audit. The profile is published in signed metadata and verified by clients.

## ATA-06:09 Declaration and Conformance

- Each implementation MUST document its supported signature algorithms, trust anchors, failure behavior, and any unsupported features.
- Conformance tests MUST cover valid, malformed, expired, revoked, mismatched, and untrusted attestations, and are traced in `amk-test-matrix`.

## ATA-06:10 Audit Record Format and Retention

- The audit trail is JSON Lines (one JSON object per line, UTF-8) and is append-only.
- Each record MUST contain `seq`, `ts` (RFC 3339), `event` (`issue`, `revoke`, `bind`, `key_status`, `metadata_publish`, or `reject`), `outcome`, `prev_hash` and `hash`. It carries `nonce`, `kid`, `session_handle`, `epoch` and `role` where they apply.
- `hash` is the SHA-256 (FIPS 180-4) of the JCS serialization of the record without `hash`, and `prev_hash` is the previous record's `hash`.
- Records MUST NOT contain secrets, private keys, long-term identity, or personal data. [INV-ATA-03]
- An operation that requires an audit record MUST NOT take effect unless that record is committed. If the record cannot be committed, the Authority MUST fail the operation with an opaque error. A record's `outcome` MUST reflect the actual result and MUST NOT be `success` before the operation has taken effect.
- Under High, the trail MUST be protected by hardware and the Authority MUST periodically sign a checkpoint of `seq` and `hash` with a signing key.
- Minimum retention is stated in `DV-ATA-10`. Revocation never alters or deletes audit records.
