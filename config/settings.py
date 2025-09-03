import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')

# Ensure exports directory exists
os.makedirs(EXPORTS_DIR, exist_ok=True)

# MongoDB settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = 'news_aggregator'
MONGODB_COLLECTION = 'news_feed'

# Date format for exports
DATE_FORMAT = '%Y-%m-%d'
CURRENT_DATE = datetime.now().strftime(DATE_FORMAT)