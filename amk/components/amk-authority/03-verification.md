# 03-verification.md

**File:** `03-verification.md`
**Scope:** Verification obligations for clients.
**Reference prefix:** `ATA-03`

---

## ATA-03:01 Verification Obligations

- A client receiving a role attestation MUST verify:
  - the signature, using the key named by `kid` in the signed metadata (`ATA-03:02`),
  - the validity window (`ATA-03:03`),
  - the presentation proof (`ATA-03:04`),
  - the revocation status (`ATA-04`),
  - that the session handle and epoch match the current session context (`ATA-03:06`).
- A client MUST reject an attestation that fails any check.

## ATA-03:02 Signature Verification

- The client MUST obtain the verification key by `kid` from the Authority's signed metadata, verified against the pinned root key (`ATA-01:07`).
- The client MUST reject the attestation if the `kid` is absent from the metadata, the key's status is `revoked`, or the attestation's `valid_from` is outside the key's `not_before` and `not_after`.
- The client MUST verify the signature over the canonical serialization of the attestation fields, using the algorithm the metadata lists for that key.
- A signature verification failure MUST result in opaque denial. [INV-ATA-04]

## ATA-03:03 Validity Window Verification

- The client MUST check that `valid_to` has not passed. No clock tolerance applies to `valid_to`.
- The client MAY allow the clock skew tolerance (`DV-ATA-07`) when checking that `valid_from` has been reached.
- The client MUST reject an attestation outside its validity window.

## ATA-03:04 Presentation Proof

- A verifier MUST obtain proof that the presenter holds the private key for `subject_public_key`.
- The verifier supplies a fresh `verifier_nonce` of at least `DV-ATA-05` bits. It is single-use and expires after `DV-ATA-04`.
- The presenter returns an Ed25519 signature by the session private key over the JCS (`ATA-01:02`) serialization of:
  - `typ`: the string `amk-ata-presentation-v1`,
  - `aud`: the verifier's identifier,
  - `attestation_nonce`: the attestation's `nonce`,
  - `verifier_nonce`,
  - `timestamp`.
- The verifier MUST reject a missing or invalid proof, and a reused or expired `verifier_nonce`.
- The attestation `nonce` identifies the attestation and is not a replay token. The same attestation MAY be presented again with a fresh proof.

## ATA-03:05 Revocation Status

- The client MUST check revocation status on every verification. [INV-ATA-05]
- If the client's revocation list is older than `R_MAX`, or no revocation list is available, it MUST NOT accept the attestation as current.
- The relying party's policy MAY define suspension or restricted handling for that case. Absent such a policy, the client MUST deny.
- Under High, the client MUST also query the real-time status endpoint before relying on the attestation (`ATA-04:04`), and MUST reject it if the endpoint cannot be reached or its answer is not current.

## ATA-03:06 Session Context Verification

- The client MUST verify that the `session_handle` and `epoch` in the attestation match the current session context.
- A mismatch MUST result in opaque denial. [INV-ATA-04]

## ATA-03:07 Controller Behavior

- The controller is a verifying client: it applies ATA-03:01 to ATA-03:06 before relying on an attestation. What a verified attestation permits is decided by controller policy, not by the attestation.
- The controller treats a failed verification as opaque denial. [INV-ATA-04]
- The controller MUST NOT distinguish failure causes to unauthenticated parties.
- The controller MUST log verification failures for audit, and MUST redact secrets and personal data from those logs.

## ATA-03:08 Summary

- Clients verify signature, validity window, presentation proof, revocation status, and session context. A failed verification is opaque denial. Missing or stale revocation data is never treated as "not revoked". Controller behavior follows the same rules.

---

Defaults: values for `DV-ATA-nn` are stated in `amk-authority.md` (Defaults).
