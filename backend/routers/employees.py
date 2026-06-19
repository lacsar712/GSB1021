from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Employee, User
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, Result
from routers.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/employees", tags=["员工管理"])


@router.get("", response_model=Result[List[EmployeeResponse]])
async def get_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取员工列表"""
    logger.info("Fetching employee list")
    employees = db.query(Employee).order_by(Employee.id.desc()).all()
    return Result(
        code=200,
        message="获取成功",
        data=[EmployeeResponse.model_validate(emp) for emp in employees]
    )


@router.get("/{employee_id}", response_model=Result[EmployeeResponse])
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个员工信息"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    return Result(code=200, message="获取成功", data=EmployeeResponse.model_validate(employee))


@router.post("", response_model=Result[EmployeeResponse], status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """新增员工"""
    logger.info(f"Creating new employee: {employee.name}")
    
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    logger.info(f"Employee created successfully: {db_employee.id}")
    return Result(
        code=201,
        message="创建成功",
        data=EmployeeResponse.model_validate(db_employee)
    )


@router.put("/{employee_id}", response_model=Result[EmployeeResponse])
async def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新员工信息"""
    logger.info(f"Updating employee: {employee_id}")
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    
    logger.info(f"Employee updated successfully: {employee_id}")
    return Result(code=200, message="更新成功", data=EmployeeResponse.model_validate(db_employee))


@router.delete("/{employee_id}", response_model=Result[None])
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除员工"""
    logger.info(f"Deleting employee: {employee_id}")
    
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    db.delete(db_employee)
    db.commit()
    
    logger.info(f"Employee deleted successfully: {employee_id}")
    return Result(code=200, message="删除成功")
