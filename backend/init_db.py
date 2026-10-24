from database import engine, Base
from models import ArticleModel 

print("Connecting to database and creating tables...")

# connect to db and create all needed tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully in PostgreSQL!")