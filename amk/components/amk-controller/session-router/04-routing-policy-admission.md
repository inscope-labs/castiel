# Routing, Policy & Entity Admission

**Overview.**  
This module defines the role-based, epoch-scoped policy model. Roles are arbitrary strings declared in the Init Envelope; there is no hard-coded role set or default matrix. The complete policy (permitted (sender-role, receiver-role, msg_class, direction) tuples) is supplied with the Init Envelope. Entity admission is driven solely by the roles listed in that envelope and the ability to present a valid attestation for one of those roles.

---

## 10. Routing and Policy

Policy is defined over (sender-role, receiver-role, session, epoch, msg_class, direction), never over identities.

- **RTR-42** A denial MUST return an opaque unreachable result to the sender. It MUST NOT distinguish “role absent,” “policy denied,” and “receiver offline.”
- **RTR-43** Policy MUST be held by the router for enforcement. It MAY be mirrored to an external audit log or the Attestation Authority.
- **RTR-44** Policy MUST be epoch-scoped. Admission in epoch N MUST NOT imply admission in epoch N+1.
- **RTR-45** The absence of a policy rule MUST be treated as deny.
- **RTR-46** Every policy violation SHOULD be audited.

- **RTR-47** The policy supplied in the Init Envelope is the sole policy for the instance. There is no fixed ceiling of hard-coded roles.
- **RTR-107** The Init Envelope MUST carry the session policy (the complete set of permitted tuples, plus `T_MAX`, `N_MAX`, `G`, `X`, and the list of roles) signed by the Session Initiator.
- **RTR-108** The factory MUST reject an Init Envelope whose policy is malformed or whose role list is empty.
- **RTR-109** At instance creation the factory MAY send the signed policy to an external audit destination.
- **RTR-110** A policy change MUST be sent as a signed control message, take effect only from the next epoch, and remain within the roles originally declared (or an explicitly extended set if the factory supports dynamic role addition).

---

## 11. Entity Admission and Extensibility

- **RTR-48** A role is admitted for a session solely by its inclusion in the `roles` list of the Init Envelope and the subsequent successful registration of an entity presenting a valid attestation for that role.
- **RTR-49** A role that has not yet been registered is treated as absent; attempts to address it receive the opaque unreachable result.
- **RTR-50** An entity that cannot hold a session keypair itself MUST participate through an adapter (see Adapters module). An entity with no compliant adapter MUST NOT register.
- **RTR-51** No external component may introduce a transport that bypasses the router for traffic the session is intended to mediate.
- **RTR-52** Components that communicate solely through an owning entity are not themselves entities and need not register.
