import os
import fastapi
import azure.functions as func
from . import fastapi_routes
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
# load_dotenv('.env')
# db_url = "postgresql://xhirmsie:va8fZ76fuuda23yUlUYPlglFBHmsnF5s@dumbo.db.elephantsql.com/xhirmsie"
# db_url = "postgresql://postgres:default@localhost:5432/cow"

address = "cowshed.postgres.database.azure.com"
username = "cowshed"
password = "azure123!"
dbname = "cowshed"

db_url = f"postgresql://{username}:{password}@{address}/{dbname}?sslmode=require"
app = fastapi.FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=db_url)
app.include_router(fastapi_routes.router)