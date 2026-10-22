# Per-Session Router Instances & Discovery

**Overview.**  
This module specifies the complete lifecycle of a router instance: creation by the factory from a signed Init Envelope that declares the set of roles and the policy, isolation guarantees, the authenticated control interface between factory and instance, Binding Data exchange, issuance of single-use registration tickets, delivery of the factory-signed Discovery Record, first registration, registration-window enforcement, and the re-discovery procedure. Every value associated with an instance is generated fresh and is never shared with any other instance. Isolation strength scales with the declared complexity profile.

---

## 16. Per-Session Router Instances

- **RTR-67** One router instance MUST be created for each session. An instance MUST serve exactly one session and no other.
- **RTR-68** An instance MUST share no value with any other instance, including instance id, endpoint, instance keypair, LA derivation secret, `from_tag` secret, nonce and sequence state, policy state, tables, control credential, and registration tickets. Every such value MUST be generated fresh at creation from a cryptographically secure source.
- **RTR-69** Instances MUST be isolated from one another at the execution level required by the claimed profile (process/container for Standard, TEE or equivalent for High; soft isolation permitted for Basic).
- **RTR-70** Only the router factory MAY create an instance. No other component MAY create, start, clone, or resume one.
- **RTR-71** After creating an instance the factory MUST NOT retain the instance’s private key, LA table, or full policy state beyond what is required for lifecycle management. It MAY retain the session handle, instance id, endpoint, status, expiry, and per-role registered flags.
- **RTR-72** An instance MUST generate its own keypair inside its isolate. The private key MUST NOT leave it.
- **RTR-73** An instance MUST be destroyed on session close, session handle revocation, registration window expiry, idle timeout, or failure. On destruction all state MUST be erased and the endpoint MUST thereafter behave as absent.
- **RTR-74** Instance state MUST NOT persist beyond the session under Standard and High profiles. A destroyed instance MUST NOT be resumed. A later session requires a new instance. (Basic profile may relax persistence for experimentation.)
- **RTR-114** The factory and each instance MUST communicate over an authenticated control interface using a credential unique to that instance, minted at creation. Core operations include readiness notification, role-registration notification, policy/ticket loading, ticket revocation, and destruction.
- **RTR-115** The control interface MUST NOT carry entity payload, the LA table, or any key other than the instance public key.

---

## 17. Session Router Discovery

Creation and discovery flow (high level):

1. Session Initiator → factory ingress: Init Envelope (declares roles, policy, parameters).
2. Factory validates the envelope.
3. Factory requests Binding Data from the parties that will occupy the declared roles.
4. Parties return Binding Data (role, epoch-0 session public key + attestation, return path, etc.).
5. Factory creates the instance, loads policy and ticket verifiers.
6. Factory delivers Discovery Record + sealed registration ticket to each bound role via its return path.
7. Each entity registers with the instance.

- **RTR-75** The Session Initiator MUST create an Init Envelope containing at least: `session_handle`, initiator attestation or equivalent authenticity proof, `roles` (the complete list of role strings for the session), `policy`, return-path information, `nonce`, `issued_at`, `expires_at`, and factory identifier. The envelope MUST be signed and sealed to the factory’s public key.
- **RTR-76** The ingress MUST forward the sealed envelope to the factory unchanged and MUST NOT open or retain it after delivery.
- **RTR-77** The factory MUST accept Init Envelopes only through the designated ingress and MUST discard any other arrival without response.
- **RTR-78** The factory MUST unseal the envelope and verify the signature and authenticity proof. It MUST reject the envelope if it is expired, if its nonce was seen before, if its session handle is already bound, or if its policy or role list is malformed.
- **RTR-79** The factory MUST request Binding Data for each role listed in the Init Envelope. Each request carries the session handle, factory identifier, a fresh nonce, and the factory’s own attestation or authenticity proof.
- **RTR-80** Binding Data MUST be signed by the responding party and MUST contain: role, session handle, epoch-0 session public key and its attestation, the return path for Discovery Record delivery, a suite identifier, and an echo of the factory nonce.
- **RTR-81** The factory MUST create the instance only after receiving valid Binding Data for every role in `roles` (or a documented subset if partial binding is supported). It MUST issue one single-use registration ticket per role, bound to the instance id, role, and session handle, with expiry `REG_WINDOW`, sealed to that role’s epoch-0 session public key. The instance holds only verifiers for the tickets.
- **RTR-82** The Discovery Record MUST contain: session handle, instance id, endpoint, `router_pk`, suite identifier, `registration_window_expiry`, `instance_expiry`, and factory identifier. It MUST be signed by the factory. The endpoint MUST be unique to the instance and unguessable.
- **RTR-83** The factory MUST deliver the Discovery Record and the sealed ticket to each bound role only through that role’s return path.
- **RTR-84** An entity MUST verify the Discovery Record (factory signature, matching session handle, not expired). It MUST register only with an endpoint from a verified Discovery Record.
- **RTR-85** On first registration a role MUST present its registration ticket in addition to the normal registration contents; the instance MUST consume it. The instance MUST sign the registration nonce with its instance key; the entity MUST verify that signature against `router_pk` and abort on failure.
- **RTR-86** Every role that the factory expects to register MUST do so before `registration_window_expiry`. Otherwise the instance MUST be destroyed.
- **RTR-87** An instance MUST accept at most one active registration per (role, epoch).
- **RTR-88** An entity that has lost its Discovery Record MAY send a signed Re-Discovery Request containing the session handle, role, current-epoch attestation, and a nonce. If the instance is live and the role is bound, the factory MUST re-deliver the Discovery Record. If the role has not yet registered, the factory MAY issue a fresh ticket and invalidate the previous one.
- **RTR-89** The ingress, factory, and instance MUST NOT distinguish failure causes to the requester. A failed request receives no response or one opaque response.
- **RTR-116** The Session Initiator MUST obtain the factory identifier and public key from a trusted source and MUST NOT seal an Init Envelope to any other key.
