import json
import csv
import pandas as pd
from datetime import datetime
import os
from config import settings

def export_to_json(data, filename=None):
    if not filename:
        filename = f"news_feed_{settings.CURRENT_DATE}.json"
    
    filepath = os.path.join(settings.EXPORTS_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return filepath

def export_to_csv(data, filename=None):
    if not filename:
        filename = f"news_feed_{settings.CURRENT_DATE}.csv"
    
    filepath = os.path.join(settings.EXPORTS_DIR, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['source', 'headline', 'link', 'published_time'])
        writer.writeheader()
        writer.writerows(data)
    
    return filepath

def export_to_xlsx(data, filename=None):
    if not filename:
        filename = f"news_feed_{settings.CURRENT_DATE}.xlsx"
    
    filepath = os.path.join(settings.EXPORTS_DIR, filename)
    
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return filepath