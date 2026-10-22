# Runtime Contract — In-Band API, Runtime Map, Channels, UI & Errors

**File number:** 3  
**Overview.**  
This module defines exactly what a runtime is obliged to provide and what it may and may not do. The contract is the same for every runtime. Wire formats and transports are deferred (see RTM-O-12).

---

## Contract Version

- **RTM-3:1** The runtime contract carries a version. A runtime declares the version it implements in its manifest.
- **RTM-3:2** The loader MUST reject a package whose contract version it does not support. It MUST NOT silently downgrade (RTM-1:19).

## In-Band API

- **RTM-3:3** A runtime MUST implement the following operations, invoked only by the controller through the loader:
  - **Describe:** return the runtime's declared identity, version, and operations.
  - **Initialize:** prepare the runtime in a fresh execution context for one session.
  - **Include:** attach the runtime to a session after an inclusion decision.
  - **Invoke:** perform one operation requested through the surface, under a capability token.
  - **Retire:** stop accepting new work and end in-flight work with the defined retirement error.
  - **Detach:** release all session resources.
- **RTM-3:4** Every `Invoke` carries the session handle and the controller-issued capability token (CTR-7:1). The runtime MUST verify the token and MUST refuse the operation if verification fails.
- **RTM-3:5** A runtime MUST NOT be invoked by any party other than the controller through the loader.
- **RTM-3:6** A runtime MUST NOT receive a console key, an operator credential, or a controller key at any point.
- **RTM-3:7** The Host AI never calls the in-band API. It reaches a runtime only through the surface.

## Runtime Map

- **RTM-3:8** The runtime map declares the full proposed surface the runtime could contribute. Each node MUST state its minimum kernel level, its risk class, and the settings, if any, that control its visibility.
- **RTM-3:9** A runtime map MUST NOT contain a kernel-owned path or a console-only operation (CTR-5:2, CTR-4:7).
- **RTM-3:10** The console derives the runtime subtree from the runtime map according to the operator's runtime settings or runtime profile. A subtree MUST be a subset of the map. A runtime MUST NOT expand its own subtree.

## Channels

- **RTM-3:11** A runtime reaches the Host AI only through HTSM, the baseline channel.
- **RTM-3:12** A runtime MAY use an additional channel only if the channel is declared in its manifest, is permitted at the session's kernel operating level, and was approved at inclusion (see CTR-O-06).
- **RTM-3:13** A runtime MUST NOT communicate with the console directly. The console reaches a runtime only through the controller.

## User Interface

- **RTM-3:14** A runtime presents UI to the operator only through its UI manifest, rendered by the console.
- **RTM-3:15** The operator decides which settings reach the Host AI. A runtime MUST NOT transmit a setting to the Host AI that the operator has not allowed in its subtree.
- **RTM-3:16** A runtime MUST NOT open an interface to the operator that bypasses the console.

## Prompts

- **RTM-3:17** Runtime prompts are scaffolding data delivered through the runtime's subtree. They carry no authority.
- **RTM-3:18** The prompts of a system package that scaffolds through the kernel subtree are governed by file 7.

## Errors and Failure Scope

- **RTM-3:19** A runtime MUST report failures using standard error codes defined in the contracts layer (see RTM-O-12).
- **RTM-3:20** The retirement error MUST be used for work in flight when a runtime is removed or retired.
- **RTM-3:21** A runtime failure is scoped to that runtime and that session (CTR-2:7). It MUST NOT halt another runtime or session.

## State

- **RTM-3:22** Runtime state is isolated per runtime and per session. A runtime MUST NOT inherit state or authority from another runtime or session (CTR-7:10).
- **RTM-3:23** Any state a runtime keeps beyond a session is not defined in this version (see RTM-O-06).
