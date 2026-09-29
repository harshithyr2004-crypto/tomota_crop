# -*- coding: utf-8 -*-
"""
Authentication & User Session API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    fullname: str
    username: str
    password: str
    farm_location: Optional[str] = "Karnataka, India"
    farm_size_acres: Optional[float] = 2.5

@router.post("/auth/login")
def login_user(req: LoginRequest):
    """Simple authenticated session handler."""
    if not req.username or not req.password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    # Allow demo farmer / agronomist login
    return {
        "success": True,
        "token": "token_demo_farm_guard_2026",
        "user": {
            "username": req.username,
            "role": "Agronomist / Farmer",
            "farm_location": "Karnataka, India"
        }
    }

@router.post("/auth/signup")
def register_user(req: SignUpRequest):
    """User registration endpoint."""
    if not req.username or not req.password or not req.fullname:
        raise HTTPException(status_code=400, detail="Full name, username, and password are required.")
    
    return {
        "success": True,
        "token": "token_registered_farm_guard_2026",
        "user": {
            "fullname": req.fullname,
            "username": req.username,
            "role": "Registered Tomato Farmer",
            "farm_location": req.farm_location,
            "farm_size_acres": req.farm_size_acres
        }
    }
