from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product_schema import ProductRead


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, default=1)


class CartItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantity: int
    added_at: datetime
    product: ProductRead