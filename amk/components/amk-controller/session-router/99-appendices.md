# Appendices

**Overview.**  
This non-normative module records the change history, open questions, and a concise summary. It exists solely for traceability; no requirement in this file is normative.

---

## Appendix A — Changes (selected)

| ID | Change | Reason |
|---|---|---|
| C21 | Component renamed to session-router; language-agnostic design formalised; three complexity profiles introduced. | Support hobby-to-enterprise spectrum. |
| C22 | All AMK / OS/10 references removed. Component made fully general-purpose and self-contained. | Enable public, independent use. |
| C23 | All hard-coded roles (console, controller, host-ai, ledger, etc.) removed. Roles are now arbitrary strings declared in the Init Envelope. | Generalise to any set of participants. |
| C24 | Host-AI-specific binding module replaced by a general Adapters module for constrained entities. | Remove domain-specific assumptions. |
| C25 | Default policy matrix removed. Complete policy (including role list) is supplied in the Init Envelope. | Eliminate hard-coded assumptions. |
| C26 | amk-sessions generalised to “Attestation Authority” treated as a black-box interface. | Self-containment. |
| C27 | Version advanced to 0.5.0-draft. | Reflect general-purpose redesign. |

Earlier change history (C1–C20) from previous domain-specific drafts is retained in archival form but is no longer normative.

---

## Appendix C — Open Questions

| ID | Question |
|---|---|
| O1 | Concrete values and profile-specific recommended ranges for `T_MAX`, `N_MAX`, `G`, `X`, `R_MAX`, `CELL_SIZE`, `TAG_MAX`, `HS_MAX`, `REG_WINDOW`. |
| O2 | Exact schema of the Init Envelope, Binding Data, Discovery Record, and control-interface messages (serialisation format, mandatory vs optional fields). |
| O3 | Recommended cryptographic suites and algorithm identifiers. |
| O4 | Whether dynamic addition of roles after instance creation should be supported, and under what conditions. |
| O5 | Optional decoy-traffic generation algorithms and parameters. |
| O6 | Formal verification targets for the High profile. |

---

## Appendix E — Summary

The Session Router is a general-purpose, language-agnostic, self-contained blind ingress/egress relay. Entities address one another by arbitrary roles declared at session creation. The router alone holds the mapping to opaque logical addresses. Channels are established by mutual-attestation brokered ECDH; payloads are E2E encrypted with keys the router never sees. Policy is fully dynamic and supplied with the session. Per-session instances, fixed-size cells (except under Basic), and opaque denials bound residual knowledge to traffic metadata. Three complexity profiles allow implementations ranging from simple hobbyist code to hardware-backed enterprise deployments. The component defines only its own interaction surface; external entities and the Attestation Authority are treated as black boxes that must satisfy the stated cryptographic and message contracts.
