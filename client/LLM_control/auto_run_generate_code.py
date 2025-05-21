import requests
import subprocess
import os
from openai import OpenAI
from datetime import datetime

def get_code_from_llm(prompt):
    client = OpenAI(
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    
    SYSTEM_PROMPT = """你是一个Python代码生成专家。请根据用户的需求生成可执行的Python代码。
    只返回代码本身，不要包含任何解释或markdown标记。确保代码是完整且可执行的。"""
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content.strip()

def write_code_to_file(code, prompt):
    # 创建code目录（如果不存在）
    code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code')
    os.makedirs(code_dir, exist_ok=True)
    
    # 生成文件名：使用时间戳和提示词的前几个字
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 从提示词中提取有意义的名称（取前10个字符，去除特殊字符）
    name_part = ''.join(c for c in prompt[:10] if c.isalnum() or c.isspace()).strip().replace(' ', '_')
    filename = f"{timestamp}_{name_part}.py"
    
    file_path = os.path.join(code_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return file_path

def run_code(file_path):
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        print("执行结果:")
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
    except Exception as e:
        print(f"执行出错: {str(e)}")

if __name__ == "__main__":
    prompt = "写一个打印 'Hello from LLM' 的 Python 脚本"
    print("正在生成代码...")
    code = get_code_from_llm(prompt)
    print("\n生成的代码：")
    print(code)

    file_path = write_code_to_file(code, prompt)
    print(f"\n代码已保存到: {file_path}")
    
    print("\n正在执行代码...")
    run_code(file_path)