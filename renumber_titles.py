import json
import re

json_path = r'e:\Quant\PineScript_study\web\data\lessons.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define regex to strip existing prefixes
# Patterns: "1. ", "10. ", "指标 1: ", "策略 1: "
def clean_title(title):
    # Remove "X. " or "XX. " prefix
    title = re.sub(r'^\d+\.\s*', '', title)
    # Remove "指标 X: " prefix
    title = re.sub(r'^指标\s*\d+:\s*', '', title)
    # Remove "策略 X: " prefix
    title = re.sub(r'^策略\s*\d+:\s*', '', title)
    return title

# Counters for each category
category_counters = {}

for lesson in data['lessons']:
    cat = lesson.get('category', '其他')
    if cat not in category_counters:
        category_counters[cat] = 1
    
    original_title = lesson['title']
    cleaned = clean_title(original_title)
    
    # Format new title based on category
    idx = category_counters[cat]
    
    if "基础语法" in cat:
        new_title = f"{idx}. {cleaned}"
    elif "内置指标" in cat:
        new_title = f"指标 {idx}: {cleaned}"
    elif "量化策略" in cat:
        new_title = f"策略 {idx}: {cleaned}"
    elif "参考资料" in cat:
        # Keep original or just prefix
        new_title = cleaned # No numbering for appendix usually, or keep original name if it's special
        if "附录" not in new_title:
             new_title = f"附录: {new_title}"
    else:
        new_title = f"{idx}. {cleaned}"
        
    lesson['title'] = new_title
    category_counters[cat] += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Titles renumbered successfully.")
