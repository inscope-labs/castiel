# amk-ssot — Operating System 10 (OS/10) Framework Overview

| Field | Value |
|---|---|
| Spec ID | `amk-ssot` |
| Suite version | `OS10-AMK 2.0-draft` |
| Status | Draft |
| Scope | The five core AMK components only: `amk-authority`, `amk-console`, `amk-controller`, `amk-prompt`, `amk-runtime`. No other specification is referenced. |

Every row below is a single statement with exactly one rule reference. A statement without a reference is invalid. Rows marked `PENDING` await the specification named in the row.

## Suite Rules

- **SSOT-1:1** The suite version is `OS10-AMK 2.0-draft`.
- **SSOT-1:2** Each core specification declares the suite versions with which it is compatible.
- **SSOT-1:3** The `contract_version` carried in every envelope is the suite major.minor.
- **SSOT-1:4** The AMK consists of five core components: amk-authority, amk-console, amk-controller, amk-prompt, and amk-runtime.

## Overview

| Ref | Statement |
|---|---|
| ATA-00:01 | The Attestation Authority is the sole issuer of role attestations. |
| ATA-00:02 | The Authority is trusted for the statements it signs and untrusted for enforcement. |
| ATA-06:07 | A party does not accept a peer that declares a lower profile than its own unless explicitly allowed and audited. |
| CNS-1:1 | The console is the sole seat of operator authority. |
| CNS-1:2 | The controller has no independent notion of an operator. |
| CNS-1:5 | The console is untrusted for enforcement. |
| CNS-1:9 | No action that affects system state is implicit. |
| CNS-3:19 | The console and controller communicate over an administrative channel and a session channel. |
| CNS-3:21 | Delivery of the handoff to a Host AI is the only transport that is not an envelope exchange. |
| CTR-1:1 | The controller is the sole enforcement point, token-issuance engine and state authority. |
| CTR-1:4 | The controller has no notion of a human operator. |
| CTR-1:7 | The Host AI and prompt layer are untrusted for enforcement and authorization. |
| CTR-1:9 | Authority is never inferred from presence, context, prompt content or authentication alone. |
| CTR-1:16 | The controller fails closed on any failure condition. |
| CTR-1:18 | The controller never creates or widens a pre-authorization envelope. |
| CTR-1:19 | The Host AI never receives a capability token. |
| CTR-10:1 | The controller distinguishes the Release Key, the Controller Signing Key and the Token Signing Key. |
| CNS-7:1 | Every console implementation declares exactly one profile: basic, standard or high. |
| CTR-8:1 | Every controller implementation declares exactly one profile: basic, standard or high. |
| PENDING (`amk-prompt`) | The Host AI Kernel Prompt statements are added when the specification is uploaded to `specs/core/amk-prompt`. |
| PENDING (`amk-runtime`) | The runtime statements are added when the specification is added to `specs/core/amk-runtime`. |
