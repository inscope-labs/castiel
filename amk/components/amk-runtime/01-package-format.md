# Package Format — Structure, Manifest, Identity, Versioning & Signatures

**File number:** 2  
**Overview.**  
This module defines what a runtime package contains and how it is identified, versioned and signed. It is the only place package structure is defined. Concrete serialization and hash algorithms are deferred to the shared envelope serialization decision (see RTM-O-13).

---

## Package Contents

- **RTM-2:1** A runtime package MUST contain exactly one manifest and the following content parts:
  - **Prompts:** the scaffolding text delivered to the Host AI through the runtime's subtree.
  - **In-band API descriptor:** the operations the runtime implements (file 3) and its executable code.
  - **Runtime map:** the full proposed surface map.
  - **UI manifest:** a zip of declarative UI definitions. It MUST provide at least an "about" view and a "settings" view.
  - **Settings schema:** the settings the operator may change, and which settings influence the subtree.
- **RTM-2:2** A package MUST NOT contain a user interface that runs outside the console's rendering of the UI manifest.
- **RTM-2:3** A package MUST NOT contain keys, credentials or operator-specific data.

## Manifest

- **RTM-2:4** The manifest MUST declare:
  - `package_id` and `version`,
  - `class` (`system` or `third-party`),
  - `publisher_id` (third-party) or the Release identity (system),
  - `contract_version` (the runtime contract version it implements),
  - `min_kernel_level` and the highest risk class of any operation it exposes (see CTR-O-13),
  - declared channels beyond HTSM, if any,
  - declared egress destinations, if any,
  - resource requests (CPU time, memory, size),
  - a digest of every content part.
- **RTM-2:5** Anything not declared in the manifest MUST be treated as not permitted.
- **RTM-2:6** The manifest MUST be self-consistent: every content part present is digested, and every digest refers to a present part.
- **RTM-2:7** A package MUST NOT declare a dependency on another runtime's authority or state. Runtime-to-runtime dependencies are not supported in this version (see RTM-O-07).

## Identity and Versioning

- **RTM-2:8** A package is identified by the pair (`package_id`, `version`) and by its package hash.
- **RTM-2:9** The package hash is computed over the canonical manifest, which includes the digests of every content part.
- **RTM-2:10** A published (`package_id`, `version`) is immutable. Any change to any content part MUST produce a new version and a new package hash.
- **RTM-2:11** `package_id` MUST be unique per publisher. The globally unique identity of a package is (`publisher_id`, `package_id`).

## Signatures

- **RTM-2:12** Every package MUST carry a signature over the canonical manifest.
- **RTM-2:13** Third-party packages MUST be signed by the publisher's key.
- **RTM-2:14** System packages MUST be signed by the Release Key and MUST be listed in the Release Manifest by identity and package hash (file 7).
- **RTM-2:15** The signature algorithm MUST be identifiable from the package or from published publisher metadata. Verifiers MUST reject an unknown or unsupported algorithm.
- **RTM-2:16** A package whose signature, manifest consistency or content digests fail verification MUST be rejected.

## Update Metadata

- **RTM-2:17** A package MAY carry update metadata identifying the publisher's update channel. Update status (current, advisory, mandatory, withdrawn) is governed by file 6 and is not part of the signed package hash.
