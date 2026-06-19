from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Salary, Employee, User
from schemas import SalaryCreate, SalaryUpdate, SalaryResponse, Result
from routers.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/salaries", tags=["工资管理"])


@router.get("", response_model=Result[List[SalaryResponse]])
async def get_salaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取工资记录列表"""
    logger.info("Fetching salary list")
    salaries = db.query(Salary).order_by(Salary.id.desc()).all()
    return Result(
        code=200,
        message="获取成功",
        data=[SalaryResponse.model_validate(sal) for sal in salaries]
    )


@router.get("/{salary_id}", response_model=Result[SalaryResponse])
async def get_salary(
    salary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单条工资记录"""
    salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if not salary:
        raise HTTPException(status_code=404, detail="工资记录不存在")
    return Result(code=200, message="获取成功", data=SalaryResponse.model_validate(salary))


@router.post("", response_model=Result[SalaryResponse], status_code=status.HTTP_201_CREATED)
async def create_salary(
    salary: SalaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """新增工资记录"""
    logger.info(f"Creating new salary record for employee: {salary.employee_id}")
    
    # 检查员工是否存在
    employee = db.query(Employee).filter(Employee.id == salary.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    # 计算实发工资
    total = salary.base_salary + salary.bonus - salary.deduction
    
    db_salary = Salary(**salary.model_dump(), total=total)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    
    logger.info(f"Salary record created successfully: {db_salary.id}")
    return Result(
        code=201,
        message="创建成功",
        data=SalaryResponse.model_validate(db_salary)
    )


@router.put("/{salary_id}", response_model=Result[SalaryResponse])
async def update_salary(
    salary_id: int,
    salary: SalaryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新工资记录"""
    logger.info(f"Updating salary record: {salary_id}")
    
    db_salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if not db_salary:
        raise HTTPException(status_code=404, detail="工资记录不存在")
    
    # 检查员工是否存在
    employee = db.query(Employee).filter(Employee.id == salary.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    # 更新字段
    for key, value in salary.model_dump().items():
        setattr(db_salary, key, value)
    
    # 重新计算实发工资
    db_salary.total = db_salary.base_salary + db_salary.bonus - db_salary.deduction
    
    db.commit()
    db.refresh(db_salary)
    
    logger.info(f"Salary record updated successfully: {salary_id}")
    return Result(code=200, message="更新成功", data=SalaryResponse.model_validate(db_salary))


@router.delete("/{salary_id}", response_model=Result[None])
async def delete_salary(
    salary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除工资记录"""
    logger.info(f"Deleting salary record: {salary_id}")
    
    db_salary = db.query(Salary).filter(Salary.id == salary_id).first()
    if not db_salary:
        raise HTTPException(status_code=404, detail="工资记录不存在")
    
    db.delete(db_salary)
    db.commit()
    
    logger.info(f"Salary record deleted successfully: {salary_id}")
    return Result(code=200, message="删除成功")
