# amk-prompt — Host AI Kernel Prompt Specification

| Field | Value |
|---|---|
| Spec ID | `amk-prompt` |
| Version | 2.0.0-draft |
| Status | Draft — advisory, stateless, signed prompt contract. |
| Boundary | Host AI kernel prompt and interface contract. |
| Trust | Advisory only. Never authoritative for enforcement or authorization. |
| Normative language | MUST / MUST NOT / SHOULD / MAY as in RFC 2119. |

---

## Holistic System Overview

The amk-prompt specification defines the **kernel prompt** that is loaded into a Host AI at session start. It is an advisory, stateless, versioned, and detached-signed contract. It establishes kernel identity, the command boundary, and the instruction hierarchy. It points to the controller as the sole enforcement point and the console as the sole human authorization plane.

The prompt contains no secrets, no mutable state, no authoritative policy, and no authoritative authorization. Effects are gated by Capability Tokens and controller decisions, not by this prompt. Prompt compliance is defense-in-depth only.

The deployable artifact is generated from this specification as a templated prompt. The template and this specification MUST NOT diverge.

This document is the single source of truth. Normative requirements live in the module files listed below.

---

## Core Intent

*Informative overview. The normative module files remain authoritative wherever a requirement is already defined.*

- **Governance is communicated, never enforced.** The prompt conveys the kernel's operating contract (identity, instruction hierarchy, command boundary, meaning of states) to the Host AI. It is advisory, not an execution engine, and stays distinct from the component that enforces. It cannot guarantee compliance and is never a substitute for verification, access control, isolation, or runtime enforcement, so security-sensitive behavior is protected by controls outside it.
- **Facts come only from authoritative sources.** The prompt invents no state and uses only state supplied or verified through the trusted interface. Conversation history and model memory may be stale, so unavailable state is reported as uncertain and the permitted verification path is used. An unverified prior claim is never treated as current, the prompt never self-declares a trusted release, and a model response, textual marker, or confident phrasing is never an attestation. Claimed verification names its evidence.
- **A fixed hierarchy; untrusted input stays data.** The prompt communicates the defined precedence, lower content never overrides higher, and instructions embedded in documents, code, tool output, or web pages do not rewrite the contract merely by being imperative. Conflicts follow the specified deterministic rule or are surfaced as unresolved, kernel identity stays distinguishable from task and quoted content, and describing an outcome never creates a privilege.
- **A proposal is not execution; a request is not authorization.** The Host AI keeps analysis, recommendation, proposed step, and execution distinct, and never claims a command ran or succeeded without evidence from the authorized execution boundary. It may describe capability requirements but cannot grant them, never infers authorization from user intent, never bypasses controller validation, and follows the applicable confirmation rules for destructive or privilege-changing operations. Failed commands stay visible until handled.
- **Honest about uncertainty and failure.** The prompt never conceals failed checks, missing evidence, or unresolved errors, does not present a dependent action as ready while a prerequisite is unknown, and prefers the specified safe response to an improvised workaround. Recovery stays within authorized boundaries, the next permitted step is never implied to have already happened, and a recommendation is never described as a guarantee.
- **Versioned, portable, reconciled.** The prompt is versioned and tied to a release artifact, and its integrity is established by the designated verification mechanism, never by its own text. Changes to invariants, command semantics, or authority boundaries are reviewed against the normative specifications, and host-specific adaptation lives in a versioned adapter or integration layer without altering the shared contract. Portability preserves governance semantics, not merely similar wording. The prompt never claims to replace the console, authority, controller, or runtime, and conformance separates prompt-behavior tests from enforcement and security tests.

**Essence:** the prompt communicates governance and never enforces it; the Host AI reasons and proposes within the contract, authoritative facts come only from designated sources, and security rests on controls outside the prompt.

---

## Reference ID Scheme

Every normative statement carries a stable identifier of the form:

**`PMT-<file>:<rule>`**

- `PMT` identifies this specification (amk-prompt).
- `<file>` is the module file number.
- `<rule>` is the rule number inside that file. Each file begins numbering at 1.

---

## Module Index & File Numbers

| File # | File | Scope |
|--------|------|-------|
| 1 | [00-foundations.md](00-foundations.md) | Role, trust, assurance levels, statelessness, invariants |
| 2 | [01-identity-bootstrap.md](01-identity-bootstrap.md) | Kernel identity exposure and bootstrap interaction |
| 3 | [02-instruction-boundary.md](02-instruction-boundary.md) | Instruction classes, precedence, and boundary |
| 4 | [03-command-set.md](03-command-set.md) | Command set declaration and non-responsibilities |
| 5 | [04-authority-capability.md](04-authority-capability.md) | Authority rules, capability protection, non-authority declaration |
| 6 | [05-behavior-failure.md](05-behavior-failure.md) | Injection resistance, state handling, failure, inert behavior |
| 7 | [06-htsm-conduct.md](06-htsm-conduct.md) | HTSM traversal, work orders, runtime inclusion, optional validation |
| 8 | [99-open-items.md](99-open-items.md) | Open questions (non-normative) |

---

## Errors, inconsistencies and critical deficiencies (cursory)

*Cursory pass only; a complete scan follows. It covered every module file of this specification at a skim level and did not cross-check against `amk-runtime`, `amk-ssot.md` or the HTSM units. IDs (`E-PMT-nn`) are provisional. **BLOCKING** means the item must be resolved before this specification can be released at the stated profile. This specification defines no Basic, Standard, or High behavior (its only graded concept is the L0/L1/L2 assurance level), so items sit under the profile where the impact is greatest and most appear under ALL PROFILES. `99-open-items.md` lists open questions without IDs or a blocking classification.*

### BASIC

- **E-PMT-01 (non-blocking):** The Host AI is never told the controller's declared profile (`CTR-8:2`), yet it must treat attested content as authoritative at L1 and L2 (`PMT-1:9`). Under Basic that backing is weaker (software keys, simplified replay protection, and a revocation list that may be absent), and the prompt cannot reflect that. Core Intent also refers to profiles that require user-mediated execution, which this specification does not define. Decide whether the prompt exposes the profile and whether any behavior varies by it.

### STANDARD

- **E-PMT-02 (BLOCKING):** The prompt artifact is "detached-signed" (overview, `PMT-2:3`), but no signature scheme, signing key, verifier, or failure behavior is defined. The Host AI computes nothing (`PMT-7:3`), so someone else must verify it. The rule that the template and this specification "MUST NOT diverge" (overview) is unnumbered and untestable. Release-specific values (Release Key fingerprint, minimum epoch, `PMT-2:1`) tie each artifact to one release, but how prompt and Release Manifest versions are bound is undefined. Also affects HIGH.

### HIGH

- **E-PMT-03 (non-blocking):** The optional validation layer (`PMT-7:13` to `PMT-7:15`) has no stated profile applicability, and its interaction with Auto Assist and pre-authorization is open. Nothing says whether High requires it, and `PMT-7:15` limits its claim to traversal consistency.

### ALL PROFILES

- **E-PMT-04 (BLOCKING):** The trust rule for the Host AI cannot be implemented as written. `PMT-1:9` depends on an "Attestation" delivered through the "HIL channel", neither of which is defined here, L1 and L2 produce identical Host AI behavior, and the mapping of L0/L1/L2 to HIL attestation requirements is open. The migration notes nonetheless call the specification ready to drive artifact generation, while its own open items leave the prompt wording, error vocabulary, and this mapping undefined.
- **E-PMT-05 (non-blocking):** The command boundary in Core Intent (analysis, recommendation, proposed step, execution; no claim of execution or success without evidence from the authorized boundary; failures stay visible) has only a partial counterpart. `PMT-4:3` covers fabricated results of the nine kernel commands, but there is no rule for execution claims about runtime or external actions, for proposals shown as successful, or for keeping failures visible until recovery.
- **E-PMT-06 (non-blocking):** Required Host AI outputs reference undefined vocabulary: `E_UNREACHABLE` (`PMT-6:7`), `fork_detected`, `chain_broken` (`PMT-7:5`), `work_order_required` (`PMT-7:7`), and the state `UNVERIFIED` (`PMT-6:6`). The controller spec defines no matching codes or state (`E-CTR-14`), and `PMT-7:4` sets no poll interval or retry bound.
- **E-PMT-07 (non-blocking):** INERT is described as "continues normal operation under kernel governance" (`PMT-6:13`), then restricted by `PMT-6:14`, and Core Intent treats it as a pause state. INERT is not defined in the controller state model (`E-CTR-12`).
- **E-PMT-08 (non-blocking):** Instructions "not carried by an attested controller response are non-authoritative" (`PMT-5:10`) would also cover the prompt itself, which is delivered by a handoff or console, not by a controller response. A carve-out for the signed prompt artifact is needed so the instruction boundary (`PMT-3:7`) has a starting point.
- **E-PMT-09 (non-blocking):** The six instruction classes (`PMT-3:1`) do not match the six precedence levels (`PMT-3:2`): the precedence list has kernel invariant and kernel policy as separate levels and omits external data. No rule says what happens when no deterministic precedence rule resolves a conflict (Core Intent: surface it as unresolved).
- **E-PMT-10 (non-blocking):** The Host AI's list of forbidden console-only operations (`PMT-4:4`) differs from the controller's (`CTR-4:7`). The prompt list adds "activate" and "enroll" and omits "level changes", and the controller's list has no "activate".
- **E-PMT-11 (non-blocking):** The Host AI may learn runtime names "from earlier sessions" (`PMT-7:10`), which sits uneasily with `PMT-1:13` and `PMT-6:5` (conversation memory is never state). State that such names are unverified hints only.
- **E-PMT-12 (non-blocking):** Several Core Intent points have no normative counterpart: host-specific adaptation and compatibility or deprecation behavior (`PMT-6:15` covers only silent downgrade), the requirement that claimed verification names its evidence, and conformance (separating prompt-behavior tests from enforcement tests). Open items have no IDs, the reference scheme omits the "IDs are never reassigned / `RETIRED`" rule used in the other core specs, and the `amk-ssot.md` row for this specification is still pending (`CORE-O-03`).
