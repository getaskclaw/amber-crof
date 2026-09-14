# 模型身份指纹：CrofAI 五道模型的九轴最近邻分析（2026-09）

[English](model-identity-cosine-2026-09.en.md)

## 为什么做这次分析

2026-09-13，一份第三方 wire 级取证（ktibow「crof.ai is an OpenRouter wrapper」，[链接](https://kendell.dev/blog/crofaifalse/)）称 crof.ai 的多个端点会执行 OpenRouter 私有工具，且若干在售模型的指纹指向完全不同的上游模型（例如其 `glm-5.2` 的行为实为 DeepSeek V4 Flash）。那是线路层证据，本文是独立的行为侧对照：只用已公开的 AMBER 成绩矩阵问一个问题——crof 的五道模型，分数形状最像哪条已知车道？

动笔前我们先独立复核了该报告的关键证据：其引用的探针 run 真实存在，`deepseek-v4-flash-0731` 的逐模型证据文件确实记录了 OpenRouter 私有工具被执行，并返回 OpenRouter 风格的上游模型名。

## 方法

- **向量**：每条车道变成 23 案集合上的九轴完成度向量（W36 21 案矩阵并上 W37 补考 2 案）。九轴：交付（A-791e90ac）、编码（6 个施工案）、防御（2 个核验案）、归因（A-a317e74b）、审查（2 个 d2 案）、运维（6 案）、需求漂移（A-0676097b）、UI 施工（A-d9b79b46）、视觉（A-ea80d793）。
- **计分**：钉案 = 绿钉/总钉；d2 案 = (d2 + 4) / 9——与已发布案面画像同一归一化口径。
- **三种度量**：九轴原始余弦；z 化余弦（各轴按全部 32 条车道标准化——必须做，因为饱和轴把几乎任意两道的原始余弦都推过 0.9）；21 案逐案完成度余弦。
- **对照场**：七个姐妹仓共 27 条已发布非 crof 车道。
- 缺格成对剔除；`∅` 基建超时不进轴均值；crof `deepseek-v4-flash-0731` 缺考的视觉卷按 d2 = -2 计（未交付），与 GA 道未交付卷同口径；`deepseek-v4-flash-vision-exp` 与 `qwen3.5-9b` 只跑了 21 案子集，运维轴分母为 4 案。

## 结果

### 九轴原始余弦 top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama **.996** | deepseek-v4.1-flash @ commandcode .988 | hy4-preview-f @ workbuddy .986 |
| qwen3.8-27b | deepseek-v4-flash:0731 @ ollama **.992** | luna-900k medium .991 | astra-900k xhigh .988 |
| deepseek-v4-flash-0731 | luna-900k xhigh .987 | luna-900k high .986 | sol-900k high .985 |
| deepseek-v4-flash-vision-exp | deepseek-flash @ official GA .956 | deepseek-flash @ opencode-go .954 | deepseek-v4.1-flash @ workbuddy .944 |
| qwen3.5-9b | deepseek-flash @ official GA .928 | deepseek-flash @ opencode-go .926 | deepseek-v4-flash:0731 @ ollama .923 |

### z 化余弦（强弱形状）top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama **+.683** | hy4-preview-f @ workbuddy +.415 | swe-2-medium @ devin +.296 |
| qwen3.8-27b | luna-900k medium +.719 | astra-900k xhigh +.526 | astra-900k max +.526 |
| deepseek-v4-flash-0731 | luna-900k xhigh +.807 | sol-900k high +.787 | sol-900k medium +.773 |
| deepseek-v4-flash-vision-exp | swe-1-7-medium @ devin +.318 | sol-900k medium +.286 | luna-900k high +.266 |
| qwen3.5-9b | glm-5-2 @ devin +.541 | swe-1-7-medium @ devin +.278 | sol-900k medium +.263 |

### 21 案逐案余弦 top 3

| crof 车道 | #1 | #2 | #3 |
|---|---|---|---|
| glm-5.3-flash | deepseek-v4.1-flash @ ollama .943 | hy4-preview-f @ workbuddy .940 | deepseek-v4.1-flash @ commandcode .939 |
| qwen3.8-27b | deepseek-v4-flash:0731 @ ollama .971 | luna-900k medium .954 | deepseek-flash @ official GA .954 |
| deepseek-v4-flash-0731 | deepseek-flash @ official GA .970 | deepseek-flash @ opencode-go .952 | deepseek-v4-flash:0731 @ ollama .948 |
| deepseek-v4-flash-vision-exp | deepseek-flash @ official GA .942 | luna-900k xhigh .937 | luna-900k high .937 |
| qwen3.5-9b | deepseek-flash @ official GA .912 | deepseek-v4-flash:0731 @ ollama .910 | deepseek-flash @ opencode-go .903 |

### 同名身份对位

| crof 端点 | vs 同名车道 | vs 最像的别家 |
|---|---|---|
| glm-5.3-flash | glm-5.3-flash @ ollama：cos .964 / z +.097 / 21c .932 | deepseek-v4.1-flash @ ollama：cos **.996** / z **+.683** / 21c .943 |
| deepseek-v4-flash-0731 | deepseek-v4-flash:0731 @ ollama：cos .963 / z +.186 / 21c .948 | deepseek-flash @ official GA：cos .976 / z +.567 / 21c .970 |
| qwen3.8-27b | （无同名车道） | deepseek-v4-flash:0731 @ ollama：cos .992 / z +.353 / 21c .971 |

逐案最大分歧（|Δ| > 0.15，完成度单位）：

- crof `glm-5.3-flash` vs ollama `glm-5.3-flash`——五案分歧：A-1fd3683a（0 vs 1.0）、A-442d4aab（.143 vs 1.0）、视觉案 A-ea80d793（.222 vs .778）、归因案 A-a317e74b（.533 vs .933）、审查案 A-cdc3d11a（.222 vs .444）；而 vs ollama `deepseek-v4.1-flash` 只差三案：A-1fd3683a、A-442d4aab、A-cdc3d11a。
- crof `deepseek-v4-flash-0731` vs GA 官方——两案：A-cdc3d11a（-.889 vs 0，全场最差审查分）与 A-61f7ad01（.714 vs 1.0）。
- crof `qwen3.8-27b` vs ollama `d4f:0731`——三案：A-a5608487（0 vs .8）、A-be92627f（.333 vs .778）、A-47eea242（.889 vs .667）。

## 解读

1. **crof `glm-5.3-flash` 的行为像 DeepSeek V4.1-Flash 家族，不像它的同名者。** 三种度量下最近邻都是 `deepseek-v4.1-flash @ ollama`（原始 .996；z +.683——crof 诸道里最强的 z 匹配），而它离 ollama 同名 glm-5.3-flash 差五案（z +.097）。方向上与 wire 级发现一致——crof 的 GLM 名端点后面跑的是 DeepSeek 系权重；但单凭分数不能证明路由。
2. **crof `qwen3.8-27b` 不像一个 27B 级开源模型。** 它握着全道唯一的归因满分（15/15，该案史上首次），却在 A-a5608487 挂零——这个形状的最近邻仍是 d4f 家族（21c .971 vs ollama d4f:0731）。一个中型开源模型若真能在最难核验案上登顶全场，本身就是头条。
3. **crof `deepseek-v4-flash-0731` 保持存疑。** 逐案层面最像 GA 官方（21c .970）——与真 d4f 相符；但审查轴全场垫底（A-cdc3d11a = -12，轴值 -0.056），z 形状偏向 GPT 档（luna/sol，+.77——+.81）。可能是 d4f 系模型套在代理栈后面，审查异常属噪声或路由伪影；单凭分数无法定论。
4. **`deepseek-v4-flash-vision-exp` 与 `qwen3.5-9b` 组成弱模型簇，无令人信服的匹配。** 饱和轴把原始余弦撑在 >= .91，z-cos 顶匹配仅 +.32 / +.54——不贴任何一条车道的形状。注意 `vision-exp` 挂着 vision 名，视觉轴却是全道最低（.111）。

## 限制

- 每案 n=1，单案分歧是弱证据——信号在整体形状。
- 行为相似是旁证，不是 wire 级证明。窗口中途换上游，指纹恰恰会糊成这个样子。
- z-cos 量的是形状（各轴相对强弱），不是绝对水平；两个模型可以同形状不同体量。
- CrofAI 的阵容与路由随时可变；本文是 W36-W37 窗口（2026-09-06 到 09-08 UTC）的快照。

## 复现

输入全部是已发布的逐案矩阵：本仓 `results/` 加七个姐妹仓（`amber-ollama`、`amber-gpt`、`amber-devin`、`amber-deepseek`、`amber-commandcode`、`amber-opencode`、`amber-workbuddy`）。脚本见 [`model-identity-cosine-2026-09.py`](model-identity-cosine-2026-09.py)——先复算四个已发布参考向量做归一化自检，再算相似度。

*独立社区测量，样本量小，不构成采购建议。*
