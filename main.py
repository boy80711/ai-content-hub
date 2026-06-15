import yaml
import json
import argparse
import logging
from pathlib import Path
from scraper import ArticleScraper
from processor import AIProcessor
from generator import SiteGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATA_FILE = Path("data/articles.json")

def load_config():
    with open("config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_existing():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_articles(articles):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def main():
    config = load_config()
    new_articles = ArticleScraper(config).scrape_all()
    if new_articles:
        processed = AIProcessor(config).process_batch(new_articles)
        existing = load_existing()
        existing_ids = set(a["id"] for a in existing)
        for a in processed:
            if a["id"] not in existing_ids:
                existing.append(a)
        save_articles(existing)
    SiteGenerator(config).generate()
    print("done!")

if __name__ == "__main__":
    main()
