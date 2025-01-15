from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/PruebaII"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session