import yaml
import json
import os
import re
import logging
from pathlib import Path
from scraper import ArticleScraper
from processor import AIProcessor
from generator import SiteGenerator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
DATA_FILE = Path("data/articles.json")


def resolve_env(obj):
    """遞迴解析 ${VAR} 環境變數語法"""
    if isinstance(obj, str):
        return re.sub(r'\$\{(\w+)\}', lambda m: os.environ.get(m.group(1), m.group(0)), obj)
    elif isinstance(obj, dict):
        return {k: resolve_env(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_env(i) for i in obj]
    return obj


def load_config():
    with open("config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    config = resolve_env(config)
    # 直接從環境變數覆蓋 API Key，確保一定拿到
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        config.setdefault("ai", {})["gemini_api_key"] = env_key
        logger.info("API Key loaded from env")
    return config


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
    ai_cfg = config.get("ai", {})
    key = ai_cfg.get("gemini_api_key", "")

    # 清除舊的 seen_ids 以確保重新抓取
    seen_file = Path("data/seen_ids.json")
    if seen_file.exists():
        seen_file.unlink()
        logger.info("Cleared seen_ids.json")

    if not key or key.startswith("${"):
        logger.error("GEMINI_API_KEY not set! Check repo Settings > Secrets > Actions")
        raise SystemExit(1)

    logger.info(f"API Key starts with: {key[:8]}...")
    logger.info(f"Model: {ai_cfg.get('gemini_model', 'unknown')}")
    logger.info(f"Feeds: {len(config.get('feeds', []))}")

    new_articles = ArticleScraper(config).scrape_all()
    logger.info(f"Scraped {len(new_articles)} new articles")

    if new_articles:
        processed = AIProcessor(config).process_batch(new_articles)
        logger.info(f"Processed {len(processed)} articles")
        existing = load_existing()
        existing_ids = set(a["id"] for a in existing)
        added = 0
        for a in processed:
            if a["id"] not in existing_ids:
                existing.append(a)
                added += 1
        logger.info(f"Added {added} new, total {len(existing)}")
        save_articles(existing)
    else:
        logger.info("No new articles found")

    SiteGenerator(config).generate()
    logger.info("Site generated!")


if __name__ == "__main__":
    main()
