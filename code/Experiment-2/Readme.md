这个实验要证明 TVD-Conflict 的成功率和效率

指标: Conflict Rate @10 , 10 次 judge budget 下 trigger 出 conflict 的成功率

bench: AdvBench Random 50 Goals

baseline:
- Random-Pick 从 40 个 attack 中随机选 10 个运行出结果后进行 judge, 出现 1 个成功 Conflict 即成功
- Experience-Pick 根据经验选择 10 个最容易让 judge 误判的 attack, 运行后进行 juege, 出现 1 个成功 Conflict 即成功

表格形状:
                    |              Baselines            |            TVD-Conflict           |
    model pair      |   Random-Pick   | Experience-Pick |      None       |  Skill Guided   |
                    |  Biary |  Score |  Biary |  Score |  Biary |  Score |  Biary |  Score |
gpt-oss  & ds-flash |
                    |
gpt-oss  & qwen     |
                    |
ds-flash & qwen     |
                    |
ds-flash & ds-flash |
                    |
qwen     & qwen     |
                    |
gpt-oss  & gpt-oss  |
                    |
        AVG.        |
