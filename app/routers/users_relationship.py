from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.users_relationship import UsersRelationship
from app.schemas.users_relationship import (
    UsersRelationshipCreate,
    UsersRelationshipRead,
    UsersRelationshipUpdate
)

router = APIRouter(prefix="/api/relationships", tags=["relationships"])

@router.post("/", response_model=UsersRelationshipRead)
def create_relationship(
    relationship: UsersRelationshipCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crea una nueva relación entre usuarios
    """
    # Verificar que ambos usuarios existen
    user = session.get(User, relationship.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {relationship.user_id} no encontrado"
        )
    
    related_user = session.get(User, relationship.related_user_id)
    if not related_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario relacionado con ID {relationship.related_user_id} no encontrado"
        )
    
    # Verificar que no existe ya una relación entre estos usuarios
    existing_relationship = session.exec(
        select(UsersRelationship).where(
            UsersRelationship.user_id == relationship.user_id,
            UsersRelationship.related_user_id == relationship.related_user_id
        )
    ).first()
    
    if existing_relationship:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una relación entre estos usuarios"
        )
    
    # Crear la relación
    new_relationship = UsersRelationship(**relationship.dict())
    session.add(new_relationship)
    session.commit()
    session.refresh(new_relationship)
    return new_relationship

@router.get("/", response_model=List[UsersRelationshipRead])
def read_relationships(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene todas las relaciones entre usuarios
    """
    relationships = session.exec(
        select(UsersRelationship).offset(skip).limit(limit)
    ).all()
    return relationships

@router.get("/user/{user_id}", response_model=List[UsersRelationshipRead])
def get_user_relationships(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene todas las relaciones de un usuario específico
    """
    relationships = session.exec(
        select(UsersRelationship).where(UsersRelationship.user_id == user_id)
    ).all()
    return relationships

@router.get("/{relationship_id}", response_model=UsersRelationshipRead)
def read_relationship(
    relationship_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene una relación específica por su ID
    """
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )
    return relationship

@router.patch("/{relationship_id}", response_model=UsersRelationshipRead)
def update_relationship(
    relationship_id: int,
    update: UsersRelationshipUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualiza una relación existente
    """
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )
    
    # Actualizar los campos de la relación
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(relationship, key, value)
    
    # Actualizar la fecha de actualización
    from datetime import datetime, timezone
    relationship.updated_at = datetime.now(timezone.utc)
    
    session.add(relationship)
    session.commit()
    session.refresh(relationship)
    return relationship

@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(
    relationship_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Elimina una relación existente
    """
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )
    
    session.delete(relationship)
    session.commit()
    return None

@router.get("/between/{user_id}/{related_user_id}", response_model=UsersRelationshipRead)
def get_relationship_between_users(
    user_id: int,
    related_user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la relación entre dos usuarios específicos
    """
    relationship = session.exec(
        select(UsersRelationship).where(
            UsersRelationship.user_id == user_id,
            UsersRelationship.related_user_id == related_user_id
        )
    ).first()
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe relación entre estos usuarios"
        )
    
    return relationship

@router.get("/mutual/{user_id}", response_model=List[UsersRelationshipRead])
def get_mutual_relationships(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene relaciones mutuas (donde el usuario tiene relación con otro y viceversa)
    """
    # Obtener todas las relaciones donde el usuario es el origen
    outgoing_relationships = session.exec(
        select(UsersRelationship).where(UsersRelationship.user_id == user_id)
    ).all()
    
    # Crear un conjunto de IDs de usuarios con los que el usuario actual tiene relación
    related_user_ids = {rel.related_user_id for rel in outgoing_relationships}
    
    # Obtener relaciones donde esos usuarios tienen relación de vuelta con el usuario actual
    mutual_relationships = session.exec(
        select(UsersRelationship).where(
            UsersRelationship.user_id.in_(related_user_ids),
            UsersRelationship.related_user_id == user_id
        )
    ).all()
    
    return mutual_relationships


# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, select
# from typing import List

# from app.core.database import get_session
# from app.core.security import get_current_active_user
# from app.models.user import User
# from app.models.users_relationship import UsersRelationship
# from app.schemas.users_relationship import (
#     UsersRelationshipCreate,
#     UsersRelationshipRead,
#     UsersRelationshipUpdate
# )

# router = APIRouter(prefix="/api/relationships", tags=["relationships"])

# @router.post("/", response_model=UsersRelationshipRead)
# def create_relationship(
#     relationship: UsersRelationshipCreate,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Crea una nueva relación entre usuarios
#     """
#     # Verificar que ambos usuarios existen
#     user = session.get(User, relationship.user_id)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Usuario con ID {relationship.user_id} no encontrado"
#         )
    
#     related_user = session.get(User, relationship.related_user_id)
#     if not related_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Usuario relacionado con ID {relationship.related_user_id} no encontrado"
#         )
    
#     # Verificar que no existe ya una relación entre estos usuarios
#     existing_relationship = session.exec(
#         select(UsersRelationship).where(
#             UsersRelationship.user_id == relationship.user_id,
#             UsersRelationship.related_user_id == relationship.related_user_id
#         )
#     ).first()
    
#     if existing_relationship:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Ya existe una relación entre estos usuarios"
#         )
    
#     # Crear la relación
#     new_relationship = UsersRelationship(**relationship.dict())
#     session.add(new_relationship)
#     session.commit()
#     session.refresh(new_relationship)
#     return new_relationship

# @router.get("/", response_model=List[UsersRelationshipRead])
# def read_relationships(
#     skip: int = 0,
#     limit: int = 100,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Obtiene todas las relaciones entre usuarios
#     """
#     relationships = session.exec(
#         select(UsersRelationship).offset(skip).limit(limit)
#     ).all()
#     return relationships

# @router.get("/user/{user_id}", response_model=List[UsersRelationshipRead])
# def get_user_relationships(
#     user_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Obtiene todas las relaciones de un usuario específico
#     """
#     relationships = session.exec(
#         select(UsersRelationship).where(UsersRelationship.user_id == user_id)
#     ).all()
#     return relationships

# @router.get("/{relationship_id}", response_model=UsersRelationshipRead)
# def read_relationship(
#     relationship_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Obtiene una relación específica por su ID
#     """
#     relationship = session.get(UsersRelationship, relationship_id)
#     if not relationship:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Relación no encontrada"
#         )
#     return relationship

# @router.patch("/{relationship_id}", response_model=UsersRelationshipRead)
# def update_relationship(
#     relationship_id: int,
#     update: UsersRelationshipUpdate,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Actualiza una relación existente
#     """
#     relationship = session.get(UsersRelationship, relationship_id)
#     if not relationship:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Relación no encontrada"
#         )
    
#     # Actualizar los campos de la relación
#     update_data = update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(relationship, key, value)
    
#     # Actualizar la fecha de actualización
#     from datetime import datetime, timezone
#     relationship.updated_at = datetime.now(timezone.utc)
    
#     session.add(relationship)
#     session.commit()
#     session.refresh(relationship)
#     return relationship

# @router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_relationship(
#     relationship_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Elimina una relación existente
#     """
#     relationship = session.get(UsersRelationship, relationship_id)
#     if not relationship:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Relación no encontrada"
#         )
    
#     session.delete(relationship)
#     session.commit()
#     return None

# @router.get("/between/{user_id}/{related_user_id}", response_model=UsersRelationshipRead)
# def get_relationship_between_users(
#     user_id: int,
#     related_user_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Obtiene la relación entre dos usuarios específicos
#     """
#     relationship = session.exec(
#         select(UsersRelationship).where(
#             UsersRelationship.user_id == user_id,
#             UsersRelationship.related_user_id == related_user_id
#         )
#     ).first()
    
#     if not relationship:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No existe relación entre estos usuarios"
#         )
    
#     return relationship

# @router.get("/mutual/{user_id}", response_model=List[UsersRelationshipRead])
# def get_mutual_relationships(
#     user_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Obtiene relaciones mutuas (donde el usuario tiene relación con otro y viceversa)
#     """
#     # Obtener todas las relaciones donde el usuario es el origen
#     outgoing_relationships = session.exec(
#         select(UsersRelationship).where(UsersRelationship.user_id == user_id)
#     ).all()
    
#     # Crear un conjunto de IDs de usuarios con los que el usuario actual tiene relación
#     related_user_ids = {rel.related_user_id for rel in outgoing_relationships}
    
#     # Obtener relaciones donde esos usuarios tienen relación de vuelta con el usuario actual
#     mutual_relationships = session.exec(
#         select(UsersRelationship).where(
#             UsersRelationship.user_id.in_(related_user_ids),
#             UsersRelationship.related_user_id == user_id
#         )
#     ).all()
    
#     return mutual_relationships