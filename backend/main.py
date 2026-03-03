from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from database import create_user, fetch_all_users, database_connection_test
from redis_cache import get_cached_users, set_cached_users, clear_cache, redis_connection_test

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: int
    name: str
    mobile: str
    email: str

@app.get("/")
def read_root():
    return {"message": "User Management System API is running"}

@app.get("/health")
def health_check():
    db_status = database_connection_test()
    redis_status = redis_connection_test()
    return {
        "database": "connected" if db_status else "disconnected",
        "redis": "connected" if redis_status else "disconnected"
    }

@app.post("/createuser")
def create_new_user(user: User):
    success, message = create_user(user.id, user.name, user.mobile, user.email)
    
    if success:
        clear_cache()
        return {
            "message": "User Created Successfully"
        }
    else:
        raise HTTPException(status_code=400, detail=message)

@app.get("/users/mysql")
def fetch_users_from_mysql():
    start_time = time.perf_counter()
    users = fetch_all_users()
    end_time = time.perf_counter()
    
    if users is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    fetch_time_ms = (end_time - start_time) * 1000
    
    return {
        "users": users,
        "fetch_time": f"{fetch_time_ms:.2f} ms",
        "source": "MySQL"
    }

@app.get("/users/redis")
def fetch_users_from_redis():
    cached_users, is_cached = get_cached_users()
    
    if is_cached:
        start_time = time.perf_counter()
        cached_users, _ = get_cached_users()
        end_time = time.perf_counter()
        
        fetch_time_ms = (end_time - start_time) * 1000
        
        return {
            "users": cached_users,
            "fetch_time": f"{fetch_time_ms:.2f} ms",
            "source": "Redis"
        }
    else:
        start_time = time.perf_counter()
        users = fetch_all_users()
        end_time = time.perf_counter()
        
        if users is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        set_cached_users(users)
        
        fetch_time_ms = (end_time - start_time) * 1000
        
        return {
            "users": users,
            "fetch_time": f"{fetch_time_ms:.2f} ms",
            "source": "MySQL (Cached to Redis)"
        }

@app.get("/users")
def get_all_users():
    users = fetch_all_users()
    if users is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return {"users": users}
