# Academic Harness

当前交付是工程基座和完整研究现状调研入口。支持领域地图、文献证据、来源追踪、断点继续和按知识缺口更新；问题发现与方法设计模块在下一步实现。有效科研要求见 [SCIENTIFIC_REQUIREMENTS.md](docs/SCIENTIFIC_REQUIREMENTS.md)。

## 安装与检查

需要 Python 3.10 或以上。在新仓库目录创建独立虚拟环境，使用源码的 editable 安装；该安装会引用本仓库内的 `vendor/aris`，不需要安装或访问旧 Harness。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m harness check
.\.venv\Scripts\python.exe -m pytest -q
```

以下命令中的 `python` 指安装了新项目的虚拟环境解释器。控制台入口 `academic-harness` 与 `python -m harness` 等价。

## 使用调研入口

将科研产物存放在独立研究目录。开始实际科研前，在 Codex 中以该研究目录作为活动项目打开；复制的 `.codex` 运行配置需要被当前会话加载。`--root` 指向产物目录，不能代替 native reader/reviewer 对活动项目目录的要求。

```powershell
python -m harness --help
python -m harness --root "<研究目录>" lit start "<run-id>" --executor "<实际执行模型标识>"
python -m harness --root "<研究目录>" lit status "<run-id>"
python -m harness --root "<研究目录>" lit allowed-actions "<run-id>"
python -m harness --root "<研究目录>" lit allowed-agents "<run-id>"
```

调研执行者读取 [research-lit Skill](skills/research-lit/SKILL.md)，按照当前状态执行。保留的链路如下：

1. 起草来源策略，提交校验后由用户批准。模板在 `vendor/aris/templates/SOURCE_ADMISSION_POLICY_TEMPLATE.yaml`，应按项目填写。
2. 提交查询计划，执行分层检索，核验身份并筛选候选。保留综述、高引用骨干、近期前沿、定向补缺、分页及引文扩展。
3. 选择初始阅读集合，读取全文并形成 Evidence Cards；建立 Initial Map，再依据地图选择正式 Primary 集合。
4. 根据证据修订同一份领域地图，由独立 coverage reviewer 判断覆盖；缺口继续进入调研循环。
5. 覆盖及机械检查通过后停在 `LANDSCAPE_ACCEPTED`，可交接地图与证据。当前不会自动进入问题发现或方法设计。

调研 Skill 保留从现有地图和结构化 Evidence 派生 `ACTIVE_FIELD_MAP_AUDIT.md` 的人类审计说明；该视图便于核对支持论文，不参与状态推进。恢复快照通过 `lit save-recovery` 保存，新快照记录新入口的继续运行命令。

各命令参数沿用旧调研 CLI，例如：

```powershell
python -m harness lit submit-query-plan --help
python -m harness lit admit --help
python -m harness lit select-reading-subset --help
python -m harness lit submit-field-map --help
```

来源策略校验后，必须由人工明确选择批准或要求修订；AI 只记录该决定，不自行批准。以研究目录为当前工作目录，单独运行对应命令，保留以下完整前缀（审批命令不在 `lit` 前插入 `--root`）：

```powershell
python -m harness lit human-approve "<run-id>" source_policy_approval --decision approve
python -m harness lit request-source-policy-revision "<run-id>"
```

这两行表示不同人工决定，不连续执行。`python3 -m harness`、`py -m harness` 和 `academic-harness lit` 的对应前缀也受相同提示规则覆盖。安装到研究目录的 PreToolUse Hook 放行这些前缀，由 `.codex/rules/aris.rules` 逐次提示人工确认；Hook 放行本身不代表批准。若当前运行环境不能显示确认，交由人工在该研究目录直接执行，不由 AI 替代确认。其余命令仍可使用上方的全局 `--root` 写法。

已在旧提交下初始化的研究目录，可从该目录运行 `python -m harness lit start "<已有run-id>" --executor "<实际执行模型标识>"` 刷新受管 `.codex` 层；原 run 的地图和证据继续保留。按已有 Hook 信任说明确认变更后的定义并加载当前项目配置；安装器不会覆盖已有 `AGENTS.md`，因此其审批说明须参照本节更新。

SerpApi 使用环境变量 `SERPAPI_KEY`；浏览器 Scholar 和 IEEE Xplore、arXiv、元数据核验、OA 全文及人工补交等路由按保留的来源策略和 Gateway 调用。未配置或不可用的路由会返回原有人工检索／全文交接，不自动把缺失访问解释为不存在相关研究。本轮没有测试这些外部服务的实际可用性。

## 按需补充调研与交接

已接受地图后，用具体缺口重新打开同一 run。调用者可以是领域认知、问题发现或方法设计；`context.json` 是可选对象，记录核心应用、人工选定问题及版本、路线版本和当前判断目的。

```powershell
python -m harness --root "<研究目录>" update-literature "<run-id>" --requested-by method_design --gap "<会影响当前判断的知识缺口>" --context context.json
python -m harness --root "<研究目录>" lit allowed-actions "<run-id>"
python -m harness --root "<研究目录>" literature-handoff "<run-id>"
```

更新复用同一 Corpus、Search Ledger 和 Evidence Registry；计划必须覆盖请求的缺口，历史 Evidence 可在当前范围内继续使用，仅按需读取新材料。新地图再次走已有覆盖检查；完成后回到 `LANDSCAPE_ACCEPTED`。旧地图版本归档，交接包含当前文件路径、哈希、Evidence 引用及更新请求上下文。更新进行中不能交接为已接受地图。

既有科研案例与成果完整保留在旧目录，本轮没有复制案例状态、重做文献或运行案例。旧案例的状态绑定历史 workflow，不能直接作为新 `literature_only` run 的状态文件；后续若需要接入既有案例，应明确映射其已接受成果，保留证据及来源，不重新调研。

## 交付与下一步

- [迁移依据](docs/MIGRATION_PRECHECK.md)：实际来源、复用范围、适配与已有工作。
- [复用清单](docs/REUSE_MANIFEST.json)：逐文件来源及迁移后的哈希，含本地未提交修改说明。
- [检查结果](docs/CHECK_RESULTS.md)：工程已验证能力与实际运行待确认部分。
- [下一步接口](docs/NEXT_INTERFACES.md)：问题发现、人工选择、技术路线和贡献验证的接入要求。

完成修改后按 `AGENTS.md` 自动检查、提交；Git `post-commit` hook 自动上传到新仓库。新克隆启用 hook：`git config --local core.hooksPath .githooks`。
