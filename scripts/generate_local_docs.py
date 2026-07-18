from __future__ import annotations

import argparse
from pathlib import Path

from visualize_bundle import build_graph, generate_html, read_documents, read_records, write_or_check


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ("examples/visualization/tasks", "OKF Tasks visualization example", "okf-tasks-visualization.html"),
    ("examples", "OKF Tasks example bundles", "okf-tasks-examples.html"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the reviewable local OKF Tasks HTML pages.")
    parser.add_argument("--root", default=str(PROJECT_ROOT), help="OKF Tasks repository root")
    parser.add_argument("--output-dir", help="Output directory (default: <root>/local-docs)")
    parser.add_argument("--check", action="store_true", help="Fail if either generated page is stale")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output_dir).resolve() if args.output_dir else root / "local-docs"
    for source_name, title, filename in PAGES:
        source = root / source_name
        records = read_records(source)
        graph = build_graph(records, read_documents(source, records))
        write_or_check(output / filename, generate_html(graph, title), args.check)
    verb = "Checked" if args.check else "Generated"
    print(f"{verb} {len(PAGES)} local documentation pages in {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
