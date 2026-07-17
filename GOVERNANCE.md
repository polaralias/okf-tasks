# Governance

OKF Tasks is maintained by James Whelan (`@polaralias`). The maintainer accepts releases and has final responsibility for the profile's published meaning.

## Decision process

Changes are proposed through pull requests. Normative proposals must describe the interoperability gap, alternatives considered, compatibility effect, and conformance evidence. Discussion is welcome; acceptance requires maintainer approval and a green release gate.

The protected branch requires a pull request, one approving Code Owner review, resolved review threads, and the `release-gate` status check. Because this is currently a single-maintainer personal repository, the maintainer has a pull-request-only ruleset bypass. It exists to permit an accountable self-merge when GitHub cannot supply an independent approval, not to bypass tests or review discussion.

## Version policy

`VERSION` uses semantic versioning and release tags use `vX.Y.Z`.

- Patch: corrections that do not change which records conform.
- Minor: backward-compatible additions or new optional capabilities.
- Major: incompatible syntax or semantics.

Published tags, schema `$id` values, and profile URLs are immutable. A normative change updates the spec, schemas, changelog, skill reference, conformance corpus, and both implementations as applicable.

## Release criteria

A release is eligible when:

1. the version agrees across `VERSION`, package metadata, profile text, and schema identities;
2. every machine-testable requirement has positive and negative fixture coverage;
3. the Python producer/validator and independent TypeScript validator agree on the manifest;
4. examples and the public skill remain valid;
5. generated fixtures and indexes are current;
6. CI and the release consistency check pass;
7. the maintainer accepts the release notes and compatibility statement.

## Security and conduct

Security-sensitive reports should use GitHub's private vulnerability reporting when enabled rather than a public issue. Contributors are expected to engage constructively, focus criticism on artifacts and decisions, and respect the maintainer's enforcement of repository boundaries.
