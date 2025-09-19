from fastapi import APIRouter, Form, status, HTTPException
from typing import Annotated
from pydantic import EmailStr
from db import users_collection
import bcrypt
import jwt
import os
from datetime import timezone, datetime, timedelta

# create users router
users_router = APIRouter()


# Define endpoints
@users_router.post("/users/register")
def register_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
    username: Annotated[str, Form()],
):
    # Ensure user does not exist
    user_count = users_collection.count_documents(filter={"email": email})
    if user_count > 0:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exist!")
    # Harsh user password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # Save user into database
    users_collection.insert_one(
        {"username": username, "email": email, "password": hashed_password.decode()}
    )
    # Return response
    return {"Message": "User registered successfully!"}


@users_router.post("/users/login")
def login_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
):
    # Ensure user exist
    user = users_collection.find_one(filter={"email": email})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist!")
    # Compare their password
    hashed_password_in_db = user["password"]
    correct_password = bcrypt.checkpw(password.encode(), hashed_password_in_db.encode())
    if not correct_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    # Generate an access token for them
    encoded_jwt = jwt.encode(
        {
            "id": str(user["_id"]),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
        },
        os.getenv("JWT_SECRET_KEY"),
        "HS256",
    )
    # Return response
    return {"Message": "User Logged in successfully!", "access_token": encoded_jwt}
