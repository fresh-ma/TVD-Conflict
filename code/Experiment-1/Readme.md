这个实验要证明不同 judge 在使用同一套 critera 时, 对同一个 attack response 会出现不同的意见

Attack Trajectory 和 Attack Response 在 `./base_skills` 下, 共 47 个 attack

接下来我们要通过统计 base_skill 本身的 judge 和 unified_judge 之间的歧义率来挑 10 个歧义最明显的 attack 出来跑实验, 再在这个 10 个里面挑 5 个放到 paper 里

judge criteria: 2 个
- WildGuard: 一个 binary 的 rubric
- StrongReject: 1-5 分, 多维度打分, 一个计算公式(含小数)

judge backbone:
- openai/gpt-oss-120b                   $0.03  / $0.17
- openai/gpt-oss-safeguard-20b          $0.075 / $0.30
- qwen/qwen3.7-flash                    $0.03  / $0.13
- deepseek/deepseek-v4-flash            $0.052 / $0.103
