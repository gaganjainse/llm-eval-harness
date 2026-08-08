"""CLI: python -m eval_harness --golden-set golden_sets/example.yaml"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .golden_set import GoldenSet
from .metrics import Metrics
from .report import build_report, write_json, write_markdown


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="LLM evaluation harness")
    parser.add_argument("--golden-set", required=True, type=Path, help="Path to golden-set YAML")
    parser.add_argument("--out-json", type=Path, default=Path("eval-report.json"))
    parser.add_argument("--out-md", type=Path, default=Path("eval-report.md"))
    args = parser.parse_args(argv)

    golden = GoldenSet.from_yaml(args.golden_set)
    metrics = Metrics()
    rows = []
    for case in golden.cases:
        results = metrics.evaluate(case.question, case.golden_answer, case.context, case.answer)
        row = {"id": case.id}
        for r in results:
            row[r.name] = r.score
        rows.append(row)

    report = build_report(rows)
    write_json(report, args.out_json)
    write_markdown(report, args.out_md)

    print(f"Evaluated {report['cases']} cases -> {args.out_json} / {args.out_md}")
    for name, stats in report["summary"].items():
        print(f"  {name}: mean={stats['mean']} min={stats['min']} max={stats['max']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
