# Agent Test Skills

供大模型和 agent 使用的测试工作流，包含测试用例设计与测试用例执行两份独立 skill。

| Skill | 用途 | 主要产物 |
|---|---|---|
| [test-case-writing](skills/test-case-writing/SKILL.md) | 从需求设计、评审和维护测试用例；主动澄清需求缺口与冲突 | 需求依据、用例、待澄清问题、设计覆盖关系与执行条件 |
| [test-case-execution](skills/test-case-execution/SKILL.md) | 在指定环境实际执行用例、记录证据、复现与复测 | 逐用例及逐断言结果、缺陷、阻塞问题、执行报告与证据 |

推荐先编写并澄清用例，再执行；也可以单独使用任意一份。执行 skill 支持已有用例格式，无需先经过编写 skill。

## 项目结构

本项目采用 [Agent Skills 通用规范](https://agentskills.io/specification)：每个 skill 是一个独立目录，以带 YAML frontmatter 的 `SKILL.md` 为入口，详细内容通过相对路径按需加载。

```text
.
├── README.md
├── skills/                              # 可独立安装的 skill 源文件
│   ├── test-case-writing/
│   │   ├── SKILL.md                     # 名称、适用场景与设计流程
│   │   └── references/
│   │       ├── case-format.md           # 用例交接格式与示例
│   │       └── design-decisions.md      # 澄清、选例与变更的判断方法
│   └── test-case-execution/
│       ├── SKILL.md                     # 名称、适用场景与执行流程
│       └── references/
│           ├── run-record.md            # 执行记录、证据与报告格式
│           └── exceptions.md            # 异常判定与恢复案例
└── docs/                                # 仓库维护资料
    ├── test-case-writing-skills.md       # 第三方项目调研与选型资料
    └── skill-validation.md              # 本项目的设计与验证记录
```

安装时复制选中的整个 skill 目录，包括 `references/`。根目录 README 与 `docs/` 供维护者阅读，无需随单个 skill 安装。

通用规范中的 `scripts/`、`assets/` 等目录为可选项。本项目目前使用说明和参考文件实现工作流；需要时再添加实际使用的脚本或资源。客户端专属的 UI 元数据和插件配置也不作为通用格式的必需项。

## 使用条件

- 使用支持 Agent Skills 的客户端，或能读取本地 Markdown 文件及其引用文件的 agent。
- 编写用例时，需要可访问的需求材料，以及用于澄清问题的对话能力。
- 执行用例时，需要目标环境、相应角色的会话、测试数据及实际操作与观察工具。具体可以是浏览器、应用连接器、API 或命令行工具，按测试目标选择。

这两份 skill 本身没有固定的运行时依赖。执行工具、账号和目标系统由使用环境提供；安装 skill 不会自动安装浏览器、配置认证或启动被测应用。

## 安装与加载

### 安装到支持 Agent Skills 的客户端

将所需目录复制到客户端支持的 skill 发现目录。目录名称与 frontmatter 中的 `name` 一致：`test-case-writing`、`test-case-execution`。客户端支持的安装位置和显式调用语法以其文档为准。

对于 Codex，[官方技能文档](https://learn.chatgpt.com/docs/build-skills)列出的本地位置包括：

| 使用范围 | 安装位置 |
|---|---|
| 项目级 | `<目标项目>/.agents/skills/` |
| 用户级 | `~/.agents/skills/` |

在本仓库根目录运行以下命令，可首次安装到一个目标项目。将示例路径替换为实际项目路径：

```bash
QA_TARGET_PROJECT="/absolute/path/to/your-project"
mkdir -p "$QA_TARGET_PROJECT/.agents/skills"
cp -R skills/test-case-writing "$QA_TARGET_PROJECT/.agents/skills/"
cp -R skills/test-case-execution "$QA_TARGET_PROJECT/.agents/skills/"
```

用户级首次安装：

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/test-case-writing "$HOME/.agents/skills/"
cp -R skills/test-case-execution "$HOME/.agents/skills/"
```

更新已有安装时，先核对同名 skill 中的本地修改，再更新完整目录。安装后按客户端方式查看技能列表；若 Codex 中未出现，可重启后检查。[官方说明](https://learn.chatgpt.com/docs/build-skills)

仓库中的 `skills/` 是分发目录；仅克隆本仓库不代表客户端已经自动加载了其中的 skill。

### 直接按文件使用

在能够读取本仓库的 agent 中，也可直接要求：

```text
请读取 skills/test-case-writing/SKILL.md，按其中流程为 docs/invite-prd.md 编写测试用例。
按需读取 SKILL.md 中引用的 references 文件。
```

这里的路径相对于本仓库根目录；跨项目使用时，提供实际可访问的完整路径。直接读取文件是显式使用流程，不等同于客户端的自动发现与加载。

## 使用示例

以下 `$skill-name` 是 Codex 的显式调用写法；其他客户端使用对应的技能选择或调用方式。示例中的需求文件、地址、账号别名和输出位置需要替换成实际值。

### 1. 从需求编写用例

```text
使用 $test-case-writing，为 docs/invite-prd.md 的团队邀请功能编写测试用例。
本轮覆盖所有者邀请、普通成员权限、邮箱校验和邀请过期。
不覆盖批量邀请。
输出到 tests/cases/invite.md；需求冲突或影响预期的规则缺失时向我澄清，
同时继续完成不依赖答案的部分。
```

需求未形成文档时，可以直接描述业务规则，并附原型、用户故事或验收标准。已有用例需要维护时，提供旧用例与变更依据，要求保留稳定 ID 并标出受影响范围。

### 2. 回答澄清问题

```text
关于 Q-001：邀请从成功创建的服务端时间起连续 72 小时有效，等于到期时刻即过期。
请据此更新规则、相关用例、就绪状态和覆盖表，保留原用例 ID。
```

agent 应将答复落实到实际预期和测试数据约束。只缺少执行时的账号或环境实例，可以继续完成设计；会改变业务结果的未决规则仍须标为待澄清。

### 3. 执行已有用例

```text
使用 $test-case-execution，执行 tests/cases/invite.md 中的 READY 用例。
目标为测试环境 https://staging.example.com，构建标识以环境实际信息为准。
已有 owner-test 和 member-test 两个授权会话，使用项目现有浏览器工具。
允许在该测试环境创建并清理本次测试数据，收件地址使用团队受控测试邮箱。
本轮仅执行与记录；缺少条件时向我澄清，并继续其他独立用例。
报告输出到 tests/runs/invite-run-001/report.md。
```

会话使用别名或现有授权入口说明，不在提示词或报告中填写密码和令牌。更换为 API 或命令行工具时，仍需实际验证用例要求的目标；例如验证页面交互时，需要能够操作和观察页面。

### 4. 补充条件后恢复或修复后复测

```text
管理员会话已准备好，请继续上次因 Q-002 阻塞的用例。
先核对原环境、对象和前置状态仍然有效；保留原运行记录及证据。
```

```text
缺陷 D-001 已在新构建中修复，请复测关联用例并检查直接受影响的回归范围。
另存本次结果，关联原失败记录；旧版本的通过结果不计入新构建的通过汇总。
```

另开对话时，同时提供原用例、执行报告、环境和已确认的澄清答复，便于恢复上下文。

## 输入、输出与状态

| 阶段 | 建议提供的输入 | 默认输出位置 |
|---|---|---|
| 用例设计 | 需求来源与版本、范围、角色、已有用例和验收约定 | `tests/cases/<feature>.md` |
| 用例执行 | 用例来源与版本、目标环境、执行范围、会话、数据和可用工具 | `tests/runs/<run-id>/report.md`，证据保存在本次运行目录 |

输出路径相对于执行任务的工作项目，用户指定路径和项目约定优先。设计与执行各使用自己的状态：

| 阶段 | 状态 | 含义 |
|---|---|---|
| 设计 | `READY` | 预期有依据，步骤、数据要求和观察方式已明确；执行条件仍需核对 |
| 设计 | `NEEDS_CLARIFICATION` | 业务预期或适用条件依赖未解决问题 |
| 执行 | `PASS` | 前置条件有效，全部断言已实际验证符合预期 |
| 执行 | `FAIL` | 至少一个明确预期有证据证明被违反，保留其他未验证项 |
| 执行 | `BLOCKED` | 尚无已证实违背，但缺少条件或证据，无法完成判断 |
| 执行 | `NOT_RUN` | 已选定但尚未尝试，且未确定阻塞原因 |

首次失败后诊断重试通过，仍保留本轮首次失败和重试记录；修复后的独立复测可以产生新的结果。覆盖矩阵描述设计范围，执行报告描述实际验证结果，两者分别维护。

## 维护与验证

- 修改 `SKILL.md` 时保留有效的 `name`、`description`；名称与所在目录保持一致。
- 引用文件使用 skill 内部的相对路径，确保单独复制目录后仍能读取。
- 新增脚本或资源时，放入对应 skill 的 `scripts/` 或 `assets/`，并从入口说明何时使用。
- 修改业务判断流程后，用有歧义的需求或有障碍的执行场景检验实际行为；结构校验只能验证格式。

已有[设计与验证记录](docs/skill-validation.md)包含独立模拟试用及其验证边界。[第三方项目调研](docs/test-case-writing-skills.md)是背景选型资料，其中的历史安装命令和仓库信息按其核实日期理解，使用时以对应项目当前文档为准。

格式参考：[Agent Skills Specification](https://agentskills.io/specification)。Codex 安装与调用参考：[官方技能文档](https://learn.chatgpt.com/docs/build-skills)。
