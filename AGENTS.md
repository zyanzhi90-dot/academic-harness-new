# 项目工作规则

## 项目位置

- 新项目：`D:\桌面\科研harness-新`。
- 旧 Harness：`D:\桌面\科研Agent Harness设计`，主体位于 `ARIS` 子目录。
- GitHub 仓库：https://github.com/zyanzhi90-dot/academic-harness-new。
- Git remote：`origin`，地址为 `git@github.com:zyanzhi90-dot/academic-harness-new.git`。
- 默认分支：`main`。

## 每次修改后自动提交并上传

用户已明确授权本项目每次修改后的 Git 提交和 GitHub 推送。后续执行者必须自动完成以下步骤，无须再次询问：

1. 每完成一项完整修改（包括代码、文档和配置），运行与修改相关的必要检查。
2. 检查 `git diff` 和 `git status`，仅暂存本次修改的文件。
3. 执行 `git commit`，提交说明使用 `<type>: <summary>` 格式。
4. 仓库的 `.githooks/post-commit` 会自动将提交推送到 `origin` 的当前分支。
5. 核实推送成功后再报告完成；若推送失败，保留本地提交，解决问题并重试 `git push --set-upstream origin HEAD`。未成功上传时必须明确说明。

不得将已完成的修改留在未提交或未上传状态。不得强制推送，不得提交密钥、访问令牌或本地环境文件。

## 修改范围

- 当前科研要求见 `docs/SCIENTIFIC_REQUIREMENTS.md`，源自根目录两份 `20261004` 规划文件与用户当前指令。
- 实际科研入口为 `python -m harness`；当前只实现领域调研、按缺口更新和调研交接，在 `LANDSCAPE_ACCEPTED` 停止。
- 研究现状、问题发现与方法设计需反复迭代；贡献检查与验证贯穿方法设计。两类问题路径、人工选择、强 prior 后追问、核心问题保持及成熟方法复用以有效要求为准。
- `vendor/aris` 的旧后半段规则是复用材料，不是新设计的必经流程；新问题／方法模块尚未实现。
- ARS-Codex 与 Nature Skills 后续选择性接入统一流程。本轮不运行科研案例或新的文献调研。

- 按用户明确指定的步骤执行，保持修改最小且完整。
- 旧 Harness 用于参考；对新项目的操作只在新目录中执行。
- 不覆盖或提交旧项目中已有的未提交修改。

## 本地 Git 配置

当前目录已设置 `core.hooksPath=.githooks`，因此每次提交都会触发自动推送。
在新克隆中继续工作前，执行 `git config --local core.hooksPath .githooks` 以启用同一规则。
