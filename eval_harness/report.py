"""Evaluation report builders (JSON + Markdown)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from .metrics import MetricResult


def build_report(rows: List[dict]) -> dict:
    """Aggregate per-case metric rows into a summary report."""
    metric_names = [m for m in rows[0] if m != "id"] if rows else []
    summary = {}
    for name in metric_names:
        values = [row[name] for row in rows]
        summary[name] = {
            "mean": round(sum(values) / len(values), 3) if values else 0.0,
            "min": round(min(values), 3) if values else 0.0,
            "max": round(max(values), 3) if values else 0.0,
        }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases": len(rows),
        "summary": summary,
        "rows": rows,
    }


def write_json(report: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2), encoding="utf-8")


def write_markdown(report: dict, path: str | Path) -> None:
    lines = [
        "# Evaluation Report",
        "",
        f"- **Generated:** {report['generated_at']}",
        f"- **Cases:** {report['cases']}",
        "",
        "## Summary",
        "",
        "| Metric | Mean | Min | Max |",
        "|---|---|---|---|",
    ]
    for name, stats in report["summary"].items():
        lines.append(f"| {name} | {stats['mean']} | {stats['min']} | {stats['max']} |")
    lines += ["", "## Per-case", ""]
    for row in report["rows"]:
        parts = " · ".join(f"{k}={v}" for k, v in row.items())
        lines.append(f"- {parts}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
