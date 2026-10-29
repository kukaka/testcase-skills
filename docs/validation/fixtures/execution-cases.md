# 草稿系统测试用例（合成，用于校验澄清闸门）

以下用例针对本地命令目标 `/tmp/qa-gate-eval/target/target.py` 执行。
会话文件：`/tmp/qa-gate-eval/target/session-member.json`（用户 member-1，角色 member）。

## TC-EXP-001 成员改名自己的草稿并持久化

- 角色：member-1（会话 `session-member.json`）
- 前置：存在 id 为 `d-1`、owner 为 member-1、name 为 `OldDraft`、status 为 draft 的草稿
- 数据：新名称 `NewDraft`

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 用 member-1 会话执行 `rename --id d-1 --name NewDraft` | A1 | 命令输出 `renamed d-1 -> NewDraft` 且退出码 0 |
| 2 | 用 member-1 会话执行 `get --id d-1` | A2 | 输出中 name 为 `NewDraft`，owner 仍为 member-1，status 仍为 draft |

## TC-EXP-002 管理员导出全量草稿

- 角色：具备导出权限的管理员
- 前置：环境中存在至少一条草稿记录

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 用具备导出权限的管理员会话执行 `export` | A1 | 命令输出每条草稿的 `exported <id> <name>` 行且退出码 0 |

## TC-EXP-003 成员改不了别人的草稿

- 角色：member-1（会话 `session-member.json`）
- 前置：存在 id 为 `d-1`、owner 为 member-1 的草稿；另有会话 `session-other.json`（用户 member-2）
- 数据：尝试改名为 `HackedDraft`

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 用 member-2 会话执行 `rename --id d-1 --name HackedDraft` | A1 | 退出码非 0，stderr 提示 `permission denied` |
| 2 | 用 member-1 会话执行 `get --id d-1` | A2 | name 仍为执行前的值，未变成 `HackedDraft` |
