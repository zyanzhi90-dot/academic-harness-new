# 统一科学核心使用说明

在安装了本项目 editable 包的 Python 环境中，以独立研究目录作为当前工作目录。`python -m harness` 和 `academic-harness` 等价。初始化自动安装 `.codex` 角色、Hook、命令规则及 `.agents/skills/research-lit`、`.agents/skills/research-cycle`，不覆盖已有 AGENTS.md。按原有项目配置加载和 Hook 信任机制启用研究目录；实际 native 工作必须从该目录进行，`--root` 不能替代活动项目目录。

已有 accepted 调研直接接入，不重新调研：

```powershell
python -m harness science begin RUN frame.json
python -m harness science status RUN
python -m harness science allowed-actions RUN
python -m harness science allowed-agents RUN
```

新 run 使用 `science start RUN --executor "实际模型标识"`，沿既有 `lit` 调研链完成来源策略人工批准、查询、筛选、全文、地图及覆盖评审，再 `science begin`。`lit start` 继续提供独立调研。重复 `science start` 可刷新受管加载层，不重建科学状态；已有自定义 AGENTS.md 的使用者按本说明加载新的科学 Skill。

读 [统一科研 Skill](../skills/research-cycle/SKILL.md) 和 [JSON 契约](../skills/research-cycle/references/schemas.md)。提交前读取状态、live request 和待消费反馈。问题与方法基于已有 Evidence ID；mature_method_search 的查询须来自实际 query_events，新外域来源通过共享调研补充。

```powershell
python -m harness science submit-problems RUN problems.json
python -m harness science review-handoff RUN
# fresh configured scientific_reviewer 阅读 bound originals，实际完成 Hook 记录 verdict
python -m harness science submit-review RUN verdict.json
```

PROBLEM_SELECTION 向人工展示候选及证据，只记录人的明确决定：

```powershell
python -m harness science human-select-problem RUN CANDIDATE --request-id REQUEST
```

核心应用必须保留；关键研究问题实质改变需要新的人工选择，并在该命令添加 `--accept-scope-change`。问题版本绑定 `{problem_id, version, sha256}`；方法不能偷换为未选定的候选。AI 不自行选择。人工命令必须独立执行，不在 science 前放 `--root`，使已安装 prompt 规则匹配；`python3`、`py`、控制台入口均覆盖。Hook 放行不等于人工同意；界面不能确认时交由人直接运行。

```powershell
python -m harness science submit-method RUN method.json
python -m harness science submit-prior-assessment RUN prior.json
python -m harness science submit-check RUN result.json
```

具体模型、变量、输入输出、算法、推导、组件、成熟方法与贡献计划共同组成方法包。允许直接复用、迁移、改造、融合及有理由的自行设计，无强制 RCA／Principle 链。新路线版本保存主线调整理由和消费的反馈。跨域资源身份与实际覆盖分别判断；本领域 SUBSTANTIAL prior 自动暂停工作、发起明确缺口更新，覆盖完成后回到 PROBLEM_DISCOVERY，追问重要剩余痛点并重新人工选择。

理论和试验在设计中产生真实结果时，按已有科研授权执行并提交结果文件；本轮没有运行真实科研。`submit-check` 验证路线、实际文件哈希、计划摘要、主张及声明的评估单位。计划摘要使用 `harness.scientific_validators.digest(plan)`（sorted keys、紧凑 UTF-8 JSON）。结果影响下一版本或触发补调研／问题返回；不能从试验计划直接标记 VALIDATED，设计试验不能证明独立贡献。已有结果仅支持同一问题、未改变的技术机制及确切主张，文件被修改会使支持失效。检查声明不能证明试验本身真实、独立或正确，评审必须审查这些条件。

其他具体知识缺口：

```powershell
python -m harness science request-literature-update RUN update.json
python -m harness update-literature RUN --requested-by method_design --gap "具体缺口"
```

Controller 自动绑定当前应用、问题与路线版本。继续安装的 research-lit Skill，沿原查询、筛选、阅读和地图覆盖链完成更新；只补必要缺口。结束后恢复原科学工作，新增反馈要求解释新证据的影响。连续更新保留全部地图历史和原 Evidence。

METHOD_REVIEW 用同一 scientific_reviewer 独立协议。Controller 只接受 fresh configured role 经实际 SubagentStop／Stop Hook 留下的完整原始 verdict，不接受 Main 改写。收到 METHOD_READY 后向人工展示完整路线、作者证据、推断与待验证主张；经人工明确决定记录：

优先使用配置角色。当前运行环境不能选择角色时，`science review-handoff RUN --dispatch-mode native_generic_compat` 提供精确任务；将它原样交给 `fork_turns=none` 的 fresh native child。此路径复用基座已有的原生 generic attestation 机制，完整携带同一角色契约和绑定原文，Hook 核对自然 child transcript、任务绑定、原文字节和禁工具条件。不得用 Main、手写 transcript、嵌套 `codex exec` 或新顶层会话代替独立评审。任务超出当前上下文容量或自然 Hook 不可用时不能接受正式评审；本轮未验证真实模型生命周期。

```powershell
python -m harness science human-confirm-method RUN --request-id REQUEST
python -m harness science handoff RUN
python -m harness lit save-recovery RUN SNAPSHOT_DIRECTORY
python -m harness lit resume RUN
```

METHOD_CONFIRMED 是 bounded method 的人工确认，不宣布贡献已验证，不自动启动实验。新证据要求重新考虑问题时用 `science reopen-problem RUN --reason "依据" --evidence-id P1`。交接包括原文路径和哈希、问题／路线版本、反馈、主张边界、结果及下一步动作。恢复复制同一状态，保留版本与 receipt；外部 attestation root 沿原机制记录。

本轮通过合成输入验证工程循环及返回。native 模型实际加载、UI 确认、真实 prior 判别、科学效果与顶会顶刊方法质量仍需负责人复验和实际案例检验，详见 [CHECK_RESULTS.md](CHECK_RESULTS.md)。
