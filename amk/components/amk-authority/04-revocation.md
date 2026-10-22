# 04-revocation.md

**File:** `04-revocation.md`
**Scope:** Revocation list / real-time revocation.
**Reference prefix:** `ATA-04`

---

## ATA-04:01 Revocation List

- The Authority MUST publish a signed revocation list (RL) under every profile. The list is served by HTTPS GET at `revocation_list_url` from the signed metadata. Distribution is pull-only.
- The RL is a JSON object that MUST contain:
  - `issuer`: the Authority's identifier.
  - `kid`: the key that signed the list.
  - `version`: an integer that increases whenever the list's contents change.
  - `published_at`: the publication timestamp.
  - `revoked`: a list of entries, each with the attestation `nonce`, `revoked_at`, and optionally an opaque `reason` code.
  - `signature`: the signature over the JCS serialization (`ATA-01:02`) without the `signature` field.
- The RL MUST be signed by a key that the signed metadata lists as `active`.
- The RL MUST be republished with a new `published_at` at least every `RL_INTERVAL` (`DV-ATA-06`), even when unchanged.
- An entry MAY be removed once the revoked attestation's `valid_to` has passed.
- Clients MUST reject a list whose `version` is lower than one they have seen.

## ATA-04:02 Revocation Reasons and Requests

- An attestation MAY be revoked for:
  - key compromise,
  - role change,
  - session termination,
  - policy violation,
  - or any other reason defined by the Authority or profile.
- The reason MAY be included in the RL as an opaque code.
- Revocation MUST be requested only by the controller or the Authority's operator over an authenticated channel. Requests from session participants MUST be rejected.
- Revocation never alters or deletes historical audit records (`ATA-06:10`).

## ATA-04:03 Client Obligations

- Clients MUST check the RL on every verification. [INV-ATA-05]
- Clients MUST verify the RL signature using the key named by its `kid` in the signed metadata.
- The age of an RL is the current time minus `published_at`. If it exceeds `R_MAX`, the client MUST NOT accept the attestation as current.
- If no RL is available, the client MUST NOT accept the attestation as current.
- The relying party's policy MAY define suspension or restricted handling for these cases. Absent such a policy, the client MUST deny. This applies to every profile.

## ATA-04:04 Real-Time Revocation Endpoint

- Under the Standard profile, the Authority MAY provide a real-time revocation endpoint. Under the High profile it MUST.
- The endpoint is published as `revocation_status_url` in the signed metadata.
- The endpoint MUST accept a query for a specific attestation `nonce` and return a signed response containing `nonce`, `status` (`good` or `revoked`), `checked_at`, `kid` and `signature`.
- The response MUST be signed by an `active` key listed in the metadata. The client MUST NOT rely on a response older than `DV-ATA-09`.
- Under High, the client MUST query the endpoint when it accepts an attestation, and again whenever its policy re-verifies that attestation. An unreachable endpoint or a response that is not current MUST result in rejection.
- The endpoint MUST be authenticated or rate-limited to prevent abuse.
- Real-time revocation is not offered under the Basic profile.

## ATA-04:05 Revocation Propagation

- The Authority MUST propagate revocations as quickly as the profile allows.
- Worst-case time from revocation to rejection through the RL is about `RL_INTERVAL` plus `R_MAX` (about 360 seconds under Basic and 180 seconds under Standard and High with the default values). Under High the real-time endpoint closes this gap.

## ATA-04:06 Summary

- The Authority publishes a signed, versioned revocation list under every profile. Clients check it on every verification and reject stale, missing, or revoked cases unless policy defines restricted handling. Real-time revocation is optional under Standard and required under High.

---

Defaults: values for `DV-ATA-nn` are stated in `amk-authority.md` (Defaults).
