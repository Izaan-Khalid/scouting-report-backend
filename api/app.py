from fastapi import FastAPI
from api.routes.teams import router as teams_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Scouting Report API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(teams_router, prefix="/teams")