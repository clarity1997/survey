
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    COPY . .

    CMD ["python", "app.py"]
    