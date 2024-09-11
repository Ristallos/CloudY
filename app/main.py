import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .api import users, products, orders, deliveries, reviews
from .database import engine
from . import models, dependencies
from .bot_text import WELCOME_MESSAGE, MAIN_BUTTONS
# Configurazione del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea le tabelle del database
models.Base.metadata.create_all(bind=engine)

# Inizializza l'applicazione FastAPI
app = FastAPI(title="Marketplace Cannabis API")

# Includi i router
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["deliveries"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/", tags=["root"])
async def root():
    return {
        "message": WELCOME_MESSAGE,
        "buttons": MAIN_BUTTONS
    }

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)