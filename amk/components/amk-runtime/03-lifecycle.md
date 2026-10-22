# Lifecycle — Registration, Loading, Inclusion, Removal & Update

**File number:** 4  
**Overview.**  
This module defines the lifecycle of a runtime package from arrival to removal and states exactly who decides at each step. Envelope names are placeholders pending the cross-spec envelope decisions (see RTM-O-02).

---

## States

- **RTM-4:1** A runtime package moves through these states: `ARRIVED → VERIFIED → REGISTERED → LOADED → INCLUDED → RETIRING → REMOVED`. A package may also be `REJECTED` (verification or operator rejection), `WITHDRAWN` (file 6) or `SUSPENDED` (loader fault).
- **RTM-4:2** State is scoped. `ARRIVED`, `VERIFIED` and `REGISTERED` are console-local per operator. `LOADED`, `INCLUDED` and `RETIRING` are scoped to a session and a runtime.

## Registration (install)

- **RTM-4:3** A package MAY arrive by file, link, in-app repository, QR code or paste. The arrival method confers no trust (RTM-1:11).
- **RTM-4:4** Registration is performed by the console. The console MAY reject the package at any failed step.
- **RTM-4:5** Before registering, the console MUST verify the manifest consistency, content digests, signature, contract version and conformance (file 6), and MUST require the operator's fresh confirmation of the package identity and, for third-party packages, the publisher.
- **RTM-4:6** Fresh confirmation for registration is required under every profile (see RTM-O-20).
- **RTM-4:7** System packages are registered in the same way as any other package (file 7).
- **RTM-4:8** Registration is console-local. The console records the package identity and package hash it accepted and uses that record for every later inclusion.

## Session Start With A Runtime

- **RTM-4:9** When a session selects a runtime, the console supplies the controller with the scoped runtime subtree and a package reference (identity and package hash) in a console-signed envelope (see RTM-O-02).
- **RTM-4:10** The loader MUST confirm that the package it is about to load matches the package hash in the console-signed reference. A mismatch MUST abort the load.
- **RTM-4:11** The loader then verifies the package (file 5), loads it, and initializes it. The controller builds the surface as defined in CTR-5:4 to 5:9.
- **RTM-4:12** The runtime is not live until the console has returned a `SurfaceAcceptance` and the handoff has been issued.

## Mid-Session Inclusion

- **RTM-4:13** Inclusion may be requested by the Host AI through the surface or by the operator.
- **RTM-4:14** The console decides inclusion. Where no covering pre-authorization exists, the operator must authorize it (see RTM-O-04).
- **RTM-4:15** After an inclusion decision, the loader loads and initializes the package. The controller produces a new surface revision. No new handoff is issued (CTR-5:10).
- **RTM-4:16** A change to the kernel subtree requires a new session start and is never a mid-session inclusion.

## Removal and Retirement

- **RTM-4:17** The operator may remove a runtime during a session through a console-signed revocation.
- **RTM-4:18** On removal, the loader MUST stop the runtime at the next operation boundary, MUST end in-flight work with the retirement error (RTM-3:20), and MUST release all resources.
- **RTM-4:19** Removal produces a new surface revision. Capability tokens for the runtime end at expiry (CTR-7:7).

## Update

- **RTM-4:20** A new version of a package is a different package (RTM-2:10). It MUST be registered by the operator before it can be included.
- **RTM-4:21** A runtime update to a new version voids pre-authorization coverage for that runtime (CTR-6:8).
- **RTM-4:22** The loader MUST NOT load a version whose status is `WITHDRAWN`.
- **RTM-4:23** A `mandatory` update flag (file 6) never installs a package automatically. It only blocks inclusion of the superseded version after its effective time.

## Operator Authorization Rule

- **RTM-4:24** Every runtime package, system or third-party, requires operator registration through the console and console-authorized inclusion in every session. A covering console-signed pre-authorization MAY authorize that inclusion where the console specification permits (see RTM-O-04).
