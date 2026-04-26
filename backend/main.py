from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import precios_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(precios_router.router)





app.mount("/", StaticFiles(directory="../fronted", html=True), name="frontend")