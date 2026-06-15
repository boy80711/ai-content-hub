import json
import shutil
import logging
import markdown
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class SiteGenerator:
    def __init__(self, config):
        self.site = config.get("site", {})
        self.output_dir = Path("output")
        self.templates_dir = Path("templates")
        self.per_page = self.site.get("articles_per_page", 12)
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)), autoescape=True)
        self.env.filters["format_date"] = self._format_date
        self.env.filters["md_to_html"] = self._md_to_html
        self.env.filters["time_ago"] = self._time_ago

    def _format_date(self, s):
        if not s: return ""
        try: return datetime.fromisoformat(s).strftime("%Y-%m-%d")
        except: return s

    def _time_ago(self, s):
        if not s: return ""
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            diff = datetime.now(dt.tzinfo) - dt
            if diff.days > 30: return f"{diff.days//30}mo ago"
            if diff.days > 0: return f"{diff.days}d ago"
            h = diff.seconds // 3600
            return f"{h}h ago" if h > 0 else "now"
        except: return ""

    def _md_to_html(self, text):
        return markdown.markdown(text, extensions=["extra", "codehilite"])

    def _load_articles(self):
        p = Path("data/articles.json")
        if not p.exists(): return []
        with open(p, encoding="utf-8") as f:
            articles = json.load(f)
        articles.sort(key=lambda a: a.get("scraped_at", a.get("published", "")), reverse=True)
        return articles

    def generate(self):
        articles = self._load_articles()
        all_tags = sorted({t for a in articles for t in a.get("tags", [])})
        if self.output_dir.exists(): shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        self._gen_index(articles, all_tags)
        for a in articles:
            self._gen_article(a, all_tags)
        self._gen_rss(articles)
        self._gen_sitemap(articles)

    def _gen_index(self, articles, all_tags):
        tpl = self.env.get_template("index.html")
        total_pages = max(1, (len(articles) + self.per_page - 1) // self.per_page)
        html = tpl.render(site=self.site, articles=articles[:self.per_page], all_tags=all_tags,
            page_num=1, total_pages=total_pages, has_prev=False, has_next=total_pages > 1)
        (self.output_dir / "index.html").write_text(html, encoding="utf-8")

    def _gen_article(self, article, all_tags):
        tpl = self.env.get_template("article.html")
        html = tpl.render(site=self.site, article=article, all_tags=all_tags)
        d = self.output_dir / f"article/{article['id']}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html, encoding="utf-8")

    def _gen_rss(self, articles):
        base = self.site.get("url", "")
        title = self.site.get("title", "AI Hub")
        items = []
        for a in articles[:20]:
            items.append(f"  <item><title><![CDATA[{a.get('title','')}]]></title><link>{base}/article/{a['id']}/</link><description><![CDATA[{a.get('summary','')}]]></description><pubDate>{a.get('scraped_at','')}</pubDate></item>")
        rss = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>' + title + '</title><link>' + base + '</link><description>' + self.site.get("subtitle","") + '</description>\n' + '\n'.join(items) + '\n</channel></rss>'
        (self.output_dir / "rss.xml").write_text(rss, encoding="utf-8")

    def _gen_sitemap(self, articles):
        base = self.site.get("url", "")
        urls = ['  <url><loc>' + base + '/</loc></url>']
        urls += ['  <url><loc>' + base + '/article/' + a['id'] + '/</loc></url>' for a in articles]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'
        (self.output_dir / "sitemap.xml").write_text(sm, encoding="utf-8")
