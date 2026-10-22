# Bootstrap, State Model & Lifecycle

**File number:** 2  
**Overview.**  
This module defines bootstrap from the Release Manifest, the nested state model, and lifecycle transitions. Concrete durable-storage technology is left to the implementation; only the required durability and single-writer properties are normative. Profile strength governs how strongly these properties must be enforced.

---

## Bootstrap

- **CTR-2:1** The controller MUST fetch and verify the Release-signed Release Manifest from the designated bootstrap location against the Release Key fingerprint and anti-rollback epoch rules.
- **CTR-2:2** The Release Manifest MUST identify the HTSM protocol version, a hash of the kernel subtree definition, and the release’s required-items list or its hash.
- **CTR-2:3** Lifecycle state moves through ABSENT → LOADING → VERIFYING → READY.
- **CTR-2:4** On bootstrap failure the controller MUST notify the administrator (out of band) and answer consoles with a standard error code.
- **CTR-2:5** After the Release Manifest verifies, the controller is idle and waits for connections.
- **CTR-2:6** The controller MUST enforce strict bootstrap readiness before accepting any connection or command.

## State Model

- **CTR-2:7** State is nested and scoped. Release and deployment state are global; everything else is scoped to a session, surface, subtree, proposal, or runtime so that one failure does not halt another party.
- **CTR-2:8** Failure conditions include INTEGRITY-FAILED, CONTRACT-FAILED, FAULTED, and SAFE-HALT, with health NORMAL or DEGRADED. BLOCKED and AUTHORIZATION-FAILED are scoped conditions.
- **CTR-2:9** Each session carries an anomaly level (see file 6).
- **CTR-2:10** The controller changes lifecycle only by restricting. Permissive transitions require console authority.
- **CTR-2:11** Duplicate of CTR-1:16. The requirement is defined only there.

## Durability and Concurrency

- **CTR-2:12** Session and epoch state MUST be held in durable storage that supports point-in-time recovery (or an equivalent durability guarantee required by the claimed profile).
- **CTR-2:13** Concurrent requests for a given session MUST be serialized with a single writer.
- **CTR-2:14** Under Standard and High profiles, instance and session state MUST survive process restart according to the durability guarantees of the claimed profile. The Basic profile MAY relax persistence for experimentation.
