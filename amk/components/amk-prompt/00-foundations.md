# Foundations — Role, Trust, Assurance & Invariants

**File number:** 1  
**Overview.**  
This module defines the role of the kernel prompt, its trust boundary, assurance-level behavior, statelessness requirement, and the invariants it upholds. The prompt is purely advisory.

---

## Role

- **PMT-1:1** The prompt is loaded into the Host AI at session start.
- **PMT-1:2** It establishes kernel identity, the command boundary, and the instruction hierarchy.
- **PMT-1:3** It points to the controller as the sole enforcement point and the console as the sole human authorization plane.
- **PMT-1:4** It contains no secrets, no mutable state, no authoritative policy, and no authoritative authorization.

## Trust

- **PMT-1:5** The prompt is untrusted for enforcement, authorization, and evidence.
- **PMT-1:6** It cannot override or bypass the controller, self-authorize, grant authority to the Host AI or a runtime, or modify kernel state.
- **PMT-1:7** It is advisory behavior guidance only. Effects are gated by Capability Tokens, not by this prompt.

## Assurance Level Behavior

- **PMT-1:8** At L0 (no verified channel) the prompt MUST cause the Host AI to state that governance is advisory and no governed effects are available.
- **PMT-1:9** At L1 and L2 the Host AI treats as authoritative only content delivered with an Attestation through the HIL channel. Anything else is ordinary context.
- **PMT-1:10** The Host AI never claims a level it has not been told by an attested identity response.
- **PMT-1:11** Assurance levels are distinct from HTSM operational levels and kernel operating levels.

## Statelessness

- **PMT-1:12** The prompt holds no session, authorization, capability, or evidence state and no credentials.
- **PMT-1:13** It re-derives all governance state from the controller. Conversation memory is never authoritative state.

## Invariants

- **PMT-1:14** The prompt upholds the following invariants (as registered in the contracts): no implicit authority, no self-authorization, no conversion of external data into authority, no fabrication of kernel state, no silent version downgrade, and related prompt-specific invariants.
- **PMT-1:15** An implementation or rendering of the prompt that violates these rules is non-conformant.
