# Controller Key Hierarchy

**File number:** 10  
**Overview.**  
This module defines the key roles held or verified by the controller and the trust relationships that anchor them. Key protection strength per profile is defined in file 8 and is not repeated here. Items not yet decided are listed in file 9 (see CTR-O-16).

---

## Key Roles

- **CTR-10:1** The controller distinguishes three key roles: the Release Key, the Controller Signing Key, and the Token Signing Key.
- **CTR-10:2** A key MUST NOT serve more than one role.

## Release Key

- **CTR-10:3** The Release Key is used to sign the Release Manifest. The controller holds and uses only its verification key(s). The private key MUST NOT be present on the controller.
- **CTR-10:4** The controller MUST verify the Release Manifest against the Release Key before accepting any connection (CTR-2:1, CTR-2:6).
- **CTR-10:5** Trust in the administrative channel (CTR-3:12) is rooted in the Release Key.

## Controller Signing Key

- **CTR-10:6** The Controller Signing Key signs controller-originated envelopes (including `SurfaceProposal`), audit entries, and checkpoints (CTR-1:3, CTR-7:4).
- **CTR-10:7** The Controller Signing Key MUST NOT sign capability tokens.

## Token Signing Key

- **CTR-10:8** The Token Signing Key signs capability tokens only (CTR-7:1).
- **CTR-10:9** A compromise of the Token Signing Key MUST NOT enable forging of envelopes, audit entries or checkpoints.

## Console Pins

- **CTR-10:10** A console build pins the Release Key fingerprint(s), the list of controller URLs, and the list of Authority URLs (CNS-2:12). The controller is administered out of band and consoles are principals only (CTR-4:2).
