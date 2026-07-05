from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

app = FastAPI(title="IT Asset Management API")

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

class AssetRequestDTO(BaseModel):
    serial_number: str
    model: str
    stock_available: int
    status: str

class AllocationRequestDTO(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int
    start_date: str
    duration_months: int

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

@app.post("/assets", tags=["Assets"], status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetRequestDTO, request: Request):
    if len(asset.model) < 2 or len(asset.model) > 255:
        raise HTTPException(status_code=400, detail="Model length must be between 2 and 255 characters")
        
    if asset.stock_available < 0:
        raise HTTPException(status_code=400, detail="Stock available must be greater than or equal to 0")
        
    if asset.status not in ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]:
        raise HTTPException(status_code=400, detail="Status must be READY, ALLOCATED, REPAIRING, or SCRAPPED")

    for a in assets:
        if a["serial_number"].lower() == asset.serial_number.lower():
            raise HTTPException(status_code=400, detail="Serial number must be unique")

    next_id = 1
    for a in assets:
        if a["id"] >= next_id:
            next_id = a["id"] + 1

    new_asset = {
        "id": next_id,
        "serial_number": asset.serial_number,
        "model": asset.model,
        "stock_available": asset.stock_available,
        "status": asset.status
    }
    assets.append(new_asset)
    return success_response(201, "Asset created successfully", new_asset, request)

@app.get("/assets", tags=["Assets"])
def get_assets(
    request: Request,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_stock: Optional[int] = None
):
    filtered_assets = []
    
    for a in assets:
        match = True
        
        if keyword is not None:
            if (keyword.lower() not in a["serial_number"].lower()) and (keyword.lower() not in a["model"].lower()):
                match = False
                
        if status is not None:
            if a["status"] != status:
                match = False
                
        if min_stock is not None:
            if a["stock_available"] < min_stock:
                match = False
                
        if match == True:
            filtered_assets.append(a)
            
    return success_response(200, "Get assets successfully", filtered_assets, request)

@app.get("/assets/{asset_id}", tags=["Assets"])
def get_asset_by_id(asset_id: int, request: Request):
    for a in assets:
        if a["id"] == asset_id:
            return success_response(200, "Get asset details successfully", a, request)
            
    raise HTTPException(status_code=404, detail="Asset not found")

@app.put("/assets/{asset_id}", tags=["Assets"])
def update_asset(asset_id: int, asset_data: AssetRequestDTO, request: Request):
    target_asset = None
    for a in assets:
        if a["id"] == asset_id:
            target_asset = a
            break
            
    if target_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    if len(asset_data.model) < 2 or len(asset_data.model) > 255:
        raise HTTPException(status_code=400, detail="Model length must be between 2 and 255 characters")
    if asset_data.stock_available < 0:
        raise HTTPException(status_code=400, detail="Stock available must be greater than or equal to 0")
    if asset_data.status not in ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]:
        raise HTTPException(status_code=400, detail="Status must be READY, ALLOCATED, REPAIRING, or SCRAPPED")

    for a in assets:
        if a["id"] != asset_id and a["serial_number"].lower() == asset_data.serial_number.lower():
            raise HTTPException(status_code=400, detail="Serial number must be unique")

    target_asset["serial_number"] = asset_data.serial_number
    target_asset["model"] = asset_data.model
    target_asset["stock_available"] = asset_data.stock_available
    target_asset["status"] = asset_data.status

    return success_response(200, "Asset updated successfully", target_asset, request)

@app.delete("/assets/{asset_id}", tags=["Assets"])
def delete_asset(asset_id: int, request: Request):
    for i in range(len(assets)):
        if assets[i]["id"] == asset_id:
            deleted_asset = assets.pop(i)
            return success_response(200, "Asset deleted successfully", deleted_asset, request)
            
    raise HTTPException(status_code=404, detail="Asset not found")

@app.post("/allocations", tags=["Allocations"], status_code=status.HTTP_201_CREATED)
def create_allocation(allocation: AllocationRequestDTO, request: Request):
    if allocation.allocated_quantity <= 0:
        raise HTTPException(status_code=400, detail="Allocated quantity must be greater than 0")
        
    if allocation.duration_months < 1 or allocation.duration_months > 12:
        raise HTTPException(status_code=400, detail="Duration months must be between 1 and 12")

    email = allocation.employee_email
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format (missing @ or .)")
        
    parts = email.split("@")
    if len(parts) != 2 or parts[0] == "" or parts[1] == "":
        raise HTTPException(status_code=400, detail="Invalid email format")

    target_asset = None
    for a in assets:
        if a["id"] == allocation.asset_id:
            target_asset = a
            break

    if target_asset is None:
        raise HTTPException(status_code=400, detail="Asset not found")

    if target_asset["status"] != "READY":
        raise HTTPException(status_code=400, detail="Asset is not READY for allocation")

    if allocation.allocated_quantity > target_asset["stock_available"]:
        raise HTTPException(status_code=400, detail="Allocated quantity exceeds available stock")

    target_asset["stock_available"] = target_asset["stock_available"] - allocation.allocated_quantity

    next_id = 1
    for alt in allocations:
        if alt["id"] >= next_id:
            next_id = alt["id"] + 1

    new_allocation = {
        "id": next_id,
        "asset_id": allocation.asset_id,
        "employee_email": allocation.employee_email,
        "allocated_quantity": allocation.allocated_quantity,
        "start_date": allocation.start_date,
        "duration_months": allocation.duration_months
    }
    allocations.append(new_allocation)
    return success_response(201, "Allocation registered successfully", new_allocation, request)

@app.get("/allocations", tags=["Allocations"])
def get_allocations(request: Request):
    return success_response(200, "Get allocations successfully", allocations, request)