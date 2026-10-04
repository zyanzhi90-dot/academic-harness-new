# 基座迁移依据与范围

两份 `20261004` 规划文件已完整读取并保留在项目根目录。以用户确认的科研思路和本轮明确指令为准：交付工程基座与可用调研入口，本轮不执行完整后半段改造或真实案例。

## 仓库与实际来源

- 新仓库实际 remote：`git@github.com:zyanzhi90-dot/academic-harness-new.git`。
- 开始时本地 `main` 与 remote 一致；保留 `aa518ef` 的自动提交／推送配置及 `67d08eb` 的有效依赖核对发现。
- 旧项目：`D:\桌面\科研Agent Harness设计\ARIS`，分支 `scientific-core`，提交 `4212c84da80fac41a3433cf01859d955617888dc`。
- 旧 remote：`git@github.com:zyanzhi90-dot/research-harness.git`；声明包 `aris-harness-controller` 版本 `0.2.0`。
- 规划中的 Harness `5faa38b` 是历史分析版本，本轮按指定本地目录的实际代码复用。
- 来源工作区有八个未提交文件，涉及 Controller、Validator、run_state、workflow、method contract 镜像及 Controller 测试。选用实际本地文件，保留已有有效实现；逐文件原始哈希及本地修改标记见 `REUSE_MANIFEST.json`，不将其冒称为纯提交内容。

旧项目仅作只读来源，未提交、推送或改写旧代码。旧科研案例及已接受成果保留在原目录；本轮未复制案例状态、运行案例或重新调研。

## 实际依赖与组织

运行时位于 `vendor/aris`，保持原 import 与资源相对位置。新入口 `python -m harness` 显式加载这份运行时及 `literature-workflow.yaml`。使用新源码的 editable 安装，可从独立研究目录调用，不依赖旧项目或旧 ARIS 安装。

| 保留范围 | 实际依赖与用途 |
| --- | --- |
| 全部 `arisctl` Python 模块 | CLI、Controller、状态、工作流、Validator、检索／全文 Gateway、Scholar／IEEE 浏览器适配、reviews、transcript attestation、recovery 的 import 闭包 |
| 三个 `tools` 文件 | `run_state.py`、`provenance.py`、`literature_coverage_audit.py`；状态锁、来源、领域地图交接审计等共享依赖 |
| `.codex` 运行层 | `project_setup.MANAGED_FILES` 对应配置、角色、hook 和规则；实际初始化需要复制 |
| 调研 Skill 及引用闭包 | 原版与 Codex 镜像的 research-lit、来源策略及其引用契约；保持本地 Markdown 引用完整 |
| 相关旧 Skill 资料 | idea-discovery 中的调研人类审计视图、research-refine 及引用文件，供现有回归和后续分析；旧后半段不作为当前执行要求 |
| workflow 与模板 | 旧 workflow 两份镜像用于 kernel 回归；来源策略和方法模板保持链接完整；新 profile 只有 landscape |
| 相关既有测试 | Controller、Gateway、浏览器、领域地图审计视图、项目配置、CLI、恢复、attestation、provenance、run_state，及 fixture import 闭包 |
| 许可和元数据 | 原 MIT `LICENSE`、版权文本及 `pyproject.toml` 随复用代码保留 |

Controller 与 Validator 同时包含调研和旧后半段，拆函数会扩大改动并遗漏共享依赖，因此保留完整 kernel，在默认入口和工作流层切开。外部写作、图像、实验队列、通知、MCP 服务和全量旧 Skill 安装系统不属于本次调研运行闭包，未引入。

## 必要适配

1. 新增 literature-only profile，复用原调研阶段、动作、角色、产物及预算；Loader、Controller 接受该内置 profile，原 profile 用于 kernel 回归。
2. 新入口提供调研命令、按缺口更新及交接；覆盖接受后停在 LANDSCAPE_ACCEPTED，不启动旧后半段。保留的 scientific-core 状态字段标为 NOT_IMPLEMENTED。
3. 同一 run 记录具体缺口、请求来源及可选上下文，复用查询、筛选、阅读、地图修订及覆盖复核。原 phase-scoped 增量代码也保留供后续适配；当前入口不要求旧 RCA／Principle anchors。
4. CLI 可显式调用内置 profile。项目生成说明引用新 checkout 及有效要求，去除旧绝对目录依赖。迁移模块自带机制保留，没有额外建设安全架构。
5. 安装到研究目录的 attestation hook 从已有运行层 manifest 找到新 vendor checkout，避免依赖旧 editable 安装；用隔离进程验证。
6. 当前 `skills/research-lit/SKILL.md` 从旧 Codex 调研 Skill 派生，只改入口、profile、引用和当前科研边界，保留科学调研内容。
7. 修复旧 Codex research-refine 镜像中已有的一个方法模板相对链接，并复制实际模板，以保证复用资料链接完整。

新有效要求明确两类问题路径、人工选择、强 prior 后持续追问、核心问题保持、具体技术主线与成熟方法复用，见 `SCIENTIFIC_REQUIREMENTS.md`。规则已写入当前入口及 AGENTS.md；完整问题／方法模块尚未实现。

## 保留能力与验证边界

保留领域全景、方法族、假设／有效／失败矩阵、证据支持的发展脉络、未解决线索，以及 Corpus、Search Ledger、Evidence Registry、可回查阅读内容和主张定位。综述带动 Initial Map、正式 Primary 阅读、来源筛选、元数据核验、引文扩展、访问失败回退、覆盖补缺、地图历史及断点恢复沿原实现运行。

检查结果见 `CHECK_RESULTS.md`。本轮 fixture／mock 测试验证工程链路与迁移完整性；真实外部服务、Codex native reader／reviewer 生命周期、实际领域地图质量和后半段科研效果仍需实际运行确认，不能据此宣称已稳定产出顶会顶刊方法。
