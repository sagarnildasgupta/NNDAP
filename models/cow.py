from sqlalchemy import Column, DateTime, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid  # Import the UUID type

Base = declarative_base()

class Cow(Base):
    __tablename__ = "cow"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True, unique=True)
    sex = Column(String)
    condition = Column(String)
    birthdate = Column(Date())
    has_calf = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class Weight(Base):
    __tablename__ = "weight"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    cow_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    mass_kg = Column(Integer)
    last_measured = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class Feeding(Base):
    __tablename__ = "feeding"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    cow_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    amount_kg = Column(Integer)
    cron_schedule= Column(String)
    last_measured = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
class Milk_production(Base):
    __tablename__ = "milk_production"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    cow_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    last_milk = Column(DateTime(timezone=True))
    cron_schedule = Column(String)
    amount_l = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
