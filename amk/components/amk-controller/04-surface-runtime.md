# Surface Construction, Runtime Intake & HTSM

**File number:** 5  
**Overview.**  
This module defines how the controller constructs and proposes surfaces, intakes runtime subtrees, and serves the baseline Host AI channel (HTSM). Additional channels may exist according to the kernel operating level; their definition is left to companion specifications.

---

## Runtime Subtree Intake

- **CTR-5:1** The controller receives a console-scoped runtime subtree only when a session selects the runtime or an inclusion is approved.
- **CTR-5:2** It MUST validate the subtree against kernel policy and size limits, and MUST reject any kernel-owned path, console-only operation, or minimum level lower than the risk class allows.
- **CTR-5:3** Provenance binding between a provider-signed runtime map and the console-derived subtree remains an open item; until defined, the controller treats a successfully validated subtree as authoritative for that session.

## Surface Construction

- **CTR-5:4** On session start the controller receives session information and the execution profile (work orders, scoped runtime subtrees, context assets).
- **CTR-5:5** It inspects the work orders and context, mounts the context, and builds the proposed surface from the kernel subtree, the scoped runtime subtrees, and policy-required items.
- **CTR-5:6** The controller MAY add or remove items according to policy, but on its own it MAY add only items the release policy requires.
- **CTR-5:7** It returns a `SurfaceProposal` envelope to the console. The surface is not live until the console returns a `SurfaceAcceptance` signed with the appropriate key.
- **CTR-5:8** After acceptance the controller creates the start and next endpoints and returns only a `Handoff` envelope, with genesis at 0.
- **CTR-5:9** The genesis anchor binds the approved surface.
- **CTR-5:10** Mid-session inclusion and removal produce a new surface revision; the chain and session continue and no new handoff is issued. A change to the kernel subtree requires a new session start.

## HTSM Service

- **CTR-5:11** HTSM is the baseline Host AI channel. It is not the only channel; runtimes MAY introduce other channels according to the kernel operating level.
- **CTR-5:12** The controller applies the HTSM verification order, continuation rules, fork and chain handling, console turns, and generations as defined in the HTSM companion units. This specification does not restate them.
- **CTR-5:13** A handoff is reusable until expiry only for the same session identity; an unused handoff expires. A different identity is a fork.
- **CTR-5:14** Session identity is the Host AI client fingerprint set at first use plus the delivery gateway when one was used.
