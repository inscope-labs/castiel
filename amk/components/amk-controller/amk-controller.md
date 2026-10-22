# amk-controller — Kernel Enforcement Point Specification

| Field | Value |
|---|---|
| Spec ID | `amk-controller` |
| Version | 2.0.0-draft |
| Suite compatibility | `OS10-AMK 2.x` (suite version defined in `amk-ssot.md`) |
| Status | Draft — self-contained, language- and platform-agnostic, with three operational profiles. |
| Boundary | Kernel Enforcement Point. Sole trusted enforcement, token-issuance, and state authority. |
| Trust | Sole trusted enforcement point. |
| Normative language | MUST / MUST NOT / SHOULD / MAY as in RFC 2119. |

---

## Holistic System Overview

The amk-controller is the sole authoritative enforcement point, token-issuance engine, and state authority. It holds the complete picture of session and epoch state. Principals are consoles identified by cryptographic keys; the controller has no notion of a human operator.

All control-plane interaction with consoles occurs through signed envelopes. The controller verifies console signatures and envelope validity; it does not rely on the internal implementation of any console. Interactions with Host AI channels (HTSM and any additional channels) and with runtimes are defined by protocol contracts. The controller treats external parties as black boxes beyond the verification and protocol obligations stated in this specification.

The specification is language- and platform-agnostic. An implementation may be written in any language and run on any platform that can satisfy the cryptographic, isolation, durability, and sequencing requirements of the claimed operational profile. Higher profiles (especially High) may exclude languages or platforms that cannot provide the required key protection, isolation, or audit strength.

Three operational profiles—Basic, Standard, and High—govern privacy, security, and implementation complexity. Higher profiles subsume all requirements of lower profiles.

Local presentation, user-interface design, and operator-facing summaries are outside the scope of this specification and belong in an implementation guide.

Normative requirements live in the module files listed below.

---

## Core Intent

*Informative overview. The normative module files remain authoritative wherever a requirement is already defined.*

- **Governance becomes enforceable behavior.** The controller is the sole authoritative enforcement point and state authority. Every governed operation passes through the enforcement boundary, and the controller denies when identity, authorization, policy, integrity, or state checks fail. It prevents disallowed operations rather than recommending against them, never delegates the final decision to the Host AI or treats prompt compliance as security, and keeps every decision attributable to policy and state.
- **Evidence is not permission.** A valid request is not an authorized one. A signature, package hash, attestation, capability reference, or a participant's presence, name, or unrelated credentials is evidence for a check, never a grant. The controller keeps requester, console, Host AI client, runtime, package, and target distinct, validates Authority attestations only within their scope, rejects expired, revoked, malformed, untrusted, replayed, or scope-mismatched credentials, and treats integrity as proving only what its procedure covers.
- **Deterministic precedence.** Kernel invariants outrank policy, runtime rules, capability grants, task instructions, and agent suggestions, and lower inputs never relax higher ones. Policy conflicts resolve by an explicit deterministic rule or fail closed, policy configuration stays distinct from untrusted task data, and changes to policy or precedence need the system's authorization and integrity controls.
- **Scoped, bounded capabilities and surfaces.** Capabilities are bound to subject, operation, target, context, and validity, are non-transferable by default, follow a defined lifecycle, never exceed what policy and state permit, and never prove that preconditions still hold. Runtimes, maps, manifests, and adapters cannot self-authorize, governed surfaces change only through the authorized lifecycle, and loading is never permission to use.
- **Authoritative, fail-safe state.** State changes follow a defined state machine with explicit preconditions and postconditions, and a transition is complete only when its effects are confirmed. Stale, contradictory, or corrupt state is never resolved permissively, and session or epoch changes re-evaluate the credentials and approvals they affect. Bootstrap verifies kernel identity, release metadata, integrity, and trust anchors before activation, and unverifiable critical artifacts block activation or force the defined safe state. Failures never become implicit approval, recovery is explicit, bounded, and authorized, and audit evidence explains decisions without exposing secrets.
- **Clear boundaries, stable across profiles.** The console conveys requests and the controller evaluates and enforces them, returning outcomes that distinguish rejection, acceptance, completion, and uncertainty. Host AI output and prompt text stay untrusted. Authority and runtime integrity never remove the operation-specific authorization check, each contract owns its checks and failure responses, and shared code never creates undocumented shared authority. Optional profiles and features cannot weaken invariants, and security-critical requirements are traceable to normative IDs and tests covering escalation, stale credentials, state corruption, replay, policy conflict, malformed inputs, and bypass.

**Essence:** the controller is where governance becomes enforceable behavior: it treats every signature, token, and claim as evidence, decides under fixed precedence, and fails safe rather than guess permissively.

---

## Reference ID Scheme

Every normative statement carries a stable identifier of the form:

**`CTR-<file>:<rule>`**

- `CTR` identifies this specification.
- `<file>` is the module file number (see table below).
- `<rule>` is the rule number inside that file. Each file begins numbering at 1.

Once published, an ID is never reassigned. A withdrawn requirement keeps its ID and is marked `RETIRED`. File numbers are stable identifiers and need not follow file-name order.

---

## Module Index & File Numbers

| File # | File | Scope |
|--------|------|-------|
| 1 | [00-foundations.md](00-foundations.md) | Role, trust, authority, invariants |
| 2 | [01-bootstrap-state.md](01-bootstrap-state.md) | Bootstrap, state model, lifecycle |
| 3 | [02-envelope-interface.md](02-envelope-interface.md) | Envelope validation and catalogue |
| 4 | [03-console-identity.md](03-console-identity.md) | Console identity and administration |
| 5 | [04-surface-runtime.md](04-surface-runtime.md) | Surface construction, runtime intake, HTSM |
| 6 | [05-work-preauth-capability.md](05-work-preauth-capability.md) | Work orders, pre-authorization, capability, anomaly |
| 7 | [06-tokens-audit-revocation.md](06-tokens-audit-revocation.md) | Capability tokens, audit, revocation, recovery |
| 8 | [07-profiles.md](07-profiles.md) | Basic / Standard / High profile requirements |
| 9 | [99-open-items.md](99-open-items.md) | Open questions (non-normative) |
| 10 | [08-keys.md](08-keys.md) | Controller key hierarchy |

---

## Operational Profiles (Summary)

| Profile | Target | Key Protection | Isolation | Durability & Audit | Language / Platform |
|---|---|---|---|---|---|
| **Basic** | Hobby / educational / prototypes | Software keys permitted | Soft isolation acceptable | Minimal durable state | Any language/platform that meets basic crypto |
| **Standard** | Production services | Non-exportable keys; OS keystore or equivalent | Process / container isolation | Full durable state + signed audit chain | Languages/platforms with mature isolation & crypto |
| **High** | Enterprise / regulated / high-assurance | HSM / TEE; keys never in clear process memory | Strong isolation (TEE or equivalent) | Hardware-protected audit + remote attestation | Only languages/platforms that can meet TEE / HSM / measured-boot requirements |

Detailed obligations are defined in file 8. Higher profiles may exclude languages or platforms that cannot satisfy the required isolation, key protection, or audit strength.

---

## Errors, inconsistencies and critical deficiencies (cursory)

*Cursory pass only; a complete scan follows. It covered every module file of this specification at a skim level and did not cross-check against `amk-authority`, `amk-console` (beyond shared open items) or `session-router`. IDs (`E-CTR-nn`) are provisional. **BLOCKING** means the item must be resolved before this specification can be released at the stated profile. Items already tracked as `CTR-O-nn` in `99-open-items.md` are not repeated unless their blocking status is itself inconsistent; that file currently contains no blocking classification at all.*

### BASIC

- **E-CTR-01 (BLOCKING):** Each runtime must have an isolated execution context and independent authority with no profile qualifier (`CTR-7:10`), and the Host AI and runtimes are untrusted (`CTR-1:6`, `CTR-1:7`), yet Basic accepts "soft isolation" (`CTR-8:7`), which is never defined. As written, either `CTR-7:10` is not enforceable at Basic or Basic is non-conformant. Decide the minimum isolation Basic must keep between runtimes, and from the Host AI.
- **E-CTR-02 (non-blocking):** Basic relaxations are undefined and collide with rules that apply at every profile (`CTR-8:5`): "simplified" sequencing and replay protection (`CTR-8:8`, `CTR-3:5`; tracked only by `CTR-O-08`) versus the unconditional nonce rule (`CTR-3:4`), and "minimal durable state" (`CTR-2:14`, `CTR-8:9`) versus the unconditional durability and single-writer rules (`CTR-2:12`, `CTR-2:13`). "Simpler recovery" (`CTR-7:12`) is also undefined.

### STANDARD

- **E-CTR-03 (BLOCKING):** The controller has no normative obligation to verify Authority attestations, which Core Intent requires (validate before relying, only within scope). This specification only pins Authority URLs (`CTR-10:10`), and the verification rules in `amk-authority` (`ATA-03`) address "clients" without naming the controller. Revocation-list age checks and failure behavior are therefore unassigned. Also affects HIGH.
- **E-CTR-04 (BLOCKING):** Policy evaluation cannot be tested: risk classes, kernel policy, capability policy, and the rule mapping an operation to a decision are referenced (`CTR-1:11`, `CTR-1:12`, `CTR-5:2`) but never defined, and the capability tests and kernel-level matrix are open (`CTR-O-05`). Enforcement decisions cannot be shown to be attributable to a policy. Also affects HIGH.
- **E-CTR-05 (BLOCKING):** The capability-token lifecycle is incomplete. "Short-lived" has no value (`CTR-7:1`), validation, renewal, and expiry rules are absent, and only pre-authorizations have a revocation registry (`CTR-7:8`), so tokens cannot be revoked before expiry (`CTR-7:7`). Compromise of the Token Signing Key is contained only against forging envelopes and audit entries (`CTR-10:9`). The token's recipient is "authorized party" (file 3 table), and `CapabilityToken` has no behavioural rules (`CTR-O-15`). Also affects HIGH.
- **E-CTR-06 (BLOCKING):** Several Standard MUSTs cannot be tested as written: the required recovery protocols do not exist (`CTR-7:12`, `CTR-O-07`); skew windows, nonce lifetime, and sequence storage are undefined (`CTR-O-08`); the durable-state set is undefined (`CTR-O-02`); envelope schemas are undefined (`CTR-O-01`); and console key enrollment has no procedure (`CTR-4:5`, `CTR-O-03`), although signatures are verified against "registered" console keys (`CTR-3:2`). Key distribution and rotation (`CTR-O-16`) are also open. `CTR-O-01`, `O-02`, `O-03`, `O-07`, `O-08` and `O-16` need a blocking classification. Also affects HIGH.
- **E-CTR-07 (non-blocking):** Auto Assist continuation (`CTR-6:15`) depends on "check-in due" and "console unreachable", which have no definition or timeout (`CheckIn` is open, `CTR-O-14`), so an induced outage could start Auto Assist periods (bounded by the envelope). Anomaly criteria, the baseline level, and "other defined triggers" for capability re-tests (`CTR-6:10`, `CTR-6:11`, `CTR-6:13`) are also undefined.
- **E-CTR-08 (non-blocking):** Core Intent has the controller validating identity, provenance, and integrity of each registered component, but this specification delegates registration to the console and accepts a validated runtime subtree as authoritative while provenance binding is open (`CTR-5:3`, `CTR-O-04`). Decision needed: add a controller obligation or amend the intent.

### HIGH

- **E-CTR-09 (BLOCKING):** High cannot be verified. Remote attestation is only SHOULD (`CTR-8:18`) although the summary table and overview promise it, profile discovery (`CTR-8:2`) relies on `StatusResponse`, which has no behavioural rules (`CTR-O-15`), and the peer rule (`CTR-8:22`) trusts that self-declared profile.
- **E-CTR-10 (BLOCKING):** A hardware-protected, tamper-resistant audit trail is a MUST (`CTR-8:19`), but audit entry format, retention, and checkpoint protection (`CTR-7:4` to `CTR-7:6`) are not defined, and no open item tracks them.
- **E-CTR-11 (non-blocking):** `CTR-8:20` says side-channel resistance and high-assurance practices are "expected", which is not RFC 2119 language and is untestable.

### ALL PROFILES

- **E-CTR-12 (BLOCKING):** The lifecycle state machine required by Core Intent is missing. `CTR-2:3` defines only the bootstrap states (ABSENT, LOADING, VERIFYING, READY), and session states such as UNREGISTERED, REGISTERED, ACTIVE or INERT, and INVALIDATED are not defined as states with preconditions and postconditions. SAFE-HALT appears only as a failure condition (`CTR-2:8`): its entry actions and authorized exit are unspecified, although `CTR-1:15` depends on it.
- **E-CTR-13 (non-blocking):** "The controller changes lifecycle only by restricting" (`CTR-2:10`) conflicts with permissive moves the controller makes itself: reaching READY (`CTR-2:3`), raising the operating level after a passed capability test (`CTR-6:10` to `CTR-6:12`), and lowering the anomaly level (`CTR-6:13`). Clarify that "lifecycle" excludes these, or state them as exceptions.
- **E-CTR-14 (non-blocking):** The "standard error code" on bootstrap failure (`CTR-2:4`) is undefined, and there is no outcome taxonomy that lets the console distinguish rejection, acceptance, completion, and uncertainty, or that separates recoverable faults, integrity failures, and authorization denials.
- **E-CTR-15 (non-blocking):** `CTR-2:11`, `CTR-6:6`, `CTR-7:3` and `CTR-7:9` are "Duplicate of ..." stubs rather than `RETIRED`, and `CTR-7:9` sits under Revocation. "Conforming adapters" are trusted (`CTR-1:5`) but never defined. No rule says session or epoch changes invalidate or re-evaluate credentials and approvals (see `CORE-O-01`), and `amk-test-matrix` is not yet updated for traceability.
