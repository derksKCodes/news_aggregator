from .base_scraper import BaseScraper

class NYTimesScraper(BaseScraper):
    def __init__(self):
        super().__init__("NYTimes", "https://www.nytimes.com")
    
    def scrape(self):
        soup = self.fetch_dynamic_content(self.base_url + "/section/world", wait_for_element=".css-1cp3ece")
        if not soup:
            return
        
        # Find headline elements
        headline_elements = soup.select('a[data-testid="internal-link"]')
        
        for element in headline_elements[:15]:  # Limit to top 15 headlines
            headline_span = element.select_one('h3, .css-1j2kdqa, .css-1kv6qi e15t083i0')
            if headline_span:
                headline = headline_span.get_text(strip=True)
                link = element.get('href')
                
                if headline and link:
                    full_link = self.base_url + link if link.startswith('/') else link
                    self.add_headline(headline, full_link)