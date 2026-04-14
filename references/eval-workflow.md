# 测试评估详细操作流程

本文档包含 SKILL.md 第五步（测试与评估）中 5.2-5.6 的详细操作步骤。

---

## 5.2 同时启动两组子 Agent 运行

**重要：必须在同一轮操作中同时启动「有 Skill」和「无 Skill（或旧版 Skill）」两组，不要先跑完一组再启动另一组。** 

结果保存到 `<skill-name>-workspace/iteration-1/` 目录，每个测试用例一个子目录，目录名使用描述性名称（如 `eval-query-new-users/`）。

**有 Skill 的运行：**
```
执行以下任务：
- Skill 路径：<当前 skill 目录路径>
- 任务：<eval prompt>
- 输入文件：<eval files，如无填 none>
- 将输出保存到：<workspace>/iteration-1/eval-<ID>/with_skill/outputs/
```

**无 Skill 的基准线（新建 Skill 时）：**
```
执行以下任务（不使用任何 Skill）：
- 任务：<eval prompt>（与上方完全相同）
- 将输出保存到：<workspace>/iteration-1/eval-<ID>/without_skill/outputs/
```

**迭代改进时**，将「无 Skill」替换为「旧版 Skill」作为基准线（运行前先将旧版复制到 `<workspace>/skill-snapshot/`，子 Agent 指向 snapshot）。

同时为每个测试用例创建 `eval_metadata.json`（expectations 先留空）：
`{"eval_id": 1, "eval_name": "query-new-users-today", "prompt": "今天有多少新用户注册了？", "expectations": []}`

### 改进模式（迭代已有 Skill）

与新建模式的差异：
- 将当前 Skill 复制到 `<workspace>/skill-snapshot/` 作为基准线
- 「无 Skill」组替换为「旧版 Skill」组
- 使用 `history.json` 跟踪每轮迭代的 pass_rate 变化（schema 见 `references/schemas.md` 的 history.json 章节）
- 停止条件：连续两轮 pass_rate 提升 < 5%，或用户满意

---

## 5.3 捕获运行耗时数据

每个子 Agent 完成时立即将通知中的 `total_tokens` 和 `duration_ms` 保存到 `timing.json`——**这是唯一的捕获时机**，逐条处理不要批量：
`{"total_tokens": 84852, "duration_ms": 23332, "total_duration_seconds": 23.3}`

---

## 5.4 等待运行期间，起草量化断言（expectations）

不要等子 Agent 完成后再思考如何评估——利用等待时间起草 expectations，并向用户解释每条 expectation 在检验什么。好的 expectation 要可以客观验证，名称要一眼看出它在检验什么：

```json
"expectations": [
  {
    "text": "返回了具体数字而非模糊描述",
    "check": "输出中包含具体的用户数量数字"
  },
  {
    "text": "引用了正确的飞书字段名",
    "check": "输出提到了 references/schema.md 中定义的字段名"
  }
]
```

主观类 Skill（写作风格、创意质量）不适合量化断言，优先依赖人工评审。

将更新后的 expectations 写入 `evals/evals.json` 和各 `eval_metadata.json`。

---

## 5.5 评分、聚合、解读、查看结果

子 Agent 全部完成后，按顺序执行：

**1. 让 grader agent 评分**——参考 `references/agents/grader.md`，对每个 expectation 判断 pass/fail，将结果保存到各 eval 目录的 `grading.json`（字段名用 `text`/`passed`/`evidence`——eval-viewer 的前端 JavaScript 通过这三个固定字段名渲染评分结果，使用其他名称会导致界面显示为空）。能用脚本验证的断言，优先写脚本检验，比人工查看更快更可靠。

**2. 聚合 benchmark：**
```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-1 --skill-name <name>
```
生成 `benchmark.json` 和 `benchmark.md`，包含 pass rate、耗时、token 用量。

**3. 解读 benchmark 数据**——聚合后先做一次分析，再开评审界面。特别留意以下信号：

| 信号 | 含义 | 应对 |
|------|------|------|
| 某断言在「有Skill」和「无Skill」两组通过率相差不大 | 这条断言没有区分价值 | 删除或改写这条断言 |
| 某 eval 两次运行结果差异很大 | Skill 指令不稳定，或 prompt 太模糊 | 检查 SKILL.md 是否有矛盾指令 |
| 有 Skill 时耗时/token 大幅增加，但质量提升不明显 | Skill 在引导 Agent 做无效步骤 | 读完整 transcript（不只是最终输出）定位问题所在 |

**4. 启动 eval-viewer：**

**本地 Agent Code / Cowork 环境：**
```bash
nohup python scripts/generate_review.py \
  <workspace>/iteration-1 \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-1/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

迭代第 2 轮起，加 `--previous-workspace <workspace>/iteration-1`，可三列对比：新版 / 旧版 / 无 Skill。

**Claude.ai 环境（无法启动本地服务器）**：加 `--static /tmp/review-my-skill.html` 生成独立 HTML 文件，下载后在本地浏览器打开；用户点击「Submit All Reviews」后下载 `feedback.json`，放回 workspace 目录供下一步读取：
```bash
python scripts/generate_review.py \
  <workspace>/iteration-1 \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-1/benchmark.json \
  --static /tmp/review-my-skill.html
```

**5. 告知用户**：「已在浏览器中打开评审界面，有 Outputs（逐条对比两组输出，可写文字反馈）和 Benchmark（量化通过率、耗时、token 对比）两个 Tab。查看完成后点击『Submit All Reviews』，然后回来告诉我。」

**6. 读取反馈**：用户完成后，读取 `feedback.json`。空反馈 = 该项没问题；有文字 = 该项需要改进。关闭 viewer：`kill $VIEWER_PID`（Claude.ai 环境跳过此步）。
