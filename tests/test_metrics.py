"""Unit tests for metrics with the offline heuristic judge."""

from __future__ import annotations

import os

os.environ["OPENAI_API_KEY"] = ""  # force heuristic judge

import pytest

from eval_harness.judge import Judge, token_overlap
from eval_harness.metrics import Metrics


@pytest.fixture
def metrics() -> Metrics:
    return Metrics()


def test_token_overlap_identical():
    assert token_overlap("hello world", "hello world") == 1.0


def test_token_overlap_disjoint():
    assert token_overlap("alpha beta", "gamma delta") == 0.0


def test_token_overlap_partial():
    assert 0.0 < token_overlap("alpha beta gamma", "alpha beta omega") < 1.0


def test_judge_pair_heuristic():
    j = Judge()
    assert j.score_pair("cats like fish", "cats like fish and milk") > 0.5
    assert j.score_pair("cats like fish", "quantum physics") < 0.5


def test_faithfulness_grounded():
    m = Metrics()
    r = m.faithfulness("VIT is a university in India", "VIT is a university in India with strong CS")
    assert r.name == "faithfulness"
    assert 0.0 <= r.score <= 1.0


def test_faithfulness_unrelated():
    m = Metrics()
    r = m.faithfulness("Rust has ownership semantics", "The Eiffel tower is in Paris")
    assert r.score < 0.5


def test_answer_relevance():
    m = Metrics()
    good = m.answer_relevance("What is RAG?", "RAG grounds answers in retrieved documents")
    bad = m.answer_relevance("What is RAG?", "I like pizza")
    assert good.score > bad.score


def test_correctness_golden():
    m = Metrics()
    r = m.correctness("FastAPI is a web framework", "FastAPI is a web framework for APIs")
    assert r.score > 0.3


def test_evaluate_returns_three_metrics():
    m = Metrics()
    results = m.evaluate("Q", "golden", "context", "answer")
    assert [r.name for r in results] == ["faithfulness", "answer_relevance", "correctness"]
    assert all(0.0 <= r.score <= 1.0 for r in results)
