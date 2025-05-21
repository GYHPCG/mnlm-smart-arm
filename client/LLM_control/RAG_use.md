# RAG 索引器文档

## 概述
RAG 索引器是一个基于 Python 的工具，用于创建和管理 FAISS（Facebook AI 相似性搜索）索引，主要用于函数描述的语义搜索。它使用 OpenAI 的嵌入 API 来创建函数描述和指令的向量嵌入，从而实现语义搜索功能。

## 功能特点
- 从函数定义创建 FAISS 索引
- 使用 OpenAI 的 text-embedding-3-small 模型生成嵌入向量
- 保存和加载索引及函数序列
- 基于语义相似度检索函数序列
- 提供命令行界面进行索引创建和查询

## 环境要求
- Python 3.x
- OpenAI API 密钥（在 .env 文件中设置）
- 必需的包：
  - faiss-cpu
  - numpy
  - openai
  - python-dotenv

## 安装步骤
1. 确保已安装 Python 3.x
2. 安装必需的包：
```bash
pip install faiss-cpu numpy openai python-dotenv
```
3. 创建 `.env` 文件并设置 OpenAI API 密钥：
```
OPENAI_API_KEY=你的API密钥
```

## 使用方法

### 命令行界面

#### 创建索引
```bash
python rag_indexer.py index --command-bank-file-path 路径/到/operations_data.json
```

可选参数：
- `--index-destination`：保存 FAISS 索引的路径（默认：rag/index/instructions.index）
- `--data-destination`：保存函数序列的路径（默认：rag/index/instructions_data.json）

#### 查询索引
```bash
python rag_indexer.py query -q "你的查询内容"
```

可选参数：
- `--index-path`：FAISS 索引文件路径
- `--data-path`：函数序列文件路径
- `--k`：要检索的函数序列数量（默认：1）

### 编程方式使用

```python
from rag_indexer import RAGIndexer

# 初始化索引器
indexer = RAGIndexer()

# 创建新索引
indexer.create_index(
    command_bank_file_path="路径/到/operations_data.json",
    index_destination="路径/到/index.index",
    data_destination="路径/到/data.json"
)

# 加载现有索引
indexer.load_index_and_data(
    index_path="路径/到/index.index",
    data_path="路径/到/data.json"
)

# 检索函数序列
result = indexer.retrieve_function_sequence("你的查询内容")
```

### 输入数据格式
输入 JSON 文件应包含函数定义数组，格式如下：
```json
[
    {
        "description": "函数描述",
        "function_name": "函数名称",
        "parameters": {
            "参数1": "参数描述",
            "参数2": "参数描述"
        },
        "example": {
            "instruction": "示例指令"
        }
    }
]
```

## 文件结构
- `rag_indexer.py`：主要实现文件
- `rag/index/instructions.index`：默认的 FAISS 索引文件
- `rag/index/instructions_data.json`：默认的函数序列文件

## 错误处理
索引器包含以下错误处理：
- 缺失或无效的 JSON 文件
- OpenAI API 错误
- 文件系统操作错误
- 无效的索引操作

## 注意事项
- 索引器使用 L2（欧几里得）距离进行相似度搜索
- 嵌入向量使用 OpenAI 的 text-embedding-3-small 模型生成
- 所有文件路径都统一使用正斜杠
- 索引器会自动创建必要的目录（如果不存在） 