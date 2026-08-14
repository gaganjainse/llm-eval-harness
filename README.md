# LLM Eval Harness

Reusable **golden-set evaluation harness** for LLM/RAG systems: faithfulness,
answer relevance, and correctness metrics with **LLM-as-judge** when an API key is
available and **offline heuristic fallbacks** so evals run in CI for free.

## Features

- Golden-set YAML format: `question`, `golden_answer`, `context`, optional `answer`
- Metrics: **faithfulness**, **answer_relevance**, **correctness**
- Judge: OpenAI-compatible LLM-as-judge; automatic lexical fallback without a key
- JSON + Markdown reports with per-metric mean/min/max
- CLI: `python -m eval_harness --golden-set golden_sets/example.yaml`
- CI: `pytest` on every push (15 tests)

## Quick start

```bash
pip install -r requirements.txt
python -m eval_harness --golden-set golden_sets/example.yaml
```

Output:

```
Evaluated 3 cases -> eval-report.json / eval-report.md
  faithfulness: mean=0.456 min=0.333 max=0.579
  answer_relevance: mean=0.079 min=0.0 max=0.15
  correctness: mean=0.719 min=0.5 max=0.833
```

### Use an LLM judge (optional)

```bash
export OPENAI_API_KEY=sk-...
export LLM_MODEL=gpt-4o-mini
```

### Use it to gate a pipeline (CI)

```bash
python -m eval_harness --golden-set golden_sets/rag.yaml
python - <<'PY'
import json
r = json.load(open("eval-report.json"))
assert r["summary"]["faithfulness"]["mean"] >= 0.7, "faithfulness below threshold"
PY
```

## Golden-set format

```yaml
name: my-golden-set
cases:
  - id: c1
    question: "What is RAG?"
    golden_answer: "Retrieval-augmented generation grounds LLM answers in documents."
    context: "RAG combines retrieval with generation to ground answers."
```

Pair with [`rag-service`](https://github.com/gaganjainse/rag-service) to evaluate
end-to-end retrieval + generation quality.

## License

GPL-3.0-or-later
