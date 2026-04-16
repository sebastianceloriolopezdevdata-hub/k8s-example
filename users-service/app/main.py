from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="users-service", version="1.0.0")

USERS = [
    {
        "username": "admin",
        "full_name": "Platform Administrator",
        "email": "admin@skyroute.local",
        "role": "admin",
        "status": "active",
        "password": "admin123",
    },
    {
        "username": "operator1",
        "full_name": "Weather Operations Analyst",
        "email": "operator1@skyroute.local",
        "role": "operator",
        "status": "active",
        "password": "operator123",
    },
    {
        "username": "viewer1",
        "full_name": "Dashboard Viewer",
        "email": "viewer1@skyroute.local",
        "role": "viewer",
        "status": "active",
        "password": "viewer123",
    },
]


class PublicUser(BaseModel):
    username: str
    full_name: str
    email: str
    role: str
    status: str


class UsersResponse(BaseModel):
    users: list[PublicUser]


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
    role: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "users-service"}


@app.get("/users", response_model=UsersResponse)
def get_users() -> UsersResponse:
    return UsersResponse(users=[to_public_user(user) for user in USERS])


@app.get("/users/admin", response_model=PublicUser)
def get_admin_user() -> PublicUser:
    admin = next((user for user in USERS if user["username"] == "admin"), None)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return to_public_user(admin)


@app.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = next((candidate for candidate in USERS if candidate["username"] == payload.username), None)
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(
        message="Login successful",
        username=user["username"],
        role=user["role"],
    )


def to_public_user(user: dict) -> PublicUser:
    return PublicUser(
        username=user["username"],
        full_name=user["full_name"],
        email=user["email"],
        role=user["role"],
        status=user["status"],
    )
