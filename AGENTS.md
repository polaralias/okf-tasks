# AGENTS

<!-- repo-setup:shared-governance:start -->
## Shared Git Workflow

- work from a short-lived branch created from `main`
- do not commit directly to `main`
- use branch names prefixed with `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`, or `test/`
- keep one logical change per branch and pull request
- open a pull request before merging to `main`, including for solo work
- prefer squash merge unless multiple commits carry durable review value
- delete the merged or closed feature branch after the work is finished; never delete `main`
- use tags in `vX.Y.Z` format for releases and do not move published tags
<!-- repo-setup:shared-governance:end -->

## Project-specific requirements

- treat `SPEC.md` as normative and `VERSION` as the release source of truth
- preserve unknown YAML fields when modifying task records
- add manifest fixtures for every machine-testable normative change
- keep the Python and TypeScript validators behaviourally independent
- regenerate indexes and conformance fixtures rather than editing generated files
- run the complete release bar before proposing a merge
