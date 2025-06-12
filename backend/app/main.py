from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.database import engine, Base
from .routes import auth, products, chat, cart

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Uplyft E-commerce Chatbot API",
    description="A modern e-commerce chatbot API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Uplyft E-commerce Chatbot API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running smoothly"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
