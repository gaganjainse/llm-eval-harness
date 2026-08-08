"""Golden-set loading from YAML."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import yaml


@dataclass
class GoldenCase:
    id: str
    question: str
    golden_answer: str
    context: str
    answer: str = ""


@dataclass
class GoldenSet:
    name: str
    cases: List[GoldenCase] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "GoldenSet":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        cases = [
            GoldenCase(
                id=str(c.get("id", i)),
                question=c["question"],
                golden_answer=c.get("golden_answer", ""),
                context=c.get("context", ""),
                answer=c.get("answer", ""),
            )
            for i, c in enumerate(data.get("cases", []))
        ]
        return cls(name=data.get("name", Path(path).stem), cases=cases)
