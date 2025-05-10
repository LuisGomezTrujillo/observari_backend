from fastapi import FastAPI
from app.core.database import create_db_and_tables
from contextlib import asynccontextmanager
from app.routers import user, auth, profile, users_relationship
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_NAME, APP_DESCRIPTION, APP_VERSION, CORS_ORIGINS

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar la aplicación
    create_db_and_tables()
    yield  # Lifespan context
    # Aquí puedes agregar lógica para el cierre si es necesario

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de salud para verificar que la API está funcionando
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Incluir routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(users_relationship.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)