import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.bbc_scraper import BBCScraper
from scrapers.cnn_scraper import CNNScraper 
from scrapers.reuters_scraper import ReutersScraper
from scrapers.aljazeera_scraper import AlJazeeraScraper
from scrapers.nytimes_scraper import NYTimesScraper

from utils.file_handlers import export_to_json, export_to_csv, export_to_xlsx
from utils.database import insert_into_mongodb
from utils.helpers import load_news_sites_config, display_headlines_table
from config import settings

def main():
    print("Starting News Aggregator...")
    
    # Initialize scrapers
    scrapers = [
        BBCScraper(),
        CNNScraper(),
        ReutersScraper(),
        AlJazeeraScraper(),
        NYTimesScraper()
    ]
    
    all_headlines = []
    
    # Scrape each site
    for scraper in scrapers:
        print(f"Scraping {scraper.source_name}...")
        try:
            scraper.scrape()
            headlines = scraper.get_headlines()
            all_headlines.extend(headlines)
            print(f"Found {len(headlines)} headlines from {scraper.source_name}")
        except Exception as e:
            print(f"Error scraping {scraper.source_name}: {e}")
    
    print(f"\nTotal headlines collected: {len(all_headlines)}")
    
    if not all_headlines:
        print("No headlines found. Exiting.")
        return
    
    # Display headlines in a table format
    print("\nAggregated News Headlines:")
    print("=" * 100)
    df = display_headlines_table(all_headlines)
    
    # Export to various formats
    print("\nExporting data...")
    json_file = export_to_json(all_headlines)
    csv_file = export_to_csv(all_headlines)
    xlsx_file = export_to_xlsx(all_headlines)
    
    print(f"Exported to JSON: {json_file}")
    print(f"Exported to CSV: {csv_file}")
    print(f"Exported to XLSX: {xlsx_file}")
    
    # Insert into MongoDB
    try:
        inserted_count = insert_into_mongodb(all_headlines)
        print(f"Inserted {inserted_count} documents into MongoDB")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")
    
    # Save screenshot of the table
    try:
        if df is not None:
            import matplotlib.pyplot as plt
            from matplotlib.table import Table
            
            plt.figure(figsize=(12, len(all_headlines) * 0.5))
            plt.axis('off')
            plt.title(f"Aggregated News Headlines - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Create table
            table = plt.table(cellText=df[['source', 'headline', 'link']].values,
                             colLabels=['Source', 'Headline', 'Link'],
                             cellLoc='left',
                             loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 2)
            
            # Save as image
            screenshot_path = os.path.join(settings.EXPORTS_DIR, f"news_feed_{settings.CURRENT_DATE}.png")
            plt.savefig(screenshot_path, bbox_inches='tight', dpi=150)
            print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Could not save screenshot: {e}")
    
    print("\nNews aggregation completed successfully!")

if __name__ == "__main__":
    main()