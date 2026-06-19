import time
import logging
from sqlalchemy.orm import Session
from database import engine, SessionLocal, init_db
from models import User, Employee, Salary
from routers.auth import get_password_hash

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def wait_for_db(max_retries=30):
    """等待数据库准备就绪"""
    for i in range(max_retries):
        try:
            engine.connect()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.warning(f"Database not ready, retrying... ({i+1}/{max_retries})")
            time.sleep(2)
    return False


def seed_data():
    """初始化数据库数据"""
    db: Session = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_user = db.query(User).first()
        if existing_user:
            logger.info("Database already seeded, skipping...")
            return
        
        logger.info("Starting database seeding...")
        
        # 1. 创建默认管理员账号
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("123456")
        )
        db.add(admin_user)
        logger.info("Admin user created: admin/123456")
        
        # 2. 创建示例员工
        employees_data = [
            {"name": "张三", "department": "技术部", "position": "高级工程师", "phone": "13800138001", "email": "zhangsan@example.com"},
            {"name": "李四", "department": "产品部", "position": "产品经理", "phone": "13800138002", "email": "lisi@example.com"},
            {"name": "王五", "department": "运营部", "position": "运营专员", "phone": "13800138003", "email": "wangwu@example.com"},
            {"name": "赵六", "department": "技术部", "position": "前端工程师", "phone": "13800138004", "email": "zhaoliu@example.com"},
            {"name": "钱七", "department": "人力资源部", "position": "HR主管", "phone": "13800138005", "email": "qianqi@example.com"},
        ]
        
        employees = []
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            db.add(employee)
            employees.append(employee)
        
        db.flush()  # 获取员工ID
        logger.info(f"Created {len(employees)} sample employees")
        
        # 3. 创建示例工资记录
        salaries_data = [
            {"employee_id": employees[0].id, "month": "2026-01", "base_salary": 15000, "bonus": 3000, "deduction": 500},
            {"employee_id": employees[1].id, "month": "2026-01", "base_salary": 12000, "bonus": 2000, "deduction": 300},
            {"employee_id": employees[2].id, "month": "2026-01", "base_salary": 8000, "bonus": 1000, "deduction": 200},
            {"employee_id": employees[3].id, "month": "2026-01", "base_salary": 10000, "bonus": 1500, "deduction": 250},
            {"employee_id": employees[4].id, "month": "2026-01", "base_salary": 11000, "bonus": 2500, "deduction": 350},
        ]
        
        for sal_data in salaries_data:
            total = sal_data["base_salary"] + sal_data["bonus"] - sal_data["deduction"]
            salary = Salary(**sal_data, total=total)
            db.add(salary)
        
        logger.info(f"Created {len(salaries_data)} sample salary records")
        
        # 提交所有数据
        db.commit()
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during database seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Waiting for database to be ready...")
    if not wait_for_db():
        logger.error("Database connection failed after max retries")
        exit(1)
    
    logger.info("Initializing database tables...")
    init_db()
    
    logger.info("Seeding initial data...")
    seed_data()
    
    logger.info("Database initialization complete!")
