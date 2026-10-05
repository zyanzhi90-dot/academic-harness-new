# 科学核心接口与后续验收

基线 14d7bac 的调研工程已验收。本轮把下面接口接到 `python -m harness science`，沿同一 run、地图、Corpus、Search Ledger、Evidence Registry 和恢复记录执行。完整命令及数据契约见 [SCIENTIFIC_CORE.md](SCIENTIFIC_CORE.md)。

| 接入点 | 当前实现 | 后续验收边界 |
| --- | --- | --- |
| 领域交接 | `literature-handoff` 提供原地图与证据绑定；`science begin` 原地采用已接受调研 | 旧案例状态映射没有运行 |
| 两类问题 | `submit-problems` 接受公认难题或多论文主动共性 failure，追问前提、反例、解释及价值 | 真实痛点、归纳质量待案例验证 |
| 人工选择 | 独立评审后 `human-select-problem` 绑定请求与问题版本；关键问题改变需显式接受 | 实际 Codex UI 确认与 Hook 信任待复验 |
| 可调整路线 | `submit-method` 绑定选定问题，检查具体模型、算法、推导、组件及成熟方法来源 | 推导真实性、路线科学价值待验证 |
| 贡献检查 | prior 身份与覆盖分别记录；本领域实质覆盖自动更新地图并返回问题发现 | 强 prior 判断、重要 pain 的持续发现待验证 |
| 理论／实验反馈 | `submit-check` 绑定实际文件、计划、路线与主张，影响修订或返回；设计试验与独立贡献验证分开 | 声明分离可检查，真实独立性与科学结论仍须审查 |
| 补充调研 | `request-literature-update` 或既有 `update-literature` 保存问题／路线与关闭条件，覆盖接受后返回原工作 | 外部服务实际可用性没有重测 |
| 反馈与版本 | immutable artifact history、问题／路线版本、逐项反馈消费、原始评审 payload 与 receipt | 语义是否充分回应反馈由实际评审判定 |
| 能力复用 | 安装 research-cycle Skill，统一契约与 scientific_reviewer；ARS／Nature 固定来源和适配记录 | 未并行执行原版 workflow，未实测能力增益 |
| 交接与恢复 | `science handoff`、`lit save-recovery`、`lit resume` 保存相同状态及下一步入口 | 未运行真实 native reviewer 生命周期 |

下一阶段由负责人复验工程接通，再按授权用既有调研和实际案例检验方法质量。本轮未重做调研、未运行案例、未扩展全部创新模式或外围功能，不能据此宣称稳定产出顶会顶刊方法。
