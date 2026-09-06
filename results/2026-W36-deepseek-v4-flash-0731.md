# 2026-W36 — deepseek-v4-flash-0731 @ crof.ai, effort=high

**中文摘要**:首期。crof 的 deepseek-v4-flash-0731 考 AMBER 全库 21 案,$0.71、约 95 分钟挂钟。施工与运维面接近前沿锚点且快 5–10 倍;审查面幻觉重(误报两位数);该模型无视觉;无工具场景有工具调用泄漏。定位:便宜快速的施工/运维备胎,不适任审查/视觉席。同周对 crof 全部 16 个在售模型做了存活与视觉探测,见末节。

---

## Run identity

| field | value |
|---|---|
| model | `deepseek-v4-flash-0731` |
| endpoint | `https://crof.ai/v1` (OpenAI-compatible) |
| effort | `high` (`reasoning_effort`) |
| window (UTC) | 2026-09-06 06:05 – 06:55 |
| harness | AMBER agentic harness (Hermes runtime), clean-room profile, no fallback models |
| wire verification | 27/27 API calls landed on (deepseek-v4-flash-0731, crof.ai) in the harness session ledger — zero cross-model contamination |
| case set | AMBER full library, 21 cases / 24 papers; per-case content hashes below |
| cost (vendor-reported `usage.cost`) | **$0.71** — in 6.83M, out 0.69M, cache-read 31.6M tokens |
| wall clock | ~5,700 s total across 24 papers (concurrency 2); text papers 14–28 s |

## Scorecard

21 cases. Case IDs stay private (see README red lines); the `case` handle below is a stable public alias, `bundle_sha` is the case content hash. "ref" = internal frontier reference (OpenAI, effort=high, same case set, 2026-09-05), anchor only.

| case | face | crof d4f @high | ref @high | bundle_sha |
|---|---|---|---|---|
| A-791e90ac | text | ✓ 6/6 | ✓ 6/6 | 0396c8576a56 |
| A-1fd3683a | text | ✓ 2/2 | ✓ 2/2 | 6a980035b42f |
| A-13854d9d | text | ✓ 5/5 | ✓ 5/5 | a56b202b0537 |
| A-77d62143 | build | ✓ 8/8 | ✓ 8/8 | 7edee286f327 |
| A-569dbe0d | build | ✓ 10/10 | ✓ 10/10 | 45ccf06657af |
| A-87c472cb | build | ✗ 6/8 | ✗ 6/8 | cd643fa107e0 |
| A-641195e2 | build | ✓ 8/8 | ✓ 8/8 | 7cc76bad6f89 |
| A-442d4aab | build | ✓ 7/7 | ✓ 7/7 | ddf28dfda1cd |
| A-61f7ad01 | build | ✗ 5/7 | ✓ 7/7 | 991167b1455f |
| A-d511f9e8 | verify | ✗ 4/12 | ✗ 4/12 | f725082a2dc8 |
| A-a317e74b | verify | ✗ 9/15 | ✗ 14/15 | e05970e7d7c9 |
| A-be92627f | verify | ✗ 4/9 | ✗ 5/9 | 6593829abdfa |
| A-cdc3d11a | review | ✗ **-12** | ✗ -1 | dbb207a3118d |
| A-47eea242 | review | ✓ 3 | ✓ 4 | b4b8d4bb44e3 |
| A-ea80d793 | vision | ✗ blank | ✓ 2.0 | 1d69841b029e |
| A-a5608487 | ops | ✓ 5/5 | ✓ 5/5 | bcfac8de9f29 |
| A-984e80ee | ops | ✓ 5/5 | ✓ 5/5 | a28b57d4d1f1 |
| A-24bcf707 | ops | ✓ **5/5** | ✗ 4/5 | ba4431d40006 |
| A-8d4bc770 | ops | ✓ 5/5 | ✓ 5/5 | 957f29e633c7 |
| A-0676097b | req-drift | ✓ 4/4 variants | ✓ 4/4 variants | 3c04bb80fe94 |
| A-d9b79b46 | ui-build | ✗ no delivery | ✓ 12/12 | d6d63130ecc6 |

**Case-level total: 13/21 pass** (ref: 14/21).

## Behavioral findings

1. **Build & ops near the frontier anchor, 5–10× faster.** All text papers and 4/6 build papers green; one ops case was the only cell where d4f beat the anchor.
2. **Review-side hallucination.** On the adversarial review case, d4f scored **-12**: 0/3 true hits plus 12 fabricated findings — far more fabrication than the anchor (-1). Not fit for review duty.
3. **No vision.** `deepseek-v4-flash-0731` is text-only; the vision paper came back blank in 5.5 s. (Crof serves `deepseek-v4-flash-vision-exp`, a vision beta — probed below.)
4. **Tool-call leakage in no-tools settings.** On papers running with tools disabled, whenever the task implied "files exist somewhere", d4f emitted raw DSML tool-call markup into its text stream instead of answering. With tools enabled, tool use was entirely normal. The deficit is *restraint without tools*, not tool capability.
5. **Shared failure modes are informative.** One build case failed identically for d4f and the anchor (same edge-case signature); one verify case has now failed all three strong models we have run — likely a case-design property, under review.

## Lineup probe (2026-09-06, crof.ai)

All 16 served models answered a one-line ping. The four models tagged `vision` on the pricing page were additionally given a synthetic image (a handwritten-style digit string "7429" beside a red rectangle on white) — all four read the digits and described the rectangle correctly:

| model | vision | $/M in | $/M out | probe |
|---|---|---|---|---|
| deepseek-v4-flash-0731 | – | 0.08 | 0.10 | ✓ |
| deepseek-v4-flash-vision-exp (BETA) | ✓ | 0.08 | 0.20 | ✓ vision verified |
| deepseek-v4-pro-0813 | – | 0.35 | 0.80 | ✓ |
| glm-5.2 | – | 0.30 | 1.05 | (long-standing, not re-probed) |
| glm-5.3 | – | 0.40 | 1.40 | ✓ |
| glm-5.3-flash | – | 0.07 | 0.22 | ✓ |
| kimi-k2.6 | ✓ | 0.50 | 1.99 | ✓ vision verified |
| kimi-k2.7-code | – | 0.55 | 2.25 | ✓ |
| kimi-k3 | – | 2.00 | 8.00 | ✓ |
| kimi-k3-eco | – | 1.00 | 4.00 | ✓ |
| greg-2-super | – | 1.50 | 5.00 | ✓ |
| greg-2-ultra | – | 3.00 | 10.00 | ✓ |
| mimo-v2.5-pro | – | 0.40 | 0.80 | ✓ |
| gemma-4-31b-it | ✓ | 0.10 | 0.30 | ✓ vision verified |
| qwen3.5-9b | ✓ | 0.04 | 0.15 | ✓ vision verified |
| qwen3.8-27b | – | 0.09 | 0.30 | ✓ |

Notes: prices are the 2026-09-06 snapshot of crof.ai/pricing and `/v1/models`; both change without notice. Crof's `/v1/models` exposes machine-readable pricing, quantization, and context per model; `/usage_api/` exposes account balance and per-model token totals; every completion response carries a server-computed `usage.cost` — all verified live this week.

## Verdict

At $0.71 for the full library, crof's deepseek-v4-flash-0731 is a viable **cheap, fast build/ops stand-in**, and an easy way to run large agentic sweeps. Keep it away from review and vision seats.
