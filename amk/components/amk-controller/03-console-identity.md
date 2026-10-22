# Console Identity & Administration

**File number:** 4  
**Overview.**  
This module defines how consoles are identified, how their signatures are verified, and the separation between console session authority and out-of-band controller administration.

---

## Console Identity

- **CTR-4:1** Principals are consoles identified by registered keys. The controller has no operator concept.
- **CTR-4:2** No console administers the controller. An authenticated administrator does so out of band.
- **CTR-4:3** Consoles administer their own sessions through the controller.
- **CTR-4:4** The controller MUST verify console signatures on genesis, turn receipts, surface approvals, pre-authorization envelopes, and other console-originated envelopes (console key), and on surface maps (map key when a distinct map key is used).
- **CTR-4:5** Enrollment of a console’s keys with the controller is performed out of band or through a defined bootstrap procedure (currently an open item).

## Administration Separation

- **CTR-4:6** Administrative operations on the controller itself use explicit multi-phase verification and two-phase commit for destructive or irreversible actions.
- **CTR-4:7** Console-only operations (session start, surface approval, authorization, denial, revocation, runtime registration support, pre-authorization management, level changes, recovery) have no kernel-subtree node and MUST be rejected from any non-console principal.
