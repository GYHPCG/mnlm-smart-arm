import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import gradio as gr
import os
from PIL import Image

def load_model(model_name="Qwen/Qwen-VL-Chat", 
              device="cuda" if torch.cuda.is_available() else "cpu",
              cache_dir="./models"):
    """
    Load the multimodal model and tokenizer
    Args:
        model_name: 模型名称
        device: 运行设备
        cache_dir: 模型下载缓存目录
    """
    os.makedirs(cache_dir, exist_ok=True)
    
    print(f"Loading model {model_name} on {device}...")
    print(f"Model will be downloaded to: {os.path.abspath(cache_dir)}")
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, 
        trust_remote_code=True,
        cache_dir=cache_dir
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        device_map="auto",
        torch_dtype=torch.float16,
        cache_dir=cache_dir
    )
    return model, tokenizer

def generate_response(message, image, history, model, tokenizer):
    """
    Generate response from the multimodal model
    """
    if image is not None:
        # 将图像转换为PIL格式
        if isinstance(image, str):
            image = Image.open(image)
        # 构建多模态输入
        query = tokenizer.from_list_format([
            {'image': image},
            {'text': message},
        ])
    else:
        query = message

    response, history = model.chat(tokenizer, query=query, history=history)
    return response, history

def create_interface(model, tokenizer):
    """
    Create Gradio interface with image upload capability
    """
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(scale=4):
                msg = gr.Textbox(
                    label="输入文本",
                    placeholder="在这里输入您的问题...",
                    lines=2
                )
            with gr.Column(scale=1):
                image = gr.Image(
                    label="上传图片",
                    type="pil"
                )
        with gr.Row():
            submit = gr.Button("发送")
            clear = gr.Button("清除对话")

        def user(user_message, user_image, history):
            return "", None, history + [[(user_image, user_message), None]]

        def bot(history):
            user_message = history[-1][0][1]
            user_image = history[-1][0][0]
            response, history = generate_response(user_message, user_image, history[:-1], model, tokenizer)
            history[-1][1] = response
            return history

        submit.click(user, [msg, image, chatbot], [msg, image, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        msg.submit(user, [msg, image, chatbot], [msg, image, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)

    return demo

def main():
    # 设置模型下载路径
    cache_dir = "./models"
    
    # Load model and tokenizer
    model, tokenizer = load_model(cache_dir=cache_dir)
    
    # Create and launch interface
    demo = create_interface(model, tokenizer)
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main() 