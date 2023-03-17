from fastapi import FastAPI
from routes.requestMethod import router
from fastapi.staticfiles import StaticFiles
from config.db import conn
import signal
from fastapi.middleware.cors import CORSMiddleware 

MyApp = FastAPI()


def kill_db_connections ():
    print('\n')
    print('==> KONEKSI KE DATABASE DIMATIKAN <== \n')
    conn.close()

@MyApp.on_event("shutdown")
def app_shutdown ():
    kill_db_connections()

def signal_handler(signum, frame):
    kill_db_connections()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MyApp.mount("/static", StaticFiles(directory="static"),name="static")

MyApp.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MyApp.include_router(router)