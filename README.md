# 🎯 llm-eval-harness

> **Golden-set evaluation harness for LLM/RAG systems.** Faithfulness, answer
> relevance, and correctness with **LLM-as-judge** when an API key is present and
> **offline heuristic fallbacks** so evals run in CI for free.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python) ![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue?style=for-the-badge) ![Tests](https://img.shields.io/badge/Tests-15-success?style=for-the-badge) ![CI](https://github.com/gaganjainse/llm-eval-harness/actions/workflows/ci.yml.yml/badge.svg)

- **License:** GPL-3.0-or-later
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Stack:** Python, YAML golden sets, OpenAI-compatible judge

---

## Why this repo exists

Pair with [rag-service](https://github.com/gaganjainse/rag-service) to evaluate
end-to-end retrieval + generation quality against a committed golden set, with
CI-ready JSON/Markdown reports.

---

## Quick start

```bash
pip install -r requirements.txt
python -m eval_harness --golden-set golden_sets/example.yaml
```

Optional LLM judge:

```bash
export OPENAI_API_KEY=sk-...
export LLM_MODEL=gpt-4o-mini
```

## Features

- Golden-set YAML: `question`, `golden_answer`, `context`, optional `answer`
- Metrics: **faithfulness**, **answer_relevance**, **correctness**
- LLM-as-judge with automatic lexical fallback when no key is set
- JSON + Markdown reports with per-metric mean/min/max

## Testing

```bash
pytest -q               # 15 tests
```

## Status

Component CI is green (reusable ecosystem pipeline). Security posture and
vulnerability reporting: [SECURITY.md](SECURITY.md).

## Documentation index

- **Part of:** [shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem)
- **Compiled reading:** [shesh-docs](https://github.com/gaganjainse/shesh-docs)

## License

GPL-3.0-or-later — see [LICENSE](LICENSE).
