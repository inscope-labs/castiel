# Runtimes, Work Orders, Pre-Authorization & Auto Assist

**File number:** 5  
**Overview.**  
This module defines the envelope contracts for runtime registration, work-order management, pre-authorization envelopes, and Auto Assist behaviour. All interactions are envelope-based; counterparts are treated as black boxes.

---

## Runtime Registration

- **CNS-5:1** RETIRED. Replaced by CNS-5:13.
- **CNS-5:2** The console does not interpret the internal semantics of a runtime beyond the fields required by the envelope schema.

## Work Orders

- **CNS-5:3** Work orders are created, extended, renewed, or cancelled by emitting the corresponding `WorkOrder` or `WorkOrderUpdate` envelopes.
- **CNS-5:4** Each work order carries its own quota and constraint fields.
- **CNS-5:5** The console treats the controller’s acceptance or rejection as authoritative.

## Pre-Authorization Envelopes

- **CNS-5:6** A pre-authorization is a reusable, console-signed envelope that authorizes a named scope up to stated limits (expiry, quota, level cap, runtime version, etc.).
- **CNS-5:7** Creation or modification of a pre-authorization MUST require a fresh confirmation under the Standard and High profiles.
- **CNS-5:8** The console deposits the signed pre-authorization with the controller via a `PreAuthorization` envelope.
- **CNS-5:9** A covering pre-authorization allows the console to emit certain acceptance envelopes without additional confirmation, subject to the limits recorded in the pre-authorization.
- **CNS-5:10** Revocation of a pre-authorization is performed by emitting a `Revocation` envelope.

## Auto Assist

- **CNS-5:11** Auto Assist is expressed as a policy flag carried in session-related envelopes or as a standing pre-authorization scope.
- **CNS-5:12** When the console is unreachable, continuation of a session is governed solely by the limits of an applicable pre-authorization and the information supplied by the controller.
- **CNS-5:13** Runtime registration is an exclusive console workflow. It is console-local and involves no envelope.
