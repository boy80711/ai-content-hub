import json
import re
import logging
import time

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = "You are a top AI content editor. Rewrite articles into Traditional Chinese. Return ONLY valid JSON with keys: title, summary, content (markdown), tags (1-3 from list), meta_description."

USER_PROMPT = "Title: {title}\nSource: {source}\nURL: {url}\nContent:\n{content}\nRewrite into Traditional Chinese. Return JSON only."

class AIProcessor:
    def __init__(self, config):
        ai = config.get("ai", {})
        self.provider = ai.get("provider", "gemini")
        self.gemini_key = ai.get("gemini_api_key", "")
        self.gemini_model = ai.get("gemini_model", "gemini-2.0-flash")
        if self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel(model_name=self.gemini_model, system_instruction=SYSTEM_PROMPT)

    def _call_gemini(self, prompt):
        return self.model.generate_content(prompt).text

    def _extract_json(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        return None

    def process_article(self, article):
        content = article.get("content", "")
        if len(content) < 50:
            return None
        prompt = USER_PROMPT.format(title=article["title"], source=article.get("source", ""), url=article.get("url", ""), content=content[:2500])
        try:
            raw = self._call_gemini(prompt)
        except Exception as e:
            logger.error(f"API failed: {e}")
            return None
        result = self._extract_json(raw)
        if not result:
            return None
        return {
            "id": article["id"], "original_title": article["title"], "original_url": article["url"],
            "original_source": article.get("source", ""), "category": article.get("category", ""),
            "scraped_at": article.get("scraped_at"), "published": article.get("published"),
            "title": result.get("title", article["title"]), "summary": result.get("summary", ""),
            "content": result.get("content", ""), "tags": result.get("tags", []),
            "meta_description": result.get("meta_description", ""),
        }

    def process_batch(self, articles):
        results = []
        for i, article in enumerate(articles, 1):
            logger.info(f"processing {i}/{len(articles)}")
            processed = self.process_article(article)
            if processed:
                results.append(processed)
            if i < len(articles):
                time.sleep(2)
        return results
