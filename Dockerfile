FROM node:18-alpine
WORKDIR /app

# 安装Python和Git
RUN apk add --no-cache python3 py3-pip git
RUN pip install gradio

# 复制项目文件
COPY package.json .
RUN npm install
COPY . .

# 设置启动命令
EXPOSE 7860
CMD ["sh", "-c", "npm start & sleep 10 && python /app/huggingface/app.py"]
