"""Evaluation metrics: faithfulness, answer relevance, correctness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .judge import Judge, token_overlap


@dataclass
class MetricResult:
    name: str
    score: float
    detail: str = ""


class Metrics:
    def __init__(self, judge: Judge | None = None) -> None:
        self.judge = judge or Judge()

    def faithfulness(self, context: str, answer: str) -> MetricResult:
        """How well the answer is grounded in the retrieved context."""
        score = self.judge.score_pair(context, answer)
        return MetricResult("faithfulness", round(score, 3))

    def answer_relevance(self, question: str, answer: str) -> MetricResult:
        """How relevant the answer is to the question."""
        score = self.judge.score_answer_relevance(question, answer)
        return MetricResult("answer_relevance", round(score, 3))

    def correctness(self, golden_answer: str, answer: str) -> MetricResult:
        """Lexical similarity against the golden answer (exact/semantic-free baseline)."""
        return MetricResult("correctness", round(token_overlap(golden_answer, answer), 3))

    def evaluate(
        self, question: str, golden_answer: str, context: str, answer: str
    ) -> List[MetricResult]:
        return [
            self.faithfulness(context, answer),
            self.answer_relevance(question, answer),
            self.correctness(golden_answer, answer),
        ]
