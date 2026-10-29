# 草稿改名测试用例（合成，用于校验失败诊断与回归范围）

目标为本地命令程序 `/Users/lixinghui/Documents/code/fe/testground/testcases/docs/validation/fixtures/target.py`，调用形式：

```text
python3 target.py <command> --session=<session.json> [--id=<id>] [--name=<name>]
```

命令：drafts、get、rename、export、query、logs、build。
会话文件：`session-member.json`（用户 member-1，角色 member）、`session-other.json`（用户 member-2，角色 member）。

观察通道：`get` 为业务读取，`query` 为存储层原始记录，`logs` 为应用操作日志。

## TC-DIA-001 修改已提交草稿的名称并持久化

- 角色：member-1（会话 `session-member.json`）
- 前置：存在 id 为 `d-2`、owner 为 member-1、name 为 `KeepName`、status 为 `submitted` 的草稿
- 数据：新名称 `NewName`

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 执行 `rename --id d-2 --name NewName` | A1 | 命令输出 `renamed d-2 -> NewName` 且退出码 0 |
| 2 | 执行 `get --id d-2` | A2 | 输出中 name 为 `NewName`，status 仍为 `submitted`，owner 仍为 member-1 |

## TC-DIA-002 修改未提交草稿的名称并持久化

- 角色：member-1（会话 `session-member.json`）
- 前置：存在 id 为 `d-1`、owner 为 member-1、name 为 `OldDraft`、status 为 `draft` 的草稿
- 数据：新名称 `RenamedOK`

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 执行 `rename --id d-1 --name RenamedOK` | A1 | 命令输出 `renamed d-1 -> RenamedOK` 且退出码 0 |
| 2 | 执行 `get --id d-1` | A2 | 输出中 name 为 `RenamedOK`，status 仍为 `draft` |

## TC-DIA-003 修改他人草稿被拒绝

- 角色：member-1（会话 `session-member.json`）
- 前置：存在 id 为 `d-3`、owner 为 member-2、name 为 `OtherDraft`、status 为 `submitted` 的草稿
- 数据：尝试改名为 `Hacked`

| 步骤 | 动作 | 断言 ID | 预期与观察方式 |
|---|---|---|---|
| 1 | 执行 `rename --id d-3 --name Hacked` | A1 | 退出码非 0，stderr 提示 `permission denied` |
| 2 | 执行 `get --id d-3` | A2 | name 仍为 `OtherDraft`，未被改为 `Hacked` |
