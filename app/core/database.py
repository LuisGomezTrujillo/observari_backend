from sqlmodel import SQLModel, create_engine, Session
from .config import DATABASE_URL

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Función para crear todas las tablas en la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Función para obtener una sesión de base de datos
def get_session():
    with Session(engine) as session:
        yield session