from fastapi import FastAPI, HTTPException, Request, status, Query
from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime, timezone

app = FastAPI(title="Logistics Management API")

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

class CarrierCreateDTO(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: str = Field(..., pattern="^(ACTIVE|INACTIVE|SUSPENDED)$")

class CarrierUpdateDTO(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: str = Field(..., pattern="^(ACTIVE|INACTIVE|SUSPENDED)$")

class ShipmentCreateDTO(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(..., gt=0)
    dispatch_date: str
    shift: str = Field(..., pattern="^(MORNING|AFTERNOON|NIGHT)$")

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

@app.post("/carriers", tags=["Carriers"], status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_carrier(carrier: CarrierCreateDTO, request: Request):
    for c in carriers:
        if c["code"].upper() == carrier.code.upper():
            raise HTTPException(status_code=400, detail="Carrier code must be unique")
    
    new_id = max([c["id"] for c in carriers], default=0) + 1
    new_carrier = {
        "id": new_id,
        "code": carrier.code,
        "name": carrier.name,
        "max_weight_capacity": carrier.max_weight_capacity,
        "status": carrier.status
    }
    carriers.append(new_carrier)
    return success_response(201, "Carrier created successfully", new_carrier, request)

@app.get("/carriers", tags=["Carriers"], response_model=APIResponse)
def get_carriers(
    request: Request,
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_weight: Optional[int] = Query(None)
):
    result = carriers
    if keyword:
        k = keyword.lower()
        result = [c for c in result if k in c["code"].lower() or k in c["name"].lower()]
    if status:
        result = [c for c in result if c["status"] == status]
    if min_weight is not None:
        result = [c for c in result if c["max_weight_capacity"] >= min_weight]
    
    return success_response(200, "Get carriers successfully", result, request)

@app.get("/carriers/{carrier_id}", tags=["Carriers"], response_model=APIResponse)
def get_carrier(carrier_id: int, request: Request):
    for c in carriers:
        if c["id"] == carrier_id:
            return success_response(200, "Get carrier details successfully", c, request)
    raise HTTPException(status_code=404, detail="Carrier not found")

@app.put("/carriers/{carrier_id}", tags=["Carriers"], response_model=APIResponse)
def update_carrier(carrier_id: int, carrier_data: CarrierUpdateDTO, request: Request):
    target_carrier = None
    for c in carriers:
        if c["id"] == carrier_id:
            target_carrier = c
            break
            
    if not target_carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
        
    for c in carriers:
        if c["id"] != carrier_id and c["code"].upper() == carrier_data.code.upper():
            raise HTTPException(status_code=400, detail="Carrier code must be unique")
            
    target_carrier["code"] = carrier_data.code
    target_carrier["name"] = carrier_data.name
    target_carrier["max_weight_capacity"] = carrier_data.max_weight_capacity
    target_carrier["status"] = carrier_data.status
    
    return success_response(200, "Carrier updated successfully", target_carrier, request)

@app.delete("/carriers/{carrier_id}", tags=["Carriers"], response_model=APIResponse)
def delete_carrier(carrier_id: int, request: Request):
    for i, c in enumerate(carriers):
        if c["id"] == carrier_id:
            deleted = carriers.pop(i)
            return success_response(200, "Carrier deleted successfully", deleted, request)
    raise HTTPException(status_code=404, detail="Carrier not found")

@app.post("/shipments", tags=["Shipments"], status_code=status.HTTP_201_CREATED, response_model=APIResponse)
def create_shipment(shipment: ShipmentCreateDTO, request: Request):
    target_carrier = None
    for c in carriers:
        if c["id"] == shipment.carrier_id:
            target_carrier = c
            break
            
    if not target_carrier:
        raise HTTPException(status_code=400, detail="Carrier does not exist")
        
    if target_carrier["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Carrier is not ACTIVE")
        
    if shipment.total_weight > target_carrier["max_weight_capacity"]:
        raise HTTPException(status_code=400, detail="Shipment weight exceeds carrier max capacity")
        
    for s in shipments:
        if (s["carrier_id"] == shipment.carrier_id and 
            s["dispatch_date"] == shipment.dispatch_date and 
            s["shift"] == shipment.shift):
            raise HTTPException(status_code=400, detail="Carrier has already been scheduled for this date and shift")
            
    new_id = len(shipment) + 1
    new_shipment = {
        "id": new_id,
        "carrier_id": shipment.carrier_id,
        "order_reference": shipment.order_reference,
        "total_weight": shipment.total_weight,
        "dispatch_date": shipment.dispatch_date,
        "shift": shipment.shift
    }
    shipments.append(new_shipment)
    return success_response(201, "Shipment created successfully", new_shipment, request)

@app.get("/shipments", tags=["Shipments"], response_model=APIResponse)
def get_shipments(request: Request):
    return success_response(200, "Get shipments successfully", shipments, request)

