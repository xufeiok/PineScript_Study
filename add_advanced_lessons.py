import json
import os

json_path = r'e:\Quant\PineScript_study\web\data\lessons.json'

new_lessons = [
    {
        "id": "l11_inputs",
        "title": "11. 交互输入 (Inputs)",
        "subtitle": "让脚本更灵活",
        "concept": """
<h3>交互式输入</h3>
<p><code>input()</code> 函数允许用户在不修改代码的情况下调整脚本参数。Pine Script v5 提供了类型安全的输入函数。</p>
<div class="detail-box">
    <h4>常用输入类型</h4>
    <ul>
        <li><code>input.int(defval, title, minval, maxval)</code>: 整数</li>
        <li><code>input.float(defval, title)</code>: 浮点数</li>
        <li><code>input.bool(defval, title)</code>:布尔开关</li>
        <li><code>input.string(defval, title, options=[...])</code>: 下拉菜单</li>
        <li><code>input.color(defval, title)</code>: 颜色选择器</li>
        <li><code>input.source(close, title)</code>: 数据源选择 (如 open, hl2)</li>
        <li><code>input.symbol(syminfo.tickerid, title)</code>: 标的选择</li>
        <li><code>input.timeframe("D", title)</code>: 时间周期选择</li>
    </ul>
    <h4>组织参数</h4>
    <p>使用 <code>group</code>, <code>inline</code>, <code>tooltip</code> 参数可以美化设置面板。</p>
</div>
""",
        "summary": [
            "input.* 系列函数用于创建设置选项",
            "options 参数可以创建下拉列表",
            "group 参数可以将选项分组显示",
            "source 输入允许用户选择计算基于收盘价还是开盘价等"
        ],
        "pine_code": """//@version=5
indicator("Inputs Demo", overlay=true)

// --- 基础输入 ---
len = input.int(14, "Length", minval=1, tooltip="均线周期")
src = input.source(close, "Source")
is_show = input.bool(true, "Show Plot")

// --- 分组与下拉菜单 ---
grp_style = "Style Settings"
col = input.color(color.red, "Line Color", group=grp_style)
type = input.string("SMA", "MA Type", options=["SMA", "EMA"], group=grp_style)

// --- 逻辑使用 ---
float ma_val = na
if type == "SMA"
    ma_val := ta.sma(src, len)
else
    ma_val := ta.ema(src, len)

plot(is_show ? ma_val : na, color=col, linewidth=2)""",
        "python_code": """# Python (Streamlit 示例)
import streamlit as st
import pandas_ta as ta

# 对应 input.int
length = st.number_input("Length", min_value=1, value=14)
# 对应 input.string options
ma_type = st.selectbox("MA Type", ["SMA", "EMA"])
# 对应 input.bool
is_show = st.checkbox("Show Plot", value=True)

if ma_type == "SMA":
    ma = ta.sma(df['close'], length)
else:
    ma = ta.ema(df['close'], length)""",
        "quiz": [
            {
                "q": "如何创建一个带有下拉菜单的输入项？",
                "choices": [
                    {"text": "input.string(..., options=['A', 'B'])", "isCorrect": True},
                    {"text": "input.list(...)", "isCorrect": False},
                    {"text": "input.menu(...)", "isCorrect": False}
                ],
                "explain": "使用 input.string 并配合 options 参数列表即可生成下拉菜单。"
            },
            {
                "q": "想要限制输入的整数最小值为 1，应该用哪个参数？",
                "choices": [
                    {"text": "limit=1", "isCorrect": False},
                    {"text": "minval=1", "isCorrect": True},
                    {"text": "low=1", "isCorrect": False}
                ],
                "explain": "input.int 和 input.float 支持 minval 和 maxval 参数。"
            },
            {
                "q": "input.source 默认通常允许用户选择什么？",
                "choices": [
                    {"text": "开盘价、收盘价、最高价等序列", "isCorrect": True},
                    {"text": "本地文件", "isCorrect": False}
                ],
                "explain": "input.source 允许用户在 UI 上选择计算指标基于哪个价格序列（如 close, hl2 等）。"
            }
        ]
    },
    {
        "id": "l12_debugging",
        "title": "12. 调试技巧 (Debugging)",
        "subtitle": "Pine Logs 与 绘图调试",
        "concept": """
<h3>调试方法</h3>
<p>编写复杂脚本时，知道变量当前的值至关重要。Pine Script v5 提供了两种主要的调试方式。</p>

<h4>1. 可视化调试 (Visual Debugging)</h4>
<p>最传统的方法是将变量画在图上：</p>
<ul>
    <li><code>plot(variable)</code>: 画在副图观察数值变化。</li>
    <li><code>plotchar(bar_index, "Bar Index", "", location.top)</code>: 在数据窗口显示数值。</li>
    <li><code>label.new(...)</code>: 在特定 K 线上打印文本。</li>
</ul>

<h4>2. Pine Logs (日志调试) - 推荐</h4>
<p>v5 引入了 <code>log.*</code> 函数，可以在专门的 "Pine Logs" 面板中查看输出，不会干扰图表。</p>
<ul>
    <li><code>log.info(message)</code>: 打印一般信息。</li>
    <li><code>log.error(message)</code>: 打印错误（红色）。</li>
    <li><code>log.warning(message)</code>: 打印警告（橙色）。</li>
</ul>
<p><b>提示:</b> 字符串拼接可以使用 <code>str.tostring(value)</code> 或 <code>str.format()</code>。</p>
""",
        "summary": [
            "log.info() 是最现代的调试工具",
            "plotchar 可以把数值显示在 Data Window 而不干扰图表",
            "str.tostring(val) 用于将数字转为字符串"
        ],
        "pine_code": """//@version=5
indicator("Debugging Demo", overlay=true)

// 场景：调试一个交叉条件
fast = ta.sma(close, 10)
slow = ta.sma(close, 20)
cross = ta.crossover(fast, slow)

// 方法 1: 绘图调试
plot(fast, "Fast", color.green)
plotchar(cross, "Cross happened?", "X", location.top) // 会在发生处显示 X

// 方法 2: 日志调试
if cross
    // 只有发生交叉时才打印
    // str.format 类似 Python 的 f-string 或 .format
    msg = str.format("Gold Cross at bar {0}. Price: {1}", bar_index, close)
    log.info(msg)
else if barstate.islast
    log.info("Current Close: " + str.tostring(close))""",
        "python_code": """# Python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

if crossover:
    # f-string 调试
    logging.info(f"Gold Cross at index {i}. Price: {close}")
    print(f"DEBUG: Fast={fast_val}, Slow={slow_val}")""",
        "quiz": [
            {
                "q": "在 Pine Script 中如何将数字转换为字符串以进行日志打印？",
                "choices": [
                    {"text": "str(123)", "isCorrect": False},
                    {"text": "str.tostring(123)", "isCorrect": True},
                    {"text": "string(123)", "isCorrect": False}
                ],
                "explain": "Pine 使用 str.tostring() 进行类型转换。"
            },
            {
                "q": "log.error() 的输出通常显示在哪里？",
                "choices": [
                    {"text": "图表上", "isCorrect": False},
                    {"text": "Pine Editor 下方的 Pine Logs 面板", "isCorrect": True},
                    {"text": "浏览器控制台", "isCorrect": False}
                ],
                "explain": "需要在编辑器下方切换到 'Pine Logs' 标签页查看。"
            },
            {
                "q": "plotchar 的作用是？",
                "choices": [
                    {"text": "绘制字符标记，且其值会显示在数据窗口", "isCorrect": True},
                    {"text": "画线", "isCorrect": False}
                ],
                "explain": "plotchar 不仅能在图上打标，其 title 和 value 也会出现在 Data Window 中，适合调试布尔值或状态。"
            }
        ]
    },
    {
        "id": "l13_maps",
        "title": "13. 映射 (Maps)",
        "subtitle": "Key-Value 键值对集合",
        "concept": """
<h3>什么是 Map?</h3>
<p>Pine Script v5 引入了 <code>map</code> 类型，允许存储 <b>Key-Value (键-值)</b> 对。这在需要关联数据时非常有用（例如：统计每个价格出现的次数，或者存储不同 Symbol 的配置）。</p>
<div class="detail-box">
    <h4>核心操作</h4>
    <ul>
        <li><code>m = map.new<key_type, val_type>()</code>: 创建新 Map。</li>
        <li><code>map.put(m, key, value)</code>: 存入或更新数据。</li>
        <li><code>map.get(m, key)</code>: 读取数据。</li>
        <li><code>map.contains(m, key)</code>: 检查键是否存在。</li>
        <li><code>map.remove(m, key)</code>: 删除键。</li>
    </ul>
</div>
<p><b>注意:</b> Map 是引用类型，修改 Map 会影响所有引用它的变量。</p>
""",
        "summary": [
            "Map 用于存储键值对",
            "必须指定 Key 和 Value 的类型",
            "比 Array 查找速度更快（哈希表）"
        ],
        "pine_code": """//@version=5
indicator("Map Demo")

// 创建一个 Map: Key是价格(float), Value是次数(int)
// 用于统计价格分布 (Market Profile 简易版)
var price_map = map.new<float, int>()

// 将价格取整到最近的 10 美元
level = math.round(close / 10) * 10

// 更新计数
if barstate.isnew // 实时bar只计算一次
    int count = 0
    if map.contains(price_map, level)
        count := map.get(price_map, level)
    
    map.put(price_map, level, count + 1)

// 在最后一根K线打印统计结果
if barstate.islast
    keys = map.keys(price_map)
    size = array.size(keys)
    if size > 0
        log.info("Total price levels tracked: " + str.tostring(size))
        // 获取某个价格的出现次数
        demo_level = array.get(keys, 0)
        log.info("Level " + str.tostring(demo_level) + " count: " + str.tostring(map.get(price_map, demo_level)))""",
        "python_code": """# Python (Dictionary)
price_map = {}

level = round(close / 10) * 10

if level in price_map:
    price_map[level] += 1
else:
    price_map[level] = 1

print(f"Level {level} count: {price_map[level]}")""",
        "quiz": [
            {
                "q": "Python 的 Dictionary (字典) 对应 Pine Script 的什么结构？",
                "choices": [
                    {"text": "Array", "isCorrect": False},
                    {"text": "Map", "isCorrect": True},
                    {"text": "Matrix", "isCorrect": False}
                ],
                "explain": "Map 和 Dictionary 都是基于键值对 (Key-Value) 的哈希结构。"
            },
            {
                "q": "如何向 map m 中存入键值对 'A': 1？",
                "choices": [
                    {"text": "m['A'] = 1", "isCorrect": False},
                    {"text": "map.put(m, 'A', 1)", "isCorrect": True},
                    {"text": "map.add(m, 'A', 1)", "isCorrect": False}
                ],
                "explain": "Pine Script 使用 map.put() 方法。"
            },
            {
                "q": "如果 map.get(m, key) 中的 key 不存在，会返回什么？",
                "choices": [
                    {"text": "0", "isCorrect": False},
                    {"text": "na (空值)", "isCorrect": True},
                    {"text": "报错停止运行", "isCorrect": False}
                ],
                "explain": "返回 na，所以通常需要配合 map.contains() 或 nz() 使用。"
            }
        ]
    },
    {
        "id": "l14_libraries",
        "title": "14. 库 (Libraries)",
        "subtitle": "代码模块化与复用",
        "concept": """
<h3>创建与使用库</h3>
<p>当你的代码越来越长，或者你想在多个脚本中复用相同的逻辑时，应该使用 <b>Library</b>。</p>

<h4>1. 创建库</h4>
<p>脚本开头声明 <code>library("LibName")</code>，并使用 <code>export</code> 关键字导出函数。</p>
<pre><code>//@version=5
library("MyTools", overlay=true)

export my_sma(float src, int len) =>
    ta.sma(src, len)</code></pre>

<h4>2. 使用库</h4>
<p>在其他脚本中使用 <code>import</code> 导入。</p>
<pre><code>//@version=5
indicator("Test Lib")
import username/MyTools/1 as mt

plot(mt.my_sma(close, 14))</code></pre>
""",
        "summary": [
            "使用 library() 声明库脚本",
            "使用 export 关键字导出函数",
            "使用 import 导入库，格式为 用户名/库名/版本",
            "库函数不能绘图 (plot)，只能返回计算结果"
        ],
        "pine_code": """// --- 文件 1: 库 (MyMath) ---
//@version=5
// 库脚本不能直接画图
library("MyMath", overlay = true)

// 导出一个计算复利增长的函数
// 必须明确指定参数类型
export compound_interest(float principal, float rate, int periods) =>
    principal * math.pow(1 + rate, periods)

// --- 文件 2: 指标 (使用库) ---
//@version=5
indicator("Lib Usage")
// 假设这是你发布的库，版本为 1
// import YourName/MyMath/1 as mm

// res = mm.compound_interest(1000, 0.05, 10)
// plot(res)""",
        "python_code": """# Python (Modules)
# file: my_math.py
def compound_interest(principal, rate, periods):
    return principal * (1 + rate) ** periods

# file: main.py
import my_math as mm

res = mm.compound_interest(1000, 0.05, 10)
print(res)""",
        "quiz": [
            {
                "q": "库脚本以什么声明开头？",
                "choices": [
                    {"text": "indicator()", "isCorrect": False},
                    {"text": "library()", "isCorrect": True},
                    {"text": "strategy()", "isCorrect": False}
                ],
                "explain": "库必须使用 library() 声明。"
            },
            {
                "q": "库中的函数如果想被外部调用，必须加什么关键字？",
                "choices": [
                    {"text": "public", "isCorrect": False},
                    {"text": "export", "isCorrect": True},
                    {"text": "global", "isCorrect": False}
                ],
                "explain": "使用 export 导出函数，未导出的函数仅为库内部私有。"
            },
            {
                "q": "库函数可以直接 plot() 画图吗？",
                "choices": [
                    {"text": "可以", "isCorrect": False},
                    {"text": "不可以", "isCorrect": True}
                ],
                "explain": "库主要用于计算逻辑复用，不能直接包含 plot, strategy.entry 等绘图或交易指令。"
            }
        ]
    }
]

# 读取现有文件
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查是否已经存在这些 ID，避免重复添加
existing_ids = [l['id'] for l in data['lessons']]
for new_lesson in new_lessons:
    if new_lesson['id'] not in existing_ids:
        # 插入到 ref_ta_all 之前，或者直接追加
        # 找到 ref_ta_all 的索引
        ref_index = -1
        for i, l in enumerate(data['lessons']):
            if l['id'] == 'ref_ta_all':
                ref_index = i
                break
        
        if ref_index != -1:
            data['lessons'].insert(ref_index, new_lesson)
            # 插入后 ref_index 需要后移，但我们是一次性插入逻辑，或者每次都找
            # 这里简单起见，每次插入都会改变索引，所以上面的逻辑其实只对单个有效
            # 更好的方法是先收集所有要插入的，然后一次性插入到 ref_ta_all 之前
        else:
            data['lessons'].append(new_lesson)

# 重新排序逻辑：为了保证顺序 l11, l12, l13, l14 在 ref_ta_all 之前
# 我们先把 ref_ta_all 拿出来，追加新课程，再放回去
# 或者更简单：完全重建列表
final_lessons = []
ref_lesson = None
for l in data['lessons']:
    if l['id'] == 'ref_ta_all':
        ref_lesson = l
    elif l['id'] not in [nl['id'] for nl in new_lessons]: # 排除掉可能已存在的旧版
        final_lessons.append(l)

# 追加新的
final_lessons.extend(new_lessons)

# 最后放回 ref
if ref_lesson:
    final_lessons.append(ref_lesson)

data['lessons'] = final_lessons

# 写入文件
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Added lessons 11-14 successfully.")
