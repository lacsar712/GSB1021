from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

from database import init_db
from routers import auth, employees, salaries

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="工资管理系统API",
    description="基于FastAPI的工资管理系统后端服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """处理全局异常"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("Application starting up...")
    logger.info("Database tables will be created by seed.py")


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}


# 注册路由
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(salaries.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
