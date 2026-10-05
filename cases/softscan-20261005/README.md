# 真实案例问题发现检查点（2026-10-05）

**本轮未完成“独立评审通过后交付人工选择”。实际停在 PROBLEM_REVIEW。** 已接入历史证据、真实执行 `science begin` 和首次 `submit-problems`，形成一个候选；Reviewer 交接受当前运行环境阻断。未自行选题，未进入方法设计。候选阅读入口：[CANDIDATE.md](CANDIDATE.md)。

新仓库起点 `597a0e0245b9476df1a435f1a5a70c0fb98eda33`；旧案例来源 `zyanzhi90-dot/e2e` 的 `scientific-core` 对象 `8fff5f3cbb1d47405f54888c0e92c61d08e31ced`。本轮读取当前有效科研要求与两份 20261004 规划文件，使用当前安装的 research-cycle／research-lit。原始旧工作树未写入；本地对象来源工作树 HEAD 为 `f1dd87b10695fcc7621ae3676a7f978cb933dd49`，读取固定 Git blob 而非混用该 HEAD 或未提交内容。

## 已完成的真实部分

- [source-8fff5f3.zip](source-8fff5f3.zip) 保存 410 个固定版本文件，包括旧状态、科学产物、失败／修订史和来源记录；[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) 保存 Git blob、版本及逐文件哈希。归档 SHA-256 为 `0fec766c0eedfe108422c0699e7243df7e576155ee15922a5b26758165289ea1`。
- 原状态有 112 个 literature accepted 记录。111 个存在的原文按其真实批准时 CRLF 恢复，哈希全部匹配。旧 `incremental-query-plan-problem_generation` 的文件缺失于固定 Git 树，记录仍在历史归档和 `legacy_imports`，未伪造文件，也未绑定为当前输入。接受的 registry 为 105 条；原 map 的证据数和后续 supplement 的证据数不混为同一时点。
- 757 个既有来源的筛选决定做了最小 phase 映射，逐条保留原记录哈希、原 context 和 import 身份；不算新筛选、阅读或批准。[SCREENING_MAPPING.json](SCREENING_MAPPING.json) 是映射依据。Corpus 的历史前缀逐字节保留，Registry／Ledger 未修改；历史 168 query、143 read event 是继承计数，不是本次成果。
- 核实历史人工 scope 与 source policy 批准。source policy 真批准 request 为 `702ca7652e8b4d22abd29485a2924c3b`，时间 `2026-08-14T05:24:35Z`。历史 v2 问题确有 `2026-09-01T07:38:27Z` 的 `explicit_human_command` 批准，request `0281f00dbdba43688634b264502f69ee`；旧 continuation 的 pending 文字已过时。保留该决定作为范围依据，未继承为本次选题。R8–R15 的方法、accepted/final 标签仅归档诊断。
- 原始导入审计、失败的公开运行与首次状态分别在 [IMPORT_AUDIT.json](IMPORT_AUDIT.json)、[MAPPED_IMPORT_AUDIT.json](MAPPED_IMPORT_AUDIT.json)、[RUN_ATTEMPT.json](RUN_ATTEMPT.json)、[IMPORTED_STATE.json](IMPORTED_STATE.json)。后续成功不覆盖这些失败记录。
- 发现一处实际阻断：当前 source-admission-policy 明确不要求撤回／身份 HOLD 或未选中、discovery-only 的候选有全文卡，审计却因历史优先级／选中字段要求补全文。只修正 `literature_coverage_audit.py` 两处判定，并更新复用文件 destination hash。当前审计结果 [ADAPTED_IMPORT_AUDIT.json](ADAPTED_IMPORT_AUDIT.json) 为 SUFFICIENT／PASS，未新增科学规则。
- [SCIENTIFIC_ATTEMPT.json](SCIENTIFIC_ATTEMPT.json) 和对应原始 stdout／stderr 保存了本次公开 CLI 的真实成功：`science begin` → PROBLEM_DISCOVERY；首次 `submit-problems` → PROBLEM_REVIEW。首次 [frame.json](frame.json) 与 [problems.first.json](problems.first.json) 保留未改，canonical envelope 的 content 与首次提交一致。

## 本次真实运行路径与阻断

[RUNTIME_EXECUTION.json](RUNTIME_EXECUTION.json) 记录实际 import 的 ScientificController／Validator 路径、工作流和已读取安装 Skill 的哈希。安装 reviewer 为 `.codex/agents/scientific_reviewer.toml`；本运行的子代理工具没有选择配置角色的参数，所以由公开 CLI 导出了兼容交接。

本次 review request 为 `4122259d32444a52b2f3cfe2a933fe52`。它绑定 111 个历史接受原文和本次 frame／problems，共 113 个原文。完整兼容 task **1,362,844 字符、1,363,577 UTF-8 字节**，无法由当前模型调用完整传入独立子代理。原样 task 已保存在 [review-task.exact.txt](review-task.exact.txt)，SHA-256 `3e681f3fb566d1f3c6a767a398b05292226c5bfc2d691c7c19fea2430f03a5f2`；[REVIEW_HANDOFF_ATTEMPT.json](REVIEW_HANDOFF_ATTEMPT.json) 及两个原始 handoff 输出保存公开入口和哈希。

[当前 research-cycle Skill](../../skills/research-cycle/SKILL.md) 要求：**“Do not edit or truncate the task; if it cannot fit or the natural Hook is unavailable, report that formal review is blocked.”** 因此未删减绑定、截短原文、替换成 Main 摘要或另开嵌套 Codex。Reviewer 没有派发，本轮独立原始 verdict 不存在，review receipt 为空。

自然 Hook 的配置入口已核对：PreToolUse → `.codex/hooks/pre_tool_use_policy.py`；SubagentStop／Stop → `.codex/hooks/subagent_attestation.py`。结构 preflight 通过，但本轮没有原生 child transcript、自然 completion Hook 或明确的项目 Hook trust 完成依据。配置文件存在不能当作实际加载／执行证据。安装器 `project_setup.py::_hook_trust_instruction` 要求真实 trust 与 `/hooks` 操作后方可正式派发；本次尚未到可派发环境，不把“继续任务”算作该确认。

## 历史 failure 是否改善

只能判断**首版行为有部分变化，科研效果未验收**。首次候选继续保留整个连续扫描应用和历史 v2 关键问题，没有因 NNBO／MPC／QP 已有能力而改成告警、拒绝扫描或极小形式残差；逐项给出强版本解释、反例、调参／执行等替代原因，并分别记录 IN_FIELD／CROSS_FIELD 与覆盖程度。实际只提交一个候选，没有为了路径或数量凑数。

这些仍是 Main 的判断。没有新实验失效或独立评审支持痛点规模／价值／prior 分类。首版对 Beber／Xue 等历史诊断中的集成强 prior 尚未显式完整分析；四篇旧方法缺口未关闭，[GAP_NOTES.md](GAP_NOTES.md) 单独记录首版之后的真实摘要核对与未完成部分。不能证明 strong prior 后已经发现真正重要的新痛点，也不能证明没有回避已有工作。**工程测试、历史通过标签及旧审计均不算本轮科研效果证据。**

## 检查与继续入口

相关检查 45 passed、247 deselected；当前 `python -m harness check` 通过。隔离缺失证据检查仍拒绝已选全文候选缺卡；[ADAPTATION_CHECK.json](ADAPTATION_CHECK.json) 保存该工程检查、原归档文件哈希、113 个当前绑定哈希及历史 JSONL 原内容保留验证。工程检查未写入科学证据。

当前 live `.aris` 留在原目录。[CURRENT_RUN_SNAPSHOT.zip](CURRENT_RUN_SNAPSHOT.zip) 和 [CURRENT_RUN_SNAPSHOT.json](CURRENT_RUN_SNAPSHOT.json) 保存 117 个当前 run／canonical／共享证据文件的真实字节。`.gitattributes` 固定本案例和 `idea-stage` 的字节，避免上传／检出行尾转换破坏记录哈希。一次性 capture/import/checkpoint 脚本保留用于解释本次接入；**继续时不要重跑 import，不要覆盖已推进的状态**。在新的空研究工作副本中恢复时，可用 `python -m zipfile -e cases/softscan-20261005/CURRENT_RUN_SNAPSHOT.zip .` 恢复该检查点，先核对 snapshot manifest 的哈希及当前根目录运行配置。

在具有配置角色派发能力、真实项目 Hook trust 和自然 child-completion 路径的运行环境中，继续同一 run：

```powershell
python -m harness science status impedance-control-landscape-e2e
python -m harness science allowed-actions impedance-control-landscape-e2e
python -m harness science review-handoff impedance-control-landscape-e2e
```

由新鲜独立 `scientific_reviewer` 使用该 request 的绑定原文执行；若只能用兼容模式，必须完整发送 `--dispatch-mode native_generic_compat` 输出的 exact task，不截短。只有实际 Hook-attested verdict 可原样 `science submit-review`。收到修订／补证意见时按同一 run 处理并另存后续版本；真正进入 PROBLEM_SELECTION 后再交付人工选择并停止。当前没有可以执行的人工选择 request，不执行选题或方法命令。
