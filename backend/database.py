from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# 数据库连接配置 - 使用服务名 'db' 而非 localhost
DATABASE_URL = "mysql+pymysql://root:root@db:3306/salary_management?charset=utf8mb4"

# 创建数据库引擎，配置连接池
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 自动检测连接是否失效
    pool_recycle=3600,   # 每小时回收连接
    echo=False,          # 不输出SQL语句
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
    }
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话的依赖注入函数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
