"""
ChromeDriver service management.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverService:
    """Manages ChromeDriver instance."""
    
    def __init__(self):
        self.driver = None
    
    def initialize(self):
        """Initialize ChromeDriver with auto-download and options."""
        print("Menyiapkan ChromeDriver...")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver siap digunakan!")
        return self.driver
    
    def quit(self):
        """Quit ChromeDriver."""
        if self.driver:
            try:
                self.driver.quit()
                print("ChromeDriver ditutup.")
            except Exception as e:
                print(f"Error saat menutup ChromeDriver: {e}")


# Global driver service instance
driver_service = DriverService()
