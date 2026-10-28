# 纯写用例类 Skills 清单

> **范围**：把需求文档 / PRD / User Story 转成结构化测试用例。**只覆盖"写"，不含"执行"**（执行见《QA_MANUAL_SKILL》与 Claude Code 插件目录）。
>
> **核实方式**：所有仓库地址已做 HTTP 可达性校验；标注"已读源"的条目，其 `SKILL.md` 已实际拉取并逐行读过，非仅凭搜索摘要。
>
> **核实日期**：2026-10-19

---

## 快速结论

| 场景 | 选谁 |
|---|---|
| 就要一份 Markdown 用例文档，零依赖 | **`test-cases`** ← 首选，199 行，MIT |
| PRD 很模糊，先澄清再写 | **`product-requirements`**（配 `test-cases`） |
| 要工程化的完整 QA 基建（可多语言项目） | **`qa-plugin`** |
| 要多维测试设计方法（EP/BVA/判定表/状态迁移） | **`qa-skills` (umitozdemirf)** 的 `test-plan-generator` + `input-validation-tester` |
| 用例要直接进 Jira | **`claude-qa-skills`** 的 `jira-story-writing` |
| 已经用 Azure DevOps 管需求 | **`ado-testcraft`** |
| 要 Playwright E2E 代码（不是文档） | **`neonwatty/qa-skills`** |

---

## 一、myclaude 系列（`stellarlinkco/myclaude`）

**仓库**：https://github.com/stellarlinkco/myclaude
> `cexll/myclaude` 是旧地址，HTTP **301 重定向**到此，不要再存。

⚠️ **关键坑**：这三个 skill 都在 **`master` 分支**，不在 `main` 分支。用 `main` 拉会找不到文件。

### 1.1 `test-cases` —— 写用例（首选，已读源）

| | |
|---|---|
| 路径 | `master:skills/test-cases/SKILL.md`（199 行，MIT） |
| 依赖 | **无**。纯 SKILL.md，零脚本、零 MCP |
| frontmatter | ✅ 合法（`name` + `description` + `license`） |
| 输入 | PRD 文件路径 / 口头需求 / User Story |
| 输出 | Markdown 用例文档 + 需求↔用例覆盖矩阵 |

**四步工作流**

1. **收集需求** — `Read` 工具读 PRD；若需求含糊，用 `AskUserQuestion` 澄清（核心用户流、验收标准、边界与异常场景、状态迁移、目标平台）
2. **提取测试场景** — 四类并行展开：
   - `TC-F-xxx` 功能（正常流程）
   - `TC-E-xxx` 边界（边界值、空态、上限）
   - `TC-ERR-xxx` 异常（非法输入、权限失败、网络错误）
   - `TC-ST-xxx` 状态迁移（有状态时覆盖所有合法状态变化）
3. **结构化** — 固定 Markdown 模板，Overview + 四类分区 + 覆盖矩阵
4. **生成**

**单条用例字段**：Requirement 链接 / Priority (High·Medium·Low) / Preconditions / Test Steps（编号） / Expected Results / Postconditions

**覆盖矩阵**（产出末尾）：

```markdown
| Requirement ID | Test Cases | Coverage Status |
|----------------|------------|-----------------|
| REQ-001        | TC-F-001, TC-E-001 | ✓ Complete |
| REQ-002        | TC-F-002 | ⚠ Partial |
```

**核心原则**：需求驱动而非实现驱动；每条需求至少 1 条用例；用例必须无歧义可被 QA 直接执行；需求↔用例可追溯。

**安装**

```bash
# 方式 A（推荐，注意分支）
npx skills add https://github.com/stellarlinkco/myclaude --skill test-cases
# 若 A 拉不到（默认分支是 main），改用 B：

# 方式 B（手动，最稳）
mkdir -p ~/.claude/skills/test-cases
curl -L https://raw.githubusercontent.com/stellarlinkco/myclaude/master/skills/test-cases/SKILL.md \
  -o ~/.claude/skills/test-cases/SKILL.md
```

### 1.2 `product-requirements` —— 需求澄清（配套，已读源）

| | |
|---|---|
| 路径 | `master:skills/product-requirements/SKILL.md`（362 行） |
| 角色 | 人格化"技术产品负责人 Sarah" |
| 机制 | **100 分质量评分制，≥90 分才输出 PRD** |
| 输出 | `docs/{feature-name}-prd.md` |

流程：先并行读 `README` + `package.json`/`pyproject.toml` 建立项目上下文 → 100 分制质量评估 → 分轮澄清（每轮问 2-3 个问题，逐轮收敛）→ 达标后生成 PRD。

**为什么它对你有用**：这是治"PRD 不详细、预期不确定"的现成方案——把模糊需求逼成 90 分以上的可执行规格，再交给 `test-cases` 展开成用例。

### 1.3 `requirements-clarity` —— 同类，⚠️ 当前装不了

| | |
|---|---|
| 路径 | `main:requirements-clarity/skills/SKILL.md`（318 行） |
| 机制 | 同样 100 分评分、迭代到 ≥90 分 |
| ❌ **问题** | **文件没有 YAML frontmatter**，Claude Code 不会自动发现 |

需要的话手动补 frontmatter 即可启用：

```yaml
---
name: requirements-clarity
description: 澄清模糊需求并迭代生成可执行 PRD。当用户提出模糊的功能请求、缺少验收标准或边界条件不清时使用。
---
```

**取舍**：`requirements-clarity`（main）和 `product-requirements`（master）功能高度重叠，**用 `product-requirements` 即可**，不必两个都装。

### 1.4 `browser` —— 配套的浏览器能力

| | |
|---|---|
| 路径 | `master:skills/browser/SKILL.md` |
| 机制 | Chrome DevTools Protocol 驱动本地 Chrome，**不需要 MCP server** |

如果执行侧不想装 Playwright MCP，这个是零依赖备选（可与 A 组 `qa-execute` 配套）。

---

## 二、`ado-testcraft` —— Azure DevOps 专用（已读源）

**仓库**：https://github.com/dgambhir01/ado-testcraft
**分支**：`main`，Claude Code 插件形式（也在官方插件目录里）

| Skill | 行数 | 作用 |
|---|---|---|
| `skills/setup` | 109 | 配置 `ADO_ORG` / `ADO_PROJECT` / `ADO_PAT` 凭证 |
| `skills/generate` | 118 | **从 ADO User Story 生成结构化用例**（正向/反向/边界值） |
| `skills/test-coverage` | 189 | 分析 User Story 的覆盖缺口——拉取验收标准 + 已关联用例（`Tested By` / `Tests` 关系），输出已覆盖/部分覆盖/未覆盖对照表 |

**适合**：需求已经在 Azure DevOps 上、用例也要关联回 Story 的团队。
**不适合**：纯本地 Markdown PRD——有 ADO 依赖包袱。

> ⚠️ 官方插件目录里也有一个同名 `ado-testcraft`，源仓库就是上面这个。

---

## 三、`qa-plugin` —— 工程化 QA 基建（已读源）

**仓库**：https://github.com/Kokoszsz/qa-plugin
**分支**：⚠️ **`master`**（`main` 没有）
**路径**：`plugins/qa/`

**4 个 skill**

| Skill | 行数 | 作用 |
|---|---|---|
| `qa-scanner` | 90 | 深度项目分析引擎：扫描目录结构、模块、入口、API 端点、组件、业务逻辑层、测试机会点 |
| `qa-scaffolder` | 159 | 基于扫描报告 + 模板，把**项目专属的** skill/agent/command + `qa-config.json` 生成到 `.claude/` |
| `qa-differ` | 81 | 检测生成物与项目现状的漂移：标记 `CURRENT` / `OUTDATED` / `STALE` / `MISSING` |
| `qa-coordinator` | 43 | 按当前 QA 状态给出"下一步建议"，让各命令保持流程连贯 |

**4 个 command**

| Command | 作用 |
|---|---|
| `/qa:init` | 分析项目 → 生成完整 QA 测试基建到 `.claude/`，自动探测技术栈、推荐测试类型 |
| `/qa:scenarios` | **生成 Gherkin 格式的功能用户场景**；可独立从代码分析产出，也可 `--spec <path>` 追加到已有 spec |
| `/qa:analyze` | 测试健康度深度分析：质量问题、覆盖缺口、未测用户流、优先级建议（**只读，不改文件**） |
| `/qa:sync` | 基建健康检查、开关测试类型、调阈值、重生成过时产物 |

**支持语言**：TS / JS / Python / Go / Rust / Java / Ruby / PHP / Elixir / Swift / Dart

**特点**：唯一有"**产物漂移检测**"的（`qa-differ`）——适合长期维护，PR 改了代码能告诉你哪些用例过时了。

---

## 四、`qa-skills` (umitozdemirf) —— 多维测试设计（已读源）

**仓库**：https://github.com/umitozdemirf/qa-skills
**分支**：`main`
**路径**：`integrations/claude/.claude/commands/qa/`（9 个 command），实际 skill 定义在 `qa-skills-plugin/skills/`

| Command | 作用 |
|---|---|
| `test-plan-generator` | 生成测试计划 |
| `e2e-test-generator` | 生成 E2E 测试 |
| `api-test-generator` | 生成接口测试 |
| `service-test-generator` | 生成服务层测试 |
| `input-validation-tester` | **输入校验专项测试**（对模糊 PRD 特别有用——专门戳输入边界） |
| `risk-analyzer` | **风险分析**（把"哪里最可能出问题"显式化） |
| `test-coverage-analyzer` | 覆盖分析 |
| `test-smell-detector` | **测试坏味道检测**（用例重复、断言缺失、脆弱写法） |
| `security-test-generator` | 安全测试用例生成 |

**设计原则**：只用原生框架（pytest / vitest / JUnit / go test），E2E 专供 Playwright，code-first、CI 友好。跨 agent 支持 Claude Code / Codex / Gemini CLI / OpenCode。

**对你的价值**：`input-validation-tester` + `risk-analyzer` 这两个是**不依赖明确规格也能跑**的——它们问的是"这个输入会怎样""哪里最容易坏"，而不是"预期结果是什么"。正好补 PRD 模糊的洞。

**安装**

```bash
npx skills add https://github.com/umitozdemirf/qa-skills
# 或
claude plugin marketplace add umitozdemirf/qa-skills
```

---

## 五、`claude-qa-skills` (deepaktiwari09) —— 全栈 + Jira（已读源）

**仓库**：https://github.com/deepaktiwari09/claude-qa-skills
**分支**：`main`

| Skill | 行数 | 作用 |
|---|---|---|
| `ui-qa-testing` | 318 | playwright-cli 驱动的 E2E UI 测试：测用户流、验证 User Story、多角色测试、生成证据报告 |
| `api-qa-testing` | 423 | API 测试 + 性能基准：curl、Hurl（断言 + 链式）、httpie、hey（压测）、jq |
| `db-qa-testing` | 466 | 数据库 QA：PostgreSQL / MySQL / MongoDB，查询优化、索引分析、schema 审计 |
| `jira-story-writing` | 333 | **写"人话"且能被自动化直接测的 Jira story / bug / subtask**（走 MCP） |

**Command**：`/qa`（随时在会话中调用）、`/qa-report`（从会话数据生成 QA 知识库报告）、`/add-logging`（加 dev-only 结构化日志）

**对你的价值**：`jira-story-writing` 解决"用例写完要人工录进 Jira"的痛点——它的产出同时满足人和 playwright-cli 自动化。

---

## 六、`qa-skills` (neonwatty) —— 面向 Playwright 代码（已读源）

**仓库**：https://github.com/neonwatty/qa-skills
**分支**：`main`
**插件安装**：

```bash
claude plugin marketplace add neonwatty/qa-skills
claude plugin install qa-skills@neonwatty-qa
```

**流水线**

```
/setup-profiles → Generators → workflow markdown → ┬→ Converters → .spec.ts → CI (GitHub Actions)
                                                      └→ Runner (Playwright CLI) → 本地交互测试
```

**关键**：`/setup-profiles` 为每个用户角色开一次有头浏览器，**你手动登录**（自动处理 OAuth / 2FA），会话状态存到 `.playwright/profiles/`。生成的测试自动加载这些 profile。

**6 个 QA agent**：`mobile-ux-auditor` / `adversarial-breaker`（对抗性破防）/ `smoke-tester` / `ux-auditor` / `security-auditor` / `performance-profiler` / `validation-subagent`，各带 `references/` 支撑文档（iOS HIG 规范、移动端写作标准、selector 发现、截图规范等）。

**对你的价值**：唯一一条**从用例直接产出 `.spec.ts` 进 CI** 的完整流水线。代价：要装 `@playwright/cli` 全局包。

---

## 七、安装方式对照

| 方式 | 命令 | 适用 |
|---|---|---|
| skills CLI | `npx skills add <repo> --skill <name>` | 纯 skill 目录（myclaude、ado-testcraft） |
| 手动 | `curl -L https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path> -o ~/.claude/skills/<name>/SKILL.md` | 单文件 skill，最可控 |
| git clone | `git clone --branch <branch> <repo> && cp -r <repo>/<path> ~/.claude/skills/` | 带 `references/` 的多文件 skill |
| plugin | `claude plugin marketplace add <owner>/<repo>` → `claude plugin install <p>@<marketplace>` | 插件形态（ado-testcraft、neonwatty、qa-plugin） |

**装在项目级还是用户级**

- 项目级：`testcases/.claude/skills/` —— 跟着仓库走，团队共享 ← **建议这个**
- 用户级：`~/.claude/skills/` —— 所有项目可用

---

## 八、选型决策树

```
需求来源是 ADO 的 User Story？
├─ 是 → ado-testcraft（自带覆盖缺口分析）
└─ 否 → PRD 模糊到写不出预期结果？
        ├─ 是 → product-requirements（澄清到 90 分）→ test-cases
        │        └─ 想额外挖输入边界 → input-validation-tester + risk-analyzer
        └─ 否 → test-cases
                 └─ 需求大、想在项目里固化 QA 基建？→ qa-plugin（/qa:init）
                 └─ 要产出 .spec.ts 进 CI？→ neonwatty/qa-skills
                 └─ 要写进 Jira？→ claude-qa-skills 的 jira-story-writing
```

---

## 九、已知坑清单

| # | 坑 | 影响 | 规避 |
|---|---|---|---|
| 1 | myclaude 的 skill 在 **`master`** 分支 | 用 `main` 拉会 404 | 手动 curl 时显式写 `master` |
| 2 | `cexll/myclaude` → 301 到 `stellarlinkco/myclaude` | 旧链接失效 | 统一用新地址 |
| 3 | `requirements-clarity` **无 frontmatter** | 装了不触发 | 补 frontmatter，或改用 `product-requirements` |
| 4 | `qa-plugin` 在 **`master`** 分支 | 同上 | 同上 |
| 5 | `umitozdemirf/qa-skills` 与 `neonwatty/qa-skills` **仓库同名** | clone 时互相覆盖、装错 | 按 owner 区分；clone 到不同目录名 |
| 6 | `qa-plugin` 生成物会随项目漂移 | 用例过时 | 定期跑 `/qa:sync`（靠 `qa-differ` 检测） |
| 7 | `test-cases` 输出是 **Markdown 文档**，不是可执行测试 | 不能直接 CI 回归 | 需要回归门禁时走 A 组 `qa-execute` 或 `neonwatty` 的 `.spec.ts` 路线 |
| 8 | 第三方 skill 可执行任意代码 | 安全风险 | 只从 GitHub 源仓库装，避开聚合站的 zip 直下；装前扫一眼 `scripts/` |

---

## 十、与本文档范围外的关联

| 类别 | 文档 / 位置 |
|---|---|
| **写 + 执行成套** | `QA_MANUAL_SKILL`（`/qa-blueprint` + `/qa-execute`）— https://github.com/ahmed-atef-albosaty/QA_MANUAL_SKILL |
| **执行侧** | `anthropics/skills` 的 `webapp-testing`、myclaude 的 `browser`（CDP，零 MCP） |
| **Claude Code 插件形态** | 官方插件目录：QA My App、Testers.ai CARBON、Agentic Beta Testers、QA Bug Hunter、Quality Supervisor (Qase)、TestDino、Checkly、TestAtlas、qa-quest |
| **造自己的 skill** | `skill-creator` — https://github.com/anthropics/claude-plugins-official （`plugins/skill-creator`） |

---

## 附：本文档涉及的全部仓库地址

```
https://github.com/stellarlinkco/myclaude          (master: test-cases, product-requirements, browser)
https://github.com/cexll/myclaude                   (301 → 上面)
https://github.com/dgambhir01/ado-testcraft         (main)
https://github.com/Kokoszsz/qa-plugin               (master)
https://github.com/umitozdemirf/qa-skills           (main)
https://github.com/deepaktiwari09/claude-qa-skills  (main)
https://github.com/neonwatty/qa-skills              (main)
https://github.com/anthropics/skills                (main: skills/webapp-testing)
https://github.com/ahmed-atef-albosaty/QA_MANUAL_SKILL
https://github.com/anthropics/claude-plugins-official  (plugins/skill-creator)
```

全部地址已做 HTTP 可达性校验（200 / 301）。
