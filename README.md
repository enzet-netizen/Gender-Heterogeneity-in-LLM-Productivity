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
#### output文件：authors_clean.csv，保留作者一共135,528个，去重之后一共23732个作者


| 数据 | 本次实验 | 论文 |
|---|---|---|
| 满足incumbent门槛的作者量 | 196,992 | 302,474 |
| 实际进回归被估计的作者 | 135,528 | 109,965 |

清除数据：
| 筛选条件 | 数据量 |
| ---- | ---- |
| 单字符 | 82  |
| 缩写 | 62,915   |
| 空值 | 116  |

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
#### 运行文件：gender_match.py
#### output文件：authors_gender.csv

<img width="522" height="93" alt="image" src="https://github.com/user-attachments/assets/629887af-b49b-4210-ba72-5030bdc78305" />


---


## 4.构建panel

<img width="897" height="94" alt="image" src="https://github.com/user-attachments/assets/1feb3055-f50e-4e50-86bd-ea668797f892" />

<img width="568" height="88" alt="image" src="https://github.com/user-attachments/assets/7e0433ee-5462-49dd-8d16-bd27f5b67c21" />

#### input文件：panel.csv,authors_gender.csv
#### 运行文件：panel_gender.py
#### output文件：panel_gender.csv

代码里面，只取两列，hashed_authro和gender，把性别接到panel上，panel添加gender_final列，去掉unknown的人，然后根据公式造post变量

<img width="409" height="33" alt="image" src="https://github.com/user-attachments/assets/3ce56874-72f2-410a-a2b4-39c75fd9a046" />

<img width="633" height="55" alt="image" src="https://github.com/user-attachments/assets/790d75a1-65ce-41ee-a4ae-8ae79595a854" />.


<img width="184" height="18" alt="image" src="https://github.com/user-attachments/assets/da4f417c-78e3-4495-b089-2109b16b506c" />

<img width="916" height="230" alt="image" src="https://github.com/user-attachments/assets/2d6072b1-31e2-4e23-88b3-3b9b2b05bc28" />

## 5.回归

#### input文件：panel_gender.csv
#### 运行文件：panel_gender.do
#### output文件：gender_coefficients.csv

<img width="309" height="17" alt="image" src="https://github.com/user-attachments/assets/b69a87b3-bfcd-42ff-9d0a-0610b5278b98" />.


<img width="314" height="177" alt="image" src="https://github.com/user-attachments/assets/1fba0d34-fa30-49b6-9134-af818058e16e" />.


<img width="190" height="20" alt="image" src="https://github.com/user-attachments/assets/b1e5564b-5123-4767-aa0c-8674429de2d7" />.


<img width="314" height="15" alt="image" src="https://github.com/user-attachments/assets/cb7c81d9-bd5a-4bdd-810e-5c436f0f8514" />.

<img width="225" height="74" alt="image" src="https://github.com/user-attachments/assets/b9fe7ea3-30b8-4461-8cfa-587644f70173" />

进回归的数据：male:75066, female:15854




## 6.生图
#### input文件：gender_coefficients
#### 运行文件：gender_plot.py

Overall 39.3%，Male 38.6%，置信区间36.3%-40.9%，Female 42.8%，置信区间37.7%-48%
<img width="495" height="501" alt="image" src="https://github.com/user-attachments/assets/b65cd48e-f231-4aba-8760-1a6111e05384" />



