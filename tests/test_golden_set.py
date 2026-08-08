"""Tests for golden-set loading and report building."""

from __future__ import annotations

import json

from eval_harness.golden_set import GoldenSet
from eval_harness.report import build_report, write_json, write_markdown


def test_golden_set_from_yaml(tmp_path):
    f = tmp_path / "golden.yaml"
    f.write_text(
        """
name: demo
cases:
  - id: c1
    question: What is RAG?
    golden_answer: Retrieval augmented generation
    context: RAG grounds LLM answers in retrieved documents.
  - id: c2
    question: What is an agent?
    golden_answer: An agent uses tools to complete tasks
    context: Agents call tools and observe results.
""",
        encoding="utf-8",
    )
    gs = GoldenSet.from_yaml(f)
    assert gs.name == "demo"
    assert len(gs.cases) == 2
    assert gs.cases[0].id == "c1"
    assert gs.cases[0].question == "What is RAG?"


def test_golden_set_empty():
    f = "/nonexistent.yaml"
    import pytest

    with pytest.raises(FileNotFoundError):
        GoldenSet.from_yaml(f)


def test_build_report_summary():
    rows = [
        {"id": "c1", "faithfulness": 0.8, "answer_relevance": 0.7},
        {"id": "c2", "faithfulness": 0.6, "answer_relevance": 0.9},
    ]
    report = build_report(rows)
    assert report["cases"] == 2
    assert report["summary"]["faithfulness"]["mean"] == 0.7
    assert report["summary"]["answer_relevance"]["max"] == 0.9


def test_build_report_empty():
    report = build_report([])
    assert report["cases"] == 0
    assert report["summary"] == {}


def test_write_json(tmp_path):
    out = tmp_path / "report.json"
    write_json(build_report([{"id": "c1", "faithfulness": 0.5}]), out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["cases"] == 1


def test_write_markdown(tmp_path):
    out = tmp_path / "report.md"
    write_markdown(build_report([{"id": "c1", "faithfulness": 0.5}]), out)
    md = out.read_text(encoding="utf-8")
    assert "Evaluation Report" in md
    assert "faithfulness" in md
