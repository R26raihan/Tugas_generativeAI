"""
FastAPI Sentiment Analysis Application
Main entry point for running the application.
"""
from fastapi import FastAPI
import uvicorn

from config.device_config import get_device_config
from services.driver_service import driver_service
from services.sentiment_service import SentimentService
from routes.analysis_routes import router as analysis_router

# Global sentiment service instance
sentiment_service = None


# Inisialisasi FastAPI
app = FastAPI(
    title="News Sentiment Analysis API",
    description="API untuk analisis sentimen berita dari berbagai sumber",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    global sentiment_service
    
    # Deteksi dan konfigurasi device
    device, device_name, device_index = get_device_config()
    
    # Inisialisasi ChromeDriver
    driver_service.initialize()
    
    # Inisialisasi sentiment analyzer
    sentiment_service = SentimentService(device_index)
    
    print("Aplikasi siap digunakan!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    driver_service.quit()
    print("Aplikasi ditutup.")


# Register routes
app.include_router(analysis_router, tags=["Analysis"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "News Sentiment Analysis API",
        "endpoints": {
            "analyze": "/analyze/{keyword}"
        }
    }


# Jalankan server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
