# 02-issuance.md

**File:** `02-issuance.md`
**Scope:** Issuance protocol, proof-of-possession, binding rules.
**Reference prefix:** `ATA-02`

---

## ATA-02:01 Issuance Request

- A client requests an attestation by sending an issuance request (JSON, UTF-8) over TLS 1.3 (RFC 8446).
- The request MUST contain:
  - `session_public_key`: the public key to bind.
  - `role`: the requested role.
  - `session_handle`: the session handle.
  - `epoch`: the epoch number.
  - `proof_of_possession`: a PoP as defined in `ATA-02:03`.
  - `request_nonce`: a unique nonce for the request (at least 128 bits).
  - `request_timestamp`: the request time.
- Session keys are Ed25519 (RFC 8032) unless a profile defines another algorithm.
- The request carries no role list and no epoch boundaries. Both come from the session record (`ATA-02:02`).

## ATA-02:02 Request Validation

- The Authority MUST validate:
  - the request format,
  - that the request nonce is fresh (within `DV-ATA-04`) and has not been seen in that window; the Authority MUST remember request nonces for the window,
  - that the request timestamp is within the freshness window plus clock skew (`DV-ATA-07`),
  - that a session record exists for the `session_handle` and `epoch`, and the epoch has not ended beyond `G`.
- The session record is a JSON object with `session_handle`, `epoch`, `epoch_start`, `epoch_end` and `declared_roles`. `declared_roles` is an array of unique, non-empty UTF-8 strings of at most 256 bytes each.
- The Authority MUST accept session records only from the pinned controller identity over an authenticated channel, and MUST NOT take a role list or epoch boundaries from a requester.
- A session record is immutable per (`session_handle`, `epoch`). A different record for the same pair MUST be rejected.
- The Authority MUST rate-limit issuance requests per source.
- On any failure, the Authority MUST reject the request with an opaque error.

## ATA-02:03 Proof-of-Possession

- The requester MUST prove possession of the session private key corresponding to `session_public_key`. [INV-ATA-01]
- The PoP is an Ed25519 signature by the session private key over the JCS (`ATA-01:02`) serialization of:
  - `typ`: the string `amk-ata-issuance-pop-v1`,
  - `aud`: the Authority's `issuer`,
  - `session_public_key`, `session_handle`, `epoch`, `role`,
  - `request_nonce`, `request_timestamp`.
- The Authority MUST verify the PoP over exactly that value before issuance.
- A failed PoP MUST result in an opaque rejection.

## ATA-02:04 Role Validation

- The Authority MUST verify that the requested role is present in `declared_roles` of the session record. [INV-ATA-02]
- If no session record exists, or the role is absent, the Authority MUST NOT issue.

## ATA-02:05 Requester and Identity Authentication (Profile-Dependent)

- Under the Basic profile, requester authentication is not required.
- Under the Standard profile, the Authority MAY require authentication of the requester or its long-term identity before issuance. Under the High profile it SHOULD.
- When authentication is required, the method MUST be one the metadata lists in `client_authentication`: mutual TLS (RFC 8705) or a JWT client assertion (RFC 7523).
- Long-term identity MUST NOT be included in the attestation. [INV-ATA-03]

## ATA-02:06 Issuance

- On successful validation, the Authority MUST:
  - generate a unique nonce for the attestation,
  - compute `valid_from` and `valid_to` inside the epoch plus grace window (`ATA-01:03`),
  - construct the attestation with all required fields, including the `kid` of an `active` signing key,
  - sign the canonical serialization,
  - return the signed attestation to the requester.
- The Authority MUST refuse to issue if any validation fails.

## ATA-02:07 Binding Rules

- An attestation is bound to:
  - the session public key,
  - the role,
  - the session handle,
  - the epoch.
- A change in any of these requires a new attestation.
- The Authority MUST NOT issue an attestation that conflicts with an existing valid attestation for the same session, epoch, and role unless the existing one is revoked.

## ATA-02:08 Summary

- Issuance requires proof-of-possession, a controller-supplied session record that defines the epoch and the permitted roles, and, under some profiles, requester authentication. The Authority validates the request, checks the role against the session record, and issues a signed attestation bound to the session key, role, session handle, and epoch.

---

Defaults: values for `DV-ATA-nn` are stated in `amk-authority.md` (Defaults).
