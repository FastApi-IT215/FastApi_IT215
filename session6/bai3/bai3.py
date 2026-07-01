from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Room Booking Management API",
    version="1.0"
)

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

class RoomCreate(BaseModel):
    code: str
    name: str
    capacity: int
    status: str

class BookingCreate(BaseModel):
    room_id: int
    class_name: str
    student_count: int
    date: str
    slot: str

@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate):

    for item in rooms:
        if item["code"] == room.code:
            raise HTTPException(
                status_code=400,
                detail="Code already exists"
            )

    if room.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    if room.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    if room.status not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    new_room = {
        "id": max([r["id"] for r in rooms]) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status
    }

    rooms.append(new_room)


    return {
        "message": "Create room successfully",
        "data": new_room
    }

@app.get("/rooms")
def get_rooms(
    keyword: str = None,
    status: str = None,
    min_capacity: int = None
):
    result = []

    for room in rooms:

        if keyword:

            if (
                keyword.lower() not in room["code"].lower()
                and keyword.lower() not in room["name"].lower()
            ):
                continue

        if status:

            if room["status"] != status:
                continue

        if min_capacity is not None:

            if room["capacity"] < min_capacity:
                continue

        result.append(room)

    return {
        "message": "Get rooms successfully",
        "data": result
    }

@app.get("/rooms/{room_id}")
def get_room(room_id: int):

    for room in rooms:

        if room["id"] == room_id:

            return {
                "message": "Found room",
                "data": room
            }


    raise HTTPException(
        status_code=404,
        detail="Room not found"
    )

@app.put("/rooms/{room_id}")
def update_room(
    room_id: int,
    room_update: RoomCreate
):
    for room in rooms:
        if room["id"] == room_id:

            for item in rooms:

                if item["code"] == room_update.code and item["id"] != room_id:

                    raise HTTPException(
                        status_code=400,
                        detail="Code already exists"
                    )

            if room_update.name.strip() == "":

                raise HTTPException(
                    status_code=400,
                    detail="Name cannot be empty"
                )



            if room_update.capacity <= 0:

                raise HTTPException(
                    status_code=400,
                    detail="Capacity must be greater than 0"
                )



            if room_update.status not in [
                "AVAILABLE",
                "IN_USE",
                "MAINTENANCE"
            ]:

                raise HTTPException(
                    status_code=400,
                    detail="Invalid status"
                )



            room["code"] = room_update.code
            room["name"] = room_update.name
            room["capacity"] = room_update.capacity
            room["status"] = room_update.status



            return {
                "message": "Update room successfully",
                "data": room
            }

    raise HTTPException(
        status_code=404,
        detail="Room not found"
    )


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for room in rooms:


        if room["id"] == room_id:


            rooms.remove(room)


            return {
                "message": "Delete room successfully",
                "data": room
            }



    raise HTTPException(
        status_code=404,
        detail="Room not found"
    )


@app.post("/room-bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):

    room = None
    for r in rooms:

        if r["id"] == booking.room_id:

            room = r



    if room is None:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )



    if room["status"] != "AVAILABLE":

        raise HTTPException(
            status_code=400,
            detail="Room is not available"
        )


    if booking.student_count <= 0:

        raise HTTPException(
            status_code=400,
            detail="Student count must be greater than 0"
        )


    if booking.student_count > room["capacity"]:

        raise HTTPException(
            status_code=400,
            detail="Student count exceeds room capacity"
        )


    if booking.slot not in [
        "MORNING",
        "AFTERNOON",
        "EVENING"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid slot"
        )



    for item in room_bookings:

        if (
            item["room_id"] == booking.room_id
            and item["date"] == booking.date
            and item["slot"] == booking.slot
        ):

            raise HTTPException(
                status_code=400,
                detail="Room already booked"
            )


    new_booking = {

        "id": max([b["id"] for b in room_bookings]) + 1,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking.date,
        "slot": booking.slot

    }


    room_bookings.append(new_booking)


    return {

        "message": "Create booking successfully",
        "data": new_booking

    }


@app.get("/room-bookings")
def get_bookings():

    return {

        "message": "Get bookings successfully",
        "data": room_bookings

    }