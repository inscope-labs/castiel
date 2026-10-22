# Package Authority — Provenance, Publishers, Repositories, Update Flags & Revocation

**File number:** 6  
**Overview.**  
This module defines how package identity and trust are established: who may sign, how the operator's trust decisions are recorded, how repositories are treated, how update status is published, and how a package is withdrawn.

---

## Roles

- **RTM-6:1** The Release Authority signs system packages with the Release Key.
- **RTM-6:2** A publisher signs third-party packages with the publisher's key.
- **RTM-6:3** The operator alone decides which publishers and packages to trust, through the console.

## Provenance

- **RTM-6:4** A package is accepted only if its signature verifies and the operator has registered it (RTM-4:4, RTM-4:5).
- **RTM-6:5** The console MUST record, at registration, the publisher identity, the publisher key and the package hash the operator accepted.
- **RTM-6:6** A change of publisher key for an already-registered publisher MUST be treated as a new publisher and require fresh operator confirmation.
- **RTM-6:7** System packages are accepted only if listed in the Release Manifest with a matching package hash (file 7).

## Repositories

- **RTM-6:8** "Public" and "private" describe how a package is distributed through an in-app repository. They do not refer to source-code visibility.
- **RTM-6:9** A public repository is available to every operator of the application.
- **RTM-6:10** A private repository is available either to a single operator or shared among a defined set of operators. Only the operator holds installation keys.
- **RTM-6:11** A repository is untrusted transport (RTM-1:11). Listing in a repository confers no authority.
- **RTM-6:12** Repository protocol details are not defined in this version (see RTM-O-15).

## Conformance

- **RTM-6:13** A package MUST meet the protocol standards defined by a versioned conformance rule set. The rule set is not yet defined (see RTM-O-08).
- **RTM-6:14** Both the console (at registration) and the loader (at load) MUST apply the conformance rule set. A failure at either point rejects the package.

## Update Status

- **RTM-6:15** Each (`package_id`, publisher) MAY have an update status published in an update profile database with one of these values: `current`, `advisory`, `mandatory`, `withdrawn`.
- **RTM-6:16** `advisory` means a newer version is available and recommended. `mandatory` means the console MUST block inclusion of the superseded version after the effective time. `withdrawn` means the version MUST NOT be loaded.
- **RTM-6:17** Update status is a signed statement by the publisher (third-party) or the Release Authority (system). Unsigned or wrongly signed status MUST be ignored.
- **RTM-6:18** The location, signer, and schema of the update profile database are not yet defined (see RTM-O-09).

## Package Revocation

- **RTM-6:19** A publisher or the Release Authority MAY withdraw a package version by publishing a signed withdrawal statement.
- **RTM-6:20** The console MUST surface a withdrawal to the operator. The loader MUST refuse to load a withdrawn version (RTM-4:22).
- **RTM-6:21** Package withdrawal is separate from revocation of role attestations (`ATA-04`) and of pre-authorizations (`CNS-5:10`).
- **RTM-6:22** Withdrawing a package does not by itself end a running session. The operator ends it through the console.
