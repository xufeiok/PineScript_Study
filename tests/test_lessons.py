# 中文说明：课程数据最小单元测试
# 目的：验证 lessons.json 的结构完整性，避免前端加载异常
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS_FILE = ROOT / "web" / "data" / "lessons.json"


def test_lessons_json_exists():
  assert LESSONS_FILE.exists(), "lessons.json 不存在"


def test_lessons_schema():
  data = json.loads(LESSONS_FILE.read_text(encoding="utf-8"))
  assert "lessons" in data and isinstance(data["lessons"], list), "lessons 字段缺失或类型错误"
  for l in data["lessons"]:
    assert "id" in l and l["id"], "课程缺少 id"
    assert "title" in l and l["title"], "课程缺少 title"
    assert "pine_code" in l and isinstance(l["pine_code"], str), "缺少 pine_code"
    assert "python_code" in l and isinstance(l["python_code"], str), "缺少 python_code"
    assert "quiz" in l and isinstance(l["quiz"], list), "缺少 quiz 列表"

