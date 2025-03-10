from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from utils import create_db, db_insert, find_long_url, get_url_map
import os
from pydantic import BaseModel
import logging


# Get the values from the environment variables
host = os.getenv("HOST", "127.0.0.1")  # Default to 127.0.0.1 if HOST is not found
port = int(os.getenv("PORT", 8000))    # Default to 8000 if PORT is not found

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define the request body model
class URLRequest(BaseModel):
    url: str

# Pydantic model to represent a row in the 'url_map' table
class UrlMap(BaseModel):
    short_url: str
    long_url: str
    clicks: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application started")
    # Create database with tables and store connection in app state
    app.state.db_connection = create_db()
    
    yield
    
    # Shutdown - directly close the connection
    if app.state.db_connection:
        app.state.db_connection.close()
        
    # Remove the database file
    if os.path.exists("mydatabase.db"):
        os.remove("mydatabase.db")
        logger.info("Database removed")

app = FastAPI(lifespan=lifespan)

@app.post("/shorten/")
def shorten(request: URLRequest):
    """
    Shortens the provided URL
    """
    url = request.url
    
    logger.info(f"This is the URL: {url}")
    
    shortened_url = db_insert(url, app.state.db_connection)

    return {"shortened_url": shortened_url}

@app.get("/{str}")
def obtain_original(str):
    new_url = find_long_url(str, app.state.db_connection)
    logger.info(f"redirect url: {new_url}")
    return RedirectResponse(url=new_url)

@app.get("/url_map/")
def get_all():
    table = get_url_map(app.state.db_connection)
    print(table)
    # Convert rows to list of dictionaries (to match Pydantic model)
    
    return table

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host, port=port, reload=True)