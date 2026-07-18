# Tracker integration setup and live evidence

This document records how OKF Tasks establishes a first-class tracker connection and the live verification performed for the v0.4 provider layer. It intentionally contains no credentials or credential references.

## Project setup process

1. Identify the repository-local task bundle and inspect existing Tracker Profiles under `tasks/trackers/`.
2. Discover the provider surface appropriate to the current project:
   - GitHub repository;
   - GitLab project and host;
   - Linear team;
   - ClickUp List, including its Workspace context.
3. If more than one surface is plausible, present the candidates and ask the user which project scope should receive new tasks. Do not infer a writable destination merely from account access.
4. Initialize the selected scope from live discovery. Review proposed status mappings, provider capabilities, custom fields, and managed-label ownership.
5. Save the selected profile as the project default with `tracker init --default` or `tracker set-default`. The default is repository data; authentication remains runtime-only.
6. Create, import, or synchronize. Provider writes are read back before the reconciliation base advances.
7. Re-run `tracker refresh` when provider configuration changes, and retain validation or live-test evidence with the delivery change.

```text
okf-tasks tracker init --root . --tracker linear-engineering --system linear --scope ENG --mode bidirectional --authority repository --default
okf-tasks tracker set-default --root . --tracker linear-engineering
okf-tasks tracker create --root . --task new-task
okf-tasks tracker sync --root . --task new-task --direction push
```

An explicit `--tracker` always wins. Without one, the CLI uses the saved default, then a sole profile. If several profiles exist without one safe default, it stops and lists the available profiles so the user can choose and save one.

## Credential boundary

Credentials were supplied only through runtime environment variables: `GITHUB_TOKEN`, `GITLAB_TOKEN`, `LINEAR_API_KEY`, and `CLICKUP_API_TOKEN`. Self-managed GitLab can use a runtime certificate trust path and `--api-base`. Profiles store the provider host, stable scope identity, discovery fingerprint, mappings, and setup evidence, but never a token, secret, credential reference, or machine-local certificate path.

## Live verification — 2026-07-18

| Provider | Surface | Verified behavior | Cleanup |
|---|---|---|---|
| GitHub | `polaralias/agentic-workflow-testing` repository | Discovery, profile validation and refresh, issue create/read-back, push, remote-revision conflict refusal, import, and managed-label preservation | Test issues closed; temporary labels removed; no open issues |
| Linear | `POL` team in the Polaralias testing workspace | Team and workflow discovery, issue create/read-back, push, conflict refusal, unique reverse-status pull, and import | Test issues archived |
| ClickUp | Disposable List in the testing Workspace | List discovery, profile validation and refresh, task create/read-back, push, conflict refusal, and import | Disposable List and tasks deleted |
| GitLab | Disposable GitLab CE 19.2.0 project served locally over HTTPS | Project discovery, profile validation and refresh, issue create/read-back, push, conflict refusal, import, inspection, and managed-label preservation | Container, project, certificate, token, test files, and image removed |

GitHub and GitLab both preserved a foreign `human-review` label while updating the OKF-owned `okf:` subset. Linear's discovered `Todo` state mapped uniquely back to `ready`. GitHub, GitLab, and ClickUp correctly refused ambiguous reverse mappings where several OKF states collapse into a provider's open state.

The live scopes did not expose writable arbitrary custom fields suitable for a safe create/read-back test. ClickUp returned zero accessible List custom fields; the GitHub, GitLab, and Linear test surfaces likewise did not provide a writable arbitrary issue-field transport. Stable custom-field identifiers and outbound value construction remain covered by the machine test suite.

## Verification evidence

- Python reference implementation: 34 tests passed during the original provider run; the expanded default-selection suite is part of the current release bar.
- Independent TypeScript validator: all manifest cases passed.
- Generated fixtures were current.
- Release metadata was consistent for v0.4.0.
- Live credentials were cleared after use and no test credential was persisted in either repository.

