import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app
from database import get_session
from models import Producto

# Configuración base de datos de prueba MySQL
TEST_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/PruebaII_test"
engine = create_engine(TEST_DATABASE_URL)

def create_test_database():
    try:
        SQLModel.metadata.drop_all(engine)
    except:
        pass
    SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    create_test_database()
    yield
    SQLModel.metadata.drop_all(engine)

# Casos de prueba para creación de productos
def test_crear_producto_valido():
    response = client.post(
        "/producto",
        json={"nombre": "Test Product", "stock": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Product"
    assert data["stock"] == 10

def test_crear_producto_stock_negativo():
    response = client.post(
        "/producto",
        json={"nombre": "Test Product", "stock": -5}
    )
    assert response.status_code == 400

# Casos de prueba para consulta de productos
def test_consultar_producto_existente():
    # Primero crear un producto
    producto = client.post(
        "/producto",
        json={"nombre": "Test Product", "stock": 10}
    ).json()
    
    # Luego consultarlo
    response = client.get(f"/producto/{producto['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Product"
    assert data["stock"] == 10

def test_consultar_producto_inexistente():
    response = client.get("/producto/999")
    assert response.status_code == 404

def test_consultar_producto_id_invalido():
    response = client.get("/producto/-1")
    assert response.status_code == 400

# Casos de prueba para actualización de stock
def test_actualizar_stock_valido():
    # Primero crear un producto
    producto = client.post(
        "/producto",
        json={"nombre": "Test Product", "stock": 10}
    ).json()
    
    # Luego actualizar su stock
    response = client.put(
        "/producto",
        json={"id": producto['id'], "stock": 20}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stock"] == 20

def test_actualizar_stock_negativo():
    producto = client.post(
        "/producto",
        json={"nombre": "Test Product", "stock": 10}
    ).json()
    
    response = client.put(
        "/producto",
        json={"id": producto['id'], "stock": -5}
    )
    assert response.status_code == 400

def test_actualizar_stock_producto_inexistente():
    response = client.put(
        "/producto",
        json={"id": 999, "stock": 20}
    )
    assert response.status_code == 404
