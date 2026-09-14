# 模型身份指纹：CrofAI 五道模型的九轴最近邻分析（2026-09）

[English](model-identity-cosine-2026-09.en.md)

## 结论先行

**这五条 CrofAI 车道不能按名字直接当身份读。** 在只看已发布 AMBER 成绩矩阵、不接触私有题目和原始回复的前提下，最强的行为证据是：crof `glm-5.3-flash` 与 `deepseek-v4.1-flash @ ollama` 的相似度，明显高于它与两条同名 Ollama `glm-5.3-flash` 车道的相似度。

| crof 端点 | 行为侧判读 | 证据强度 |
|---|---|---|
| `glm-5.3-flash` | 三种度量下都最像 `deepseek-v4.1-flash @ ollama`；离两条同名 GLM 对照道明显更远。 | **强旁证**：支持「标签与实际模型不一致」 |
| `qwen3.8-27b` | 逐案指纹最像 `deepseek-v4-flash:0731 @ ollama`（21 案余弦 .971）；没有同名对照道。 | **可疑，但未坐实** |
| `deepseek-v4-flash-0731` | 逐案最像 DeepSeek 官方道（21 案余弦 .970），但标准化形状偏 GPT 档，审查轴还是全场最差。 | **未决** |
| `deepseek-v4-flash-vision-exp` | 没有可信匹配；名字叫 vision，视觉轴却是全场最低。 | **无匹配** |
| `qwen3.5-9b` | 没有可信匹配；整体偏弱。 | **无匹配** |

本文是行为证据，不是抓包证据。它对公开 wire 级报告中的 GLM 端点结论形成独立旁证；但仅凭成绩矩阵，不能证明 CrofAI 的实际路由。

## 为什么做这次分析

2026-09-13，ktibow 发布了 wire 级取证报告 [《crof.ai is an OpenRouter wrapper》](https://kendell.dev/blog/crofaifalse/)。报告称，多个 crof.ai 端点会执行 OpenRouter 私有工具，且有若干在售模型的指纹指向完全不同的上游模型，例如 `glm-5.2` 的行为更像 DeepSeek V4 Flash。

动笔前，我们先独立复核了报告的关键证据：其引用的 GitHub Actions 探针 run 真实存在；`deepseek-v4-flash-0731` 的证据文件也确实记录了 OpenRouter 私有工具被执行，并返回了 OpenRouter 风格的上游模型名。

本文回答的是一个更窄的问题：**如果完全不看 wire 报告，只看 benchmark 行为，CrofAI 的成绩指纹最像哪条已知车道？**

## 方法

### 指纹构造

每条车道在 23 案集合上变成一个九轴完成度向量：W36 的 21 案矩阵，加上 W37 补考的 2 案。

- **交付**：A-791e90ac
- **编码**：6 个施工案
- **防御**：2 个核验案
- **归因**：A-a317e74b
- **审查**：2 个 d2 案
- **运维**：6 案
- **需求漂移**：A-0676097b
- **UI 施工**：A-d9b79b46
- **视觉**：A-ea80d793

钉案按「绿钉／总钉数」计分；d2 案按 `(d2 + 4) / 9` 归一，与已发布案面画像同口径。脚本先复算四个已发布参考向量，并把所有轴校验到 ±0.005 以内，然后才计算相似度。

### 三种度量

- **九轴原始余弦**：看整张成绩单的相似度。可用，但会偏高，因为交付、编码、运维、需求漂移在很多车道上都接近满分。
- **九轴 z 化余弦**：把每个轴按全部 32 条车道标准化后，比较「相对强弱形状」。这是这里最有区分度的指纹——它问的是：哪些不寻常的强项和弱项长得一样。
- **21 案逐案余弦**：在五条 crof 道共有的 21 案上比较逐案完成度。它能捕捉「在同一些卷子上过／挂」，即使聚合轴已经糊掉。

对照场是七个姐妹仓里的 27 条已发布非 crof 车道。缺格按成对剔除；`∅` 基建超时不进轴均值；crof `deepseek-v4-flash-0731` 缺考的视觉卷按 d2 = −2 计（未交付），与 GA 道未交付卷同口径；`deepseek-v4-flash-vision-exp` 和 `qwen3.5-9b` 只跑了 21 案子集，因此运维轴只按 4 案取均值。

## 结果

### 九轴原始余弦 top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` **.996** | `deepseek-v4.1-flash @ commandcode` .988 | `hy4-preview-f @ workbuddy` .986 |
| `qwen3.8-27b` | `deepseek-v4-flash:0731 @ ollama` **.992** | `luna-900k medium` .991 | `astra-900k xhigh` .988 |
| `deepseek-v4-flash-0731` | `luna-900k xhigh` .987 | `luna-900k high` .986 | `sol-900k high` .985 |
| `deepseek-v4-flash-vision-exp` | `deepseek-flash @ official GA` .956 | `deepseek-flash @ opencode-go` .954 | `deepseek-v4.1-flash @ workbuddy` .944 |
| `qwen3.5-9b` | `deepseek-flash @ official GA` .928 | `deepseek-flash @ opencode-go` .926 | `deepseek-v4-flash:0731 @ ollama` .923 |

### 九轴 z 化余弦 top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` **+.683** | `hy4-preview-f @ workbuddy` +.415 | `swe-2-medium @ devin` +.296 |
| `qwen3.8-27b` | `luna-900k medium` +.719 | `astra-900k xhigh` +.526 | `astra-900k max` +.526 |
| `deepseek-v4-flash-0731` | `luna-900k xhigh` +.807 | `sol-900k high` +.787 | `sol-900k medium` +.773 |
| `deepseek-v4-flash-vision-exp` | `swe-1-7-medium @ devin` +.318 | `sol-900k medium` +.286 | `luna-900k high` +.266 |
| `qwen3.5-9b` | `glm-5-2 @ devin` +.541 | `swe-1-7-medium @ devin` +.278 | `sol-900k medium` +.263 |

### 21 案逐案余弦 top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| `glm-5.3-flash` | `deepseek-v4.1-flash @ ollama` .943 | `hy4-preview-f @ workbuddy` .940 | `deepseek-v4.1-flash @ commandcode` .939 |
| `qwen3.8-27b` | `deepseek-v4-flash:0731 @ ollama` .971 | `luna-900k medium` .954 | `deepseek-flash @ official GA` .954 |
| `deepseek-v4-flash-0731` | `deepseek-flash @ official GA` .970 | `deepseek-flash @ opencode-go` .952 | `deepseek-v4-flash:0731 @ ollama` .948 |
| `deepseek-v4-flash-vision-exp` | `deepseek-flash @ official GA` .942 | `luna-900k xhigh` .937 | `luna-900k high` .937 |
| `qwen3.5-9b` | `deepseek-flash @ official GA` .912 | `deepseek-v4-flash:0731 @ ollama` .910 | `deepseek-flash @ opencode-go` .903 |

### 同名身份对位

下列数值顺序为「九轴原始余弦／z 化余弦／21 案余弦」。

| crof 端点 | vs 同名对照 | vs 最像的非同名车道 |
|---|---|---|
| `glm-5.3-flash` | `glm-5.3-flash @ ollama` W36：.964／+.097／.932；W37 重跑：.853／−.011／.890 | `deepseek-v4.1-flash @ ollama`：**.996／+.683／.943** |
| `deepseek-v4-flash-0731` | `deepseek-v4-flash:0731 @ ollama`：.963／+.186／.948 | `deepseek-flash @ official GA`：.976／+.567／.970 |
| `qwen3.8-27b` | 无同名车道 | `deepseek-v4-flash:0731 @ ollama`：.992／+.353／.971 |

逐案最大分歧（|Δ| > 0.15，完成度单位）：

- crof `glm-5.3-flash` vs Ollama `glm-5.3-flash`：五案分歧——A-1fd3683a（0 vs 1.0）、A-442d4aab（.143 vs 1.0）、视觉案 A-ea80d793（.222 vs .778）、归因案 A-a317e74b（.533 vs .933）、审查案 A-cdc3d11a（.222 vs .444）。而 vs Ollama `deepseek-v4.1-flash` 只差三案：A-1fd3683a、A-442d4aab、A-cdc3d11a。
- crof `deepseek-v4-flash-0731` vs DeepSeek 官方 GA：两案分歧——A-cdc3d11a（−.889 vs 0，全场最差审查分）与 A-61f7ad01（.714 vs 1.0）。
- crof `qwen3.8-27b` vs Ollama `d4f:0731`：三案分歧——A-a5608487（0 vs .8）、A-be92627f（.333 vs .778）、A-47eea242（.889 vs .667）。

## 判读

1. **`glm-5.3-flash` 是最干净的错位。** 它在三种度量下的最近邻都是 `deepseek-v4.1-flash @ ollama`。z 化余弦的差距尤其关键：对 DeepSeek 道是 +.683，对两条同名 GLM 道只有 +.097 和 −.011。换成大白话：它「哪里特别强、哪里特别弱」的形状，贴着 DeepSeek V4.1 Flash，而不是端点上写的 GLM。方向与 wire 级报告一致，但证据等级更弱。
2. **`qwen3.8-27b` 很反常。** 它拿着全场唯一的归因满分（A-a317e74b 15/15，也是该案史上首次），却在 A-a5608487 挂零。它的逐案指纹最像 `d4f:0731`（21 案余弦 .971），但 z 化形状更靠 GPT 档车道。真实的 27B 开源模型当然也可能表现异常，但这份指纹并不能自然确认同名身份。
3. **`deepseek-v4-flash-0731` 仍然未决。** 逐案层面，它最像 DeepSeek 官方道（21 案余弦 .970），这和真 d4f 家族相符；但审查轴是全场最差（A-cdc3d11a = −12，轴值 −0.056），标准化形状又偏 luna／sol（+.77 到 +.81）。「d4f 系上游套代理栈」「窗口中途换路由」「n=1 噪声」都能解释这种糊掉的指纹。
4. **`deepseek-v4-flash-vision-exp` 与 `qwen3.5-9b` 没有可信身份匹配。** 饱和轴把原始余弦撑到 .91 以上，但它们的最高 z 化余弦只有 +.318 和 +.541。`vision-exp` 尤其别扭：端点挂着 vision 名，视觉轴却低到 .111，是全场最低。

## 什么证据会推翻这个结论

- 出现一条同名 GLM 对照道，在 z 化余弦和逐案行为上都像 `deepseek-v4.1-flash @ ollama` 那样贴近 crof `glm-5.3-flash`。
- 新一轮重跑中，该 crof 端点复现的是 GLM 同名模型的特异行为，而不是 DeepSeek 家族指纹。
- 新的 wire 级证据证明 OpenRouter 私有工具结果是伪影，而不是路由信号。
- CrofAI 发布可验证的逐请求上游／模型证明，且与这里观察到的指纹相矛盾。

## 限制

- 每案 n=1，单案分歧是弱证据；有效信号在多轴、多案聚合出的整体形状。
- 分数相似不等于权重相同。不同模型可能在同一套题上收敛；路由、代理、重试层也会扭曲车道指纹。
- z 化余弦看的是形状，不是绝对能力；两个模型可以同形状、不同体量。
- 如果窗口中途换上游，指纹恰恰会糊成现在这个样子。
- CrofAI 的阵容与路由随时可变；本文只是 W36-W37 窗口（2026-09-06 至 2026-09-08 UTC）的快照。

## 复现

输入全部是已发布逐案矩阵：本仓 `results/` 加七个姐妹仓——`amber-ollama`、`amber-gpt`、`amber-devin`、`amber-deepseek`、`amber-commandcode`、`amber-opencode`、`amber-workbuddy`。

运行 [`model-identity-cosine-2026-09.py`](model-identity-cosine-2026-09.py)。脚本先做已发布向量的归一化自检，再输出原始余弦、z 化余弦、同名对位和逐案分歧。

*独立社区测量，样本量小，不构成采购建议。*
