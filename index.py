from fastapi import FastAPI
from routes.requestMethod import router
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware 

MyApp = FastAPI()

MyApp.mount("/static", StaticFiles(directory="static"),name="static")


MyApp.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MyApp.include_router(router)