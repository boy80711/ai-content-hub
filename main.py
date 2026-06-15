import yaml
import json
import os
import re
import logging
from pathlib import Path
from scraper import ArticleScraper
from processor import AIProcessor
from generator import SiteGenerator

logging.basicConfig(level=logging.INFO)
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
    return resolve_env(config)


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
    if not key or key.startswith("${"):
        logger.error("GEMINI_API_KEY 未正確設定！")
        return
    logger.info("API Key 載入成功")
    new_articles = ArticleScraper(config).scrape_all()
    if new_articles:
        processed = AIProcessor(config).process_batch(new_articles)
        existing = load_existing()
        existing_ids = set(a["id"] for a in existing)
        added = 0
        for a in processed:
            if a["id"] not in existing_ids:
                existing.append(a)
                added += 1
        logger.info(f"新增 {added} 篇，共 {len(existing)} 篇")
        save_articles(existing)
    else:
        logger.info("沒有新文章")
    SiteGenerator(config).generate()
    logger.info("網站生成完成！")


if __name__ == "__main__":
    main()
