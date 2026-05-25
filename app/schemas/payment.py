from pydantic import BaseModel, Field


class Payment(BaseModel):
    amount: float = Field(..., ge=200,
                          description="Amount must be greater or equal to 200")
    description: str = Field(..., description="Description of the payment")
    callback_url: str = Field(...,
                              description="URL to which the payment callback will be sent")
    unit_price: float = Field(..., ge=200,
                              description="Unit price must be greater or equal to 200")
    quantity: int = Field(..., ge=1,
                          description="Quantity must be greater or equal to 1")
    name: str = Field(..., description="Name of the item being purchased")
    cancel_page_url: str = Field(
        None, description="URL to which the user will be redirected if they cancel the payment")
    success_page_url: str = Field(
        None, description="URL to which the user will be redirected if the payment is successful")
