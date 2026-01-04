"""
API routes for news analysis.
"""
from fastapi import APIRouter, HTTPException, Depends

from config.news_sources import NEWS_SOURCES
from services.driver_service import driver_service
from services.scraper_service import scrape_headlines


router = APIRouter()


def get_sentiment_service():
    """Dependency to get sentiment_service from main module."""
    import sys
    main_module = sys.modules.get('__main__')
    if not main_module or not hasattr(main_module, 'sentiment_service'):
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    service = getattr(main_module, 'sentiment_service', None)
    if not service:
        raise HTTPException(status_code=503, detail="Sentiment service not ready")
    
    return service


@router.get("/analyze/{keyword}")
async def analyze_news(keyword: str, sentiment_service = Depends(get_sentiment_service)):
    """
    Analyze news sentiment for a given keyword.
    
    Args:
        keyword: Keyword to search for in headlines
        sentiment_service: Injected sentiment service
    
    Returns:
        JSON response with sentiment analysis results
    """
    try:
        # Proses scraping berita
        all_headlines = {}
        driver = driver_service.driver
        
        for source_name, categories in NEWS_SOURCES.items():
            all_headlines[source_name] = {}
            for category, url in categories.items():
                try:
                    all_headlines[source_name][category] = scrape_headlines(
                        driver, url, source_name, category
                    )
                except Exception as e:
                    print(f"Gagal mengambil {source_name} - {category}: {e}")

        # Hitung total judul berita yang diambil
        total_judul = sum(
            len(headlines) 
            for source in all_headlines.values() 
            for headlines in source.values()
        )
        print(f"\nTotal judul berita yang diambil: {total_judul}")

        # Analisis data dan kembalikan JSON
        result = sentiment_service.analyze_data(all_headlines, keyword)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")


