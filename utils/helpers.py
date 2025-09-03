import json
import os
from config import settings

def load_news_sites_config(filepath=None):
    if not filepath:
        filepath = os.path.join(os.path.dirname(__file__), '../config/news_sites.json')
    
    with open(filepath, 'r') as f:
        return json.load(f)

def display_headlines_table(headlines):
    try:
        import pandas as pd
        df = pd.DataFrame(headlines)
        print(df[['source', 'headline', 'link']].to_string(index=False))
        return df
    except ImportError:
        # Fallback if pandas is not available
        print("Source | Headline | Link")
        print("-" * 80)
        for item in headlines:
            print(f"{item['source']} | {item['headline'][:50]}... | {item['link']}")