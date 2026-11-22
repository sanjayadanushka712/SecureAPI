from app.db.database import Base, engine
from app.db.models import Task

Base.metadata.create_all(bind=engine, tables=[Task.__table__])

print("Database tables created successfully")
