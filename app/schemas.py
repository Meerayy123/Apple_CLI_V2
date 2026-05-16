from typing import Optional
from pydantic import BaseModel, Field


class CreateUserModel(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)
    balance: float = Field(...)


class UpdateBalanceModel(BaseModel):
    username: str = Field(..., min_length=1)
    new_balance: float = Field(...)


class CreatePortfolioModel(BaseModel):
    username: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class TradeOrderModel(BaseModel):
    portfolio_id: int
    ticker: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class SellOrderModel(TradeOrderModel):
    sale_price: float = Field(..., gt=0)
