from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    """统一响应格式"""
    code: int = Field(default=200, description="状态码")
    message: str = Field(default="success", description="消息")
    data: Optional[T] = None


# ========== 用户相关 ==========
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


# ========== 员工相关 ==========
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    department: str = Field(..., min_length=1, max_length=100, description="部门")
    position: str = Field(..., min_length=1, max_length=100, description="职位")
    phone: Optional[str] = Field(None, max_length=20, description="电话")
    email: Optional[str] = Field(None, description="邮箱")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 工资相关 ==========
class SalaryBase(BaseModel):
    employee_id: int = Field(..., description="员工ID")
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="月份 (YYYY-MM)")
    base_salary: float = Field(..., ge=0, description="基本工资")
    bonus: float = Field(default=0.0, ge=0, description="奖金")
    deduction: float = Field(default=0.0, ge=0, description="扣款")


class SalaryCreate(SalaryBase):
    pass


class SalaryUpdate(SalaryBase):
    pass


class SalaryResponse(SalaryBase):
    id: int
    total: float
    created_at: datetime
    employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True
