from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class UserProfileCreate(BaseModel):
    full_name: str
    phone: str
    address: str | None = None


users = [
    {
        "id": 1,
        "username": "nguyenvanan",
        "email": "an@gmail.com"
    },
    {
        "id": 2,
        "username": "tranthibinh",
        "email": "binh@gmail.com"
    }
]

profiles = [
    {
        "id": 10,
        "full_name": "Nguyễn Văn An",
        "phone": "0901000001",
        "address": "Hà Nội",
        "user_id": 1
    }
]


@app.get("/users")
def get_users():
    return users


@app.get("/profiles")
def get_profiles():
    return profiles


@app.post(
    "/users/{user_id}/profile",
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    user_id: int,
    profile_data: UserProfileCreate
):
    existing_user = next(
        (
            user
            for user in users
            if user["id"] == user_id
        ),
        None
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="Người dùng không tồn tại"
        )

    existing_profile = next(
        (
            profile
            for profile in profiles
            if profile["user_id"] == user_id
        ),
        None
    )

    if existing_profile:
        raise HTTPException(
            status_code=409,
            detail="Người dùng đã có hồ sơ"
        )

    duplicated_phone = next(
        (
            profile
            for profile in profiles
            if profile["phone"] == profile_data.phone
        ),
        None
    )

    if duplicated_phone:
        raise HTTPException(
            status_code=409,
            detail="Số điện thoại đã được sử dụng"
        )

    new_profile = {
        "id": len(profiles) + 1,
        "full_name": profile_data.full_name,
        "phone": profile_data.phone,
        "address": profile_data.address,
        "user_id": user_id
    }

    profiles.append(new_profile)
    return new_profile