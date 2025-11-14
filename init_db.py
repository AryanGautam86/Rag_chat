# init_db.py

from models import Base, engine

print("Creating database...")
Base.metadata.create_all(bind=engine)
print("Database created successfully!")
