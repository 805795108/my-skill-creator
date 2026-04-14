# my-skill-creator

> 帮你把任何工作流打包成可复用的 AI Agent Skill 的完整工作台。

---

## 这是什么

`my-skill-creator` 是一个 AI Agent Skill，安装后当你对支持 Skill 机制的 Agent 说「我想创建一个 Skill」，它就会自动被激活，引导你完成从零到发布的完整流程：

- **理解需求** — 通过具体例子弄清楚这个 Skill 要做什么
- **规划资源** — 识别哪些内容可以复用，应该放进 `scripts/`、`references/` 还是 `assets/`
- **编写内容** — 写出高质量的 `SKILL.md`，包括触发描述、工作流指令、输出模板
- **测试评估** — 用真实 prompt 跑测试，对比「有 Skill / 无 Skill」两种条件下的输出差异
- **迭代优化** — 根据评审反馈改写，支持多轮对比
- **打包发布** — 生成可分发的 `.skill` 文件

---

## 安装方法

仓库地址：[805795108/my-skill-creator](https://github.com/805795108/my-skill-creator)

Claude Code 示例：

```bash
git clone https://github.com/805795108/my-skill-creator ~/.claude/skills/my-skill-creator
```

Cursor / Codex CLI 示例：

```bash
git clone https://github.com/805795108/my-skill-creator ~/.codex/skills/my-skill-creator
```

将仓库放到对应平台的 Skill 目录后，重启当前 Agent/CLI 即可生效。

---

## 触发方式

安装后，以下说法都会触发这个 Skill：

- 「我想创建一个 Skill」
- 「帮我把这个工作流打包成可复用的技能」
- 「上次那个流程能不能固定下来，以后让 Agent 自动做」
- 「我每次都要手动做这件事，能不能让 Agent 记住」
- "I want to build a skill for my agent"

---

## 目录结构

```
my-skill-creator/
├── SKILL.md                      # 主指令文件（触发后加载）
├── scripts/
│   ├── run_eval.py               # 运行触发评估（测试 description 的触发准确率）
│   ├── improve_description.py    # 调用 Claude 优化 description
│   ├── run_loop.py               # 自动循环：评估 → 优化 → 再评估
│   ├── aggregate_benchmark.py    # 聚合多轮测试结果，生成 benchmark.json
│   ├── generate_report.py        # 生成可视化 HTML 报告
│   ├── generate_review.py        # 启动评审服务器 / 生成静态 HTML
│   ├── package_skill.py          # 打包 Skill 为 .skill 文件
│   ├── quick_validate.py         # 快速校验 SKILL.md 格式是否合规
│   └── utils.py                  # 公共工具函数
├── references/
│   ├── schemas.md                # 所有 JSON 文件的字段定义（evals、grading、benchmark 等）
│   ├── eval-workflow.md          # 测试评估详细操作流程（5.2-5.6）
│   └── agents/
│       ├── grader.md             # 评分 Agent：对每条断言判断 pass/fail
│       ├── comparator.md         # 盲测比较 Agent：不知道哪组是新版的情况下打分
│       └── analyzer.md           # 分析 Agent：找出胜出原因，输出改进建议
├── assets/
│   ├── eval_review.html          # 触发测试集可视化审核界面
│   └── viewer.html               # 评审界面模板（含 Outputs + Benchmark 两个 Tab）
└── requirements.txt              # Python 依赖
```

---

## 运行环境要求

```bash
pip install -r requirements.txt
```

Skill 的目录结构和主文档组织方式不只适用于 Claude Code，支持 Skill 机制的平台都可以复用。

当前自动化脚本里的 LLM 调用默认依赖 `claude` CLI：`run_eval.py`、`run_loop.py`、`improve_description.py` 会通过 `scripts/utils.py` 的 `call_llm()` 统一调用。其他平台如果也想跑这套自动评估/优化脚本，需要在 `scripts/utils.py` 里补充对应适配。

---

## 常见安装路径

| AI Agent | Skill 目录 |
|----------|-----------|
| Claude Code（全局）| `~/.claude/skills/` |
| Claude Code（项目级）| `<项目根目录>/.claude/skills/` |
| Codex | `~/.codex/skills/`（以官方文档为准）|
| OpenClaw | `~/.openclaw/skills/`（以官方文档为准）|

核心文件（`SKILL.md`、`scripts/`、`references/`、`assets/` 等）在不同平台可以保持一致，通常只需要调整安装目录和少量平台适配代码。

---

## 创建出来的 Skill 结构

用这个 Skill 创建出的新 Skill，标准结构如下：

```
your-skill-name/
├── SKILL.md          # 必须，含 name + description 元数据和正文指令
├── scripts/          # 可选，可执行脚本
├── references/       # 可选，按需加载的参考文档
└── assets/           # 可选，模板、图标等产出物资源
```

---

## 许可证

本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可证。

个人使用、学习、研究、非商业项目：不需要署名，不需要申请
公开发布衍生作品（文章、工具、课程等）：请注明来源
商业用途：需要单独授权，请联系作者

---

## 仓库

仓库地址：[https://github.com/805795108/my-skill-creator](https://github.com/805795108/my-skill-creator)

如有问题或建议，欢迎提 Issue 或 PR。
