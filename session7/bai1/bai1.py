from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(title="Manager Orders")


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str


def success_response(statusCode: int, message: str, data: Any, request: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path
    )


orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,
        "supplier_id": "SUP_DELL_01"
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,
        "supplier_id": "SUP_LOGI_02"
    }
]


class OrderResponseDTO(BaseModel):
    id: int
    customer_name: str
    total_amount: float


@app.get(
    "/orders/{order_id}",
    tags=["Orders"],
    response_model=APIResponse,
    status_code=status.HTTP_200_OK
)
def get_order_detail(order_id: int, request: Request):
    for order in orders_db:
        if order["id"] == order_id:
            order_dto = OrderResponseDTO(**order)
            return success_response(
                200,
                "Lấy thông tin đơn hàng thành công",
                order_dto,
                request
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found"
    )