from sqlmodel import Session, select
from models import Producto
from fastapi import HTTPException

def create_producto(session: Session, producto: Producto):
    try:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_producto(session: Session, id_producto: int):
    assert id_producto > 0, "El ID debe ser positivo"
    producto = session.exec(select(Producto).where(Producto.id == id_producto)).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

def update_producto(session: Session, id_producto: int, nueva_cantidad: int):
    assert id_producto > 0, "El ID debe ser positivo"
    assert nueva_cantidad >= 0, "La cantidad debe ser no negativa"
    
    producto = session.exec(select(Producto).where(Producto.id == id_producto)).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.stock = nueva_cantidad
    session.commit()
    session.refresh(producto)
    return producto