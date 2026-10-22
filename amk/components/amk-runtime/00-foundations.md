# Foundations — Terms, Role, Authority Limits, Trust & Invariants

**File number:** 1  
**Overview.**  
This module defines the core terminology, the role of amk-runtime as package authority and loader, the explicit limits of that authority, the trust boundary, and the absolute invariants. All subsequent modules presuppose these definitions.

---

## Terms

| Term | Meaning |
|---|---|
| Runtime | A package-delivered unit of capability that extends the kernel. It has no authority of its own. |
| Runtime package | The signed, versioned artefact that delivers a runtime (file 2). |
| Package class | `system` (shipped with a release, Release-signed) or `third-party` (publisher-signed). |
| Package manifest | The signed description of a package: identity, version, class, contract version, declarations. |
| Runtime map | The package's full proposed surface map: every node the runtime could contribute to the Host Traversal Surface Map (HTSM). |
| Runtime subtree | The console-scoped derivation of a runtime map for a given operator, runtime settings and profile. |
| In-band API | The interface through which the controller invokes a loaded runtime (file 3). |
| UI manifest | A zip of declarative UI definitions the console renders on the runtime's behalf. |
| Loader | The component that verifies a package and places its code into an isolated execution context. |
| Package authority | The role of establishing package identity, provenance and conformance. |
| Publisher | The party whose key signs a third-party package. |
| Registration | The console-side act of installing a package after verification and operator confirmation. |
| Inclusion | The operator-authorized addition of a registered runtime to a session. |
| Retire | To end in-flight work for a runtime with a defined error code before removal. |
| Kernel subtree | The part of the surface scaffolded by the kernel with no runtime. |
| Surface | The Host AI traversal surface (HTSM) built for a session. |
| Core runtime | A runtime available in every AMK release. |
| `amk-core` | The bundled group of core runtime capabilities, loaded first (file 7). |

---

## Role

- **RTM-1:1** amk-runtime is the sole defined authority over the identity, provenance, conformance and lifecycle of runtime packages, including system packages.
- **RTM-1:2** amk-runtime is the loader: package code MUST enter execution only through the loader.
- **RTM-1:3** A runtime is a unit of capability that extends the kernel. It holds no authority of its own and cannot widen any authority granted to it.

## Authority Limits

- **RTM-1:4** amk-runtime does not authorize. Authority to register a package and to include it in a session rests solely with the operator, expressed through console-signed envelopes.
- **RTM-1:5** amk-runtime does not enforce. Enforcement, capability-token issuance and session state belong to the controller.
- **RTM-1:6** amk-runtime does not issue role attestations. That belongs to the Attestation Authority.
- **RTM-1:7** System packages, including `amk-core`, have the same authority as any other runtime. Their class affects provenance and load order only.

## Trust Boundary

- **RTM-1:8** Trusted: the Release Key (for system packages and the Release Manifest), console keys (for operator intent only), and the loader's own verification logic (subject to the claimed profile).
- **RTM-1:9** Trusted only for what they sign, and only after operator registration: publishers of third-party packages.
- **RTM-1:10** Untrusted: runtime code, package repositories and transports, the Host AI, and unauthenticated parties.
- **RTM-1:11** Repositories are untrusted transport. Authority derives from signatures and operator registration, never from where a package was obtained.

## Invariants

- **RTM-1:12** No implicit authority. A package is never loaded, registered or included because of its presence, its class, its name or its repository.
- **RTM-1:13** Package code is never executed before its signature, hash and contract version have been verified.
- **RTM-1:14** A package is never loaded into a session without a console-signed inclusion decision (or a covering console-signed pre-authorization, see RTM-O-04).
- **RTM-1:15** A runtime never receives console keys, operator credentials, controller keys or another runtime's state.
- **RTM-1:16** A runtime MUST NOT weaken or alter kernel boundaries (CTR-1:12).
- **RTM-1:17** Any verification failure fails closed and is audited.
- **RTM-1:18** No runtime provides an external user interface. Every runtime UI is administered by the console.
- **RTM-1:19** No silent downgrades of contract, package or runtime versions.

**RTM-1:20** An implementation that violates any invariant listed above is non-conformant.
