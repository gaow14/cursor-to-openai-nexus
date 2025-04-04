import gradio as gr
import requests
import time
import os

# 加载环境变量（从Hugging Face的Secret读取）
HF_TOKEN = os.getenv("HF_TOKEN", "default_token")
API_KEY = os.getenv("API_KEY", "sk-text")

def check_service():
    """检查后端服务是否就绪"""
    try:
        requests.get("http://localhost:3010/ping", timeout=2)
        return True
    except:
        return False

def chat(message, history):
    """处理用户消息"""
    # 等待后端服务启动
    while not check_service():
        time.sleep(1)
    
    try:
        response = requests.post(
            "http://localhost:3010/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"请求失败：{str(e)}"

# 创建网页界面
demo = gr.ChatInterface(
    fn=chat,
    title="AI 助手",
    description="输入你的问题开始对话",
    theme="soft"
)

# 启动服务（必须设置server_name和server_port！）
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False
)
