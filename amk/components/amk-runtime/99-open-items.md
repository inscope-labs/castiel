# Open Items & Defaults Needed

**File number:** 9  
**Overview.**  
Non-normative list of open questions and the defaults this specification needs. This file contains no normative requirements. "Pending" refers to decision items in the AMK core review files (`X-nn`, `CNS-nn`, `CTR-nn`, `ATA-nn`).

---

## Open Questions

| ID | Item | Depends on | Draft position in this spec |
|---|---|---|---|
| RTM-O-01 | Loader placement: embedded in the controller release behind its own isolation boundary, or a separate fourth component | X-09; AMK is defined as exactly three components | Embedded in the controller release (RTM-5:1, RTM-5:2) |
| RTM-O-02 | Console→controller envelope for runtime subtree and package intake: type name, and whether package bytes are uploaded by the console or fetched by the loader by hash | X-04d | Console-signed reference with package hash (RTM-4:9); upload by hash preferred over fetch, because private repositories are operator-only |
| RTM-O-03 | Execution environment constraints and a platform implementation profile (for example JS/WASM isolates on an edge platform; no native code) | CTR-13 | Platform-agnostic here; implementation profile is a companion document |
| RTM-O-04 | Whether a console-signed pre-authorization may satisfy "authorize inclusion in every session" | CNS-12, CNS-07 | Yes, where the console spec permits (RTM-4:24) |
| RTM-O-05 | Whether inclusion or removal of a system package that scaffolds through the kernel subtree is session-start only | CTR-5:10 | Session-start only (RTM-7:13) |
| RTM-O-06 | Runtime state that persists beyond a session: storage model, scope and ownership | none | Not defined (RTM-3:23) |
| RTM-O-07 | Runtime-to-runtime dependencies | none | Not supported (RTM-2:7) |
| RTM-O-08 | The conformance rule set ("protocol standards"), its content and versioning | none | Applied by console and loader (RTM-6:13, RTM-6:14) |
| RTM-O-09 | Update profile database: location, signer, schema, freshness | none | Signed statements only (RTM-6:17) |
| RTM-O-10 | Publisher trust model: operator pins only, or a publisher PKI; publisher key rotation and compromise handling | X-02 | Operator pins; key change = new publisher (RTM-6:6) |
| RTM-O-11 | Package size limits and the upload envelope size ceiling | X-04 | Values go to the defaults manifest |
| RTM-O-12 | In-band API wire format, transport, invocation timeouts, and the standard error-code catalogue | CTR-14f | Operations defined, wire format deferred (RTM-3:3) |
| RTM-O-13 | Canonical serialization and hash algorithm for the manifest and package hash | X-04 | Shared with the envelope serialization decision (RTM-2:9) |
| RTM-O-14 | Prompt content: delivery format, and whether prompt content is signed separately from the package | none | Prompts are digested in the manifest (RTM-2:4) |
| RTM-O-15 | Repository protocol: listing, retrieval, sharing among operators, installation keys | none | Not defined (RTM-6:12) |
| RTM-O-16 | Whether runtimes receive role attestations from the Attestation Authority | CTR-10, ATA-10 | Not required; controller-issued runtime credential is the current direction |
| RTM-O-17 | Channels beyond HTSM and how the kernel operating level gates them | CTR-O-06 | Declared, level-gated, approved at inclusion (RTM-3:12) |
| RTM-O-18 | `amk-core` specification: module list, first module (host clarification), tests | none | Class rules only here (file 7) |
| RTM-O-19 | Suite versioning and reference-ID alignment with the other specs | X-06, X-08 | Ordinal file numbers, per-bullet IDs, immutable IDs |
| RTM-O-20 | Aligning the console's fresh-confirmation list so runtime registration is included at every profile | CNS-05 | Required at every profile (RTM-4:6) |

---

## Defaults Needed in `amk-defaults-manifest`

No default value is stated in this specification. Each is defined only in the defaults manifest.

| ID | Meaning | Used by |
|---|---|---|
| DV-RTM-01 | Maximum package size | RTM-5:14 |
| DV-RTM-02 | Maximum CPU time per invocation | RTM-5:14 |
| DV-RTM-03 | Maximum memory per runtime context | RTM-5:14 |
| DV-RTM-04 | Maximum outbound calls per invocation | RTM-5:14 |
| DV-RTM-05 | Load and initialize timeout | RTM-5:14 |
| DV-RTM-06 | Retirement grace period for in-flight work | RTM-4:18 |
| DV-RTM-07 | Package cache lifetime | RTM-5:6 |
| DV-RTM-08 | Effective delay before a `mandatory` update blocks the superseded version | RTM-6:16 |

---

## Dependencies

This draft depends on, and should be reconciled with, the AMK core review decisions (files 00 to 03). Companion documents needed: `amk-core` specification, a platform implementation profile for the loader, the update profile database specification, and the conformance rule set.
