# Academic Humanizer v1.1：SKILL.md 中文译本

智能体执行的是 `academic-humanizer/SKILL.md` 英文原文，两者有出入时以英文原文为准。中文文本的专门规则见 `academic-humanizer/references/chinese.md`。

## 作用

AI 辅助写成的学术文字经这个 skill 修改后，读起来像领域内认真的作者写的：字面、精确、句句相接，证据强的地方语气笃定，任何地方都不超出证据。它只改措辞，不改内容。数字、公式、引用键、交叉引用、正式陈述和表达真实不确定性的限定词都保持作者原样，并由附带脚本核对。作者仍需遵守投稿期刊关于披露 AI 使用的规定。

## 模式与范围

- **润色**：用户要求润色、精简、改写时的默认模式。全部规则适用，句子可以为衔接（规则 8）和地道表达（规则 9）而重写，但要遵守下面的编辑纪律。
- **清理**：用户只要求去 AI 味、说"成稿清理"或称文字已定稿时使用。只执行规则 1 至 4 和规则 5 的第一条。没有命中规则的句子逐字保留，命中规则的句子只改命中的部分。需要补证据的结论写进报告，不插占位符。
- **起草**：智能体撰写新的章节、回复信或申请书时使用。写作时执行全部规则，写完运行 `check_revision.py audit` 并修正检出的问题再交付。不凭记忆引用：每一篇新增文献都要检索，确认其存在，并核对描述它的句子与原文一致。文献综述要检索最近两年的工作。

请求没有说明是润色还是清理时，草稿按润色处理，用户称已定稿或已投稿的文字按清理处理。

## 编辑纪律

1. **每处改动都有规则依据。** 每一处改动对应下文的一条编号规则，没有对应规则的改动撤销。个人对措辞的偏好不算规则。
2. **改动最小且足够。** 在命中规则的句子里，只改规则针对的部分，相邻文字不动。润色模式下，规则 8 和规则 9 可以同时作用于这句。
3. **不新增。** 人名、机构、职务、地名、数字、日期、先后顺序、引语、来源、链接、因果、动机和例子，只有原文或用户提供的材料里有才能出现。修改稿中的每个实词都能在这两处之一找到出处。具体细节由作者提供，材料单薄的段落写进报告。
4. **不删减。** 观点、结论、让步和表达真实不确定性的限定词都保留，例如 may、likely、typically、可能、通常、在某些情况下。规则 7 只删两类限定：加在文中已证明或已报告的结果上的限定，以及叠用的重复限定。每一处删除都列入报告。规则 11 删去报告结果不依赖的工程细节，报告逐项列出删掉的内容及其数字。`compare` 会列出每一个消失的限定词和数字。
5. **结构不动。** 标题层级、章节顺序、段落数量与顺序、列表、表格、图、引文和代码的位置保持原样，除非用户要求调整结构。结构问题写进报告（规则 12）。

## 先读风格参考

用户提供了作者以前的论文、风格指南或目标文风说明时，修改前先读，记下句长、连接词、限定的程度、章节和段落的开头方式、标点习惯和符号用法。它与规则 1、2、3、4、8、9 冲突时，按风格参考处理，因为这几条规定的是语体，而风格参考体现作者本人的语体。作者有意使用破折号的，保留破折号。风格参考不能推翻规则 5、6、7、10，这几条保护证据、已证明结论的范围、立场和不变量。

## 运行核对脚本

SKILL_DIR 指本文件所在的文件夹。常见位置：Claude Code 为 `~/.claude/skills/academic-humanizer`，Claude 网页版和客户端为 `/mnt/skills/user/academic-humanizer`，OpenAI Codex 为 `~/.agents/skills/academic-humanizer` 或 `.agents/skills/academic-humanizer`。环境不能运行 Python 时，同样的比对靠阅读完成，并在报告中注明脚本没有运行。

## 润色和清理的流程

1. 把原文原样存到工作文件夹，例如 `ah/orig.tex`，其他文本用 `.md` 或 `.txt`。记下文本类型、期刊、语言和模式。
2. 有风格参考的，先读风格参考。
3. 运行 `python3 SKILL_DIR/scripts/check_revision.py audit ah/orig.tex`。输出按行列出可疑的 AI 词语、拼凑标签、句式、破折号、分号和括号的密度、过长句、连串短句，以及章节和结论的结构。每一条命中都只是待判断的候选。稳健统计论文里的 robust 是术语，机器人论文里的 navigation 是字面意思。
4. 改动之前通读全文，找出每段的唯一论点，以及它如何承接上一段。衔接问题在段落层面最容易看出来。
5. 按规则和编辑纪律修改。清理模式只改命中规则的句子。
6. 把修改稿存在原文旁边，运行 `python3 SKILL_DIR/scripts/check_revision.py compare ah/orig.tex ah/revised.tex --changes`。脚本比对数字、引用键、`\ref` 和 `\label`、公式、正式环境的原文和导言区，然后列出消失的限定词、新出现的大写术语和引语以及每一处改动的句子，并对修改稿做一次审查，计数与原文对照。撤销每一处非有意的差异，把每一处改动对应到规则，反复进行，直到只剩有意的差异。
7. 对照最终检查清单，按"输出"一节的要求交付。

不到 150 词的单个段落可以不跑脚本，但交付前要逐项对读数字、引用、限定词和公式。

每次对话第一次修改前，先读 `references/examples.md`。示例展示了每条规则在证据充足和证据缺失时的做法，以及同一段文字在润色模式和清理模式下的不同结果。

## 规则

### 1. 删除套话和 AI 高频词

完整的候选清单在 `references/lexicon.txt`，脚本从这里读取。主要类别如下。

- 词汇：delve、underscore、intricate、tapestry、testament、pivotal、showcase、foster、realm、seamless、harness、multifaceted、nuanced、holistic、meticulous、paramount、invaluable，只表示"重要"的 crucial，只表示"使用"的 leverage。
- 没有内容的意义宣称：paves the way、a crucial step toward、opens new avenues、sheds light on、bridges the gap、of paramount importance、transformative、groundbreaking、new paradigm。
- 套路开头："In recent years, X has attracted increasing attention""With the rapid development of""Despite recent advances""X plays a crucial role in"。改为从具体问题写起。
- 口语起手式：Simply put、Long story short、Bottom line、说白了、说穿了、先说结论。删去后直接给出判断。
- 没有数字的量词：extensive 或 comprehensive experiments、a wide range of、numerous、various、substantial。换成论文报告的数量或数值。
- 新颖性堆砌：一节里多次出现 novel，以及 for the first time 和 to the best of our knowledge。至多保留一处，而且只在作者确实检索过文献时保留。
- 宣告式强调：It is worth noting that、Importantly、Interestingly、Notably。直接陈述事实，让位置和证据体现它的分量。
- 回避系动词（用 serves as、stands as 代替 is）、用于强调的否定排比（not just X but Y）、句尾附加空泛评价的 -ing 分句（..., highlighting the importance of ...），以及本来一项就够却凑成三项的列举。
- 启示类套话：rich insights、important implications for practitioners、provides a new perspective、delicate balance、interplay，以及反复出现的 counterintuitive。
- 回复信套话：每条回复都感谢"insightful comment"。只在信的开头感谢审稿人一次，每条回复写明改了什么、改在哪里。

### 2. 字面表述

把比喻和比喻性标签换成它们所指的机制：landscape、through the lens of、cornerstone、blueprint、roadmap、double-edged sword、sweet spot、unlock、arms race、holy grail、silver bullet、at the heart of、tackle、grapple with。领域内的读者会把每句话拿来对照模型或数据检查，比喻没有可供检查的内容。

拟人化喻体最典型。把工具、模型或流程写成一个理想化的人（"acts as a tireless reviewer""like a wise mentor""像一位智慧的导师"），后面通常跟着赞美或"不仅……更……"。改为写它实际做什么："它在几秒内逐条核对约束与数据"。

起源于比喻、但已有定义的术语保留：bottleneck、halo effect、spillover、curse of dimensionality、cold start、warm start、signal and noise、指网络结构的 backbone、loss landscape、作为算法类别名称的 heuristic。判断标准是该词在领域内或本文中有没有定义。有精确说法时，精确说法胜过笼统标签："a method without a performance guarantee"比"a heuristic method"信息更多。

这条规则的依据是可核对。比喻本身区分不了模型和人类，中文非虚构写作里人类用的比喻反而更多（见"不作为改写理由"）。论文、学位论文、报告和信函执行这一条。随笔和科普等以比喻为文体特征的文字，按风格参考处理。

论文标题以及作者给模型、策略和效应起的名字保持不变。名字本身是比喻的，在报告里提一次，由作者决定。

**拼凑标签**。生成文本常用"抽象修饰词 + 系统类名词"给一个普通步骤起名："certification protocol""verification layer""safeguard mechanism""trust framework""evaluation pipeline"、认证协议、保障机制、治理闭环。这类标签读起来像读者应当熟悉的组件，但文中既不定义它，也不给出处，后文也不再把它当组件使用，它指的往往只是一次检查。脚本的"Coined labels"部分列出每个这样的短语、出现次数，以及文中是否定义、交叉引用或引用了它。逐个判断：

- 领域内有定义的术语（attention mechanism、clinical trial protocol、incentive mechanism、hidden layer），或本文定义并反复使用的术语，保留。作者给自己方法起的名字也保留，名字说得比方法本身少时在报告里提一次。
- 文中说明了标签做什么的，用这个说明替换标签。文中别处写明了两个步骤时，"Each solution then passes a certification protocol"改为"We then check each solution for feasibility and recompute its objective with the exact solver"。
- 文中从未说明标签做什么的，保留标签，在报告中给出建议：写出它包含的步骤，或改用表示实际动作的普通名词（"the check""the second review"）。不要自己补步骤。
- 修饰词断言了某种性质的，如 certified、verified、guaranteed、safe、robust，就是一个论断，按规则 5 和 6 核对："certification"意味着有证明或写明的流程作保证。
- 给文中已有名称的对象另起的标签，改回原名称（规则 8）。修改稿不得新增标签，`compare` 会列出原文中没有的每个标签。

### 3. 标点：不用破折号，少用分号和括号

删除破折号（U+2014、LaTeX 的 `---`、中文破折号）以及当作破折号用的带空格短横线，改用逗号、冒号或拆成两句。数值范围中的短横线（`2--6`）和联名中的短横线（`Karush--Kuhn--Tucker`）保留，中文连接号按 `references/chinese.md` 的说明保留。

分号和括号插入语同理。一段里有两个以上分号，或者多数句子都带括号插入语，说明这段需要改写成完整的句子。引用、公式编号、单位和首次出现的缩写所用的括号是规范用法，保留。

不同模型使用破折号的频率相差一个数量级以上。在一个中文非虚构语料中，每千字的破折号数为：人类作者 0.80，Claude 4.25，DeepSeek 5.16，Kimi 2.32，Gemini 0.51，GPT 0.11。同一语料里，五个模型中 GPT 用"不是……而是"最多。无论草稿出自哪个模型，都做完整检查。

### 4. 生成文本的句式

下列句式在中文非虚构语料的实测中（5 个模型的 300 篇 AI 文本，329 篇人类文章），模型文本的频率明显高于人类文本，而且每一种都有可以定位到具体句子的触发标记。英文形式在英文里做的是同一个动作。只有出现触发标记时才处理。

**4.1 翻案腔。** 先立一个文中没有任何人持有的误解，再纠正它："The real barrier is not technology but understanding""X is not about A; it is about B""What matters is not A but B"，以及不是……而是、并非……而是、不在于……而在于、与其说……不如说、看似……实则、你以为……其实、说到底。直接陈述判断："The barrier is understanding." 文中确有人持有 A 时，对比保留，例如前人的结论、本文放宽的假设、被数据否定的假说："Unlike \citet{ref1}, we do not assume a closed population." 递进式的"not just X but Y"归规则 1 处理。

**4.2 提示语冒号与空转引导句。** 用提示语加冒号宣布内容，而不直接说出内容："The key insight is: ...""The answer is simple: ...""The result: ...""In short: ..."，以及一句话总结：、核心是：、关键在于：、原因如下：、本质上：。提示语不承担信息就删去。它承接上一句时保留，把冒号换成普通句法。只为宣布下面有列表而存在的句子（"Here are the main reasons:""我见过的几种典型场景："）改成有内容的陈述或删去，让列表直接接上文，列表项一项不少。引出引语、定义、公式或总说之后的分说的冒号保留（"The model has two components: a measurement model and a structural model"），文体惯例的引导句也保留，例如引言里的"We make three contributions:"和"The proof has two steps:"。标题、列表项标签、网址和代码不在范围内。

**4.3 相邻句同一骨架与凑数案例。** 两句以上相邻句子用同一个句法骨架，从句顺序、逗号位置和长度都一样，读起来像在填表。实测模型文本每百段有 9.41 对，人类文本 4.81 对。合并、拆分、调换语序或改为从属结构，改变其中一句的句法，内容不变。一段里并列三个以上说明同一点的案例时，把最有代表性的放在主句，其余压缩成分句，不丢信息。叙事推进、编号步骤和同一句内部的并列结构不改。

**4.4 复述句。** 以"This means that""This suggests that""In other words"、这意味着、这表明、这说明、换句话说开头、内容与前一句相同的句子，并入前一句或只保留结论。给出前一句推不出的新结论时保留，并按规则 5 和 6 核对它的依据。

**4.5 修辞性罗列。** 一个分句里串起三项以上的并列成分，只为显得周全，例如"startups, mid-sized firms, and large groups all benefit"，改为"firms of every size benefit"。没有合适的上位词时，改变其中一项的句法。承载信息的列表完整保留：数据集、基准方法、变量、假设、参数取值、法规条目和 Markdown 列表。学术文本里的列表大多承载信息。

**4.6 序数词小标题。** 报告、讲义、推文和幻灯片里连续三个以上的小标题用一、二、三，第一、第二或 First、Second 编号时，删去序数，保留标题文字。论文模板或期刊格式规定的章节编号、编号步骤以及需要按编号指代的条目不在范围内。

**4.7 段首缺少回指。** 非首段以评论语开头，例如听起来、看起来、值得注意的是、更重要的是、关键在于、问题在于，整句又没有指回上文的词（这、那、其、此、上述），补上回指词："这听起来像……"。英文段落以"More importantly,"或"The catch is"开头时，写明所说的对象。

**4.8 段首路标连接词。** 然而、因此、此外、与此同时、换言之、总而言之、Moreover、Furthermore、However、Therefore 连续出现在几段段首时，只在论证确实转折或推出结论的地方保留。附加性连接词移入句中或删去。段落内部的连接词归规则 8。

**4.9 元叙事、自指、预告和小结。** 只谈文本自身的句子没有内容："In this section, we discuss ...""We now turn to ...""As mentioned above, ...""Before proceeding, ...""To summarize, ...""This section has shown ...""The remainder of this paper is organized as follows"，以及本节将介绍、下面我们将、如前所述、本文结构安排如下、本章小结。删去这些句子，或只保留它们包着的实质结论："As shown above, the bound is tight"改为"The bound is tight (Proposition 2)"。论文的结论部分保留总结。指向读者此刻需要的内容的交叉引用保留，例如"the bound in Section 3 gives ..."。

### 5. 实证结论与证据一致

- 同段或下一段已经给出数字、日期或对象时，概括说法（"substantially improves""a large gain"、显著提升、实现了效率的提升）换成这个具体值。原文没有数字时，只恢复动词（"achieves an improvement in accuracy"改为"improves accuracy"，完成了对流程的优化改为优化了流程），什么都不添。
- 每个实证结论都指向它的证据，即表、图、检验或文献，动词与证据强度相符：报告的结果所显示的用 show 或 find，间接证据用 suggest 或 is consistent with。prove 只用于证明。
- 笼统的幅度换成论文报告的数字，并带上指标、比较对象和样本："reduces mean absolute error by 3.1% relative to the strongest baseline (Table 4)"。
- 数字、检验结果、图表编号和文献只能来自用户提供的材料。某句需要材料中没有的证据时，插入醒目的占位符 `[[EVIDENCE: 所需内容]]`，LaTeX 中写作 `\textbf{[[EVIDENCE: 所需内容]]}`，括号内只用普通文字，不用 `%`、`_`、`&`、`#`。脚本会列出每个占位符，比对时不计入其中的内容。占位符是正确的输出，看似合理的数字是编造。文中还有占位符的稿子不能提交，报告中要明确说明（见"输出"）。清理模式下把这一需要写进报告。
- 报告论文实际计算的统计量及其汇总方式：均值及其标准误或置信区间、中位数或区间。不把一种统计量换算成另一种。
- 先与最强的基准比较。
- significant 和 significantly 必须有写明的统计检验。没有检验时，给出差值并删去这个词。
- 所有报告的数字来自同一个样本。文中混用不同样本、不同运行或不同数据版本而没有说明的，在报告中标出，数字不动。
- 措辞准确表达证据所支持的内容，不弱于证据（规则 7），也不强于证据。

### 6. 理论结论与已证明的命题一致

- 文中给出证明的结果，we prove、we show、we establish 都是正确的，保留。
- 复述一个结果的句子要带上它的条件：假设、方法类、参数区域，以及结果是否为渐近结果。"The estimator is unbiased"改为"Under Assumptions 1 and 2, the estimator is unbiased when the sampling fraction exceeds the threshold in Proposition 3." 使用论文自己的符号和名称，不引入新符号。
- 对照命题逐个核对量词：optimal、always、never、robust、for any。结果依赖某种函数形式或分布假设（例如线性关系或正态误差）时，引言和结论复述这个结果的地方也要写明。
- 实践启示写成带方向和出处的条件比较静态结论："The number of sampling rounds needed for a given precision decreases in the capture probability and increases in the heterogeneity across strata (Proposition 4)." "practitioners should carefully balance cost and precision"这类建议所含的信息少于它所替代的命题。
- 不增加、删除、合并或升级定理、命题和引理，唯一的例外是规则 11 把计算机辅助的证明步骤写成引理。关于数量的建议写进报告（规则 12）。

### 7. 立场：按证据断言

目标语气是自信的学者：动词明确，结果具体，没有证据不用最高级，不道歉。

- 已证明和已报告的结果按结果陈述。"Our method may reduce error by 3.1% (Table 4)"改为"Our method reduces error by 3.1% (Table 4)"。只有确实存在不确定性时保留限定：间接证据、超出样本的外推、猜想。
- 叠用的限定合并为一个："may potentially""might possibly suggest""could perhaps""在一定程度上可能"。
- 删去自贬："this simple attempt""a preliminary step""our modest contribution""admittedly""we humbly"、本文只是初步尝试、抛砖引玉、笔者水平有限、不足之处敬请指正。
- 删去防御性写作：反驳没人提出的质疑，"we do not claim to ..."，反复出现的"beyond the scope of this paper"，以及与结果有效性无关的缺点罗列。
- 删去非必要披露：失败的尝试、工作的先后经过、证据并未引出的疑虑。限定结果有效范围的局限只写一次，平实地写在结果处或局限段落里。期刊要求的披露，例如 AI 使用、数据可得性和利益冲突，按期刊要求的位置保留。
- 贡献直接陈述："We show""We introduce""This paper establishes"。"首个""最大""唯一"这类说法要有证据和文献检索支撑。

### 8. 衔接：一段一个论点，不跳跃

- 每段只讲一个论点，写在第一或第二句，其余句子支撑它。
- 每句都从上一句推出。两句之间缺少逻辑环节时，补一个分句，写出论证中本来就有的关系：because、so、as a result、in contrast、for example、under this condition。关系不清楚时，在报告中标出。
- 逻辑连接词保留：because、therefore、thus、however、in contrast、whereas。连续几句以附加性连接词（Moreover、Furthermore、Additionally、In addition）开头时，换成实际关系或删去。
- 超过约 35 个词或含三个以上从句的句子拆开，每句承担一步，拆开后仍要相互衔接。节奏不是拆句的理由（见"不作为改写理由"）。
- 一连串短句、"That limits progress."这样的残句、"The result: ..."这样的标题式冒号同样是错误。陈述一个条件及其结果的长句没有问题。
- 一个对象只用一个名称。定义过的术语原样重复使用，不为了变化把重复的名称换成代词。"participants""subjects""respondents"不能交替指同一群体。
- 论文做什么、结果显示什么用现在时，已完成的操作用过去时。
- 定义、假设和结论陈述保持原文，由脚本核对。

### 9. 地道的英文

很多稿件出自母语不是英语的作者，修改要让英文既没有 AI 腔，又地道。改正冠词、可数性（"a research""informations"）、介词（different from、consistent with、depend on）、which 与 that 的区分，以及从中文直译过来的结构（"with the development of""play an important role in""make a contribution to"、连串的"so as to"）。每个替换都要是真实存在的搭配："the methods remain largely empirical"是地道的，"the methods stay empirical"不是。术语不换成日常词。

### 10. 保留正确的部分

- 表达真实不确定性的限定：suggests、is consistent with、may、we conjecture。没有新证据时，suggests 不改成 shows。已证明结果上的限定归规则 7，somewhat、fairly 这类空泛限定归规则 1。
- 行为者不重要时的被动语态，以及指作者的 we。
- 术语、符号、公式、LaTeX 宏和环境、标签、引用键，一律原样保留。
- 认真的作者也用的文体惯例：引言里的"Our work relates to three streams of literature"、贡献列表、证明的结构。
- 引用：不增删任何引用键。被引文献只能依据原文已有的描述，或依据本次对话中读过的原文来描述，因为凭记忆写的描述最容易出错。一串引用从不说明与本文的区别时，写进报告。

#### 不作为改写理由

下列特征在很多读者看来像 AI 写的，但语料实测没有差异，或者人类用得更多。改掉它们只会让文字离人类写法更远，因此它们本身不能作为改动的理由。除特别说明外，数字为每千个汉字的频率。

| 特征 | 实测结果 |
|---|---|
| 句长、段长不够参差 | 没有差异：句长变异系数模型为 0.58，人类为 0.67。 |
| 被动句、名词化、长句本身 | 正常的书面语。"被认为""被视为"类抽象被动在模型文本中为 0.09。 |
| 重复全称而不用代词 | 人类文本更常见（相邻句重复 0.04，模型 0.02）。 |
| 一句之内的并列结构 | 人类用得一样多或更多，各种形式的比值在 0.61 到 1.10 之间。 |
| 正文问句、问句小标题 | 正文问句人类为 1.83，模型为 0.10。问句小标题按占全部小标题的比例计算没有差异。 |
| 段落里的"首先……其次" | 没有差异。处理对象是序数词小标题（4.6）。 |
| 虚词或口语连接词偏少 | 模型确实用得少，但补虚词无法核验，还会把书面语改成口语。 |
| 比喻本身 | 人类用得更多，约为模型的 2.4 倍。 |

### 11. 方法和证明按论文写，不写成工作日志

生成的方法部分和证明常常读起来像运行代码的记录：分几个阶段的"pipeline"、"verification protocol"、"sanity check"、对结果的"audit"、"certified bound"、求解器用的容差、从未触发的保护措施。论文要写的是方法、结果，以及得出结果的论证。润色和起草模式执行这一条。清理模式不按这一条改动，把每一项写进报告。

- **框架用词。** 方法和证明里不用 protocol、pipeline、workflow、sanity check、audit、certified bound、verification layer、guardrail 一类词来组织叙述，改为直接写对象：估计量、算法、命题 2 中的界、引理 3。"A sanity check confirms that the bound holds"改为证明这个界成立的引理或计算。只有文中的证明或精确计算确立了某个界，才能称它为 certified，此时按结果连同证明写出。领域内有定义的术语保留，与规则 2 相同：clinical trial protocol、cryptographic protocol、interval arithmetic。
- **计算机辅助的步骤。** 依赖计算的证明步骤写成引理并给出证明。引理陈述给出不等式或恒等式、成立的范围和其中的常数，这些都取自文中已有的论断。证明写明算了什么、用什么方法算的，以及计算是精确的还是数值的。精确计算指符号计算、有理数运算或区间算术，此时引理得到证明。数值计算指浮点运算，结果是证据而不是证明，陈述中要写明"数值上"，不能称为已证明。原文给出了软件和版本的，证明中写明。文中没有说明是哪种计算的，插入 `[[EVIDENCE: 精确计算还是浮点计算，以及所用软件]]`。新增这种引理是规则 6 最后一条的唯一例外。报告列出每个新增的引理，`compare` 会把它列为变动的正式环境。
- **要删的工程细节。** 删去与运行代码有关、报告结果并不依赖的细节：
  - 为数值稳定而加、不属于模型本身的正则化或抖动项取值；
  - 从未触发的保护、兜底、回退和重试；
  - 随机数安排，如哪个种子用于哪次运行、随机流如何划分；
  - 求解器容差、迭代上限和时间上限；
  - 验证残差及其他对计算本身的自检（"残差小于 10^{-12}"）；
  - 脚本、函数、文件、目录和运行环境的名称；
  - 调试、重跑和失败运行的经过。
- **要保留的复现信息。** 报告结果所依赖的取值全部保留：模型参数和超参数、样本量、重复或运行次数、数据来源和版本、报告的差距、误差或运行时间所依赖的算法及其停止规则或容差、计算机辅助证明所用的软件和版本、报告运行时间时的硬件，以及代码和数据的可得性声明。可能属于模型的取值保留，并在报告里向作者确认。报告建议把删掉的细节移到代码仓库或复现附录，但不自行移动。
- **删掉的数字。** 按这一条删掉的每个数字都在报告里列为有意改动，附原文行号。`compare` 会把它列在删除的数字下。

### 12. 结构审查：只报告，按要求才改

结合脚本的结构输出和通读结果，报告以下问题：

- 只有一个小节的章节，可并入上一级，或补上第二个小节；
- 可以合并的章节；
- 正文中的结论数量，可移入附录作引理的中间结果，以及只是换个参数重述另一结论、可改为推论或注记的结果；
- 包含不止一个论点的段落，以及论证跳跃的地方；
- 清理模式下结构不动时，非论文文档里的序数词小标题（4.6）。

## 文体与期刊

- 有严格页数限制的会议论文（计算机和工程领域常见）：简短，结果先行，贡献写成具体结果，局限平实地写一次。
- 期刊论文：研究问题落在具体情境里，按文献脉络定位，并写明与最接近工作的具体区别，假设附上理由，每个主要结果后面写出它的解释和成立条件。语气克制，结果说足。
- 审稿回复信：每条意见一条回复，引用意见原文，写明所做修改及其位置。不同意时给出论证和证据。开头感谢一次。
- 基金申请书（NSF、NIH 等）：见 `references/proposals.md`。
- 中文文本，包括教材、学位论文和报告：见 `references/chinese.md`。
- 作者以前的论文：见"先读风格参考"。

## 最终检查清单

- 每处改动都对应一条编号规则，没有对应规则的改动已撤销。
- 清理模式下，没有命中规则的句子逐字未动，命中规则的句子只改了命中的部分。
- 没有新增人名、数字、日期、引语、来源、因果或例子，每个实词都能在原文或用户材料中找到出处。
- 没有删掉真实的限定、让步、观点或结论。`compare` 列出的每个消失的限定词，都是按规则 7 删除并写进了报告。
- 标题、章节顺序、段落顺序、列表、表格和引文都在原位。
- 结论部分以外，不再有翻案腔、提示语冒号、空转引导句、复述句、口语起手式、元叙事、预告或小结。
- 没有相邻句共用一个骨架，没有段落用并列案例凑数。
- 没有当作标点的破折号，没有挤满分号或插入语的段落，术语以外没有比喻或拟人化标签。
- 每个拼凑标签要么是已有定义的术语，要么已换成它实际做的事，要么连同建议写进了报告；修改稿没有新增标签。
- 附近有具体值的概括说法已换成具体值，名词化的动词已还原。
- 实证结论的动词与证据相符，已证明的结果带着条件，已确立的结果按结果陈述，没有道歉，也没有辩解。
- 方法和证明写的是方法和论证，不是代码的运行过程。计算机辅助的步骤写成引理，并写明是精确计算还是数值计算；删掉的工程细节连同数字写进了报告；报告结果所依赖的取值都还在。
- 每一处缺失的证据，润色模式下是占位符，清理模式下是报告条目；只要还有占位符，报告开头就写明稿子不能提交。
- "不作为改写理由"中的特征没有被单独改动。
- `compare` 显示数字、引用键、标签、公式和正式陈述未变，或者每一处差异都列为有意改动。

## 输出

1. 完整的修改稿。`.tex` 或其他文件输入，交回完整的修改后文件，不用一串修改说明代替。
2. 一份简短报告，按同样的规则书写：
   - 修改稿中有任何 `[[EVIDENCE: ...]]` 占位符时，报告第一行用正文的语言提醒作者：稿子还不能提交，每个占位符都要换成作者自己数据或文献中的值或来源，或者删去对应结论，之后才能投给期刊、会议或审稿人；
   - 使用的模式，以及用过的风格参考；
   - 按规则分组的改动及数量；
   - 调整了范围、按规则 7 加强了语气或补上证据指向的结论；
   - 作者需要填写的占位符，清理模式下则是每一处需要补证据的结论；
   - 按规则 11 删掉的工程细节，每项附数字和原文行号；因可能属于模型而保留的取值；改写成引理的计算机辅助步骤；
   - 结构问题（规则 12）、作者起的比喻性名称，以及保留下来但没有定义的拼凑标签，每项附修改建议（规则 2）；
   - `compare` 对数字、引用键、标签、公式、正式陈述和限定词的最终结果。
