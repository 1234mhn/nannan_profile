# MedFILIP 论文精读文字稿

> 论文：MedFILIP: Medical Fine-grained Language-Image Pre-training
> arXiv: 2501.10775（2025-01）
> 单位：哈尔滨工业大学 + KAIST + Case Western Reserve University
> 代码：github.com/PerceptionComputingLab/MedFILIP
> 整理日期：2026-10-26

---

## 一、背景：CLIP 现在怎么干这活

CLIP 做的事很简单：把图和文本一起训练，让它们能对上号。

具体流程：

```
一张胸片  +  一份报告
    ↓           ↓
  图像编码     文字编码
    ↓           ↓
 图像向量     文本向量
    ↓           ↓
    └── 对齐 ──┘   （算相似度，让配对的更近）
```

训练完之后，它就能做零样本分类了——你给它一个病的名字，它在图库里找最像的。

这套路子在医学图像分类上确实有效。这就是背景。

---

## 二、问题：这一步「对齐」出毛病了

### 问题 1：太粗（coarse）

报告原文可能是：

> "左下肺斑片状渗出影，考虑感染；心影稍增大；未见气胸。"

CLIP 的做法：把这一整段**压成一个向量**，跟整张图对齐一次。

这个向量里装着四样东西：

| 属性 | 内容 |
|:--|:--|
| 疾病类别 | 感染、心影增大 |
| 位置 | 左下肺 |
| 形态 | 斑片状 |
| 程度 | 稍 |

四样东西被平均成一团。

想问它："病变在左边还是右边？"

它答不上来。因为位置信息已经和"感染""斑片状"一起被平均成灰色了。

> 就像红绿蓝三杯水倒进一个桶，成了灰水。想从灰水里舀一杯纯红——舀不出来。

**注意作者的用词是 averaged（平均掉），不是 lost（丢掉）。**

「丢掉」更严重，但「平均掉」更麻烦——因为它没严重到能让你察觉：

- 以为有，其实用不了
- 还会污染别的信息（位置信息平均进整个向量，连问"什么病"都跟着模糊）
- 想修都无从下手（信息没了你知道该补，信息混着你不知道错在哪）

### 问题 2：非结构化（unstructured）

医生写报告是自然语言，机器看不懂结构。

> "左下肺见斑片影，考虑感染"

机器读到的是一整句话。它不知道：
- 哪个词是"位置"
- 哪个词是"疾病"
- 哪个词是"程度"

没法拆，自然没法分开对齐。

### 问题 3：缺视觉描述（最关键）

就算成功抽出了"肺炎"这个词，它还是对不上图。

因为"肺炎"是一个**医学名词**，图像里只有像素点。中间缺一座桥。

> 你手里拿着"肺炎"两个字，对着胸片说："给我找肺炎。"
> 胸片不会回答你——它不知道"肺炎"对应哪片像素。

报告里从来没写过"肺炎在视觉上长什么样"，只写了"肺炎"。

**这三条问题加起来，CLIP 就只能糊里糊涂地粗对齐。**

---

## 三、解法：拆开、翻译、软标签

MedFILIP 的对策分三招，一招对应一个问题。

### 招 1：用 LLM 把报告拆开 → 解决「非结构化」

让 GPT-3.5 读报告，按固定模板抽成结构化数据：

```
输入：左下肺斑片状渗出影，考虑感染
输出：
  severity（程度）：轻
  location（位置）：左下肺
  disease（疾病）：感染
```

这一步叫 **GPT-IE**。

效果：随机的自然语言 → 规整的三元组，后面才好分别对齐。

### 招 2：把疾病名翻译成视觉描述 → 解决「缺视觉描述」

这是全文最巧的一步。

不拿"肺炎"直接对图，先把它**翻译成图像语言**：

```
「肺炎」
   ↓ 翻译
「肺部出现斑片状或融合的白色区域」
```

然后拿"斑片状或融合的白色区域"去和图像对齐。

这一步为什么了不起：

- "斑片状白色区域"是**图像里真的能看得到的东西**，有东西可对
- 额外好处：碰上没见过的新病（比如 COVID-19），只要它的视觉描述能写出来，模型就能认——**因为它学的是"视觉长什么样"，不是死记病名**

这一步叫 **IKI**（图像知识注入）。

### 招 3：用相似度替代 0/1 标签 → 解决「假阴性」

传统做法：

- 两个配对的 → 标签 1（该拉近）
- 两个不配对的 → 标签 0（该推远）

问题：A 病人的报告写"肺不张"，B 病人的报告也写"肺不张"。它们明明是一类，却被当成 0 —— **被强行推远。这叫假阴性。**

MedFILIP 的做法：不算 0/1，算**文本之间的相似度**。

"肺不张" vs "肺不张" → 相似度 0.9 → 该拉得比 0.1 的近

从"这是不是一对"变成"这一对有多像"。

这一步叫 **SSM**（语义相似矩阵）。

---

## 四、三招串起来

```
报告文本
   ↓ ①GPT-IE 拆解
疾病 + 位置 + 程度（结构化）
   ↓ ②IKI 翻译成视觉描述
「斑片状白色区域」（图像能懂的话）
   ↓ ③SSM 用相似度做标签
各自单独和图像对齐
   ↓
分类：已知病分对 + 未见病也能认
```

---

## 五、摘要逐句对照表

| 句 | 原文要点 | 讲什么 |
|:--|:--|:--|
| 1 | VLP models like CLIP have shown promising performance in medical image classification | 承认 CLIP 有效（给台阶） |
| 2 | However, current paradigm relies on coarse alignment using image-report pairs, struggling with fine-grained disease-attribute data | 转折，靶子：它太粗 |
| 3-4 | Reports contain fine-grained attributes (severity, location, category) that are averaged or lost during coarse alignment | 论证：粗会平均掉属性 |
| 5-6 | Therefore, extracting these attributes and aligning them individually with image features is essential | 目标：拆开，各自单独对齐 |
| 7 | However, reports are unstructured and lack visual characteristic description | 障碍：非结构化 + 缺视觉描述 |
| 8 | We propose to extract fine-grained attributes via LLM, then use them to prompt disease knowledge in visual space | 解法：LLM 抽取 + 翻译成视觉提示 |
| 9 | A semantic similarity matrix (SSM) uses text similarity to supervise alignment, mitigating false negatives | 补强：软标签解决假阴性 |
| 10 | Extensive experiments on multiple public datasets demonstrate SOTA in zero-shot classification and fine-tuning | 结论：SOTA |

---

## 六、关键数字

### 零样本分类 ACC

| 数据集 | MedCLIP | MedKLIP | MedFILIP |
|:--|:--|:--|:--|
| MIMIC-16 | 64.48 | 69.67 | **74.71** |
| Pneumonia | 76.82 | 80.02 | **81.23** |
| MIMIC-multi | 59.23 | 64.37 | **71.06** |
| ChestX-ray14 | 72.48 | **86.19** | 85.67 |
| VinBigData | 58.04 | 67.87 | **70.03** |
| MIMIC-FG | 59.77 | 65.44 | **71.85** |

最高提升 6.69%（MIMIC-multi）

### 微调（只用 10% 数据）

- Pneumonia：83.14 vs ResNet50 的 74.54
- 只用 10% 数据超过别人用 100%

### 消融阶梯（逐步加模块）

| 配置 | ACC |
|:--|:--|
| Baseline | 63.9 |
| + Entity | 67.2 |
| + FG | 70.6 |
| + IKI | 73.3 |
| + SSM | **74.7** |

每一步都有提升，逻辑一条线。

### 训练成本

单卡 RTX-3090，约 10 小时。

---

## 七、必须主动交代的短板

**ChestX-ray14 上输给了 MedKLIP**（85.67 vs 86.19），论文自己承认了。

汇报时主动指出来，比被老师问出来强。

---

## 八、一句话核心

> CLIP 把整份报告压成一个向量，细节被平均掉了。MedFILIP 用 LLM 把报告拆成「疾病、位置、程度」，再把疾病名翻译成"视觉上长什么样"，让每样东西单独和图像对齐，同时用文本相似度代替 0/1 标签避免假阴性。

---

## 九、与 MedCLIP 的关系（阅读路线连贯性）

- MedCLIP（EMNLP 2022）：用语义匹配解决假阴性问题
- MedFILIP（2025）引用 MedCLIP[6]，明确指出其 false negative 问题未解决透
- MedFILIP 的推进：不仅解决假阴性（SSM），还进一步抽细粒度实体（GPT-IE）+ 注入视觉知识（IKI）

这条线可以串成一个完整故事讲。
