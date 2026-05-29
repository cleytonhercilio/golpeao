from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, matches, predictions, groups, ranking, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GolPeão API", version="1.0.0", description="Bolão Copa do Mundo 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(predictions.router)
app.include_router(groups.router)
app.include_router(ranking.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "GolPeão API ⚽ Copa do Mundo 2026"}
