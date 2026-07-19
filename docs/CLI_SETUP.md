# CLI setup

The `okf-tasks` repository is the authoritative distribution for the reference CLI. Its Python and TypeScript validators remain independent; the console command uses the Python implementation bundled in `skills/okf-task-lifecycle/scripts/okf_tasks.py`.

## Install from a trusted checkout

From the repository root, install the current checkout in editable mode:

```text
python -m pip install -e .
okf-tasks --version
okf-tasks --help
```

`okf-tasks --version` must match the repository `VERSION` file and the version declared by a consuming skill. Do not silently install or upgrade the CLI during skill execution. When a packaged release becomes available, prefer an isolated, version-pinned installation rather than an unpinned branch head.

## Skill fallback

Both the in-repository `okf-task-lifecycle` skill and the upstream Polaralias `repo-task-lifecycle` skill carry a feature-identical `scripts/okf_tasks.py`. When the console command is missing or incompatible, run:

```text
python <skill-directory>/scripts/okf_tasks.py --version
python <skill-directory>/scripts/okf_tasks.py --help
```

The fallback requires Python 3.10 or newer and PyYAML. It is a portable execution path, not a second authority: specification, fixtures, schemas, CLI behaviour, and both skill copies must remain in parity.

For strict graph-aware creation, use repeatable `create --depends-on <task-concept-path>` and `create --related <repository-relative-markdown-path>` arguments. Related-document targets must already exist inside the repository; the CLI writes a portable relative Markdown link from the new task.
