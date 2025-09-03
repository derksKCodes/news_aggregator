from .base_scraper import BaseScraper

class CNNScraper(BaseScraper):
    def __init__(self):
        super().__init__("CNN", "https://edition.cnn.com")
    
    def scrape(self):
        soup = self.fetch_dynamic_content(self.base_url + "/world", wait_for_element=".container__headline")
        if not soup:
            return
        
        # Find headline elements
        headline_elements = soup.select('.container__headline')
        
        for element in headline_elements[:15]:  # Limit to top 15 headlines
            headline = element.get_text(strip=True)
            link = element.find('a')['href'] if element.find('a') else None
            
            if headline and link:
                full_link = self.base_url + link if link.startswith('/') else link
                self.add_headline(headline, full_link)