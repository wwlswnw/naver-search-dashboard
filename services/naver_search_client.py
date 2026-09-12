import json
import urllib.request
import urllib.parse
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
from config.settings import settings

class NaverSearchClient:
    def __init__(self, client_id: str = "", client_secret: str = ""):
        self.client_id = (client_id.strip() if client_id else "") or settings.DEFAULT_CLIENT_ID
        self.client_secret = (client_secret.strip() if client_secret else "") or settings.DEFAULT_CLIENT_SECRET
        self.base_url = settings.SEARCH_API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        cid = str(self.client_id).strip().strip('"').strip("'")
        csec = str(self.client_secret).strip().strip('"').strip("'")
        return {
            "X-NCP-APIGW-API-KEY-ID": cid,
            "X-NCP-APIGW-API-KEY": csec,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def _get_legacy_headers(self) -> Dict[str, str]:
        cid = str(self.client_id).strip().strip('"').strip("'")
        csec = str(self.client_secret).strip().strip('"').strip("'")
        return {
            "X-Naver-Client-Id": cid,
            "X-Naver-Client-Secret": csec,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def search_category(
        self,
        category: str,
        query: str,
        display: int = 50,
        start: int = 1,
        sort: str = "sim"
    ) -> Dict[str, Any]:
        """Fetch REAL search results from Naver API HUB using multi-strategy connection with exact error diagnostics."""
        sort_param = "random" if (category == "local" and sort not in ["random", "comment"]) else sort
        enc_query = urllib.parse.quote(query.strip())
        hub_url = f"{self.base_url}/{category}?query={enc_query}&display={min(display, 100)}&start={start}&sort={sort_param}"

        headers = self._get_headers()
        errors = []

        # Strategy 1: Standard urllib.request (most reliable on all cloud proxies)
        try:
            req = urllib.request.Request(hub_url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    return {
                        "category": category,
                        "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                        "total": data.get("total", 0),
                        "start": data.get("start", 1),
                        "display": data.get("display", 0),
                        "items": data.get("items", []),
                        "is_demo": False
                    }
                else:
                    errors.append(f"urllib status {resp.status}")
        except Exception as e:
            errors.append(f"urllib: {str(e)}")

        # Strategy 2: requests library to API HUB
        try:
            r = requests.get(hub_url, headers=headers, timeout=12)
            if r.status_code == 200:
                data = r.json()
                return {
                    "category": category,
                    "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                    "total": data.get("total", 0),
                    "start": data.get("start", 1),
                    "display": data.get("display", 0),
                    "items": data.get("items", []),
                    "is_demo": False
                }
            else:
                errors.append(f"requests HUB: [{r.status_code}] {r.text[:80]}")
        except Exception as e:
            errors.append(f"requests HUB: {str(e)}")

        # Strategy 3: Legacy openapi endpoint
        try:
            legacy_url = f"{settings.LEGACY_SEARCH_BASE_URL}/{category}.json?query={enc_query}&display={min(display, 100)}&start={start}&sort={sort_param}"
            r_leg = requests.get(legacy_url, headers=self._get_legacy_headers(), timeout=12)
            if r_leg.status_code == 200:
                data = r_leg.json()
                return {
                    "category": category,
                    "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                    "total": data.get("total", 0),
                    "start": data.get("start", 1),
                    "display": data.get("display", 0),
                    "items": data.get("items", []),
                    "is_demo": False
                }
            else:
                errors.append(f"Legacy: [{r_leg.status_code}] {r_leg.text[:80]}")
        except Exception as e:
            errors.append(f"Legacy: {str(e)}")

        # Return clean empty structure with exact diagnostics
        return {
            "category": category,
            "category_name": settings.SEARCH_CATEGORIES.get(category, category),
            "total": 0,
            "start": 1,
            "display": 0,
            "items": [],
            "error": " | ".join(errors)
        }

    def search_all_categories(
        self,
        query: str,
        display: int = 30,
        sort: str = "sim"
    ) -> Dict[str, Any]:
        """Fetch search results from all 8 categories for a given keyword."""
        results = {}
        for cat in settings.SEARCH_CATEGORIES.keys():
            results[cat] = self.search_category(cat, query, display=display, sort=sort)
        return results
