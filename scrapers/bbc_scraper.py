from .base_scraper import BaseScraper

class BBCScraper(BaseScraper):
    def __init__(self):
        super().__init__("BBC", "https://www.bbc.com")
    
    def scrape(self):
        soup = self.fetch_static_content(self.base_url + "/news")
        if not soup:
            return
        
        # Find headline elements
        headline_elements = soup.select('a[data-testid="internal-link"]')
        
        for element in headline_elements[:15]:  # Limit to top 15 headlines
            headline = element.get_text(strip=True)
            link = element.get('href')
            
            if headline and link:
                self.add_headline(headline, link)