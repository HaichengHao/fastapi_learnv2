# @Time    : 2026/1/28 10:57
# @Author  : hero
# @File    : main.py
from src import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=65533)