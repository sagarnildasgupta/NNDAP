from sqlalchemy import create_engine, orm
from cow import Cow, Weight, Feeding, Milk_production

# engine = create_engine( "postgresql://postgres:default@localhost:5432/adds")

address = "cowshed.postgres.database.azure.com"
username = "cowshed"
password = "azure123!"
dbname = "cowshed"

engine = create_engine(f"postgresql://{username}:{password}@{address}/{dbname}?sslmode=require")

session = orm.scoped_session(orm.sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)

try:
    Cow.__table__.drop(engine)
    Weight.__table__.drop(engine)
    Feeding.__table__.drop(engine)
    Milk_production.__table__.drop(engine)
except:
    pass

Cow.__table__.create(engine)
Weight.__table__.create(engine)
Feeding.__table__.create(engine)
Milk_production.__table__.create(engine)