# amber-crof

用 AMBER 私有题库对 [CrofAI](https://crof.ai/) 在售模型做的公开周测结果仓。

[English README](README.en.md)

## 这是什么

- 每周(外加不定期触发)用 AMBER 案例库对 crof.ai 的模型跑一轮,**结果永远公开,题目永不公开**。
- AMBER 是 agentic 实战题库(施工/运维/审查/视觉/需求漂移),规范与制题工具见 [getaskclaw/amber-eval](https://github.com/getaskclaw/amber-eval);考题本体私有。
- 我们是 crof 的付费用户,与 CrofAI 无隶属关系;这是独立第三方社区周测。

## 红线(发布纪律,违反即撤稿更正)

1. **只公开**:分数、聚合统计、成本、速度、定性行为裁决。
2. **永不公开**:题目内容、模型原始输出(transcript)、判分逻辑(oracle)。模型复述会带出题目原文,所以原始输出一律不出私域。
3. **每期钉死**:model id、effort、UTC 时间窗、harness 标识、每案 bundle 哈希——对照 amber-eval 公开哈希清单,任何人可验证题目集未被更换。
4. **案号与题目结构属私有面**:公开结果里案例只用稳定别名(A-xxxxxxxx,哈希派生)+bundle 哈希作句柄;内部案号、变体名、题目描述永不出现。
5. **基调 = 社区周测**:陈述数字与观察到的行为,不攻击厂商;发现问题先可复现再发布。

## 怎么读结果

- 一案一卷;required checks 全绿才算过(bonus 不计入)。多卷案例(一案多变体)全绿才算一案过。
- n=1 单次,存在噪声;偶发空响应按规则补考重放,并在当期文中标注。
- 成本以 crof 响应里 `usage.cost` 的服务端账单口径为准;价格为发布时 crof.ai/pricing 快照,实时价以官网为准。
- 对照列「frontier ref」= 我们内部同题同档的 OpenAI 前沿模型参考席位,仅作锚点,不构成对该厂商的评价。

## 结果索引

| 期 | 模型 | 结论 |
|---|---|---|
| [2026-W36](results/2026-W36-deepseek-v4-flash-0731.md) | deepseek-v4-flash-0731 @ high | 13/21 案过;$0.71;施工/OPS 接近前沿锚点且快,审查幻觉重、无视觉、no-tools 场景工具瘾 |

## 免责

独立测试,样本量小,不构成采购建议。厂商阵容与价格随时变动,以 [crof.ai/pricing](https://crof.ai/pricing) 实时页为准。
