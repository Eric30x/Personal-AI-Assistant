# Personal AI Assistant

一个基于 **Python + DeepSeek API** 开发的个人 AI Agent 项目。

通过自然语言与 AI 交互，实现任务创建、查询、修改和删除，并探索 AI Agent 的工具调用、数据持久化、安全控制与错误恢复机制。

## 主要功能

- **AI 智能对话**：基于 DeepSeek API 实现自然语言交互。
- **任务管理**：支持创建、查询、修改和删除任务。
- **Function Calling**：AI 根据用户意图自动选择并调用工具。
- **Agent Loop**：支持多轮工具调用与结果反馈。
- **数据持久化**：使用 JSON 保存任务数据。
- **安全确认**：删除任务前需要用户确认。
- **错误恢复**：通过 Checkpoint 保存执行状态，支持基础中断恢复。
- **自动化测试**：使用 pytest 测试核心功能。

## 技术栈

- Python 3.11
- DeepSeek API
- OpenAI Python SDK
- Pydantic
- JSON
- pytest
- Git

## 项目结构

```text
personal_ai_assistant/
├── main.py              # 程序入口
├── agent.py             # Agent 核心逻辑
├── registry.py          # 工具注册与调用
├── task_tools.py        # 任务管理工具
├── time_tools.py        # 时间工具
├── storage.py           # 数据持久化
├── checkpoint.py        # 检查点与状态恢复
├── tests/               # 自动化测试
├── requirements.txt     # 项目依赖
└── README.md
```

## 快速开始

**1. 克隆项目**

```bash
git clone https://github.com/Eric30x/Personal-AI-Assistant.git
cd Personal-AI-Assistant
```

**2. 安装依赖**

```bash
python -m pip install -r requirements.txt
```

建议先创建并激活 Python 虚拟环境。

**3. 配置 API Key**

设置环境变量 `DEEPSEEK_API_KEY`，不要将真实密钥提交到 GitHub。

**4. 启动项目**

```bash
python main.py
```

## 运行测试

```bash
python -m pytest -v
```

## 项目说明

本项目是 AI Agent 系统学习过程中的实践项目，主要用于理解大模型工具调用、Agent 执行流程及基础工程化设计。

目前为本地命令行版本，尚未实现完整的生产级可靠性和多用户支持。

## 🔮 后续计划

- [ ] 使用 FastAPI 提供 HTTP 接口
- [ ] 引入数据库替代 JSON 存储
- [ ] 完善 Agent 状态管理与错误恢复
- [ ] 增加 Web 前端界面
- [ ] 探索 LangGraph 等 Agent 框架

## 📄 License
git add README.md
本项目用于个人学习与技术实践。