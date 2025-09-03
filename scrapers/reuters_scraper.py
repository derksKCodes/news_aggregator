from .base_scraper import BaseScraper

class ReutersScraper(BaseScraper):
    def __init__(self):
        super().__init__("Reuters", "https://www.reuters.com")
    
    def scrape(self):
        soup = self.fetch_static_content(self.base_url + "/world/")
        if not soup:
            return
        
        # Find headline elements
        headline_elements = soup.select('a[data-testid="Heading"]')
        
        for element in headline_elements[:15]:  # Limit to top 15 headlines
            headline = element.get_text(strip=True)
            link = element.get('href')
            
            if headline and link:
                self.add_headline(headline, link)