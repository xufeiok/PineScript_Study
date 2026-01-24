import json
import os

json_path = r'e:\Quant\PineScript_study\web\data\lessons.json'

# Define the order and categories
structure = {
    "基础语法 (Basics)": [
        "l1_intro", "l2_vars_types", "l3_operators", "l4_control_flow", 
        "l5_functions", "l10_arrays", "l11_inputs", "l12_debugging", 
        "l13_maps", "l14_libraries"
    ],
    "内置指标 (Built-in Indicators)": [
        "l6_ta_builtins", "l7_plotting", "ind_macd", "ind_rsi", "ind_bb", 
        "ind_atr", "ind_kdj", "ind_supertrend", "ind_vwap", "ind_ichimoku", 
        "ind_cci", "ind_adx"
    ],
    "量化策略 (Strategies)": [
        "l8_strategy_basics", "l9_risk_management", "strat_dual_ma", 
        "strat_rsi_reversal", "strat_bb_breakout", "strat_inside_bar", 
        "strat_turtle", "strat_grid", "strat_dca", "strat_pivot", 
        "strat_mtf", "strat_trailing"
    ],
    "参考资料 (Reference)": [
        "ref_ta_all"
    ]
}

# Create a mapping from id to category
id_to_category = {}
id_order = []
for cat, ids in structure.items():
    for i, lesson_id in enumerate(ids):
        id_to_category[lesson_id] = cat
        id_order.append(lesson_id)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Reorganize
new_lessons = []
lesson_map = {l['id']: l for l in data['lessons']}

# Add categorized lessons in order
for lesson_id in id_order:
    if lesson_id in lesson_map:
        l = lesson_map[lesson_id]
        l['category'] = id_to_category[lesson_id]
        new_lessons.append(l)

# Add any remaining lessons that were not in the structure (just in case)
for l in data['lessons']:
    if l['id'] not in id_to_category:
        l['category'] = "其他 (Others)"
        new_lessons.append(l)

data['lessons'] = new_lessons

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Lessons reorganized successfully.")
