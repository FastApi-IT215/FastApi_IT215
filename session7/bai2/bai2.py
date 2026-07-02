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
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]


VALID_STATUS = ["PENDING", "SHIPPING", "DELIVERED"]


class StatusUpdate(BaseModel):
    status: str


class OrderResponseDTO(BaseModel):
    id: int
    customer_name: str
    status: str


@app.get("/orders/{order_id}", tags=["Orders"], response_model=APIResponse)
def get_order(order_id: int, request: Request):
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
        status_code=404,
        detail="Order not found"
    )


@app.put(
    "/orders/{order_id}/status",
    tags=["Orders"],
    response_model=APIResponse
)
def update_order_status(order_id: int, data: StatusUpdate, request: Request):

    if data.status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái không hợp lệ"
        )

    for order in orders_db:
        if order["id"] == order_id:
            order["status"] = data.status
            order_dto = OrderResponseDTO(**order)
            return success_response(
                200,
                "Cập nhật trạng thái thành công",
                order_dto,
                request
            )

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )