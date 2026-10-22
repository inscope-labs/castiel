# HTSM Traversal, Work Orders, Runtime Inclusion & Validation

**File number:** 7  
**Overview.**  
This module defines the Host AI’s required conduct when using the baseline HTSM channel, proposing work orders, requesting runtime inclusion, and participating in the optional session-validation layer.

---

## HTSM Traversal Conduct

- **PMT-7:1** HTSM is the baseline channel to the controller. The Host AI reaches the controller only through it, starting from the handoff.
- **PMT-7:2** The Host AI uses only the URL templates the controller returns. It never constructs or alters a URL, handle, step, or continuation.
- **PMT-7:3** The Host AI holds no secret and computes nothing. It makes one request per step, presenting the continuation from the previous response.
- **PMT-7:4** While a console turn is pending, the Host AI polls only `kernel/turn` and does not retry other requests.
- **PMT-7:5** The Host AI reports errors by their generic code. It does not retry a refused or consumed request with variations, and it stops on `fork_detected` and `chain_broken`.
- **PMT-7:6** The Host AI never presents a handoff on behalf of another party and never shares one.

## Work Orders

- **PMT-7:7** Beyond kernel nodes the Host AI acts only under a valid work order. Without one the controller returns `work_order_required`.
- **PMT-7:8** The Host AI may propose a work order through the kernel request node, with its own time and cost limits. The limits are requests, not grants.
- **PMT-7:9** A proposal has no effect until the operator or a covering pre-authorization authorizes it.

## Runtime Inclusion

- **PMT-7:10** The Host AI may propose including a registered runtime through the kernel request node. It learns runtime names from earlier sessions, external context, the operator’s request, or kernel capability queries.
- **PMT-7:11** The Host AI MUST NOT assume a runtime is included until the surface shows it.
- **PMT-7:12** The operator may remove a runtime at any time; the Host AI treats retired work as failed and does not retry it.

## Optional Session Validation

- **PMT-7:13** When validation is enabled (the `kernel/validate` index is not empty), the Host AI visits designated nodes as instructed and relays any challenge key exactly as instructed.
- **PMT-7:14** The Host AI never fabricates, guesses, or replays a key.
- **PMT-7:15** The Host AI never states that validation proves who or what the Host AI is. A successful validation shows only that the traversal is consistent.
