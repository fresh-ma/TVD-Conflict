# 2025--2026 LLM-as-Safety-Judge Backbone Survey

检索截止：2026-08-02。2026 年统计是不完整年度。

## 1. 统计口径

主统计纳入 19 篇核心实证论文：论文需要明确研究 safety judge 的可靠性、配置、训练、校准或系统性比较，或将 safety judge 本身作为主要方法组件。按 arXiv 首次公开年份分为 2025 年 8 篇、2026 年 11 篇。

- 计数单位是“使用该模型的论文数”，不是调用次数、prompt 数或实验行数。
- 同一篇论文中，同一模型跑多个 rubric、prompt 或 agent role，只计 1 次。
- 只计实际充当 judge/evaluator/guard 的模型；generator、attacker 和被测 target model 不计。
- 通用 prompted LLM 与专用 safety classifier/guard 分开统计。
- 模型版本明确时按精确版本记录；只报告系列名时不擅自补版本。
- 领域专用医疗、机器人、音频/多模态 judge，以及只在相关工作中提到模型的论文，不进入主计数。

因此下面的数字是“核心方法论文样本中的采用频次”，适合 backbone 选择，不应表述为 2025--2026 所有 safety 论文的穷尽计量。

## 2. 结论摘要

### 2.1 通用 prompted judge：按模型家族去重

| 模型家族 | 论文数 / 19 | 占比 | 观察 |
|---|---:|---:|---|
| OpenAI GPT 系列 | 12 | 63% | GPT-4o 与 GPT-4o-mini 是最常见的跨年公共基线 |
| Anthropic Claude 系列 | 9 | 47% | 2026 年 Sonnet/Haiku 4.5--4.6 使用明显增加 |
| Meta Llama 通用模型 | 8 | 42% | 常见开源对照，覆盖 8B、70B、Maverick |
| Qwen 系列 | 6 | 32% | 2026 年增长快，尤其适合可复现和成本受限实验 |
| Google Gemini 系列 | 4 | 21% | 多为 Flash/Pro 的闭源跨厂商对照 |
| Mistral/Mixtral | 3 | 16% | 主要出现在 2025 年工作 |
| Cohere Command/Aya | 3 | 16% | 用于跨家族、跨语言比较 |
| DeepSeek | 3 | 16% | 2026 年用于 reasoning/non-reasoning 对照 |
| Gemma 通用模型 | 3 | 16% | 同时也是多个专用 judge 的底座 |
| GLM | 2 | 11% | 2026 年开始作为独立家族对照 |

注：一篇论文可以贡献多个家族，所以百分比不相加为 100%。这里的 “Meta Llama 通用模型” 不含 LlamaGuard/HarmBench 等专用 judge。

### 2.2 专用 safety judge/evaluator：按系统系列去重

| Safety judge 系列 | 论文数 / 19 | 典型版本/配置 |
|---|---:|---|
| LlamaGuard | 9 | LlamaGuard-2、LlamaGuard-3-8B、LlamaGuard-4-12B |
| HarmBench classifier | 5 | `cais/HarmBench-Llama-2-13b-cls` |
| ShieldGemma | 4 | 2B、9B |
| StrongREJECT evaluator | 3 | 原 Gemma-2B evaluator；也有 GPT-4o/Claude prompt 实例 |
| WildGuard | 2 | released WildGuard checkpoint |
| JailJudge | 2 | 原系统及 Qwen matched-backbone 实例 |
| GPT-OSS-Safeguard | 2 | 20B |
| AegisGuard | 1 | AEGIS safety judge |
| GuardReasoner | 1 | 3B |
| Nemotron Safety Guard | 1 | Llama-3.1-Nemotron-Safety-Guard-8B-v3 |
| Atla Selene Mini | 1 | 8B，Llama-3.1-8B fine-tune |
| GPTFuzzer evaluator | 1 | GPTFuzzer harmfulness classifier |
| AILuminate / SorryBench / JBB protocols | 各 1 | 分别落在 Claude Sonnet 4.5、GPT-4o-mini、Llama-3.3-70B |

### 2.3 重复出现的精确 backbone

| 精确模型/配置 | 论文数 |
|---|---:|
| GPT-4o | 5 |
| GPT-4o-mini | 5 |
| HarmBench Llama-2-13B classifier | 5 |
| LlamaGuard-3-8B | 5 |
| ShieldGemma-9B | 4 |
| LlamaGuard-4-12B | 4 |
| Claude Haiku 4.5 | 4 |
| Claude Sonnet 4.5 | 3 |
| Qwen2.5-7B | 3 |
| Claude 3 Haiku | 2 |
| Gemini 2.5 Flash | 2 |
| Gemma-3-12B-IT | 2 |
| GPT-OSS-20B | 2 |
| GPT-OSS-Safeguard-20B | 2 |
| WildGuard | 2 |
| JailJudge | 2 |

## 3. 逐篇核对矩阵

### 2025（8 篇）

| arXiv | 论文 | 实际 judge/evaluator 模型 |
|---|---|---|
| [2501.13080](https://arxiv.org/abs/2501.13080) | Refining Input Guardrails | Mistral-7B-Instruct-v0.2; Mixtral-8x7B-Instruct-v0.1; Llama-2-13B-Chat; Llama-3-8B-Instruct; LlamaGuard-2 baseline |
| [2503.02574](https://arxiv.org/abs/2503.02574) | LLM-Safety Evaluations Lack Robustness | HarmBench Llama-2-13B; StrongREJECT Gemma-2B |
| [2503.04474](https://arxiv.org/abs/2503.04474) | Know Thy Judge | HarmBench Llama-2-13B; WildGuard; ShieldGemma-9B; LlamaGuard-3-8B; Atla Selene Mini 8B |
| [2503.09347](https://arxiv.org/abs/2503.09347) | Safer or Luckier? | Llama-3-70B/8B; Command-R-Plus/R; Mistral-Large/8x7B; Claude-3-Sonnet/Haiku; GPT-4-Turbo; GPT-4o; GPT-4o-mini |
| [2508.16347](https://arxiv.org/abs/2508.16347) | Confusion is the Final Barrier | InternLM2.5-20B; GLM-4-32B; Qwen2-7B; Qwen2.5-14B/72B; DeepSeek-V2.5; GPT-4o-mini; GPT-4.1-nano; Gemini-2.5-Flash; Claude-3-Haiku; Llama-3.1-8B; Llama-4-Maverick; Mistral-Small-3.1-24B; Gemma-3-12B |
| [2509.24384](https://arxiv.org/abs/2509.24384) | HarmMetric Eval | GPT-4o under four prompt protocols; HarmBench; LlamaGuard; LlamaGuard-4; ShieldGemma; WildGuard; GPTFuzzer evaluator; Qwen2.5-7B HarmClassifier |
| [2511.01375](https://arxiv.org/abs/2511.01375) | Align to Misalign | GPT-4o-mini as inner-loop, outer-loop and ASR judge |
| [2511.06396](https://arxiv.org/abs/2511.06396) | Efficient LLM Safety Evaluation through Multi-Agent Debate | GPT-4o; LlamaGuard-3-8B; ShieldGemma-2B/9B; Qwen2.5-7B; Qwen3-4B/8B/14B; JailJudge matched-backbone baselines |

### 2026（截至 8 月 2 日，11 篇）

| arXiv | 论文 | 实际 judge/evaluator 模型 |
|---|---|---|
| [2603.05399](https://arxiv.org/abs/2603.05399) | Judge Reliability Harness | GPT-4o; Claude Sonnet 4.5; Llama-4-Maverick; Gemini 2.5 Pro |
| [2603.06594](https://arxiv.org/abs/2603.06594) | A Coin Flip for Safety | AegisGuard; HarmBench Llama-2-13B; JailJudge; LlamaGuard-3 |
| [2604.15224](https://arxiv.org/abs/2604.15224) | Context Over Content | Qwen2.5-72B-Instruct; DeepSeek-R1-Distill-Qwen-32B; DeepSeek-V3 |
| [2604.24074](https://arxiv.org/abs/2604.24074) | How Sensitive Are Safety Benchmarks to Judge Configuration Choices? | Claude Sonnet 4.6 primary; MiniMax-M2; GLM-5 |
| [2605.06161](https://arxiv.org/abs/2605.06161) | Beyond Accuracy: Policy Invariance | GPT-5.4-mini; Claude Haiku 4.5; Gemini 3 Flash; DeepSeek-V3.2 |
| [2605.31381](https://arxiv.org/abs/2605.31381) | LLM Judges Inconsistently Disagree | Gemini-2.5-Flash; GPT-4o-mini; Claude Haiku 4.5; Command-A; Llama-3.3-70B; Gemma-3-27B; LlamaGuard-4-12B comparator |
| [2606.07874](https://arxiv.org/abs/2606.07874) | Safety is Contextual, LLM-Judges Are Not | GPT-5.2; GPT-5-mini; Claude Sonnet 4.5; Claude 3.5 Haiku; Command-A/R; Qwen3-235B; Llama-3.1-70B; GPT-OSS-20B; Tiny Aya Global; Nemotron-Safety-Guard-8B-v3; LlamaGuard-4-12B; GPT-OSS-Safeguard-20B |
| [2606.09165](https://arxiv.org/abs/2606.09165) | Reliable to Expressive | Llama-3.1-8B; Qwen2.5-14B; Gemma-3-12B; LlamaGuard-3-8B; GuardReasoner-3B; GPT-OSS-20B; GPT-OSS-Safeguard-20B; Qwen3-30B-A3B-Thinking; curriculum-tuned Gemma-3-12B |
| [2606.25487](https://arxiv.org/abs/2606.25487) | How Reliable Is Your Jailbreak Judge? | HarmBench Llama-2-13B; Qwen2.5-7B; Qwen2.5-3B; Phi-3.5-mini |
| [2606.25782](https://arxiv.org/abs/2606.25782) | Do Encoders Suffice? | Claude Haiku 4.5; GPT-4o-mini; Llama-3.3-70B; Claude Sonnet 4.5; LlamaGuard-3/4; ShieldGemma-2B/9B; Ettin-150M/400M encoder comparators |
| [2606.26185](https://arxiv.org/abs/2606.26185) | Necessary but Not Sufficient | GPT-4o; Claude Sonnet 4.6; Claude Haiku 4.5 |

## 4. 对 TVD-Conflict 的 backbone 原则

### 最小可发表配置

TVD-Conflict 的主张是“相同 rubric、只替换 backbone”。主实验应使用能够遵循同一自由格式 rubric 的通用 instruction-following judges：

1. `GPT-4o`：最常见的通用闭源基线，便于和 2025--2026 工作对齐。
2. `Claude Sonnet 4.5/4.6`：第二个闭源家族，且 2026 年 safety-judge 论文采用率高。
3. `Qwen3-14B`（预算紧时 `Qwen2.5-7B`）：开放、成本可控的通用 judge；Qwen3-14B 已有 matched-backbone debate 证据。
4. `Gemini 2.5 Flash/Pro` 或 `Llama-3.3-70B-Instruct`：补足第四个训练家族；前者提供闭源跨厂商差异，后者提供可控的开源大模型对照。

如果预算只允许 2 个 judge，主实验首选 `GPT-4o + Claude Sonnet 4.5/4.6`。它们在文献中采用率最高、都能遵循同一 rubric，同时来自不同厂商，最干净地识别 evaluator-choice variance。

另设“原生专用 judge”对照轨：`LlamaGuard-3-8B`（文献可比性最好）、`LlamaGuard-4-12B`（更新部署面）、`HarmBench-Llama-2-13B` 或 `ShieldGemma-9B`。这些模型应使用各自官方 prompt/schema，不能和主实验一起宣称“完全相同 prompt”；该轨回答的是“evaluation protocol choice”，不是纯 backbone effect。

### 不建议的选择方式

- 不要只选同一家族的大小模型，例如 GPT-4o 与 GPT-4o-mini；这主要测 scale，不足以支持“judge choice”结论。
- 不要只选多个 LlamaGuard 版本；它们共享训练目标和 policy prior，相关错误会被低估。
- 不要把 HarmBench prompt 与 HarmBench classifier 当成两个独立 backbone；prompt、rubric、backbone 是三个应分别控制的变量。
- 不要强迫 LlamaGuard、HarmBench 或 ShieldGemma 使用通用 judge 的输出 schema；这会把 interface mismatch 误写成模型分歧。
- 不要把 majority vote 当作 ground truth。2025--2026 工作反复显示，jury 能改善平均表现，但不能消除共享 artifact bias。

### 实验设计要求

- 固定完全相同的可见输入、rubric、输出 schema、temperature 和解析器；只替换 backbone。
- 同时报 individual judge、pairwise disagreement、FNR/FPR、parse failure 和 repeated-run jitter。
- 至少保留一个人标小切片，校准每个 judge 的 precision/recall；不能只报告 ASR。
- 预注册模型版本和 provider route。`temperature=0` 仍可能非确定，边界样本建议重复 3--5 次。
- 主结果用异构 judges；同家族不同尺寸作为 scale ablation，而不是主结论。

## 5. 相邻证据（未进入主计数）

[Lower-Resource, Higher Scores, arXiv:2607.14480](https://arxiv.org/abs/2607.14480) 研究的是更广义的 multilingual evaluator，而非专门的 safety judge，因此未并入 19 篇主统计。但其结果对本项目很重要：Aya-Expanse-32B、Qwen2.5-72B、Llama-3.1-70B、M-Prometheus-14B 及多种 reward model 在低资源语言上存在系统性分数偏移；GPT-4.1-mini 和 Qwen3-32B-thinking 也复现该偏差。如果 TVD-Conflict 包含跨语言样本，应把语言作为独立分层变量。

### 年份口径敏感性

[SORRY-Bench, arXiv:2406.14598](https://arxiv.org/abs/2406.14598) 首次公开于 2024 年，但正式发表于 ICLR 2025。主统计按首次公开年份，因此未纳入；若按 venue 年份统计，应把它作为第 20 篇加入。其 meta-evaluation 实际比较 GPT-4o、GPT-3.5-Turbo、Llama-3-70B/8B、Mistral-7B-Instruct-v0.2、Gemma-7B-IT、LlamaGuard-2-8B、MD-Judge、WildGuard 和 HarmBench classifier，并最终选择 fine-tuned Mistral-7B-Instruct-v0.2 作为 benchmark judge。

加入 SORRY-Bench 后，受影响的家族频次为：OpenAI 13/20、Meta Llama 通用模型 9/20、Mistral 4/20、Gemma 4/20；专用系统频次为 LlamaGuard 10/20、HarmBench classifier 6/20、WildGuard 3/20。核心 backbone 建议不变。
