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

- 按用户明确指定的步骤执行，保持修改最小且完整。
- 旧 Harness 用于参考；对新项目的操作只在新目录中执行。
- 不覆盖或提交旧项目中已有的未提交修改。

## 本地 Git 配置

当前目录已设置 `core.hooksPath=.githooks`，因此每次提交都会触发自动推送。
在新克隆中继续工作前，执行 `git config --local core.hooksPath .githooks` 以启用同一规则。
