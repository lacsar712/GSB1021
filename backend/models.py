from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Employee(Base):
    """员工模型"""
    __tablename__ = "employees"
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="姓名")
    department = Column(String(100), nullable=False, comment="部门")
    position = Column(String(100), nullable=False, comment="职位")
    phone = Column(String(20), comment="电话")
    email = Column(String(100), comment="邮箱")
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联工资记录
    salaries = relationship("Salary", back_populates="employee", cascade="all, delete-orphan")


class Salary(Base):
    """工资记录模型"""
    __tablename__ = "salaries"
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(String(7), nullable=False, comment="月份 (YYYY-MM)")
    base_salary = Column(Float, nullable=False, default=0.0, comment="基本工资")
    bonus = Column(Float, default=0.0, comment="奖金")
    deduction = Column(Float, default=0.0, comment="扣款")
    total = Column(Float, nullable=False, comment="实发工资")
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联员工
    employee = relationship("Employee", back_populates="salaries")
