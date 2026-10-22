# Open Items & Migration Notes

**File number:** 8  
**Overview.**  
Non-normative list of remaining open questions and notes on the migration from the previous draft.

---

## Open Questions

- Exact wording and structure of the deployable templated prompt artifact.
- Detailed mapping of assurance levels (L0/L1/L2) to concrete HIL attestation requirements.
- Whether additional instruction classes are needed for future channels beyond HTSM.
- Precise error-code vocabulary the Host AI must surface.
- Interaction of the optional validation layer with Auto Assist and pre-authorization.

## Migration Notes

- Component renamed from `amk-command` to `amk-prompt`.
- Reference scheme changed from `COM-` to `PMT-<file>:<rule>`.
- The specification remains purely advisory and non-authoritative.
- Console-only operations are explicitly listed as forbidden.
- HTSM traversal, work-order, runtime-inclusion, and validation conduct are collected in a dedicated module.
- The document is ready to drive generation of the templated prompt artifact.
