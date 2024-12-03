from sqlmodel import SQLModel, create_engine, Session
import os

# Load database credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL","postgresql+psycopg2://koyeb-adm:vhQ7OWJmLZ1T@ep-orange-darkness-a41e7i20.us-east-1.pg.koyeb.app/koyebdb")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Function to initialize the database (creates tables)
def init_db():
    # Only create tables without dropping them
    SQLModel.metadata.create_all(engine)


# Dependency to provide a database session
def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in the caller

# from sqlmodel import SQLModel, create_engine, Session
# from model import Question
# import os

# # SQLite database URL
# DATABASE_FILE = "test.db"
# DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# # Create the database engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Function to initialize the database
# def init_db():
#     if not os.path.exists(DATABASE_FILE):
#         SQLModel.metadata.create_all(engine)

# # Dependency to provide a database session
# def get_session():
#     with Session(engine) as session:
#         yield session

