from .base_scraper import BaseScraper

class AlJazeeraScraper(BaseScraper):
    def __init__(self):
        super().__init__("Al Jazeera", "https://www.aljazeera.com")
    
    def scrape(self):
        soup = self.fetch_static_content(self.base_url + "/news/")
        if not soup:
            return
        
        # Find headline elements
        headline_elements = soup.select('.gc__title a')
        
        for element in headline_elements[:15]:  # Limit to top 15 headlines
            headline = element.get_text(strip=True)
            link = element.get('href')
            
            if headline and link:
                full_link = self.base_url + link if link.startswith('/') else link
                self.add_headline(headline, full_link)