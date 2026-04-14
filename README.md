<p align="center">
  <h1 align="center">my-skill-creator</h1>
  <p align="center">
    <strong>Turn any workflow into a reusable AI Agent Skill — automatically.</strong><br/>
    把任何工作流变成可复用的 AI Agent Skill 的完整工作台。
  </p>
  <p align="center">
    <a href="https://creativecommons.org/licenses/by-nc/4.0/"><img src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue.svg" alt="License"></a>
    <a href="https://github.com/805795108/my-skill-creator/stargazers"><img src="https://img.shields.io/github/stars/805795108/my-skill-creator?style=social" alt="Stars"></a>
    <a href="https://github.com/805795108/my-skill-creator/issues"><img src="https://img.shields.io/github/issues/805795108/my-skill-creator" alt="Issues"></a>
  </p>
</p>

---

## Why / 为什么需要它

AI Agents are powerful, but they forget everything between sessions. You end up repeating the same instructions, correcting the same mistakes, and re-explaining the same workflows — over and over.

**Skills** fix this. A Skill is a reusable instruction pack that turns a generic Agent into a domain expert. Think of it as an onboarding manual for an AI colleague — containing the procedural knowledge it can't learn from training alone.

**my-skill-creator** is itself a Skill. Install it once, and your Agent gains the ability to create, test, iterate, and package new Skills — guided by a battle-tested methodology.

AI Agent 很强大，但它不记住上次的对话。你不得不反复解释同样的流程、纠正同样的错误。

**Skill** 解决了这个问题——它是可复用的专业能力包，让 Agent 变成领域专家。而 **my-skill-creator** 本身就是一个 Skill：安装后，你的 Agent 就具备了「创建 Skill」的能力，引导你完成从零到发布的全流程。

---

## Features / 特性

| | Feature | Description |
|---|---------|-------------|
| **1** | **Guided Creation** | Step-by-step workflow: understand → plan → write → test → iterate → package<br/>分步引导：理解需求 → 规划资源 → 编写 → 测试 → 迭代 → 打包 |
| **2** | **Built-in Eval System** | A/B test your Skill with and without — blind grading by independent Agent judges<br/>内置 A/B 对比评估，独立 Agent 盲测打分 |
| **3** | **Auto Description Optimizer** | Iteratively improves trigger accuracy with automated eval loops<br/>自动循环优化 description，提升触发精准度 |
| **4** | **Quality Validator** | Checks structure, description quality, and 6 content patterns before publish<br/>发布前校验结构、description 质量和 6 项正文质量模式 |
| **5** | **Multi-Platform** | Works with Claude Code, Cursor, Codex CLI, and any Skill-compatible Agent<br/>支持 Claude Code、Cursor、Codex CLI 及所有支持 Skill 机制的平台 |
| **6** | **Benchmark & Reporting** | Aggregate multi-round results into visual HTML reports<br/>多轮测试结果聚合成可视化 HTML 报告 |

---

## Quick Start / 快速开始

### 1. Install / 安装

Choose the path matching your platform:

```bash
# Claude Code
git clone https://github.com/805795108/my-skill-creator ~/.claude/skills/my-skill-creator

# Cursor
git clone https://github.com/805795108/my-skill-creator ~/.cursor/skills/my-skill-creator

# Codex CLI
git clone https://github.com/805795108/my-skill-creator ~/.codex/skills/my-skill-creator
```

Then restart your Agent session. Done.

### 2. Use / 使用

Just talk to your Agent. Any of these will activate the Skill:

> *"I want to build a skill for my agent"*
>
> *"帮我把这个工作流打包成可复用的技能"*
>
> *"我每次都要手动做这件事，能不能让 Agent 记住"*
>
> *"上次那个流程能不能固定下来，以后让 Agent 自动做"*

The Skill takes over from there — asking clarifying questions, scaffolding the directory, writing the `SKILL.md`, and guiding you through testing.

### 3. Install dependencies (optional) / 安装依赖（可选）

Only needed if you want to run the automated eval/optimization scripts:

```bash
pip install -r requirements.txt
```

---

## How It Works / 工作原理

```
 You: "I want to create a Skill that..."
  │
  ▼
┌─────────────────────────────────────────┐
│  Step 1  Understand the use case        │
│  Step 2  Plan reusable resources        │
│  Step 3  Scaffold the Skill directory   │
│  Step 4  Write SKILL.md + resources     │  ◄── guided by best practices:
│  Step 5  Test with A/B eval             │      examples > rules,
│  Step 6  Iterate based on feedback      │      error recovery paths,
│  Step 7  Package & publish              │      output validation, etc.
└─────────────────────────────────────────┘
  │
  ▼
 Output: a ready-to-install .skill package
```

The Skill also supports **improvement mode** — if an existing Skill underperforms, jump directly to Step 5 to run evaluations using the current version as a baseline, then iterate.

---

## What Gets Created / 产出结构

Every Skill created by my-skill-creator follows this standard structure:

```
your-skill-name/
├── SKILL.md          # Required — metadata (name + description) + instructions
├── scripts/          # Optional — executable scripts (Python, Bash, etc.)
├── references/       # Optional — loaded on demand (schemas, specs, domain docs)
└── assets/           # Optional — templates, icons, output resources
```

---

## Project Structure / 项目结构

```
my-skill-creator/
├── SKILL.md                        # Core instruction file (loaded on trigger)
├── scripts/
│   ├── run_eval.py                 # Run trigger evaluation
│   ├── improve_description.py      # LLM-powered description optimizer
│   ├── run_loop.py                 # Auto loop: eval → optimize → re-eval
│   ├── aggregate_benchmark.py      # Aggregate multi-round results
│   ├── generate_report.py          # Generate visual HTML report
│   ├── generate_review.py          # Launch review server / static HTML
│   ├── package_skill.py            # Package Skill as .skill file
│   ├── quick_validate.py           # Validate SKILL.md format & quality
│   └── utils.py                    # Shared utilities (platform-adaptive LLM calls)
├── references/
│   ├── schemas.md                  # JSON schemas for evals, grading, benchmarks
│   ├── eval-workflow.md            # Detailed eval procedure (Steps 5.2–5.6)
│   └── agents/
│       ├── grader.md               # Grader Agent: pass/fail per assertion
│       ├── comparator.md           # Blind comparator Agent: unbiased scoring
│       └── analyzer.md             # Analyzer Agent: root cause + suggestions
├── assets/
│   ├── eval_review.html            # Trigger test set visual review UI
│   └── viewer.html                 # Eval review UI (Outputs + Benchmark tabs)
└── requirements.txt                # Python dependencies
```

---

## Eval System / 评估系统

The built-in evaluation pipeline lets you **prove** your Skill works, not just hope:

```
                  ┌─────────────┐
 Same prompt ──►  │ With Skill  │──► Output A ─┐
                  └─────────────┘              │   ┌─────────┐
                                               ├──►│ Grader  │──► Benchmark
                  ┌─────────────┐              │   └─────────┘
 Same prompt ──►  │ No Skill    │──► Output B ─┘
                  └─────────────┘

 Optional: Blind comparator + Analyzer for deeper insights
```

- **Grader** — evaluates each output against defined expectations (pass/fail per assertion)
- **Comparator** — blind A/B comparison without knowing which is "new"
- **Analyzer** — finds root causes for score differences, outputs actionable improvement suggestions

---

## Common Install Paths / 常见安装路径

| Agent Platform | Skill Directory |
|---|---|
| Claude Code (global) | `~/.claude/skills/` |
| Claude Code (project) | `<project-root>/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Codex CLI | `~/.codex/skills/` |

The core files (`SKILL.md`, `scripts/`, `references/`, `assets/`) are platform-agnostic. Only the install path differs.

---

## Contributing / 贡献

Contributions are welcome! Here's how you can help:

- **Report bugs** — [open an issue](https://github.com/805795108/my-skill-creator/issues)
- **Suggest improvements** — ideas for new quality checks, better eval methods, or broader platform support
- **Submit a PR** — fix a bug, add a feature, or improve documentation
- **Share your Skills** — built something cool with my-skill-creator? Let us know!

---

## License / 许可证

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

| Use Case | Permission |
|---|---|
| Personal use, learning, research, non-commercial projects | No attribution required |
| Publishing derivative works (articles, tools, courses) | Please credit the source |
| Commercial use | Requires separate authorization — contact the author |

---

<p align="center">
  <sub>If this project helps you build better AI Agent Skills, consider giving it a ⭐</sub><br/>
  <sub>如果这个项目帮到了你，欢迎点个 ⭐ 支持一下</sub>
</p>
