# Model-identity fingerprints: nine-axis nearest-neighbor analysis of the CrofAI lanes (2026-09)

[中文](model-identity-cosine-2026-09.md)

## Why we ran this

On 2026-09-13 a third-party wire-level investigation — [ktibow, *crof.ai is an OpenRouter wrapper*](https://kendell.dev/blog/crofaifalse/) — reported that several crof.ai endpoints honor an OpenRouter-private tool and that multiple advertised models fingerprint as different upstream models (its `glm-5.2` behaving as DeepSeek V4 Flash, for example). That is wire evidence. This note is the independent **behavioral** counterpart: using only published AMBER score matrices, which known lanes do crof's five models most resemble?

We sanity-checked the report's primary evidence before running this analysis: the probe runs it cites exist, and the per-model evidence file for `deepseek-v4-flash-0731` does show the OpenRouter-private tool being executed and an OpenRouter-style upstream model string returned.

## Method

- **Vector**: each lane becomes a 9-axis completion vector over the 23-case set (W36 21-case matrix + W37 2-case makeup). Axes: delivery (A-791e90ac), coding (6 build cases), defense (2 verify cases), attribution (A-a317e74b), review (2 d2-scored cases), ops (6 cases), req-drift (A-0676097b), UI build (A-d9b79b46), vision (A-ea80d793).
- **Scoring**: pin-checked cases → green checks / total; d2-scored cases → (d2 + 4) / 9 — the same normalization used in the published face profiles.
- **Metrics**: raw 9-axis cosine; z-scored cosine (axes standardized across all 32 lanes — needed because saturated axes push raw cosine above 0.9 for almost every pair); and cosine over the 21-case completion vector all crof lanes share.
- **Field**: the 27 published non-crof lanes across the seven sister repos.
- Missing cells drop out pairwise. `∅` infra timeouts never enter an axis mean. crof `deepseek-v4-flash-0731`'s missing vision paper scores d2 = −2 (non-delivery), the same convention as the GA lane's undelivered paper. `deepseek-v4-flash-vision-exp` and `qwen3.5-9b` ran the 21-case subset only, so their ops axis averages 4 cases.

## Results

### Raw 9-axis cosine — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama **.996** | deepseek-v4.1-flash @ commandcode .988 | hy4-preview-f @ workbuddy .986 |
| qwen3.8-27b | deepseek-v4-flash:0731 @ ollama **.992** | luna-900k medium .991 | astra-900k xhigh .988 |
| deepseek-v4-flash-0731 | luna-900k xhigh .987 | luna-900k high .986 | sol-900k high .985 |
| deepseek-v4-flash-vision-exp | deepseek-flash @ official GA .956 | deepseek-flash @ opencode-go .954 | deepseek-v4.1-flash @ workbuddy .944 |
| qwen3.5-9b | deepseek-flash @ official GA .928 | deepseek-flash @ opencode-go .926 | deepseek-v4-flash:0731 @ ollama .923 |

### z-scored cosine (shape of strengths) — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama **+.683** | hy4-preview-f @ workbuddy +.415 | swe-2-medium @ devin +.296 |
| qwen3.8-27b | luna-900k medium +.719 | astra-900k xhigh +.526 | astra-900k max +.526 |
| deepseek-v4-flash-0731 | luna-900k xhigh +.807 | sol-900k high +.787 | sol-900k medium +.773 |
| deepseek-v4-flash-vision-exp | swe-1-7-medium @ devin +.318 | sol-900k medium +.286 | luna-900k high +.266 |
| qwen3.5-9b | glm-5-2 @ devin +.541 | swe-1-7-medium @ devin +.278 | sol-900k medium +.263 |

### 21-case completion-vector cosine — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama .943 | hy4-preview-f @ workbuddy .940 | deepseek-v4.1-flash @ commandcode .939 |
| qwen3.8-27b | deepseek-v4-flash:0731 @ ollama .971 | luna-900k medium .954 | deepseek-flash @ official GA .954 |
| deepseek-v4-flash-0731 | deepseek-flash @ official GA .970 | deepseek-flash @ opencode-go .952 | deepseek-v4-flash:0731 @ ollama .948 |
| deepseek-v4-flash-vision-exp | deepseek-flash @ official GA .942 | luna-900k xhigh .937 | luna-900k high .937 |
| qwen3.5-9b | deepseek-flash @ official GA .912 | deepseek-v4-flash:0731 @ ollama .910 | deepseek-flash @ opencode-go .903 |

### Same-name identity checks

| crof endpoint | vs the same-named lane | vs its closest look-alike |
|---|---|---|
| glm-5.3-flash | glm-5.3-flash @ ollama: cos .964 / z +.097 / 21c .932 | deepseek-v4.1-flash @ ollama: cos **.996** / z **+.683** / 21c .943 |
| deepseek-v4-flash-0731 | deepseek-v4-flash:0731 @ ollama: cos .963 / z +.186 / 21c .948 | deepseek-flash @ official GA: cos .976 / z +.567 / 21c .970 |
| qwen3.8-27b | (no same-named lane exists) | deepseek-v4-flash:0731 @ ollama: cos .992 / z +.353 / 21c .971 |

Largest per-case gaps (|Δ| > 0.15, completion units):

- crof `glm-5.3-flash` vs ollama `glm-5.3-flash` — five cases diverge: A-1fd3683a (0 vs 1.0), A-442d4aab (.143 vs 1.0), A-ea80d793 vision (.222 vs .778), A-a317e74b attribution (.533 vs .933), A-cdc3d11a review (.222 vs .444). Against ollama `deepseek-v4.1-flash` only three diverge: A-1fd3683a, A-442d4aab, A-cdc3d11a.
- crof `deepseek-v4-flash-0731` vs official GA — two: A-cdc3d11a (−.889 vs 0, the worst review score on any lane) and A-61f7ad01 (.714 vs 1.0).
- crof `qwen3.8-27b` vs ollama `d4f:0731` — three: A-a5608487 (0 vs .8), A-be92627f (.333 vs .778), A-47eea242 (.889 vs .667).

## Read-out

1. **crof `glm-5.3-flash` behaves like a DeepSeek V4.1-Flash-family model, not like its namesake.** Its nearest neighbor on all three metrics is `deepseek-v4.1-flash @ ollama` (raw .996; z +.683 — the strongest z-match of any crof lane), while it sits five cases away from ollama's same-named glm-5.3-flash (z +.097). Same direction as the wire-level finding that crof's GLM-labeled endpoint serves DeepSeek-family weights — though scores alone cannot prove routing.
2. **crof `qwen3.8-27b` does not look like a 27B-class open model.** It holds the lane's only perfect attribution score (15/15, the first ever on that case) yet zeroes A-a5608487 — a profile whose closest match is again the d4f family (21c .971 vs ollama d4f:0731). A mid-size open model topping the board on the hardest verify case would be a first.
3. **crof `deepseek-v4-flash-0731` stays ambiguous.** Case-level it is closest to the official GA lane (21c .970) — consistent with a real d4f — but its review axis is the board's worst (A-cdc3d11a = −12, axis −0.056) and its z-shape leans GPT-band (luna/sol, +.77–.81). Possibly a d4f-family model behind a proxy stack, with the review anomaly as noise or a routing artifact. Scores alone cannot resolve it.
4. **`deepseek-v4-flash-vision-exp` and `qwen3.5-9b` form a weak cluster with no convincing match.** Saturated axes keep raw cosine ≥ .91, but z-cos tops out at +.32 / +.54 — no lane's shape. Notably `vision-exp` posts the lane's *lowest* vision axis (.111) despite the name.

## Limits

- n=1 per case; single-case gaps are weak evidence — the aggregate pattern is the signal.
- Behavioral similarity is corroboration, not wire-level proof. A mid-window upstream swap would blur the fingerprint exactly the way these are blurred.
- z-cos measures *shape* (which axes a lane is relatively strong or weak on), not absolute level; two models can share a shape at different magnitudes.
- CrofAI's lineup and routing can change at any time. This is a snapshot of the W36–W37 windows (2026-09-06 → 09-08 UTC).

## Reproduce

All inputs are the published per-case matrices in `results/` of this repo and the seven sister repos (`amber-ollama`, `amber-gpt`, `amber-devin`, `amber-deepseek`, `amber-commandcode`, `amber-opencode`, `amber-workbuddy`). The script is [`model-identity-cosine-2026-09.py`](model-identity-cosine-2026-09.py) — it re-derives four published reference vectors as a normalization check before computing any similarity.

*Independent community measurement; small sample; not procurement advice.*
