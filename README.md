# Castiel

**The Agentic Micro Kernel (AMK) — a vendor-neutral framework specification for governed AI agents.**

Castiel specifies the Agentic Micro Kernel (AMK): a small, strictly separated set of components that keep the
**human operator as the legitimate source of authorization** while enforcement stays **cryptographically protected and
independent of Host AI assertions**. It is an *abstract framework* — a contract to implement against — not a product.

| | |
|---|---|
| **Status** | **Draft — pre-release.** No versioned release has been published. |
| **Suite version** | `OS10-AMK 2.0-draft` (see [`amk/amk-ssot.md`](amk/amk-ssot.md)) |
| **Target first release** | `v0.1` — scope in [First release scope](#first-release-scope) |
| **Contents** | Specifications only. **No AMK implementation code.** |
| **Core components** | Five — [listed below](#the-five-core-components) |
| **Language / platform** | None required. The framework is language- and platform-agnostic. |
| **Licence** | **Not yet published** (decision D-04). See [Licence](#licence). |
| **Repository** | [`inscope-labs/castiel`](https://github.com/inscope-labs/castiel) |

---

## What Castiel is

Castiel publishes **one thing**: the normative contract of the Agentic Micro Kernel.

It answers a narrow question that matters as soon as an AI agent can take actions on a real system:

> When an agent wants to do something, what proves that a human actually authorized *that*, *now*, *here* — and what
> stops the agent from deciding that it did?

Castiel's answer is structural rather than advisory. It splits authority across five components so that no single
component — and in particular **not** the AI model — can authorize, widen, or simulate an authorization:

- the **operator** acts through the **console**, which is the only representation of human intent;
- the **controller** is the only place where a decision is *enforced*;
- the **Attestation Authority** only *proves who or what is participating*, never what they may do;
- the **prompt** only *communicates* the contract to the Host AI and is explicitly advisory;
- the **runtime** only *verifies and loads* packages the operator has already authorized.

Every decision is therefore attributable to an explicit operator instruction, checked at an enforcement point that
the AI cannot influence, and recorded in an auditable form.

### The Agentic Micro Kernel

"Micro Kernel" here means *small kernel, large contract*. The kernel surface is deliberately minimal — five
components with sharply bounded responsibilities — while the specification behind it is complete enough to support
independent implementations that do not share a line of code.

The AMK is the kernel contract for **OS/10** (`Operating System 10`), the suite that Castiel targets. Castiel itself
does not specify OS/10 as an operating system; it specifies the AMK that any OS/10-conformant or independently
built agent runtime would have to honour.

## Who this is for

| Reader | What Castiel gives you |
|---|---|
| **Independent implementers** | A complete, normative contract to build against in any language, on any platform, without asking anyone's permission. |
| **Teams deploying agentic systems** | A reviewable definition of what "human-authorized" means, and which component is accountable for enforcing it. |
| **Auditors and compliance teams** | Stable, citable requirement identifiers (`ATA-…`, `CNS-…`, `CTR-…`, `PMT-…`, `RTM-…`) that can be traced to evidence. |
| **Researchers** | A precise separation of authority, trust, attestation and enforcement to build on, critique, or extend. |
| **Forkers** | A framework whose mandatory guarantees are identified as mandatory, so a fork can evolve without silently weakening them. |

## What Castiel is not

Stated plainly, because a framework that overstates its own maturity is worse than no framework:

- **It is not an operating system.** Castiel ships no kernel, no bootloader, no service manager, no reference implementation.
- **It is not a code library.** There is no `npm`, `pip`, `cargo` or `go get` artifact to install. The deliverable is the specification.
- **It is not an AI product, model, or provider.** The Host AI is explicitly *untrusted* for enforcement and authorization. Castiel is not tied to any AI vendor, model, or hosting environment.
- **It is not a certification body.** Conformance is defined in terms of published test vectors and declarations; no third-party certification exists yet, and the framework never claims regulatory compliance on an implementation's behalf.
- **It is not finished.** Every specification in this repository is a draft. See [Framework maturity and known limitations](#framework-maturity-and-known-limitations).

## The five core components

| Component | Spec ID | Clause prefix | Version | Responsibility | Trusted for |
|---|---|---|---|---|---|
| **Attestation Authority** | `amk-authority` | `ATA-nn:nn` | 1.2.0-draft | Issues and validates bounded role attestations. Never authorizes, never enforces. | The attestations it signs — nothing beyond their defined meaning. |
| **Operator Console** | `amk-console` | `CNS-nn:nn` | 2.1.0-draft | The sole representation of human operator authority. Carries intent, shows confirmed outcomes only. | Authenticated operator intent — never enforcement. |
| **Controller** | `amk-controller` | `CTR-nn:nn` | 2.0.0-draft | The sole enforcement point, token-issuance engine and state authority. Fails closed. | Enforcement decisions and issued capability tokens. |
| **Host AI Kernel Prompt** | `amk-prompt` | `PMT-nn:nn` | 2.0.0-draft | Advisory, stateless, signed prompt contract and Host AI interface boundary. | Nothing. It is advisory by construction. |
| **Runtime** | `amk-runtime` | `RTM-nn:nn` | 0.1.0-draft | The single authority over runtime packages, and the only loader that brings package code into execution. | Package provenance, conformance verification and load integrity. |

A sixth specification, the **Session Router** ([`session-router`](amk/components/amk-controller/session-router/session-router.md),
v0.5.0-draft, `RTR-1`–`RTR-116`), is a companion to the controller: a blind ingress/egress relay that separates
identity from address and forwards payloads it cannot read. It is not one of the five core components and cannot
create an authority path of its own.

### Operational profiles

The console, controller and runtime each define three operational profiles. **Higher profiles subsume all
requirements of lower profiles**, and every implementation must declare exactly one.

| Profile | Target | Key protection | Isolation | Confirmation | Audit |
|---|---|---|---|---|---|
| **Basic** | Hobby, educational, rapid prototypes | Software keys permitted | Soft isolation acceptable | Risk-based | Minimal |
| **Standard** | Production services | Non-exportable keys; OS keystore or equivalent | Process / container isolation | Fresh confirmation for high-impact actions | Full envelope audit trail |
| **High** | Enterprise, regulated, high-assurance | HSM or TEE; keys never in ordinary process memory | Strong isolation (TEE or equivalent) | Strict fresh confirmation + measured environment | Hardware-protected audit + remote attestation |

The prompt specification is graded differently: it defines **assurance levels L0/L1/L2** rather than the
Basic/Standard/High profiles.

## Authority and trust principles

These are the framework's load-bearing invariants. They are stated in the specifications with stable identifiers
and are not negotiable by an implementation.

1. **The console is the sole seat of operator authority** (`CNS-1:1`). The controller has no independent notion of an
   operator (`CNS-1:2`, `CTR-1:4`).
2. **The controller is the sole enforcement point**, token-issuance engine and state authority (`CTR-1:1`). It fails
   closed on every failure condition (`CTR-1:16`).
3. **The Attestation Authority is the sole issuer of role attestations** (`ATA-00:01`). It is trusted for the
   statements it signs and untrusted for enforcement (`ATA-00:02`).
4. **The Host AI and the prompt layer are untrusted for enforcement and authorization** (`CTR-1:7`). The prompt is
   advisory; prompt compliance is defence-in-depth, never a security control on its own.
5. **Authority is never inferred** from presence, context, prompt content or authentication alone (`CTR-1:9`).
6. **Evidence is not permission.** A valid signature, attestation, package hash or capability reference is input to a
   check — never a grant.
7. **No state-affecting action is implicit** (`CNS-1:9`). Silence, UI focus, clipboard contents, model suggestions
   and inferred preference are never approval.
8. **The controller never creates or widens a pre-authorization envelope** (`CTR-1:18`), and **the Host AI never
   receives a capability token** (`CTR-1:19`).
9. **Separate checks stay separate.** Provenance, integrity, authorization and enforcement are distinct obligations,
   even when two components share a process or a codebase.
10. **Precedence is deterministic.** Kernel invariants outrank policy, runtime rules, capability grants, task
    instructions and agent suggestions. Lower inputs never relax higher ones; conflicts resolve by an explicit rule
    or fail closed.

## How the specifications fit together

```
                       amk/amk-ssot.md          suite-level single source of truth
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   components/            framework areas            implementation
   (normative core)      (normative support)        (normative contract)
        │                        │                        │
   amk-authority            abstract-kernel/          implementation-
   amk-console              protocols/                specification/
   amk-controller           cross-cutting-            conformance/
   amk-prompt               requirements/
   amk-runtime              package-framework/             │
        │                          │                        │
        └──────────────┬───────────┬────────────┬───────────┘
                       │           │            │
                  governance/  reference-    releases/
                  (versioning, material/     (manifest,
                   change       (informative) provenance)
                   control)
```

Three rules make the hierarchy unambiguous:

- **One statement, one reference.** Every row of the SSOT carries exactly one rule reference (`ATA-00:01`,
  `CNS-1:1`, `CTR-1:1`, …). A statement without a reference is invalid.
- **Normative text lives in the module files.** Each component's `00-foundations.md` … `99-open-items.md` files carry
  the requirements. The `amk-<name>.md` file is the index and overview; where it differs from the module files, **the
  module files are authoritative**.
- **Informative material is labelled.** Architecture, examples, terminology and compliance mappings are references
  for humans, not obligations on an implementation.

## Authoritative specification locations

| Document | Path | Kind |
|---|---|---|
| Suite overview and rules | [`amk/amk-ssot.md`](amk/amk-ssot.md) | Normative (suite level) |
| Attestation Authority | [`amk/components/amk-authority/`](amk/components/amk-authority/) | Normative |
| Operator Console | [`amk/components/amk-console/`](amk/components/amk-console/) | Normative |
| Controller | [`amk/components/amk-controller/`](amk/components/amk-controller/) | Normative |
| Host AI Kernel Prompt | [`amk/components/amk-prompt/`](amk/components/amk-prompt/) | Normative |
| Runtime | [`amk/components/amk-runtime/`](amk/components/amk-runtime/) | Normative |
| Session Router (controller companion) | [`amk/components/amk-controller/session-router/`](amk/components/amk-controller/session-router/) | Normative |
| Open-items index | [`amk/OPEN-ITEMS.md`](amk/OPEN-ITEMS.md) | Informative (working view) |
| Per-component open items | `amk/components/amk-*/99-open-items.md` | Informative (normative lists) |
| Kernel foundations | `amk/abstract-kernel/` | Placeholder — plan 10008 phase 2 |
| Protocols (envelopes, identity, errors, session launch) and their schemas | `amk/protocols/` | Placeholder — plan 10008 phase 3 |
| Cross-cutting requirements | `amk/cross-cutting-requirements/` | Placeholder — plan 10008 phase 4 |
| Package framework | `amk/package-framework/` | Placeholder — plan 10008 phase 4 |
| Implementation specification | `amk/implementation-specification/` | Placeholder — plan 10008 phase 6 |
| Conformance model, taxonomy, vectors | `amk/conformance/` | Placeholder — plan 10008 phase 7 |
| Reference architecture, examples, compliance mappings | `amk/reference-material/` | Placeholder — plan 10008 phase 8 |
| Governance: versioning, compatibility, change control, clause naming, licensing | [`amk/governance/`](amk/governance/) | Placeholder — decisions D-04, D-05, D-06 |
| Release process: manifest schema and provenance | [`amk/releases/`](amk/releases/) | Manifest schema published; provenance records are placeholders |

Each component directory holds:

- `amk-<name>.md` — the index and informative overview;
- `00-foundations.md` … `99-open-items.md` — the normative module files;
- no committed `amk-<name>-spec-full.md`: the merged specification is **generated** at build time (see
  [Repository tooling](#repository-tooling)) and published in the release artifact, never committed;
- one or more extension-point directories (for example
  [`amk/components/amk-controller/policy-engine-extension-point/`](amk/components/amk-controller/policy-engine-extension-point/)),
  which are placeholders awaiting plan 10008.

## Repository layout

| Path | What lives there |
|---|---|
| [`amk/`](amk/) | **The framework.** All specifications, in the areas listed above. |
| [`amk/components/`](amk/components/) | The five core component specifications plus the session-router companion. |
| [`docs/`](docs/) | Repository and process documentation for this repository — operator guide, pending register, decisions, setup. Not framework specifications. |
| [`plans/castiel-framework/`](plans/castiel-framework/) | Plan 10008: the framework completion plan that produces the remaining specifications. |
| [`engine/`](engine/) | The Build Engine v0.5.0 — repository tooling for planning and task execution. Implements no part of the AMK. |
| [`operator/`](operator/) | Operator-side tooling for the build/bridge workflow. |
| [`amk/scripts/`](amk/scripts/) | Specification tooling: `merge_spec.py` (merge one spec area), `build_release.py` (build, verify and archive the release artifact) and its tests. |
| `.github/workflows/` | CI: `spec-build.yml` (regenerate and verify on every change), `release.yml` (strict build on a version tag) and the Build Engine integration workflow. |
| Root files | `LICENSE`, `LICENSES/`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `VERSION` — repository-level policy files, at the root so GitHub surfaces them. All are placeholders today. |

## Reading order for a new implementation

1. **Read the SSOT** — [`amk/amk-ssot.md`](amk/amk-ssot.md). It is one page and fixes the suite version, the five
   components, and the suite-level rules.
2. **Read the five component overviews** — [`amk-authority`](amk/components/amk-authority/amk-authority.md),
   [`amk-console`](amk/components/amk-console/amk-console.md),
   [`amk-controller`](amk/components/amk-controller/amk-controller.md),
   [`amk-prompt`](amk/components/amk-prompt/amk-prompt.md) and
   [`amk-runtime`](amk/components/amk-runtime/amk-runtime.md). Each states its role, trust boundary and invariants.
3. **Read the normative module files**, not only the overviews. The `amk-<name>.md` overviews are informative; the
   numbered module files carry the requirements.
4. **Read the open items** for each component (`amk/components/amk-*/99-open-items.md`) and the cross-component index
   ([`amk/OPEN-ITEMS.md`](amk/OPEN-ITEMS.md)). These are the places where the contract is not yet closed.
5. **Choose a profile** and implement to it. Start at **Basic**; it is the smallest profile that still satisfies every
   mandatory check.

## Implementations, forks and conformance

Castiel uses a **fork-and-conform** model:

- **Fork or implement.** Take the framework as the basis for a complete, independent implementation. Implementations
  share the contract, not the code — there is no code to share.
- **Never weaken a mandatory guarantee.** Extensions may add capability; they may not relax a mandatory requirement.
  The framework distinguishes what may be extended from what may not, and requires deviations to be declared
  explicitly rather than assumed.
- **Declare conformance.** An implementation states which requirements it satisfies and which profile it implements.
  Conformance is defined along separate axes — specification, behavioural, security, profile and interoperability
  conformance — and distinguishes self-declaration from independent assessment. The taxonomy, declaration format and
  test-vector framework are being specified in plan 10008 phase 7 and remain **placeholders today**.
- **Interoperate on contracts, not on luck.** Two independent implementations interoperate because they implement the
  same envelopes, identities, error handling and version-negotiation rules — not because they share an origin.

> **Honest caveat.** The conformance model, the deviation policy and the commercial boundary for forks are open
> owner decisions (D-07, D-04). Treat "fork and conform" as the intended model, not yet as a settled mechanism.

## Framework maturity and known limitations

This section is deliberately specific. Nothing here is a guess; each item is either visible in the repository or was
verified against it.

### Current state

- **All specifications are drafts.** Every component carries a `-draft` version. The suite version is
  `OS10-AMK 2.0-draft`.
- **No release exists.** The repository has **no tags and no published releases** as of 29 October 2026.
- **The framework is mid-completion.** Plan 10008 ([`plans/castiel-framework/`](plans/castiel-framework/)) contains
  **125 tasks across 20 stages and 9 phases, with 0 tasks done** and **11 owner decisions still open** (D-01 … D-11).
- **Much of the `amk/` tree is placeholder.** The kernel-foundation, system-protocol, cross-cutting, package,
  implementation-specification, conformance and reference-material areas exist as directory scaffolds whose index
  files are still `TODO`. The substantive content today is the five component specifications, the SSOT, the
  session-router specification and the open-items registers.

### Known defects and gaps

| Area | Finding |
|---|---|
| **Generated specs are not committed** | The five `amk-*-spec-full.md` files were removed from `main` and are now build outputs (ignored by `.gitignore`). `python3 amk/scripts/build_release.py build` regenerates all of them; `release.yml` publishes them. |
| **Merged specs still include placeholders** | The merge includes every `.md` file in a spec area, including `TODO` placeholders. A normal build reports them as warnings; the strict build used for a release tag fails on any placeholder, so none can ship. |
| **Spec-merge CI replaced** | The six `merge-spec*.yml` workflows pointed at `specs/core/amk-*`, which does not exist, and are removed. `spec-build.yml` and `release.yml` replace them (pending register **P-003**). |
| **Obsolete path references** | `amk/amk-ssot.md` still marks the prompt and runtime specifications as pending addition to `specs/core/` (cross-item **CORE-O-03**), and [`amk/components/amk-authority/amk-authority.md`](amk/components/amk-authority/amk-authority.md) points at `specs/core/OPEN-ITEMS.md` while the real index is [`amk/OPEN-ITEMS.md`](amk/OPEN-ITEMS.md). |
| **Open items remain** | Cross-component `CORE-O-01`…`CORE-O-07`; console `CNS-O-01`…`CNS-O-13`; controller `CTR-O-01`…`CTR-O-16`; authority `O-ATA-01`…`O-ATA-10`; plus runtime (`RTM-O-nn`) and prompt open items. The epoch terminology collision (`CORE-O-01`) is unresolved. |
| **No licence, governance or contribution policy** | [`LICENSE`](LICENSE), [`LICENSES/LICENSE-CODE`](LICENSES/LICENSE-CODE), [`amk/governance/licensing.md`](amk/governance/licensing.md), [`GOVERNANCE.md`](GOVERNANCE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md) and [`amk/governance/commercial-boundary.md`](amk/governance/commercial-boundary.md) are placeholders pending decisions D-04 and D-05. |
| **Framework README placeholder** | [`amk/README.md`](amk/README.md) is still `TODO` (plan task `10008-9-201-00`). |
| **Build Engine not configured** | [`engine/engine.json`](engine/engine.json) still contains `OWNER/PROJECT` placeholders (pending register **P-002**). |
| **Bridge unavailable for this repo** | The `cbridge` operator bridge assumes a private working repository plus a public upstream and refuses to run against a single public repository (**P-006**). Until that is fixed upstream, task work is published by hand. |
| **Branch protection unverified** | Whether `main` is protected, and whether required status checks are enforced, could not be confirmed from the tooling available for this assessment (**P-005** covers the adjacent Actions-permission setting). Treat it as unverified rather than absent. |

### What is deferred beyond the first release

Deliberately out of scope for `v0.1`, so long as the Basic contract stays complete: Standard and High operational
implementations, reference implementations, delegated and batch attestation, hardware-backed security guarantees,
third-party certification, advanced multi-agent orchestration, cloud-provider deployment guides, and the commercial
ecosystem. Deferring a feature never leaves its security boundary undefined — each deferred area is still required to
state whether it is unsupported, optional, or reserved.

## Governance, contribution, security and licensing

The documents below are the framework's governance surface. **Their status is stated explicitly**, because linking to a
placeholder and letting a reader assume it is a published policy would be misleading.

| Document | Path | Status |
|---|---|---|
| Framework governance | [`GOVERNANCE.md`](GOVERNANCE.md) | **Placeholder** — pending decision D-05 (who decides framework changes, how proposals are made, and the security-disclosure channel). |
| Contribution guide | [`CONTRIBUTING.md`](CONTRIBUTING.md) | **Placeholder** — pending decision D-05. |
| Framework security policy | [`SECURITY.md`](SECURITY.md) | **Placeholder** — pending decision D-05. |
| Licensing model | [`amk/governance/licensing.md`](amk/governance/licensing.md) | **Placeholder** — pending decision D-04 (specification text vs. code, and the commercial boundary for forks and implementers). |
| Specification licence text | [`LICENSE`](LICENSE) | **Placeholder** — pending decision D-04. |
| Code licence text | [`LICENSES/LICENSE-CODE`](LICENSES/LICENSE-CODE) | **Placeholder** — pending decision D-04. |
| Commercial boundary | [`amk/governance/commercial-boundary.md`](amk/governance/commercial-boundary.md) | **Placeholder** — pending decision D-04. |
| Repository & process security model | [`docs/SECURITY.md`](docs/SECURITY.md) | **Published** — covers the build/bridge token model, leak controls and credentials hygiene for this repository. |
| Pending register (repository work) | [`docs/PENDING-REGISTER.md`](docs/PENDING-REGISTER.md) | **Published** — the operator's list of outstanding repository work. |
| Operator guide | [`docs/OPERATOR-GUIDE.md`](docs/OPERATOR-GUIDE.md) | **Published** — how the plan and tasks are run in this repository. |
| Architecture decisions | [`docs/DECISIONS.md`](docs/DECISIONS.md) | **Published** — repository-level decisions. |
| Framework decisions | `plans/castiel-framework/decisions.json` | **Open** — D-01 … D-11, the owner decisions that gate the framework contract. |

## First release scope

**Target: `v0.1`** — the first complete, normative, independently implementable and testable *abstract framework
contract*. Not a partially implemented operating system, and not a collection of draft specifications.

The repository release version (`v0.1`) and the suite version currently declared in the SSOT
(`OS10-AMK 2.0-draft`) are separate identifiers; how they relate is decision **D-06** and is not yet settled.

**In scope for `v0.1`:**

- the five core component specifications at **Basic profile**, closed on their mandatory requirements;
- the session-router companion specification reconciled with the console and controller;
- the suite SSOT reconciled with the actual component set and free of obsolete path references;
- the envelope model, identity, error handling, policy expression and version negotiation closed;
- a published conformance baseline — taxonomy, declaration format, harness interface and test vectors;
- governance, contribution, security and licensing documents actually published;
- deterministic specification generation, with CI able to regenerate and verify the merged specifications;
- a verifiable release artifact: version, tag, source commit, manifest and checksums.

**Release gates.** The release is not declared official until every one of these holds:

1. repository identity — this README, the scope, and the five components;
2. normative hierarchy — every mandatory requirement has one authoritative specification;
3. trust model — trust boundaries and cryptographic bootstrap are defined;
4. authority model — operator authorization, enforcement and attestation responsibilities are unambiguous;
5. protocol contracts — all mandatory envelopes, schemas and state transitions are defined;
6. component closure — all five components have complete mandatory Basic-profile specifications;
7. cross-spec consistency — no unresolved mandatory contradiction or obsolete normative reference;
8. implementation contract — an independent team can implement the Basic framework without inventing normative behaviour;
9. platform neutrality — no mandatory behaviour depends on one AI provider, OS or programming language;
10. conformance — baseline test vectors and evidence requirements are published;
11. versioning — suite version, compatibility and change rules are established;
12. governance — governance, contribution and security disclosure policies exist;
13. licensing — the specification and any code have explicit licence terms;
14. specification generation — all merged specifications regenerate deterministically;
15. CI — mandatory repository and conformance checks pass;
16. artifact integrity — manifest, source commit and cryptographic checksums are verified;
17. publication — the official versioned release and artifact are available.

## Contributing

The framework's own contribution policy is still being written (decision D-05). Until it is published, this is how
work is actually done in this repository:

- **Framework work is planned, not improvised.** The work is defined in
  [`plans/castiel-framework/`](plans/castiel-framework/) — 125 tasks with acceptance criteria, dependencies and
  verification. Read [`plans/castiel-framework/README.md`](plans/castiel-framework/README.md) for how to start.
- **Changes arrive as pull requests.** Four pull requests have been merged into `main` so far: the Build Engine
  integration, its CI workflow, the framework plan, and the pending register. Earlier scaffolding was committed
  directly to `main`.
- **Keep the register current.** If your change affects a repository-level work item, update
  [`docs/PENDING-REGISTER.md`](docs/PENDING-REGISTER.md) in the same pull request.
- **Never commit generated files.** The `*-spec-full.md` files are build outputs of
  [`amk/scripts/build_release.py`](amk/scripts/build_release.py) (via [`merge_spec.py`](amk/scripts/merge_spec.py)) and
  carry a `GENERATED FILE - DO NOT EDIT.` marker; `.gitignore` excludes them.
- **Specification changes cite clause IDs.** Requirement identifiers are never reassigned; a withdrawn requirement
  keeps its ID and is marked `RETIRED`.

## Licence

**No licence has been published for this repository.** [`LICENSE`](LICENSE), [`LICENSES/LICENSE-CODE`](LICENSES/LICENSE-CODE)
and [`amk/governance/licensing.md`](amk/governance/licensing.md) are placeholders awaiting decision **D-04**, which will separate the
licensing of the specification text from the licensing of any code, and define the commercial boundary for forks and
implementers.

Until that decision is published and the licence texts are in place, the ordinary copyright default applies: **no
permission is granted to use, copy, modify or redistribute this material.** If you need to rely on these
specifications in something you intend to ship, please open an issue asking for the licensing decision to be resolved —
that is the fastest way to move it.

## Repository tooling

The `engine/` directory holds the **Build Engine v0.5.0**, which plans and executes framework work as tasks with
acceptance criteria and verification steps. It implements no part of the AMK and is not part of the framework
contract.

- [`engine/ENGINE-JSON.md`](engine/ENGINE-JSON.md) — how to configure the engine for this repository (values still to
  be set, pending **P-002**).
- [`engine/prompts/`](engine/prompts/) — the supervisor and worker prompts.
- [`engine/tools/plan_tool.py`](engine/tools/plan_tool.py) — plan validation, rendering, ordering and status.

### Specification build and release

`python3 amk/scripts/build_release.py build` regenerates every merged specification and writes the release tree to
`dist/castiel-v<version>/`, with `release/MANIFEST.json` (version, source commit, generator hashes, per-file hashes)
and `release/SHA256SUMS`. The output is deterministic. `build --strict` is what `release.yml` runs on a `v*` tag: it
fails on placeholders, an invalid `VERSION`, a dirty tree or a merge error. `verify <dir>` re-checks a built tree and
`archive <dir>` writes a deterministic `.tar.gz` with its checksum. Checksums prove integrity only; authenticity comes
from the detached signature (when a signing key is configured) and the build-provenance attestation. The
release layout is defined by `build_release.py`; the manifest format by
[`amk/releases/manifest.schema.json`](amk/releases/manifest.schema.json).

Plan progress is tracked in [`plans/castiel-framework/PLAN.md`](plans/castiel-framework/PLAN.md), which is generated
and must not be edited by hand.

---

*Castiel — the Agentic Micro Kernel framework specification.*
*This document describes a draft framework in progress. It is not a release announcement, and it does not claim that
any conformance, certification or regulatory compliance has been achieved.*
