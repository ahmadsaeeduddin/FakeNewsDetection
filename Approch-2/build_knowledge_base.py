import os
import hashlib
import json
from urllib.parse import urlparse
from scraper2 import ContentScraper
from fact_check import FactChecker

class KnowledgeBaseBuilder:
    def __init__(self, kb_dir="knowledge_base"):
        self.kb_dir = kb_dir
        os.makedirs(self.kb_dir, exist_ok=True)
        self.fact_checker = FactChecker()
        self.scraper = ContentScraper()

    def _clean_filename(self, url: str) -> str:
        """Create a safe filename using domain + short hash"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace(".", "_")
        short_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f"{domain}_{short_hash}.json"

    def _save_json(self, data: dict, filename: str):
        """Save the extracted data to a JSON file in the KB folder"""
        path = os.path.join(self.kb_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {path}")

    def build(self, claim_text: str, urls: list):
        print(f"\n🧠 Building knowledge base for claim: \"{claim_text}\"\n")
        for url in urls:
            try:
                print(f"🔍 Processing: {url}")
                if "snopes.com" in url:
                    data = self.fact_checker.scrape_snopes(url)
                elif "politifact.com" in url:
                    data = self.fact_checker.scrape_politifact(url)
                else:
                    data = self.scraper.scrape_content(url)

                filename = self._clean_filename(url)
                self._save_json(data, filename)

            except Exception as e:
                print(f"❌ Failed to process {url}: {e}")
