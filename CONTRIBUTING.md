# Contributing

Thanks for contributing to `okf-tasks`.

## Branch workflow

- create a short-lived branch from `main`
- use `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`, or `test/` prefixes
- do not commit directly to `main`
- open a pull request before merging to `main`
- prefer squash merge unless commit history shape matters
- delete the merged or closed feature branch when the work is finished
- never delete `main`

## Repo hygiene

- keep docs and automation changes in the same slice as the behavior they govern
- avoid mixing unrelated changes into the same branch
- update versioning and release surfaces deliberately when the repo is release-enabled

## Specification changes

A normative change must:

- state the interoperability problem and proposed rule;
- update `SPEC.md` and any affected schema;
- add positive and negative cases to `conformance/manifest.json`;
- update both independent implementations where the rule is machine-testable;
- update examples or the public skill when producer behaviour changes;
- add a changelog entry and choose a version according to `GOVERNANCE.md`.

Clarifications that do not change the set of conformant data may be patches. New optional fields are normally minor changes. Breaking changes require an explicitly versioned profile.

## Required checks

Run the commands under “Verify the release bar” in `README.md`. Pull requests require the `release-gate` check, resolved review threads, and Code Owner approval. The accepting maintainer may use the configured pull-request-only ruleset bypass when GitHub cannot represent self-approval.
