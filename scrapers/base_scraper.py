from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BaseScraper(ABC):
    def __init__(self, source_name, base_url):
        self.source_name = source_name
        self.base_url = base_url
        self.headlines = []
        
    def fetch_static_content(self, url):
        """Fetch content from static websites using requests and BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def fetch_dynamic_content(self, url, wait_for_element=None, timeout=10):
        """Fetch content from dynamic websites using Selenium"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            driver.get(url)
            
            # Wait for specific element if provided
            if wait_for_element:
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                )
            
            # Optional: Scroll to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            return soup
        except Exception as e:
            print(f"Error fetching dynamic content from {url}: {e}")
            return None
        finally:
            driver.quit()
    
    @abstractmethod
    def scrape(self):
        """Abstract method to be implemented by each specific scraper"""
        pass
    
    def add_headline(self, headline, link, published_time=None):
        """Add a headline to the collection"""
        self.headlines.append({
            'source': self.source_name,
            'headline': headline,
            'link': link if link.startswith('http') else self.base_url + link,
            'published_time': published_time
        })
    
    def get_headlines(self):
        """Return all scraped headlines"""
        return self.headlines