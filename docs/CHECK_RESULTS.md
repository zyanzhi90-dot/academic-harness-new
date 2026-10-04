# 第一步工程检查结果

检查日期：2026-10-05。使用合成数据、mock Gateway 和测试用 reader/reviewer receipt；没有执行真实文献调研、科研案例或物理实验。

| 检查 | 实际结果 | 可支持的判断 |
| --- | --- | --- |
| 独立 `.venv`：`pip install -e ".[dev]"` | 安装成功；Python 3.10.11、PyYAML 6.0.3、pytest 9.1.1 | 新源码可独立安装，不需要旧 ARIS 安装 |
| 独立 `.venv`：`python -m pytest -q --tb=short --junitxml=.aris/checks/foundation.xml` | **378 passed**，0 failed，0 skipped，278.76 秒 | 迁移后的既有 kernel 检查和新基座检查通过 |
| 最终交接输出调整后：`python -m pytest checks vendor/aris/tests/test_recovery_snapshot.py -q --tb=short` | **7 passed**，12.01 秒 | 最新交接、连续更新、安装后 hook 及恢复入口通过 |
| `python -m harness check` | `ok: true`；88 条复用文件记录、15 个运行模块、单一 landscape 阶段；无错误 | 文件哈希、内置 profile 镜像、必读依据哈希、运行资源、引用和 import 闭包完整 |
| 从仓库外调用安装后的 `academic-harness check` 与子命令帮助 | 成功 | editable 安装后的命令可从研究项目目录调用 |
| `pip check`、`compileall` | 无依赖冲突；编译通过 | 当前解释器下的依赖和代码语法可运行 |
| 原来源文件逐文件哈希与旧 Git 状态复核 | 与初始记录一致 | 本轮未改写所选旧源文件，旧项目已有八个未提交修改保持原状态 |
| `git diff --check` 与暂存区检查 | 通过；两个原样复用 reference-paper-intake 文件的既有末尾空行以属性保留 | 新改动无空白错误；提交／remote 同步在交付时另行核实 |

## 已验证能力

- 新 CLI 创建、加载、查询调研状态；默认 profile 只声明 landscape。
- 来源策略起草、校验与人工批准链；查询计划、候选筛选、Initial Map 与正式 Primary 阅读。
- 原 Gateway 的检索顺序、元数据处理、访问失败／人工补交分支、浏览器页面处理、Evidence 及来源链；相关外部调用使用 mock。
- 领域地图校验、覆盖 review、缺口继续检索、地图历史和证据保留。
- 新 standalone 调研覆盖接受后停在 LANDSCAPE_ACCEPTED，不进入旧后半段；调研交接包含地图、来源策略、覆盖判断、查询计划、Corpus／Ledger／Registry 和 Evidence 的路径及哈希。
- 连续两次知识缺口更新在同一 run 中完成，保留 P1 的原 Evidence，新增并复用 P2，归档地图版本，保留问题／路线上下文，更新期间不伪装为已接受交接。
- 安装到研究目录的 hook 在隔离 Python 进程中找到新 vendor 运行时；新恢复快照沿新入口读取并保持地图哈希。
- 原 phase-scoped 增量调研和后半段相关 kernel 的既有检查通过。这只说明复用实现的回归检查保持，不表示新问题／方法模块已完成。

## 待实际运行确认

- SerpApi、Google Scholar／IEEE 可见浏览器、arXiv、Crossref／OpenAlex、OA 全文及机构访问在使用环境中的实际可用性。
- Codex 是否加载研究目录的 `.codex` 配置、原有 hook 信任与 native reader／reviewer 的真实生命周期；本轮验证的是文件配置、Python hook 和 receipt 路径，未派遣真实科研角色。
- 具体领域的检索覆盖、地图科学质量、重要痛点、prior 分类及方法产出的推导和理论／实验验证。
- 新问题发现、人工选择与问题版本、可调整技术路线、统一贡献／验证循环及 ARS／Nature 能力接入；下一步需求见 NEXT_INTERFACES.md。
- 既有案例成果接入新 workflow 的映射。本轮原样保留旧成果，不复制或改写案例状态。

当前结论是工程基座和调研入口通过上述检查。稳定产出顶会顶刊级方法仍是建设目标，需要后续真实科研产物验收。
