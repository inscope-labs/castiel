# Foundations — Role, Trust, Authority & Invariants

**File number:** 1  
**Overview.**  
This module defines the controller’s role as the sole enforcement and state authority, the trust boundary, the authority model, and the absolute invariants. The specification is language- and platform-agnostic; profile requirements may exclude languages or platforms that cannot meet the stated isolation and key-protection strength.

---

## Role

- **CTR-1:1** The controller is the sole authoritative enforcement point, token-issuance engine, and state authority. It holds the complete picture of state.
- **CTR-1:2** It verifies the Release Manifest, authenticates runtimes, validates request envelopes, builds and serves surface maps, and runs the baseline Host AI channel protocol (HTSM).
- **CTR-1:3** It emits cryptographically signed responses, capability tokens, audit entries, and checkpoints.
- **CTR-1:4** The controller has no notion of a human operator. Its principals are consoles identified by their keys. One controller MAY serve many consoles.

## Trust Boundary

- **CTR-1:5** Trusted: Release Key holders, console keys (for intent), conforming adapters, and the platform on which the controller itself runs (subject to the claimed profile).
- **CTR-1:6** Untrusted: the Host AI, runtimes, unauthenticated parties, and external network data. The console is trusted only for authenticated operator intent.
- **CTR-1:7** The Host AI and prompt layer are entirely untrusted for enforcement or authorization.
- **CTR-1:8** The controller and console do not trust each other blindly: each verifies the other’s signatures and responses.

## Authority Model

- **CTR-1:9** No implicit authority. Authority is never inferred from presence, context, prompt content, or authentication alone.
- **CTR-1:10** Identity authentication, capability authorization, runtime execution, and task completion remain separate.
- **CTR-1:11** Layered policy precedence: immutable invariants, kernel policy, runtime contract, capability policy, task policy, agent request. Deny beats require-confirmation beats allow.
- **CTR-1:12** Risk classes are evaluated; runtime policies MUST NOT weaken kernel boundaries.
- **CTR-1:13** The release policy defines the required items the controller may add to a surface on its own. It MUST NOT add anything else.

## Invariants

- **CTR-1:14** No action occurs without cryptographic verification, valid tokens (where required), and explicit authorization.
- **CTR-1:15** A failed integrity check triggers safe-halt and is never bypassed.
- **CTR-1:16** Fail-closed on any failure condition.
- **CTR-1:17** No silent downgrades of protocol, contract, or capability versions.
- **CTR-1:18** The controller never creates or widens a pre-authorization envelope.
- **CTR-1:19** The Host AI never receives a capability token; it learns only outcomes.
- **CTR-1:20** An implementation that violates any invariant is non-conformant.
