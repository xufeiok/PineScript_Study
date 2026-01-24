# 中文说明：后端服务（FastAPI）
"""
功能概述：
- 提供课程数据 API（/lessons）
- 提供用户进度读写 API（/progress）
- 允许前端跨域访问（本地开发）

输入/输出：
- GET /lessons -> 返回 lessons.json 中的课程数据
- GET /progress?user=default -> 返回指定用户进度
- POST /progress { user, progress } -> 保存指定用户进度

边界与安全：
- 简易文件存储，生产环境建议使用数据库与鉴权
- 不保存敏感信息，不记录密钥
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI(title="Pine Script 学习系统 API", version="0.1.0")

# 允许本地与移动端访问（开发阶段）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT = Path(__file__).resolve().parent.parent
LESSONS_FILE = ROOT / "web" / "data" / "lessons.json"
DATA_DIR = ROOT / "server" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROGRESS_FILE = DATA_DIR / "progress.json"


class ProgressPayload(BaseModel):
    user: str
    progress: dict


@app.get("/lessons")
def get_lessons():
    """中文说明：返回课程数据 JSON"""
    if not LESSONS_FILE.exists():
        raise HTTPException(status_code=404, detail="课程数据不存在")
    with LESSONS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/progress")
def get_progress(user: str = "default"):
    """中文说明：读取指定用户的学习进度"""
    if not PROGRESS_FILE.exists():
        return {"user": user, "progress": {}}
    try:
        with PROGRESS_FILE.open("r", encoding="utf-8") as f:
            all_data = json.load(f)
        return {"user": user, "progress": all_data.get(user, {})}
    except Exception:
        return {"user": user, "progress": {}}


@app.post("/progress")
def save_progress(payload: ProgressPayload):
    """中文说明：保存指定用户的学习进度"""
    try:
        if PROGRESS_FILE.exists():
            with PROGRESS_FILE.open("r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = {}
        all_data[payload.user] = payload.progress
        with PROGRESS_FILE.open("w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {e}")

