# -*- coding: utf-8 -*-
"""FastAPI 人脸识别小助手 - 入口文件"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        'app:create_app',
        host='0.0.0.0',
        port=8003,
        reload=True,
        factory=True,
    )
