# bi-LSTM + CRF 中文命名实体识别

## 模型

1. 中文文字Embedding
2. Bi-LSTM
3. CRF

### code environment
在 python3.6 & Tensorflow1.13 下工作正常

其他环境也许也可以，但是没有测试过。

还需要安装额外的 `tf_metrics` package 来计算指标，包括准确率回召率和F1因子等等。运行以下命令安装
```
pip install git+https://github.com/guillaumegenthial/tf_metrics.git
```
### 语料的准备
本项目语料选用msra公开的命名实体标注集，位于本工程的`data/msra/raw_data`中。

### 字向量的准备
中文文字的向量表征，来源于[Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors)

其中关于字符向量的讨论，详情可见 https://github.com/Embedding/Chinese-Word-Vectors/issues/18

本项目选取词向量的链接地址 https://pan.baidu.com/s/1c9yiosHKNIZwRlLzD_F1ig ， 需要百度云下载，解压，放在`data/msra`目录下

### 训练数据的数据格式
参考 `data/msra/*.txt` 文件

##### step1
对于训练集和测试集，制作训练数据时遵循如下格式：
在`{}.words.txt`文件中，每一行为一个样本的输入
```text
中 共 中 央 致 中 国 致 公 党 十 一 大 的 贺 词
各 位 代 表 、 各 位 同 志 ：
```
在`{}.tags.txt`文件中，每一行为一个样本的标记
```text
B-ORG I-ORG I-ORG I-ORG O B-ORG I-ORG I-ORG I-ORG I-ORG I-ORG I-ORG I-ORG O O O
O O O O O O O O O O
```
本项目中，可在`data/msra`目录下运行`build_data_format.py`得到相应的格式

##### step2
因为本项目用了`index_table_from_file`来获取字符对应的id，需要两个文件表示词汇集和标志集，对应于`vocab.tags.txt`和`vocab.words.txt`,其中每一行代表一个词或者是一行代表一个标志。

本项目中，可在`data/msra`目录下运行`build_vocab.py`得到相应的文件

##### step3
由于下载的词向量非常巨大，需要提取训练语料中出现的字符对应的向量，对应本项目中的`data/msra/ch2vec.npz`文件

本项目中，可在`data/msra`目录下运行`build_embeddings.py`得到相应的文件

### 训练
在`bilstm_crf`目录底下运行 
```
python main.py
```

关于训练时间，在**GTX 1060 6G**的加持下大概耗了35分钟

### 计算模型的得分
在`bilstm_crf`目录底下运行 
```
./conlleval < results/score/testright.preds.txt > results/score/score.testright.metrics.txt
```
可在`bilstm_crf/results/score/score.testright.metrics.txt`得到模型在验证集上的得分

### export and serving
在`bilstm_crf`目录底下运行 
```
python saved_model.py
```
导出`estimator`推断图，可以用作prediction。本项目包含了`saved_model`可以不通过训练直接使用。

在`bilstm_crf`目录底下运行 `python serve.py`可以利用导出的模型进行实体识别。详情见代码。

### 测试结果

在固定参数下运行程序5次，`bilstm_crf/metrics.py`记录了这5次在验证集上测试的结果，测试结果汇总如下表：

| | `A` | `P` | `LOC-P` | `ORG-P` | `PER-P` | `R` | `LOC-R` | `ORG-R` | `PER-R` | `F` | `LOC-F` | `ORG-F` | `PER-F` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|1st | 98.49 |89.52 | 92.39 |86.52 | 87.48 |87.38 | 88.67 |83.40 | 88.19 |88.44 | 90.49 |84.93 |87.83 |
|2nd | 98.52 |90.47 | 94.36 |86.68 | 87.67 |85.73 | 86.69 |83.62 | 85.76 |88.04 | 90.36 |85.12 |86.70 |
|3rd | 98.36 |89.08 | 93.21 |84.44 | 86.42 |85.88 | 87.80 |82.34 | 85.45 |87.45 | 90.42 |83.38 |85.93 |
|4th | 98.46 |89.58 | 90.30 |87.81 | 89.68 |86.39 | 89.33 |82.79 | 84.54 |87.96 | 89.81 |85.23 |87.03 |
|5th | 98.43 |89.74 | 92.34 |84.16 | 89.88 |85.62 | 87.52 |83.02 | 84.59 |87.63 | 89.86 |83.59 |87.15 |
|best | 98.52 |90.47 | 94.36 |87.81 | 89.88 |87.38 | 89.33 |83.62 | 88.19 |88.44 | 90.49 |85.12 |87.83 |
|mean| 98.45 | 89.68 | 92.52 |85.92 | 88.23 | 86.2 | 88.0 | 83.03| 85.71| 87.90 | 90.18 | 84.45 | 86.93 |

上表中字母与指标的对应关系是
 - `A` -> `Accuracy`
 - `P` -> `Precision`
 - `R` -> `Recall`
 - `F` -> `FB1因子`
 
 由上表可以得到，模型在验证集上平均F因子接近**88%**
 
 #### `Serve.py`的输出
 ![截图](https://github.com/linguishi/chinese_NER/blob/master/clip.png?raw=true)
 
 
 ## 参考
 
 [1] https://guillaumegenthial.github.io/sequence-tagging-with-tensorflow.html
 
 [2] https://github.com/guillaumegenthial/tf_ner/tree/master/models/lstm_crf
 
 [3] https://pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html
 
 [4] https://github.com/Determined22/zh-NER-TF