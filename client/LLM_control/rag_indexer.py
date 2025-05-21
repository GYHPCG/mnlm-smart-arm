import argparse
import json
import os
from typing import Any, Dict, List

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from utils import Logger


class RAGIndexer:

    def __init__(self):
        """
        Initialize the RAGIndexer class.
        """
        load_dotenv(override=True)
        self.logger = Logger(__file__)
        self.client = OpenAI()
        self.function_sequences = []
        self.index = None

    def create_index(
        self, command_bank_file_path: str, index_destination: str, data_destination: str
    ) -> None:
        """
        Create the FAISS index for function descriptions.
        """
        # 加载函数定义数据
        functions_data = self._load_json_file(command_bank_file_path)
        descriptions = []
        function_sequences = []
        
        # 处理每个函数定义
        for function_data in functions_data:
            # 组合description和instruction作为检索文本
            combined_text = f"{function_data['description']} {function_data['example']['instruction']}"
            descriptions.append(combined_text)
            # 保存完整的函数信息
            function_sequences.append({
                "description": function_data["description"],
                "function_name": function_data["function_name"],
                "parameters": function_data["parameters"],
                "example": function_data["example"]
            })

        # 生成嵌入向量
        embeddings = self._embed_instructions(descriptions)

        # 创建FAISS索引
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        # 保存索引和函数序列
        self._save_index_and_data(
            function_sequences=function_sequences,
            index_destination=index_destination,
            data_destination=data_destination,
        )

    def _load_json_file(self, command_bank_file_path: str) -> List[Dict[str, Any]]:
        """
        Load the JSON file containing function definitions.

        Returns:
            list: List of function definitions.
        """
        self.logger.info(f"Loading JSON file: {command_bank_file_path}")
        with open(command_bank_file_path, "r", encoding='utf-8') as file:
            return json.load(file)

    def _embed_instructions(self, instructions: List[str]) -> np.ndarray:
        """
        Embed instructions using OpenAI's embedding API.

        Args:
            instructions (list): List of instructions.

        Returns:
            np.ndarray: Array of instruction embeddings.
        """
        self.logger.info(f"Embedding instructions...")
        embeddings = []
        for instruction in instructions:
            # Ensure instruction is a single line
            instruction = instruction.replace("\n", " ")
            # Create embedding
            response = self.client.embeddings.create(
                input=[instruction], model="text-embedding-3-small"
            )
            embeddings.append(response.data[0].embedding)
        return np.array(embeddings, dtype="float32")

    def _save_index_and_data(
        self,
        function_sequences: List[Dict[str, Any]],
        index_destination: str,
        data_destination: str,
    ) -> None:
        """
        Save the FAISS index and function sequences to files.

        Args:
            function_sequences (list): List of function sequences.
            index_destination (str): Path to save the FAISS index.
            data_destination (str): Path to save the function sequences.
        """
        # Ensure the index and data are created
        if self.index is None:
            raise ValueError("Index has not been created. Call create_index() first.")

        # 打印索引信息
        print(f"索引类型: {type(self.index)}")
        print(f"索引维度: {self.index.d}")
        print(f"索引中的向量数量: {self.index.ntotal}")
        print(f"索引是否训练: {self.index.is_trained}")

        # 统一使用正斜杠作为路径分隔符
        index_destination = index_destination.replace('\\', '/')
        data_destination = data_destination.replace('\\', '/')

        # Save the FAISS index
        if os.path.exists(index_destination):
            os.remove(index_destination)
        os.makedirs(os.path.dirname(index_destination), exist_ok=True)
        print(f"FAISS路径: {index_destination}")
        faiss.write_index(self.index, index_destination)

        # Save the function sequences
        if os.path.exists(data_destination):
            os.remove(data_destination)
        os.makedirs(os.path.dirname(data_destination), exist_ok=True)
        with open(data_destination, "w", encoding='utf-8') as file:
            json.dump(function_sequences, file, indent=2, ensure_ascii=False)

    def load_index_and_data(
        self, index_path: str = None, data_path: str = None
    ) -> None:
        """
        Load the FAISS index and function sequences from files.

        Args:
            index_path (str): Path to the FAISS index file.
            data_path (str): Path to the function sequences file.
        """
        if not index_path:
            index_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "rag/index/instructions.index",
            )
        if not data_path:
            data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "rag/index/instructions_data.json",
            )
        self.index = faiss.read_index(index_path)
        with open(data_path, "r", encoding='utf-8') as file:
            self.function_sequences = json.load(file)

    def retrieve_function_sequence(self, description: str, k: int = 5) -> str:
        """
        Retrieve the function sequence for a given query.

        Args:
            description (str): Query to search for.
            k (int): Number of function sequences to retrieve for each action.

        Returns:
            str: JSON string containing all retrieved function sequences.
        """
        # 将查询按各种分隔符分割成多个动作
        actions = []
        # 顺序动作分隔符
        sequential_separators = [
            # 中文分隔符
            '，', ',',  # 中英文逗号
            '然后', '接着', '之后', '随后',  # 表示顺序
            '再', '又', '还',  # 表示追加
            '最后', '最后再',  # 表示最后
            '先', '首先',  # 表示开始
            '其次', '再次',  # 表示中间
            # 英文分隔符
            'then', 'after', 'afterwards',  # 表示顺序
            'next', 'subsequently',  # 表示下一步
            'finally', 'lastly',  # 表示最后
            'first', 'firstly',  # 表示开始
            'secondly', 'thirdly',  # 表示中间
            'and then', 'and after',  # 复合顺序
        ]
        # 同时动作分隔符
        simultaneous_separators = [
            # 中文分隔符
            '一边', '一边',  # 表示同时
            '同时', '与此同时',  # 表示同时
            '并且', '而且',  # 表示并列
            '和', '与',  # 表示并列
            '以及', '还有',  # 表示追加
            # 英文分隔符
            'while', 'whilst',  # 表示同时
            'simultaneously', 'at the same time',  # 表示同时
            'and', 'as well as',  # 表示并列
            'along with', 'together with',  # 表示一起
            'plus', 'in addition',  # 表示追加
            'while also', 'while at the same time',  # 复合同时
        ]
        
        # 合并所有分隔符
        all_separators = sequential_separators + simultaneous_separators
        
        # 尝试用每个分隔符分割
        for sep in all_separators:
            if sep in description:
                actions.extend([action.strip() for action in description.split(sep)])
                break
                
        # 如果没有找到分隔符，则整个描述作为一个动作
        if not actions:
            actions = [description]

        all_results = []
        # 对每个动作分别进行检索
        for action in actions:
            # Embed the query
            query_embedding = self._embed_instructions([action])
            # Search the index
            _, indices = self.index.search(query_embedding, k)
            # 获取前k个最相关的结果
            if len(indices[0]) > 0:
                # 获取该动作的top-k个结果
                action_results = []
                for i in range(min(k, len(indices[0]))):
                    retrieved_function = self.function_sequences[indices[0][i]]
                    action_results.append(retrieved_function)
                all_results.extend(action_results)

        # 返回所有检索到的结果
        json_blob = json.dumps(all_results, ensure_ascii=False)
        return json_blob


def parse_args():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Function Indexer")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    index_destination = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "rag/index/instructions.index"
    )

    data_destination = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "rag/index/instructions_data.json",
    )

    # Subparser for creating index
    create_index_parser = subparsers.add_parser(
        "index", help="Create a new FAISS index from function definitions"
    )

    default_command_file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "rag/operations_data.json"
    )
    create_index_parser.add_argument(
        "--command-bank-file-path",
        type=str,
        default=default_command_file_path,
        help="Path to the JSON file containing function definitions",
    )

    create_index_parser.add_argument(
        "--index-destination",
        type=str,
        default=index_destination,
        required=False,
        help="Path to save the FAISS index",
    )

    create_index_parser.add_argument(
        "--data-destination",
        type=str,
        default=data_destination,
        required=False,
        help="Path to save the function sequences",
    )

    # Subparser for querying index
    query_index_parser = subparsers.add_parser(
        "query", help="Query an existing FAISS index"
    )
    query_index_parser.add_argument(
        "-q", "--query", type=str, help="Query to search for"
    )
    query_index_parser.add_argument(
        "--index-path",
        type=str,
        default=index_destination,
        required=False,
        help="Path to the FAISS index file",
    )
    query_index_parser.add_argument(
        "--data-path",
        type=str,
        default=data_destination,
        required=False,
        help="Path to the JSON file containing function sequences",
    )
    query_index_parser.add_argument(
        "--k",
        type=int,
        default=1,
        required=False,
        help="Number of function sequences to retrieve",
    )

    # Parse arguments
    return parser.parse_args()

def get_rag_result(command_str):
    """
    Get RAG result for a given command string.
    
    Args:
        command_str (str): The command string to search for
        
    Returns:
        str: JSON string containing the retrieved function sequence
    """
    indexer = RAGIndexer()
    # Use default paths
    index_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "rag/index/instructions.index"
    )
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "rag/index/instructions_data.json",
    )
    indexer.load_index_and_data(
        index_path=index_path,
        data_path=data_path
    )
    return indexer.retrieve_function_sequence(command_str)

if __name__ == "__main__":
    args = parse_args()
    if args.command == "index":
        indexer = RAGIndexer()
        indexer.create_index(
            command_bank_file_path=args.command_bank_file_path,
            index_destination=args.index_destination,
            data_destination=args.data_destination,
        )
        print("Index and data saved.")
    else:
        indexer = RAGIndexer()
        indexer.load_index_and_data(
            index_path=args.index_path, data_path=args.data_path
        )
        function_sequence = indexer.retrieve_function_sequence(args.query, args.k)
        print(f"Function sequence: {function_sequence}")
