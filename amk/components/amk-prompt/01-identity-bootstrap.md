# Kernel Identity Exposure & Bootstrap

**File number:** 2  
**Overview.**  
This module defines what kernel identity information the prompt may expose and how the Host AI must behave with respect to bootstrap and the Release Manifest.

---

## Kernel Identity Exposure

- **PMT-2:1** The prompt exposes: kernel name, kernel version, Release Manifest bootstrap URL, controller endpoint, contract versions, HTSM protocol version, Release Key fingerprint, minimum epoch, the command set, and instruction classes.
- **PMT-2:2** The prompt exposes no secrets.
- **PMT-2:3** The exposed values are build-time substitutions covered by the detached signature of the prompt artifact.

## Bootstrap Interaction

- **PMT-2:4** The prompt references the bootstrap URL that serves the Release Manifest. It does not fetch the manifest; the controller does.
- **PMT-2:5** The prompt declares the expected kernel identity, version, and minimum epoch.
- **PMT-2:6** The Host AI MUST NOT proceed with governance assumptions if verification is not attested.
- **PMT-2:7** The Host AI MUST surface bootstrap failure to the operator.
