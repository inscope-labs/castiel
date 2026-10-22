# Router Knowledge Boundary, Failure & Compromise

**Overview.**  
This module enumerates precisely the residual knowledge the Session Router is permitted to possess (traffic metadata) and the knowledge it is forbidden to possess. It then catalogues significant failure and compromise conditions together with the required system response, emphasising fail-closed behaviour and the impossibility of decrypting, impersonating, or disclosing long-term identities. These boundaries hold at every complexity profile.

---

## 13. Router Knowledge Boundary

The router **knows** (traffic metadata):

- which role sent to which role, within the session;
- cell sizes (when fixed-size cells are used), timings, and message classes;
- the network endpoint of each registered entity;
- session membership (which roles have registered);
- policy and its outcomes;
- that successive registrations of the same role within a session belong to the same logical participant.

The router **does not know**:

- payload contents;
- derived shared secrets;
- long-term identity of any party;
- session private keys;
- anything about any other session.

The router **cannot**:

- impersonate any entity;
- decrypt traffic;
- reveal one entity’s long-term identity to another;
- forge a role attestation without the Attestation Authority.

- **RTR-56** The router’s residual knowledge MUST be the traffic metadata listed above and nothing else. It MUST be bounded by cell padding (when required by profile), bounded timing jitter (when required), and per-session instances. Decoy traffic is OPTIONAL.
- **RTR-57** A receiver MUST NOT be able to learn, through the router, the sender’s platform, physical endpoint, or the route resolution. If a sender reveals itself in the payload, that is the sender’s decision.
- **RTR-113** Metadata exposure at any hop other than the router is limited to what the adapter and factory modules state. No hop MAY learn payload contents.

---

## 14. Failure and Compromise

| Condition | Required effect |
|---|---|
| Router instance down | Data plane stops. Entities MUST NOT assume any other mediated path. |
| Router compromised | Learns traffic metadata. Cannot decrypt, impersonate, or disclose long-term identities. May drop, delay, or replay; mitigated by nonces, receiver-side sequence numbers, and the E2E AEAD. |
| Router colludes with one entity | Can reveal that entity’s counterparty role, not long-term identity. Can selectively deny or delay. |
| Attestation Authority compromised | Attestations become forgeable. Mitigated by key protection, mutual authentication, and pinned verification keys held by entities. |
| Attestation Authority unreachable | No new attestations. Epochs extend by at most `X`, then channels close. |
| One entity compromised | Gains its own role’s channels only. Cannot derive other channels’ keys. |
| Epoch rollback attempt | Rejected by monotonic epoch checks in the router and (when available) the Attestation Authority. |
| Router factory compromised | Can mint a rogue instance and sign a Discovery Record pointing at it. A rogue instance has only the router-compromised effect. Cannot reach other sessions’ instances. |
| Ingress compromised | Can drop or delay Init Envelopes and learn that an init occurred. Cannot read sealed envelopes or forge the Session Initiator’s signature. |
| One router instance compromised | Affects its one session only. |

- **RTR-58** The router MUST reject a non-monotonic epoch. Sequence numbers are enforced by receivers, not by the router.
- **RTR-59** When the router instance is unavailable, entities that rely on it MUST stop inter-entity traffic mediated by it and enter an appropriate application-defined safe state.
