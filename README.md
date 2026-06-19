# 工资管理系统

一个基于 Vue3 + Element Plus + FastAPI + MySQL 的现代化工资管理系统，支持员工信息管理和工资记录管理。

## 🛠 技术栈

### 前端
- **框架**: Vue 3.4
- **UI组件库**: Element Plus 2.5
- **构建工具**: Vite 5.0
- **HTTP客户端**: Axios 1.6
- **路由**: Vue Router 4.2

### 后端
- **框架**: FastAPI 0.109
- **ORM**: SQLAlchemy 2.0
- **数据库驱动**: PyMySQL 1.1
- **认证**: JWT (python-jose)
- **密码加密**: Passlib (bcrypt)

### 数据库
- **数据库**: MySQL 8.0
- **字符集**: utf8mb4 (支持中文)

### 部署
- **容器化**: Docker + Docker Compose
- **Web服务器**: Nginx (Alpine)

---

## 🚀 启动指南

### 前置要求
- Docker Desktop 已安装并运行
- 确保端口 3000、8000、3306 未被占用

### 一键启动

1. **克隆或进入项目目录**
   ```bash
   cd /Users/yuwangi/Documents/www/test/longmao/1021
   ```

2. **启动所有服务**
   ```bash
   docker compose up --build
   ```

3. **等待容器启动完成**
   - 首次启动需要下载镜像和安装依赖，大约需要 3-5 分钟
   - 看到以下日志表示启动成功：
     ```
     salary_backend  | Database initialization complete!
     salary_backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
     salary_frontend | ... (nginx启动日志)
     ```

4. **访问系统**
   - 浏览器打开: http://localhost:3000

---

## 🔗 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:3000 | Vue3 + Element Plus |
| 后端API | http://localhost:8000 | FastAPI |
| API文档 | http://localhost:8000/docs | Swagger UI |
| 数据库 | localhost:3306 | MySQL 8.0 |

---

## 🧪 测试账号

- **管理员账号**: `admin`
- **管理员密码**: `123456`

> 💡 默认账号信息也会显示在登录页面下方

---

## 📦 项目结构

```
.
├── backend/                 # FastAPI后端
│   ├── routers/            # API路由模块
│   │   ├── auth.py        # 认证路由
│   │   ├── employees.py   # 员工管理路由
│   │   └── salaries.py    # 工资管理路由
│   ├── main.py            # 应用入口
│   ├── models.py          # 数据模型
│   ├── schemas.py         # Pydantic模型
│   ├── database.py        # 数据库配置
│   ├── seed.py            # 数据初始化
│   ├── requirements.txt   # Python依赖
│   └── Dockerfile         # 后端镜像
│
├── frontend/               # Vue3前端
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── utils/         # 工具类
│   │   ├── router.js      # 路由配置
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 应用入口
│   ├── index.html
│   ├── package.json
│   ├── nginx.conf         # Nginx配置
│   └── Dockerfile         # 前端镜像
│
├── docker-compose.yml      # Docker编排文件
└── README.md              # 项目文档
```

---

## 🐳 Docker 镜像源配置

本项目已配置国内镜像加速，提升构建速度：

### 1. Docker 镜像
- 使用官方 Docker Hub 镜像（稳定可用）
- MySQL: `mysql:8.0`
- Node.js: `node:20-alpine`
- Nginx: `nginx:alpine`
- Python: `python:3.11-slim`

### 2. npm 依赖源
- 前端构建已配置淘宝镜像源
- 镜像地址: `https://registry.npmmirror.com`

### 3. pip 依赖源
- 后端构建已配置阿里云镜像源
- 镜像地址: `https://mirrors.aliyun.com/pypi/simple/`

### 构建优化
- 前端使用 `npm ci` 快速安装依赖（基于 package-lock.json）
- 后端使用分层缓存机制，依赖不变时跳过下载
- 前端使用多阶段构建，减小最终镜像体积

---

## 💡 功能特性

### 登录认证
- 现代化左右布局设计
- JWT Token 认证
- 密码加密存储 (bcrypt)
- 自动保持登录状态

### 员工管理
- 员工信息 CRUD 操作
- 字段：姓名、部门、职位、电话、邮箱
- 实时数据更新
- 自定义删除确认对话框

### 工资管理
- 工资记录 CRUD 操作
- 字段：员工、月份、基本工资、奖金、扣款
- 自动计算实发工资
- 关联员工信息显示

### UI/UX 特性
- 渐变背景和现代化配色
- 平滑过渡动画
- 响应式布局
- Element Plus 组件库
- Toast 消息提示
- 加载状态显示
- Hover 交互效果

---

## 🔧 常见问题

### Q: Docker 容器启动失败？
A: 
1. 检查 Docker Desktop 是否正常运行
2. 检查端口是否被占用：`lsof -i :3000,8000,3306`
3. 清理残留容器和镜像：`docker compose down -v`

### Q: 前端无法连接后端？
A: 
1. 确保所有容器都已启动：`docker compose ps`
2. 检查后端日志：`docker compose logs backend`
3. 确认网络配置正确（服务名通信）

### Q: 数据库初始化失败？
A: 
1. 检查数据库是否健康：`docker compose logs db`
2. 等待数据库完全启动（健康检查通过）
3. 重新启动：`docker compose restart backend`

### Q: 中文显示乱码？
A: 
- 本项目已配置 utf8mb4 字符集，正常情况下不会出现乱码
- 如遇问题，检查数据库字符集配置

---

## 🛑 停止服务

```bash
# 停止所有容器
docker compose down

# 停止并删除数据卷（会清空数据库）
docker compose down -v
```

---

## 📄 开源协议

MIT License

---

## 👨‍💻 开发者

基于 Prompt2Repo 核心开发规范构建
