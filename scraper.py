import feedparser
import requests
import json
import hashlib
import re
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

class ArticleScraper:
    def __init__(self, config):
        self.feeds = config.get("feeds", [])
        self.max_per_feed = config.get("scraper", {}).get("max_articles_per_feed", 5)
        self.lookback_days = config.get("scraper", {}).get("lookback_days", 3)
        self.timeout = config.get("scraper", {}).get("request_timeout", 15)
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.seen_file = self.data_dir / "seen_ids.json"
        self.seen_ids = self._load_seen_ids()

    def _load_seen_ids(self):
        if self.seen_file.exists():
            with open(self.seen_file, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def _save_seen_ids(self):
        with open(self.seen_file, "w", encoding="utf-8") as f:
            json.dump(list(self.seen_ids), f, ensure_ascii=False)

    def _generate_id(self, url, title):
        return hashlib.md5(f"{url}|{title}".encode()).hexdigest()[:12]

    def _parse_date(self, entry):
        for field in ["published_parsed", "updated_parsed"]:
            parsed = entry.get(field)
            if parsed:
                try:
                    return datetime(*parsed[:6], tzinfo=timezone.utc)
                except Exception:
                    pass
        for field in ["published", "updated"]:
            date_str = entry.get(field)
            if date_str:
                try:
                    return date_parser.parse(date_str).replace(tzinfo=timezone.utc)
                except Exception:
                    pass
        return None

    def _extract_content(self, entry):
        if "content" in entry and entry["content"]:
            return entry["content"][0].get("value", "")
        return entry.get("summary", entry.get("description", ""))

    def _clean_html(self, html):
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:3000] + "..." if len(text) > 3000 else text

    def scrape_all(self):
        all_articles = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.lookback_days)
        for feed_config in self.feeds:
            url = feed_config["url"]
            category = feed_config.get("category", "未分類")
            logger.info(f"抓取: {category} - {url}")
            try:
                resp = requests.get(url, timeout=self.timeout, headers={"User-Agent": "AI-Content-Hub/1.0"})
                resp.raise_for_status()
                feed = feedparser.parse(resp.content)
            except Exception as e:
                logger.warning(f"失敗: {e}")
                continue
            count = 0
            for entry in feed.entries:
                if count >= self.max_per_feed:
                    break
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                if not title or not link:
                    continue
                article_id = self._generate_id(link, title)
                if article_id in self.seen_ids:
                    continue
                pub_date = self._parse_date(entry)
                if pub_date and pub_date < cutoff:
                    continue
                content = self._clean_html(self._extract_content(entry))
                all_articles.append({
                    "id": article_id, "title": title, "url": link,
                    "source": feed.feed.get("title", url), "category": category,
                    "content": content,
                    "published": pub_date.isoformat() if pub_date else None,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                })
                self.seen_ids.add(article_id)
                count += 1
                logger.info(f"  {title[:50]}")
        self._save_seen_ids()
        logger.info(f"共抓取 {len(all_articles)} 篇新文章")
        return all_articles
