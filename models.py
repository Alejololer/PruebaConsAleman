from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    stock: int = Field(ge=0)

    @field_validator('stock')
    @classmethod
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v
