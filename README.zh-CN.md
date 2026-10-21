# Academic Humanizer 学术去 AI 味

**去掉学术写作里的 AI 腔，数字、公式、引用和定理一字不改。**

[English](README.md) | **简体中文**

[中文 PDF 指南（v1.0）](docs/zh-CN/academic-humanizer-v1.0-zh.pdf) · [SKILL.md 中文译本](docs/zh-CN/SKILL.zh-CN.md) · v1.1 · MIT 许可

Academic Humanizer 是一个用于编辑和起草学术文本的智能体 skill，处理中英文论文、学位论文、审稿回复和基金申请书。它可以在 Claude、OpenAI Codex、ChatGPT 以及任何读取 `SKILL.md` 的智能体中运行。附带的核对脚本逐项检查每一次修改，保证文中的科学内容仍是作者写下的内容。

## 删去什么

- **套话和 AI 高频词**：delve、pivotal、sheds light on、"近年来……受到广泛关注""具有重要的理论意义和现实意义"。
- **模型输出特有的句式**：翻案腔（"难点不是计算，而是……"）、提示语冒号（"一句话总结："）、"这意味着"式复述、相邻几句同一个句式、修辞性罗列、序数词小标题。
- **元叙事和防御性写作**："本节将介绍""如前所述""综上所述，本节……"，自贬（"本文只是初步尝试""抛砖引玉"），叠用的限定（"在一定程度上可能"）。
- **比喻和破折号**：拟人化喻体（"像一位不知疲倦的审稿人"）、比喻性标签、当作标点用的破折号。
- **拼凑标签**："抽象修饰词 + 机制、协议、框架、闭环"一类、文中既不定义也不给出处的名称，如"认证协议""保障机制""治理闭环""certification protocol"。改为文中交代的实际做法；文中没有交代的，在报告里建议作者写明。"注意力机制""激励机制"等领域术语保留。
- **写成工作日志的方法和证明**："验证流程""健全性检查""审计""认证上界"、求解器容差、随机种子、从未触发的兜底机制、脚本名。计算机辅助的证明步骤改写成引理，并写明是精确计算还是数值计算。报告结果所依赖的取值全部保留，删掉的每个数字都列在报告里。
- **与证据不符的结论**：没做检验却写"显著"，定理证的是一致性却写"最优"，论文报告了 3.1% 却写"大幅提升"，以及给文中已经证明的结果加上的限定。

## 保留什么

数字、公式、引用键、`\ref` 和 `\label`、定义、假设和定理的原文、LaTeX 导言区，以及表达真实不确定性的限定词，全部保持原样。修改不会添加任何人名、数字、引语、来源或例子。某个结论需要证据而原文没有给出时，文中会出现醒目的 `[[EVIDENCE: ...]]` 占位符，由作者补上。只要还有占位符，报告开头就会提醒稿子不能直接提交，核对脚本的输出也以 `NOT READY TO SUBMIT` 一行结尾。

证据支持的结果按结果陈述。改出来的文字是自信学者的语气：具体，明确，对适用范围交代准确。

## 三种模式

| 模式 | 适用 | 改动范围 |
|---|---|---|
| 润色 | 草稿 | 用词、衔接、英文地道程度、结论范围 |
| 清理 | 已定稿或已投稿的文字 | 只改命中规则的句子，而且只改命中的部分 |
| 起草 | 新章节、回复信、申请书 | 按同一套规则写新内容，新增文献逐条检索确认 |

## 安装

**Claude Code**

```bash
git clone https://github.com/junbolian/Academic-Humanizer.git
cp -r Academic-Humanizer/academic-humanizer ~/.claude/skills/
```

**Claude 网页版和客户端**：把 `academic-humanizer` 文件夹压缩成 zip，作为自定义 skill 上传。

**OpenAI Codex**：把文件夹复制到 `~/.agents/skills/`（所有项目可用），或复制到某个仓库的 `.agents/skills/`。用 `$academic-humanizer` 调用，或由 Codex 按任务自动选用。

**ChatGPT**：Business、Enterprise 和 Edu 用户在侧边栏 Plugins 中打开 Skills，选择 Create，再选 Upload from your computer 上传 zip。其他方案的用户新建一个 GPT 或项目，把 [`platforms/chatgpt-instructions.md`](platforms/chatgpt-instructions.md) 粘贴到指令栏，上传 `academic-humanizer` 文件夹中的文件，并打开代码执行功能。

**其他智能体**：把 `SKILL.md` 作为指令加载，并让智能体能够读取 `references/` 和 `scripts/`。

## 用法

用自然语言提出要求即可触发。

- "润色 `paper.tex` 的引言。"
- "这段摘要已经定稿，只去 AI 味，不要改内容。"
- "Polish the discussion section."
- "起草对审稿人 2 第 3 条意见的回复，我们新增了 5.2 节。"

返回内容包括完整的修改稿和一份简短报告：按规则分组的改动、调整了范围的结论、需要补的占位符、结构建议，以及核对脚本的结果。

## 核对脚本

```bash
python3 academic-humanizer/scripts/check_revision.py audit paper.tex
python3 academic-humanizer/scripts/check_revision.py compare paper.tex revised.tex --changes
```

`audit` 按行列出可疑的词语和句式。`compare` 在数字、引用键、交叉引用、公式、定理原文或导言区有任何变化时以状态 1 退出，同时列出消失的限定词、新出现的大写术语和引语，以及每一处改动的句子，方便把每处修改对应到具体规则。脚本只需要 Python 3 标准库。

一次实际运行的片段：

```text
== Conservation warnings (do not affect the exit status) ==
  qualifiers and concessions: 1 -> 0
    LOST (each one strengthens a claim unless it was intended):
      可能 x1  original line 3: 此外，该估计量>>可能<<在捕获概率较低时表现更好，平均相对误差为 0.8%。
```

文中没有低捕获概率下的直接证据，这个"可能"表达的是真实的不确定性，所以要加回去。脚本把每一处这样的改动都摆到作者面前。

## 许可

MIT，见 [LICENSE](LICENSE)。
