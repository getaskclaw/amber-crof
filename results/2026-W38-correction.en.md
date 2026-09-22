# 2026-W38 correction notice — amber-crof: additive correction to published scores

> 中文版:[2026-W38-correction.md](2026-W38-correction.md)

**Summary**: this notice rewrites no past issue; it **appends** one set of adjudicated results. AMBER ran a full-library review of its published 2026-09 scores: some failures previously counted were adjudged a **bench-side** problem rather than a model-capability problem, and for some papers the evidence was incomplete and the conclusion stays open. This notice lists both classes cell by cell — the **reversals** and the **holds** — with the review method and the guardrails that follow. **No balanced books, no board**: papers with incomplete evidence are named and removed from the board, and enter no aggregate. Past issues stay as published; reversals take effect through this notice.

## 1. Scope of this correction

- Count for this repo in this notice: **0 standalone published cells reversed · 6 standalone published cells held** (count = standalone published cells = actual table rows).
- **Scope in one line**: 6 standalone matrix cells of the W36 five-model matrix are held; the lane is frozen, so a re-exam is infeasible for now.
- Horizon: adjudication signed 2026-09-22; this repo's published numbers stop at 2026-09-21, i.e. a **pre-adjudication** snapshot.
- Unchanged: questions, oracles, transcripts and intermediate artifacts are never published; the alias and bundle_sha handles are unchanged.
- Nature of this notice: **additive**. Past conclusions are not withdrawn, deleted or rewritten; reversals take effect through this appendix.

## 2. Reversal table (adjudicated)

None. This repo has no adjudicated cell.

## 3. Hold table (named, undecided)

| Alias | bundle_sha | Issue | Previous | Status | Action |
|---|---|---|---|---|---|
| A-ea80d793 | `1d69841b029e` | W36 | d4f column blank | held (re-exam pending) | named and removed from the board; no re-exam while the lane is frozen; excluded from all aggregates pending re-exam |
| A-d9b79b46 | `d6d63130ecc6` | W36 | d4f column ✗ | held (re-exam pending) | same |
| A-cdc3d11a | `dbb207a3118d` | W36 | g53f column ✗ -2 | held (re-exam pending) | same |
| A-ea80d793 | `1d69841b029e` | W36 | q35 column ✗ -3 | held (re-exam pending) | same |
| A-cdc3d11a | `dbb207a3118d` | W36 | q38 column ✗ -2 | held (re-exam pending) | same |
| A-ea80d793 | `1d69841b029e` | W36 | q38 column ✗ -2 | held (re-exam pending) | same |

> No re-exam while the lane is frozen.

## 4. Method

## Method: why we correct, how we checked, how we prevent

**Why we correct.**
These are our published numbers; if they are wrong, we are the ones who fix them. This review
found that some published failures were not the model failing the task, but the bench side —
a pre-scoring step cut off a healthy attempt, and the paper was recorded as a model failure.
Errors run both ways: judging good work as bad, and bad work as good. We checked both.
The point of a correction is not to look better or worse; it is to make the numbers on the
board match what actually happened.

**How we checked.**
Every paper was independently re-verified by multiple seats. Verifiers read the raw record
first-hand (the attempt log, the scorer output, the ledger timestamps, the fix commit) and
accepted no second-hand conclusion. Two independent directions worked in parallel — one
looking for wrongful failures, one looking for what was missed — and only papers where both
agreed went to adjudication; disagreements were held. Each verdict rests on the same evidence
chain and is re-computable paper by paper, with a signed confirmation on file. Outcomes fall
into four classes: exonerated (cause on the bench side; the capability score is withheld),
confirmed (a genuine model-side failure), held (evidence incomplete — **no quiet conviction
and no quiet pardon**), and report-level corrections that leave history untouched.

**How we prevent it.**
Three small things, one line each: ① **Evidence chain** — each paper's raw process is
recorded out of the driver's reach, append-only and sealed at the end; scoring trusts evidence
completeness only. Cause of death is a conclusion, not a fact — it can be recomputed from the
evidence, and when a rule is wrong we fix the rule and recompute; the raw facts never move.
② **Reconciliation gate** — papers in must equal papers out (scored + bench + held; no bucket
missing, no cell extra). **No balanced books, no board** — there is no "publish first, patch
later." ③ **Brain-identity double-check** — an identity assertion per paper, and no assertion
means no score; we also re-check *passed* papers against the reverse error.
No set of controls stops everything (hardware breaks), but it can make a bad verdict live
less than one reconciliation cycle.

**In one line.** What we sell is not a bench that never errs — it is one that cannot walk away
from a wrong call.

## 5. What comes next

- The remaining held papers go through re-exam / final adjudication; a re-exam may record **"undecided", never "brain too weak"** — a re-exam decides only once the environment differences are enumerated to zero, otherwise a reproduction is not an attribution.
- Once the fixes and guardrails land, affected case-level headlines will move with the next regular issue; reversals **do not retroactively rewrite** past issues — the original cell only gets a pointer mark.
- Sister repos are in step via each repo's README results index.

