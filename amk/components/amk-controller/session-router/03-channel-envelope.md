# Channel Establishment & Envelope Format

**Overview.**  
This module specifies the three-message brokered ECDH handshake that establishes an end-to-end encrypted channel between two roles, the mandatory mutual attestation and signature rules, and the precise format of the envelopes that travel on those channels. Under the Basic profile, fixed-size cells and related padding obligations may be relaxed.

---

## 8. Channel Establishment (Brokered Key Agreement)

The initiator (I) wants to reach a role held by the responder (R). Neither knows the other’s key. Attestation is mutual.

1. **M1, I → Router → R:** `{att_i, eph_pk_i, nonce_i, sig_i}`, where `sig_i = Sign_sk_i(T1)` and `T1 = ("hs1", session, epoch, role_i, role_r, eph_pk_i, nonce_i)`. The router resolves the target role and checks policy before forwarding. R verifies `att_i` and `sig_i`.
2. **M2, R → Router → I:** `{att_r, eph_pk_r, nonce_r, sig_r}`, where `sig_r = Sign_sk_r(T2)` and `T2 = (T1 ‖ eph_pk_r ‖ nonce_r)`. I verifies `att_r` and `sig_r`.
3. Both derive `H = Hash(T2)` and `K = KDF(ECDH(eph_sk_i, eph_pk_r) ‖ H)`.
4. **M3, I → Router → R:** `{sig_i2, tag}`, where `sig_i2 = Sign_sk_i("hs3" ‖ H)` and `tag = MAC_K("hs3" ‖ H)`. R verifies both. The channel is active only after R accepts M3.

- **RTR-28** The router MUST permit a channel request only if policy allows at least one msg_class for the (sender role, receiver role, direction) pair in the current epoch. The channel is bound to that class set, and each later envelope MUST be checked against it. Handshake messages are not subject to class filtering.
- **RTR-29** Each of M1 and M2 MUST carry a signature, made with the sender’s session private key, over the transcript as defined above. M3 MUST carry a signature and a key-confirmation MAC over `H`. Each verifier MUST check signatures against the public key in the verified attestation.
- **RTR-30** A party MUST abort the handshake on any attestation, signature, or MAC failure. R MUST NOT send application data before M3 is verified.
- **RTR-31** After the handshake each party knows the counterparty’s role and session public key for that epoch. Neither party MAY learn the counterparty’s session private key, LA, or long-term identity.
- **RTR-32** The router MUST see only public keys, nonces, attestations, signatures, and the M3 tag. It MUST NOT see or derive `K`.
- **RTR-33** Attestation exchange is mandatory in both directions. A handshake in which either party lacks a verified attestation MUST be rejected.
- **RTR-34** Channels MUST be per-epoch. On epoch change the channel MUST be re-established and the old keys retired.
- **RTR-105** The router MUST hold pending-handshake state only to route M2 and M3, MUST cap it at `HS_MAX` per instance, and MUST expire it after a bounded timeout. Over the cap, new channel requests receive the opaque unreachable result.

---

## 9. Envelope

Sender to Router:

```
{
  to:      role | capability | channel-id,
  session, epoch,
  msg_class,
  nonce,       // AEAD nonce
  ciphertext   // E2E for receiver, K-derived; sequence number inside
}
```

Router to Receiver:

```
{
  from_tag: <ephemeral, per-message>,
  session, epoch,
  msg_class,
  nonce,
  ciphertext   // unchanged
}
```

- **RTR-35** The router MUST strip the sender’s LA and substitute a fresh per-message `from_tag`.
- **RTR-36** The router MUST forward `ciphertext` unchanged.
- **RTR-37** A receiver replies to the `from_tag`. The router MUST map it back to the sender’s LA.
- **RTR-38** A `from_tag` MUST expire no later than the end of its epoch plus `G`. The router MUST cap live tags at `TAG_MAX` per epoch. Beyond the cap, and for a reply to an expired tag, the router MUST return the opaque unreachable result.
- **RTR-39** The set of valid `msg_class` values is defined by a registry supplied or referenced in the Init Envelope. Policy and routing MUST NOT accept an unregistered value. A minimal initial set is: `ctl` (session and channel control), `data` (application payload), `audit` (reserved, default-deny).
- **RTR-40** Under Standard and High profiles, entities MUST send fixed-size cells of `CELL_SIZE` bytes. A message larger than one cell MUST be fragmented into cells, with fragment index and count inside the ciphertext, and reassembled by the receiver. Under the Basic profile, fixed-size cells MAY be omitted. The router MAY enforce cell size when required by the profile; observable size is then the cell size.
- **RTR-41** The AEAD plaintext MUST carry a per-channel sequence number, monotonic from 1. Receivers MUST reject duplicate and out-of-order sequence numbers. The router does not see them.
- **RTR-106** The AEAD associated data MUST include `session`, `epoch`, `msg_class`, `nonce`, and the channel id. It MUST NOT include `from_tag`. A receiver MUST reject an envelope whose header fields fail the AEAD check.
