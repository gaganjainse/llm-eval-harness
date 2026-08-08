"""LLM-as-judge with offline heuristic fallbacks.

The judge tries an OpenAI-compatible chat endpoint when OPENAI_API_KEY is set;
otherwise it uses deterministic lexical scorers so evals run in CI for free.
"""

from __future__ import annotations

import os
import re
from typing import Callable, List

import httpx


def _tokens(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def token_overlap(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _call_openai(messages: List[dict], temperature: float = 0.0) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    resp = httpx.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


class Judge:
    """Score a claim/reference pair. LLM-as-judge when a key exists, else heuristics."""

    def __init__(self, llm_call: Callable[[List[dict], float], str] | None = None) -> None:
        self._llm = llm_call or _call_openai

    def _use_llm(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def score_pair(self, premise: str, hypothesis: str) -> float:
        """Return 0..1 for how well hypothesis is supported by premise."""
        if self._use_llm():
            prompt = (
                "You are an evaluator. On a scale 0-1, score how well the ANSWER "
                "is supported by the CONTEXT. Reply with only a number.\n\n"
                f"CONTEXT:\n{premise}\n\nANSWER:\n{hypothesis}"
            )
            try:
                raw = self._llm([{"role": "user", "content": prompt}], 0.0)
                val = float(re.sub(r"[^0-9.]", "", raw))
                return max(0.0, min(1.0, val))
            except Exception:
                pass
        # heuristic fallback
        return token_overlap(premise, hypothesis)

    def score_answer_relevance(self, question: str, answer: str) -> float:
        if self._use_llm():
            prompt = (
                "You are an evaluator. On a scale 0-1, how relevant is the ANSWER "
                "to the QUESTION? Reply with only a number.\n\n"
                f"QUESTION:\n{question}\n\nANSWER:\n{answer}"
            )
            try:
                raw = self._llm([{"role": "user", "content": prompt}], 0.0)
                return max(0.0, min(1.0, float(re.sub(r"[^0-9.]", "", raw))))
            except Exception:
                pass
        return token_overlap(question, answer)
