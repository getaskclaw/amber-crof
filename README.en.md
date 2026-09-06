# amber-crof

Public weekly benchmark results of [CrofAI](https://crof.ai/) models against the private AMBER case suite.

[中文 README](README.md)

## What this is

- Weekly (plus ad-hoc) runs of the AMBER agentic case suite (build / ops / review / vision / requirement-drift) against models served by crof.ai. **Results are always public; the cases never are.**
- AMBER spec and case-authoring tools live at [getaskclaw/amber-eval](https://github.com/getaskclaw/amber-eval); the case contents themselves are private.
- We are paying CrofAI customers, unaffiliated with the vendor. This is an independent community measurement.

## Publishing red lines (a violation means retract-and-correct)

1. **We publish**: scores, aggregates, cost, speed, and qualitative behavioral verdicts.
2. **We never publish**: case contents, raw model transcripts, or grading oracles. Model outputs can echo the prompts, so raw outputs never leave the private zone.
3. **Every issue pins**: model id, effort, UTC time window, harness identity, and per-case bundle hashes — checkable against the public hash manifest in amber-eval, so anyone can verify the case set did not change.
4. **Case IDs and suite structure stay private**: public results refer to cases only by stable aliases (A-xxxxxxxx, hash-derived) plus bundle hashes; internal case IDs, variant names, and task descriptions never appear.
5. **Tone = community measurement**: we report numbers and observed behavior, we don't attack vendors; findings are reproduced before publication.

## How to read results

- One case, one paper; a case passes only when all required checks are green (bonus checks excluded). Multi-variant cases pass only if every variant is green.
- n=1 single runs; noise exists. Occasional empty responses are retried per protocol and annotated in the issue.
- Cost uses the server-side `usage.cost` field returned by crof. Prices are snapshots from crof.ai/pricing at publication time; the live page wins.

## Results index

| Issue | Model | Verdict |
|---|---|---|
| [2026-W36](results/2026-W36-deepseek-v4-flash-0731.md) | deepseek-v4-flash-0731 @ high | 13/21 cases pass; $0.71; build/OPS near frontier anchor and much faster, but heavy review hallucination, no vision, tool-call leakage in no-tools settings |

## Disclaimer

Independent, small-sample testing; not procurement advice. Lineup and pricing change without notice — see [crof.ai/pricing](https://crof.ai/pricing).
