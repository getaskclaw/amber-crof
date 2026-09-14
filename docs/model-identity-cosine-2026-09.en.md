# Model-identity fingerprints: nine-axis nearest-neighbor analysis of the CrofAI lanes (2026-09)

[中文](model-identity-cosine-2026-09.md)

## Bottom line

**Do not read these five CrofAI lanes by label alone.** Using only the published AMBER score matrices — no private cases and no transcripts — the strongest behavioral result is that crof `glm-5.3-flash` sits much closer to `deepseek-v4.1-flash @ ollama` than to either same-named Ollama `glm-5.3-flash` lane.

| crof endpoint | Behavioral read | Confidence |
|---|---|---|
| `glm-5.3-flash` | Fingerprint is closest to `deepseek-v4.1-flash @ ollama` on all three metrics; same-named GLM controls are much farther away. | **Strong corroboration** for a label/model mismatch |
| `qwen3.8-27b` | Case-level pattern is closest to `deepseek-v4-flash:0731 @ ollama` (21-case cosine .971); no same-named control exists. | **Suspicious, not proven** |
| `deepseek-v4-flash-0731` | Case-level nearest neighbor is the official DeepSeek lane (21-case cosine .970), but its standardized shape leans GPT-band and its review axis is the board's worst. | **Unresolved** |
| `deepseek-v4-flash-vision-exp` | No convincing match; the `vision` name is especially odd because its vision axis is the lowest in the field. | **No match** |
| `qwen3.5-9b` | No convincing match; weak overall profile. | **No match** |

This is behavioral evidence, not packet capture. It independently corroborates the public wire-level report for the GLM-labeled lane; it does not, by itself, prove CrofAI's routing.

## Why we ran this

On 2026-09-13, ktibow published a wire-level investigation, [*crof.ai is an OpenRouter wrapper*](https://kendell.dev/blog/crofaifalse/). The report says several crof.ai endpoints execute an OpenRouter-private tool and that multiple advertised models fingerprint as different upstream models — for example, `glm-5.2` behaving like DeepSeek V4 Flash.

Before using that report as context, we independently checked its primary evidence. The cited GitHub Actions probe runs exist, and the evidence file for `deepseek-v4-flash-0731` shows the OpenRouter-private tool being executed and an OpenRouter-style upstream model string returned.

This note asks a narrower question: **if we ignore the wire report and look only at benchmark behavior, which known lanes do CrofAI's score fingerprints most resemble?**

## Method

### Fingerprint

Each lane becomes a nine-axis completion vector over the 23-case set: the W36 21-case matrix plus the two W37 makeup cases.

- **Delivery**: A-791e90ac
- **Coding**: six build cases
- **Defense**: two verification cases
- **Attribution**: A-a317e74b
- **Review**: two d2-scored cases
- **Ops**: six cases
- **Requirement drift**: A-0676097b
- **UI build**: A-d9b79b46
- **Vision**: A-ea80d793

Pin-checked cases score as `green checks / total checks`. d2-scored cases normalize as `(d2 + 4) / 9`, matching the published face-profile convention. The script first re-derives four published reference vectors and verifies every axis to ±0.005 before computing similarity.

### Metrics

We use three complementary distances:

- **Raw nine-axis cosine**: overall scorecard similarity. Useful, but inflated because delivery, coding, ops, and requirement drift are saturated across many lanes.
- **z-scored nine-axis cosine**: the *shape* of strengths and weaknesses after standardizing each axis across all 32 lanes. This is the best fingerprint here because it asks which lane is unusually good or bad at the same things.
- **21-case completion-vector cosine**: case-by-case similarity over the subset every crof lane shares. This catches “passes and fails on the same papers” even when aggregate axes blur.

The reference field is the 27 published non-crof lanes across the seven sister repos. Missing cells drop out pairwise. `∅` infrastructure timeouts never enter an axis mean. crof `deepseek-v4-flash-0731`'s missing vision paper scores d2 = −2, the same non-delivery convention used for the GA lane's undelivered paper. `deepseek-v4-flash-vision-exp` and `qwen3.5-9b` ran only the 21-case subset, so their ops axis averages four cases.

## Results

### Raw nine-axis cosine — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` **.996** | `deepseek-v4.1-flash @ commandcode` .988 | `hy4-preview-f @ workbuddy` .986 |
| `qwen3.8-27b` | `deepseek-v4-flash:0731 @ ollama` **.992** | `luna-900k medium` .991 | `astra-900k xhigh` .988 |
| `deepseek-v4-flash-0731` | `luna-900k xhigh` .987 | `luna-900k high` .986 | `sol-900k high` .985 |
| `deepseek-v4-flash-vision-exp` | `deepseek-flash @ official GA` .956 | `deepseek-flash @ opencode-go` .954 | `deepseek-v4.1-flash @ workbuddy` .944 |
| `qwen3.5-9b` | `deepseek-flash @ official GA` .928 | `deepseek-flash @ opencode-go` .926 | `deepseek-v4-flash:0731 @ ollama` .923 |

### z-scored nine-axis cosine — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` **+.683** | `hy4-preview-f @ workbuddy` +.415 | `swe-2-medium @ devin` +.296 |
| `qwen3.8-27b` | `luna-900k medium` +.719 | `astra-900k xhigh` +.526 | `astra-900k max` +.526 |
| `deepseek-v4-flash-0731` | `luna-900k xhigh` +.807 | `sol-900k high` +.787 | `sol-900k medium` +.773 |
| `deepseek-v4-flash-vision-exp` | `swe-1-7-medium @ devin` +.318 | `sol-900k medium` +.286 | `luna-900k high` +.266 |
| `qwen3.5-9b` | `glm-5-2 @ devin` +.541 | `swe-1-7-medium @ devin` +.278 | `sol-900k medium` +.263 |

### 21-case completion-vector cosine — top 3

| crof lane | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` .943 | `hy4-preview-f @ workbuddy` .940 | `deepseek-v4.1-flash @ commandcode` .939 |
| `qwen3.8-27b` | `deepseek-v4-flash:0731 @ ollama` .971 | `luna-900k medium` .954 | `deepseek-flash @ official GA` .954 |
| `deepseek-v4-flash-0731` | `deepseek-flash @ official GA` .970 | `deepseek-flash @ opencode-go` .952 | `deepseek-v4-flash:0731 @ ollama` .948 |
| `deepseek-v4-flash-vision-exp` | `deepseek-flash @ official GA` .942 | `luna-900k xhigh` .937 | `luna-900k high` .937 |
| `qwen3.5-9b` | `deepseek-flash @ official GA` .912 | `deepseek-v4-flash:0731 @ ollama` .910 | `deepseek-flash @ opencode-go` .903 |

### Same-name identity checks

Metric order below is `raw nine-axis cosine / z-cosine / 21-case cosine`.

| crof endpoint | vs same-named controls | vs closest non-namesake |
|---|---|---|
| `glm-5.3-flash` | `glm-5.3-flash @ ollama` W36: .964 / +.097 / .932; W37 rerun: .853 / −.011 / .890 | `deepseek-v4.1-flash @ ollama`: **.996 / +.683 / .943** |
| `deepseek-v4-flash-0731` | `deepseek-v4-flash:0731 @ ollama`: .963 / +.186 / .948 | `deepseek-flash @ official GA`: .976 / +.567 / .970 |
| `qwen3.8-27b` | No same-named lane exists | `deepseek-v4-flash:0731 @ ollama`: .992 / +.353 / .971 |

Largest per-case gaps (|Δ| > 0.15, completion units):

- crof `glm-5.3-flash` vs Ollama `glm-5.3-flash` diverges on five cases: A-1fd3683a (0 vs 1.0), A-442d4aab (.143 vs 1.0), A-ea80d793 vision (.222 vs .778), A-a317e74b attribution (.533 vs .933), and A-cdc3d11a review (.222 vs .444). Against Ollama `deepseek-v4.1-flash`, only three cases diverge: A-1fd3683a, A-442d4aab, and A-cdc3d11a.
- crof `deepseek-v4-flash-0731` vs official GA diverges on two: A-cdc3d11a (−.889 vs 0, the worst review score on any lane) and A-61f7ad01 (.714 vs 1.0).
- crof `qwen3.8-27b` vs Ollama `d4f:0731` diverges on three: A-a5608487 (0 vs .8), A-be92627f (.333 vs .778), and A-47eea242 (.889 vs .667).

## Read-out

1. **`glm-5.3-flash` is the cleanest mismatch.** Its nearest neighbor on all three metrics is `deepseek-v4.1-flash @ ollama`. The z-cosine gap is especially informative: +.683 to the DeepSeek lane versus +.097 and −.011 to the two same-named GLM controls. In plain terms, its unusual strengths and weaknesses line up with DeepSeek V4.1 Flash, not with the model name on the endpoint. This points in the same direction as the wire-level report, while remaining a weaker kind of evidence.
2. **`qwen3.8-27b` is anomalous.** It is the only lane with a perfect attribution score (15/15 on A-a317e74b, the first such score ever) while also scoring zero on A-a5608487. Its case-level fingerprint is closest to `d4f:0731` (21-case cosine .971), although its z-shape is closer to the GPT-band lanes. A real 27B-class open model could be unusual, but this profile does not look like a routine same-name confirmation.
3. **`deepseek-v4-flash-0731` stays unresolved.** Case-level, it most resembles the official DeepSeek lane (21-case cosine .970), which is consistent with a real d4f-family model. But its review axis is the board's worst (−12 on A-cdc3d11a; axis value −0.056), and its standardized shape leans toward the luna/sol lanes (+.77 to +.81). A d4f-family upstream behind a proxy stack, a mid-window route change, or simple n=1 noise could all produce a blurred fingerprint like this.
4. **`deepseek-v4-flash-vision-exp` and `qwen3.5-9b` have no convincing identity match.** Saturated axes keep their raw cosines above .91, but their best z-cosines are only +.318 and +.541. The `vision-exp` result is especially awkward: the endpoint carries a vision label while posting the field's lowest vision-axis value (.111).

## What would change this conclusion

- A same-named control lane matching crof `glm-5.3-flash` on z-cosine and case-level behavior as closely as `deepseek-v4.1-flash @ ollama` does.
- A fresh rerun in which the crof endpoint reproduces namesake-specific behavior rather than the DeepSeek-family fingerprint.
- New wire-level evidence showing that the OpenRouter-private-tool result was an artifact rather than a routing signal.
- CrofAI publishing verifiable per-request provider/model attestations that contradict the observed fingerprints.

## Limits

- Each case has n=1; a single case gap is weak evidence. The signal is the aggregate pattern across axes and cases.
- Similar scores do not prove identical weights. Different models can converge on the same benchmark behavior, and a router, harness, or retry layer can also distort a lane.
- z-cosine measures *shape*, not absolute capability. Two models can share a shape at different levels.
- A mid-window upstream swap would blur the fingerprint in exactly the way several crof lanes are blurred.
- CrofAI's lineup and routing can change at any time. This is a snapshot of the W36-W37 windows (2026-09-06 to 2026-09-08 UTC).

## Reproduce

All inputs are the published per-case matrices in `results/` of this repo and the seven sister repos: `amber-ollama`, `amber-gpt`, `amber-devin`, `amber-deepseek`, `amber-commandcode`, `amber-opencode`, and `amber-workbuddy`.

Run [`model-identity-cosine-2026-09.py`](model-identity-cosine-2026-09.py). It performs the published-vector normalization check first, then prints the raw cosine, z-cosine, same-name checks, and per-case gaps.

*Independent community measurement; small sample; not procurement advice.*
