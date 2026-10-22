# Addressing, Registration & Epochs

**Overview.**  
This module defines the three addressable forms (role, capability, channel) that the Session Router resolves to opaque logical addresses, the registration procedure that an entity must complete at the start of each epoch, and the complete epoch lifecycle. Roles are arbitrary strings declared in the Init Envelope; there are no hard-coded role names.

---

## 6. Address Space

Three addressable forms, each resolved by the router to an LA.

| Form | Example | Scope |
|---|---|---|
| Role address | `role:<name>` where `<name>` is any string declared in the Init Envelope | Stable within a session and epoch |
| Capability address | `cap:<token>` | Minted at session start |
| Channel address | per-epoch, per-direction opaque ID | One established channel |

- **RTR-21** The router MUST resolve all three forms to LAs and MUST NOT expose an LA to any entity. A sender MUST NOT learn the LA it reached, and a receiver MUST NOT learn the LA that reached it.
- **RTR-22** A capability address MUST encode a right and MUST NOT encode an identity.

---

## 7. Registration and Epochs

Performed by each entity at the start of each epoch.

- **RTR-23** The entity MUST present: session handle, epoch, role, session public key, and attestation. On the first registration of a role in an instance it MUST also present its registration ticket.
- **RTR-24** The router MUST issue a registration nonce. The entity MUST sign it with its session private key (proof of possession).
- **RTR-25** The router MUST verify the attestation against the Attestation Authority and the revocation list (when available), and MUST reject registration on any failure.
- **RTR-26** The router MUST assign an opaque, epoch-scoped LA and record LA to (role, PK, endpoint) in its private table.
- **RTR-27** LAs and session keys MUST rotate every epoch to limit key, tag, and LA lifetime. Because each role has at most one active registration per epoch, the router can link successive registrations of the same role within a session. Unlinkability across sessions comes from per-session instances.
- **RTR-104** An entity MUST re-register each epoch with a fresh session key and a fresh attestation.
- **RTR-100** An epoch MUST end at the earliest of: `T_MAX` elapsed, `N_MAX` envelopes processed by the instance, or a rollover request sent as a control message.
- **RTR-101** When an epoch limit is reached the router MUST send an epoch notice to every registered entity. Entities then follow RTR-104.
- **RTR-102** Channels of epoch N remain valid until the corresponding epoch N+1 channel is established or `G` elapses, whichever is first. At most two epochs MAY be live at once.
- **RTR-103** If the Attestation Authority is unreachable when an epoch ends, an entity MAY keep epoch N for at most `X` further. After that the entity and router MUST close all channels (fail closed).
