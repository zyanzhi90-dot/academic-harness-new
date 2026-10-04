# 第一步迁移前核对（2026-10-04）

本文件记录已完成的只读核对。工程基座及调研迁移尚未完成，不能据此宣布第一步通过验收。

## 已有工作与目标仓库

- 新项目已有提交 `aa518efe7c67f728c7a3ae3690bcf564d7c4b271`。
- 本地 `main` 与实际 remote 的 `refs/heads/main` 一致，核对时工作区干净。
- 实际 remote：`git@github.com:zyanzhi90-dot/academic-harness-new.git`，对应用户指定的 GitHub 仓库。
- 保留现有 `AGENTS.md`、Git 提交后自动推送 hook、换行规则和忽略规则。

## 尚缺的必读依据

用户要求先阅读以下两份文件，以用户确认的科研思路为准：

- `科研Harness_新对话接力与长期规划依据_20261004.txt`
- `科研Harness_基座与复用方案_20261004.md`

在新旧项目、桌面、用户文档和下载目录，以及扩展的可读文件路径检索中均未找到。部分系统目录无法访问。需要用户提供两份文件的实际完整路径或正文，才能核定迁移组织方式及两类问题发现路径的确切要求。

## 旧项目的实际基线

- 来源目录：`D:\桌面\科研Agent Harness设计\ARIS`。
- 来源分支：`scientific-core`。
- 来源提交：`4212c84da80fac41a3433cf01859d955617888dc`。
- 来源 remote：`git@github.com:zyanzhi90-dot/research-harness.git`。
- 项目声明：`aris-harness-controller`，版本 `0.2.0`，Python `>=3.10`，直接依赖 `PyYAML>=6`。
- 授权文件：旧项目 `LICENSE` 为 MIT，复用时须保留版权与许可文本。

来源工作区存在未提交修改，不能将实际文件等同于上述提交：

```text
arisctl/controller.py
arisctl/validators.py
skills/shared-references/idea-workflow.yaml
skills/shared-references/method-design-contract.md
skills/skills-codex/shared-references/idea-workflow.yaml
skills/skills-codex/shared-references/method-design-contract.md
tests/test_aris_controller.py
tools/run_state.py
```

本轮截至此核对记录仅对旧项目执行只读操作。正式迁移时须记录实际选用文件的内容哈希，并注明是否包含上述本地修改。

## 已确认的依赖关系

| 能力或入口 | 实际依赖 | 对迁移的影响 |
| --- | --- | --- |
| `python -m arisctl` | `__main__`、Controller、工作流、状态、校验器、reviews、recovery、transcript_attestation、gateways | 仅复制 Skill 无法运行入口 |
| 状态推进与断点继续 | `arisctl/state.py`、`tools/run_state.py`、`tools/provenance.py` | Controller 与通用状态工具须一起复用 |
| 检索、元数据核验、全文访问 | `arisctl/gateways.py`、`browser_scholar.py`、`browser_ieee.py` | 浏览器适配为运行时依赖；外部服务与浏览器可用性须另行确认 |
| 文献证据及来源追踪 | Gateway 事件记录、Corpus、Search Ledger、Evidence Registry、Evidence Card 校验 | 保留证据内容与事件之间的关联，不能只保留领域地图文本 |
| 领域地图和覆盖判断 | `tools/literature_coverage_audit.py`、`arisctl/validators.py`、`coverage_reviewer` 配置 | 包含方法族、发展脉络、瓶颈、边界和未解决问题线索 |
| 按需增量调研 | Controller 的 `incremental_literature_active`、阶段证据绑定、共享 Gateway 与 Registry | 旧入口依赖 scientific-core 阶段，不可遗漏；新入口适配须独立验证 |
| 项目本地运行层 | `arisctl/project_setup.py` 中的 `MANAGED_FILES`、`.codex` 配置、角色、hook、规则 | 初始化会复制这些文件，均是隐含资源依赖 |
| 调研科学规则 | 两份 `research-lit/SKILL.md` 与它们链接的 `source-admission-policy.md`、`problem-discovery-contract.md`、`fan-out-pattern.md` | 必须追踪相对链接及其后续引用，不能只复制主文档 |
| 默认工作流 | `skills/shared-references/idea-workflow.yaml`、镜像文件、`arisctl/workflow.py` | 加载器强制要求完整 scientific-core 声明 |

上述来自 Python import 和资源访问检查，尚未构成迁移后完整性验证。

## 已确认需要处理的适配点

1. Controller 构造函数只接受 checked-in canonical workflow；加载器要求完整 scientific-core 声明。新项目入口须保留调研功能，同时避免将旧后半段作为新科研设计的必经流程。
2. `project_setup.py` 生成的项目说明硬编码旧 Harness 路径。复用后的运行不得继续依赖旧目录。
3. 正式增量调研目前依赖旧 scientific-core 的 phase 与 upstream bindings。需依据新规划确定本轮可用的按需入口，以及后续问题发现／方法设计的接入契约。
4. 现有代码混有调研与旧后半段逻辑。可保留复用模块自带机制；用户未要求额外建设旧式安全机制，也未要求清理所有旧机制。

## 后续检查依据

旧项目已有相关检查可用于迁移后验证：`test_aris_controller.py` 中的调研生命周期、来源策略、检索回退、全文读取、Evidence、覆盖与增量调研用例，以及 `test_research_lit_gateways.py`、`test_browser_scholar.py`、`test_browser_ieee.py`、`test_field_map_audit_view.py`、`test_project_setup.py`、`test_aris_cli_output.py`、`test_recovery_snapshot.py`。

本轮尚未运行迁移后的测试，没有执行新的文献调研或科研案例。外部检索服务、浏览器访问、实际 reader/reviewer 运行及科研质量不能用只读依赖分析替代验证。

收到两份规划文件后继续：核定有效科研要求 → 确定完整复用闭包 → 迁移及必要适配 → 验证入口、依赖、调研生命周期与增量入口 → 交付使用说明、迁移清单、检查结果和下一步接口需求 → 提交同步并停止验收。
