# Daily AI Report

全栈 AI 新闻聚合应用，自动从多个来源抓取、处理和展示 AI 领域的最新动态。

## 架构

- **后端**: FastAPI + PostgreSQL + APScheduler
- **前端**: React + TypeScript + Vite
- **部署**: Railway (后端) + Vercel (前端)

## 目录结构

```
daily-ai-report/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── fetchers/       # 数据抓取器
│   │   ├── models/         # 数据库模型
│   │   ├── processors/     # AI 处理器
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务服务
│   │   └── tasks/          # 定时任务
│   ├── alembic/            # 数据库迁移
│   └── requirements.txt
│
├── frontend/               # React 前端
│   ├── src/
│   │   ├── components/     # UI 组件
│   │   ├── hooks/          # React hooks
│   │   ├── pages/          # 页面组件
│   │   ├── services/       # API 服务
│   │   ├── styles/         # CSS 样式
│   │   └── types/          # TypeScript 类型
│   └── package.json
│
├── fetchers/               # 原始抓取器 (已迁移)
├── processors/             # 原始处理器 (已迁移)
└── renderers/              # 原始渲染器 (已弃用)
```

## 快速开始

### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的配置

# 运行数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## API 端点

| Method | Endpoint | 描述 |
|--------|----------|------|
| GET | `/api/v1/modules/` | 首页数据（所有模块预览） |
| GET | `/api/v1/modules/{module}` | 模块详情页数据 |
| GET | `/api/v1/items/{item_id}` | 单条内容详情 |
| GET | `/api/v1/items/?q=&module=` | 搜索内容 |
| POST | `/api/v1/admin/fetch/trigger` | 触发数据抓取 |
| GET | `/api/v1/admin/fetch/status/{id}` | 抓取状态 |
| GET | `/health` | 健康检查 |

## 数据源

- **YouTube**: Lex Fridman, Two Minute Papers, AI Explained, Andrej Karpathy
- **Substack**: The Batch, Import AI, One Useful Thing, Interconnects 等
- **Twitter/X**: Sam Altman, Andrej Karpathy, OpenAI, Anthropic 等
- **Products**: ProductHunt, GitHub Trending
- **Papers**: HuggingFace Daily Papers, arXiv
- **Business**: TechCrunch, VentureBeat, The Verge, Wired

## 环境变量

### 后端

```
DATABASE_URL=postgresql://user:password@localhost:5432/daily_ai_report
DEEPSEEK_API_KEY=your_deepseek_api_key
RAPIDAPI_KEY=your_rapidapi_key
ADMIN_API_KEY=your_admin_api_key
FRONTEND_URL=http://localhost:5173
```

### 前端

```
VITE_API_URL=http://localhost:8000
```

## 部署

### Railway (后端)

1. 连接 GitHub 仓库
2. 设置 Root Directory 为 `backend`
3. 添加 PostgreSQL 插件
4. 配置环境变量

### Vercel (前端)

1. 连接 GitHub 仓库
2. 设置 Root Directory 为 `frontend`
3. 配置 `VITE_API_URL` 环境变量

## License

MIT
