# Gender-Heterogeneity-in-LLM-Productivity

Replicator: Enzo Tang

Original paper: Kusumegi, K., de Vaan, M., Stuart, T., & Yin, Y. (2025).
Scientific production in the era of large language models.
*Science*, 390, 1240. https://doi.org/10.1126/science.adw3000

Last updated: June 2026

---

## 1.姓名消歧去重

#### input文件：panel.csv
#### 运行文件：author_clean.py
#### output文件：authors_clean.csv，保留作者一共110,286个，去重之后一共22,064个作者


| 数据 | 本次实验 | 论文 |
|---|---|---|
| 满足incumbent门槛的作者量 | 196,992 | 302,474 |
| 实际进回归被估计的作者 | 135,528 | 109,965 |

清除数据：
| 筛选条件 | 数据量 |
| ---- | ---- |
| 单字符 | 82  |
| 缩写 | 62,915   |
| 空格 | 116  |

保留数据：133，879条（能够通过名字进行性别查询的占68%）
去重之后的名字量：23,732

<img width="147" height="151" alt="image" src="https://github.com/user-attachments/assets/d1c2b3d5-21f5-48c2-a4ad-f53679ad2885" />

保留数据

<img width="384" height="183" alt="image" src="https://github.com/user-attachments/assets/c10da53d-9f13-43e0-9a59-d156a374d572" />

删除数据

<img width="254" height="76" alt="image" src="https://github.com/user-attachments/assets/0ba44cc9-f9c3-455f-9468-b8b45cd31ccc" />



## 2.性别分析
#### input文件：authors_clean.csv
#### 运行文件：name_gender_identification.py
#### output文件： gender_cache.csv

取出去重后的23,731个名字，分批到genderize API，每个名字存回 name，gender，probability，count，并做了一个断点续传。
无法查到性别（返回none）：2009，占8.5%.

按照count：

<img width="230" height="103" alt="image" src="https://github.com/user-attachments/assets/45812852-18e2-46a3-82d0-ac63e695b1d1" />

按照probablity:

<img width="218" height="77" alt="image" src="https://github.com/user-attachments/assets/3d7aded2-91c7-4f69-9665-8b8f1c2594c0" />



---


## 3.连接作者与性别分析结果
把性别结果贴回每个作者,通过左连接进行。性别没有判断出来的就写unknown.

#### input文件：authors_clean.csv，gender_cache.csv'
#### 运行文件：sample gender_match.py
#### output文件：authors_gender.csv

<img width="522" height="93" alt="image" src="https://github.com/user-attachments/assets/629887af-b49b-4210-ba72-5030bdc78305" />


---


## 4.构建panel

#### panel文件：panel.csv
#### 运行文件：build_panel.py
#### output文件：panel.csv

<img width="897" height="94" alt="image" src="https://github.com/user-attachments/assets/1feb3055-f50e-4e50-86bd-ea668797f892" />


作者email:
"Active periods: see S2.3 “For each author, we track the number of preprints they posted each month,” so the panel is not conditioned on active publication periods.
Control construction: see S2.4 “Each author in this group is assigned a unique event time,” so control observations are not reused.
Hope this clarifies the design. We’re also aware of other groups that have independently replicated the pattern without clear pre-trends, following the paper and SM."


| # | 实现 | 原文 |
|---|---|---|
| 1 | incumbent = 2018-01~2021-12 发文 ≥4 篇 | S2.3 "researchers with at least 4 works published between 2018 and 2021" |
| 2 | 观测窗 2022-01~2024-06，零产出月记 0 保留 | S2.3 "the number of preprints they posted each month during a 30-month period (Jan 2022 - June 2024) |
| 3 | treated = 第一篇 is_llm 论文的月份 | S2.4 "treatment time as the author's first month of LLM adoption" |
| 4 | control = incumbents − ever_llm | S2.4 "never-treated authors–those with no LLM-assisted publications as of June 2024" |
| 5 | placebo 在 2023-01~2024-06 均匀随机，seed=42 | S2.4 "assigned a unique event time, randomly drawn between January 2023 and June 2024" |
| 6 | 事件窗 −12~+18，排除 τ=0，参照期 τ=−1 | 3.1 "we exclude the month of treatment"、"D^k for k ≥ −1 |
| 7 | control 只进 stack 一次 | 作者email回信 |

---


## 8.生图
#### input文件：coefs_stata.csv
#### 运行文件：plot.do
#### output文件：fig1.pdf
<img width="1475" height="870" alt="image" src="https://github.com/user-attachments/assets/606dd62b-012c-493f-95e8-57874016087a" />


