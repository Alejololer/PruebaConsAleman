from fastapi import FastAPI, Depends, HTTPException
from typing import Dict
from crud import get_producto, create_producto, update_producto
from database import create_db_and_tables, get_session
from models import Producto
from sqlmodel import Session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/producto/{item_id}")
def consultar_producto(item_id: int, session: Session = Depends(get_session)):
    try:
        return get_producto(session=session, id_producto=item_id)
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/producto")
def agregar_producto(producto: Producto, session: Session = Depends(get_session)):
    try:
        if producto.stock < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
        return create_producto(session=session, producto=producto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/producto")
def actualizar_stock(datos_actualizacion: Dict[str, int], session: Session = Depends(get_session)):
    try:
        return update_producto(
            session=session,
            id_producto=datos_actualizacion["id"],
            nueva_cantidad=datos_actualizacion["stock"]
        )
    except KeyError:
        raise HTTPException(status_code=400, detail="Se requiere 'id' y 'stock' en el JSON")
    except AssertionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

