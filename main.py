from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from sqlmodel import Session
import models

from routers import users, records, dashboard

# This runs when you start the server
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend API for managing financial records and user roles.",
    lifespan=lifespan
)

# Connect the routers to the main app
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router) 

# A simple health check route to verify everything is working
@app.get("/")
def read_root():
    return {"status": "Backend is running!", "database": "Connected"}