"""
Web scraping service for news headlines.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List
import time
import random

from utils.selectors import SELECTORS


def scroll_to_bottom(driver, max_scrolls=3):
    """
    Scroll to the bottom of the page.
    
    Args:
        driver: Selenium WebDriver instance
        max_scrolls: Maximum number of scrolls to perform
    """
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Reduced wait time
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(f"Error saat scrolling: {e}")


def scrape_headlines(driver, url: str, source_name: str, category: str) -> List[str]:
    """
    Scrape headlines from a news source.
    
    Args:
        driver: Selenium WebDriver instance
        url: URL to scrape
        source_name: Name of the news source
        category: Category of news
    
    Returns:
        List of headline strings
    """
    headline_list = []
    
    try:
        print(f"Mengakses {source_name} - {category}: {url}")
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)
        
        print(f"Memuat {source_name} - {category}...")
        scroll_to_bottom(driver)

        # Try to find headlines using selectors
        for selector in SELECTORS.get(source_name, ["title", "h2", "h3", "article-title"]):
            try:
                # Try class name first
                headlines = driver.find_elements(By.CLASS_NAME, selector)
                if not headlines:
                    # Try tag name
                    headlines = driver.find_elements(By.TAG_NAME, selector)
                
                if headlines:
                    headline_list = [headline.text.strip() for headline in headlines if headline.text.strip()]
                    if headline_list:
                        print(f"✓ Ditemukan {len(headline_list)} judul dari {source_name} - {category}")
                        break
            except Exception as e:
                continue
        
        if not headline_list:
            print(f"⚠ Tidak ada judul ditemukan dari {source_name} - {category}")
                
    except TimeoutException:
        print(f"✗ Timeout saat mengakses {source_name} - {category}")
    except Exception as e:
        print(f"✗ Error saat scraping {source_name} - {category}: {str(e)[:100]}")
    
    return headline_list
