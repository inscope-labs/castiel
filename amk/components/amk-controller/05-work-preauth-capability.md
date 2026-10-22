# Work Orders, Pre-Authorization, Capability & Anomaly

**File number:** 6  
**Overview.**  
This module defines the controller’s obligations for work-order enforcement, pre-authorization verification, Host AI capability testing, operating-level calculation, and anomaly-level decisions including Auto Assist.

---

## Work Orders

- **CTR-6:1** A session may hold many work orders, each with its own quota and constraints. The controller enforces them and extends, renews, or cancels them only on a console command.
- **CTR-6:2** Without a valid work order the Host AI may not engage beyond kernel requests.
- **CTR-6:3** A Host-AI-originated work order is a proposal needing console authorization unless a covering pre-authorization exists.

## Pre-Authorization Envelopes

- **CTR-6:4** The controller verifies envelope signature (console key), scope, expiry, runtime and version where relevant, per-session quota, and kernel-level cap before honoring it.
- **CTR-6:5** It honors an envelope only for the scopes it lists.
- **CTR-6:6** Duplicate of CTR-1:18. The requirement is defined only there.
- **CTR-6:7** For offline continuation, envelopes are deposited with the controller. A revocation registry is checked on every use; expiry is the backstop.
- **CTR-6:8** A runtime update to a new version voids coverage for that runtime.

## Capability Verification and Operating Level

- **CTR-6:9** The controller tests Host AI capability. Stated capability is never trusted.
- **CTR-6:10** A test runs once per Host AI profile and is repeated when something changes (model or version change, changed client signature, verification failure, Elevated anomaly, or other defined triggers).
- **CTR-6:11** A new or unverified profile starts at the baseline level.
- **CTR-6:12** Operating level is the lower of the console-allowed level and the verified capability.

## Anomaly Level and Auto Assist

- **CTR-6:13** The controller decides each session’s anomaly level: Normal, Elevated, or High.
- **CTR-6:14** The console sets, with a signed command, the allowed anomaly ceiling and the Auto Assist flag.
- **CTR-6:15** If a check-in is due and the console is unreachable, the controller lets the session continue only if Auto Assist is on, a covering envelope exists, and the anomaly level is at or below the ceiling. It may continue until the envelope expires.
- **CTR-6:16** Every such period is audited.
