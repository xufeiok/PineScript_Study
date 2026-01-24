# Pine Script 学习系统（对照 Python）

面向量化交易从业者的 Pine Script 学习平台，支持网页端与移动端访问，按现代学习法设计：主动回忆、间隔重复、示例驱动、对照学习、即时反馈、渐进难度。

## 目标与原则
- 针对真实量化场景：从指标到策略回测的完整链条
- 与 Python 对照：每个概念均有 Pine 与 Python 的并列示例
- 高交互性：测验、代码对照、进度可视化、复习提醒
- 轻依赖：前端静态页面可离线使用，后端可选开启进度保存

## 项目结构
```
e:\Quant\PineScript_study
├─ web                # 前端（静态站点）
│  ├─ index.html
│  ├─ styles.css
│  ├─ app.js
│  └─ data\lessons.json
└─ server             # 后端（可选）
   ├─ main.py         # FastAPI 提供课程与进度接口
   └─ requirements.txt
```

## 快速运行
### 仅前端（推荐，零依赖）
- 使用任意静态服务器（或直接双击 index.html 打开）
- 或在 web 目录下启动内置服务器：
  ```bash
  cd web
  python -m http.server 8000
  # 访问 http://localhost:8000
  ```

### 后端（可选）
- 安装依赖：
  ```bash
  pip install -r server/requirements.txt
  ```
- 启动服务：
  ```bash
  uvicorn server.main:app --reload --port 8001
  # 访问：
  #  - 课程数据：GET http://localhost:8001/lessons
  #  - 进度读取：GET http://localhost:8001/progress?user=default
  #  - 进度保存：POST http://localhost:8001/progress
  ```

前端默认从 `web/data/lessons.json` 加载课程；如需改为后端，请在 `app.js` 中将 fetch 路径替换为后端接口。也可在前端保留 localStorage 作为离线进度存储，后端用于汇总。

## 教学设计（方法论）
- 主动回忆：每一课配套测验题，提交后立即反馈并解释
- 间隔重复：错误题自动加入复习队列（简化版），后续可扩展为计划提醒
- 对照学习：并排展示 Pine Script 与 Python 示例，概念一一对应
- 渐进难度：从变量序列 → 绘图 → 条件交叉 → 函数 → 策略脚手架
- 总结笔记：每课含关键要点列表，帮助迁移与复盘

## 课程内容（首批）
1. 变量与序列（series）— Pine 的时间序列与 Python 的向量列
2. 绘图与颜色 — plot/plotshape 与可视化控制
3. 条件与交叉 — ta.crossover/crossunder 对照 Python shift 检测
4. 函数定义 — 箭头语法与返回，Python def 对比
5. 策略脚手架 — strategy 声明与 entry/close，对照常见回测框架

## 后续扩展计划
- 更丰富的课程库：指标（RSI/MACD/布林）、多周期、多品种、风控与绩效分析
- 高级交互：可编辑代码区、实时运行模拟、图形化回测报告（前端）
- 完整复习系统：SM-2 间隔重复算法、每日练习卡片、错题集
- 用户系统与数据持久化：登录、云端同步、数据加密与备份
- 国际化与主题：中英双语、更多主题皮肤与可访问性支持

## 贡献与规范
- 代码注释统一中文，简洁描述功能、输入/输出与边界
- 避免引入不必要的依赖；优先复用现有模块与模式
- 重要变更请在 PR 中说明动机与设计权衡，附最小复现或单元测试

—— 欢迎一起把 Pine Script 学习体验做到极致！

