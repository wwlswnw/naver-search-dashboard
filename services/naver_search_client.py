import requests
from typing import Dict, Any
from config.settings import settings

class NaverSearchClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id.strip() if client_id else ""
        self.client_secret = client_secret.strip() if client_secret else ""
        self.base_url = settings.SEARCH_API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        # NAVER API HUB header format
        return {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret
        }

    def _get_legacy_headers(self) -> Dict[str, str]:
        return {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

    def search_category(
        self,
        category: str,
        query: str,
        display: int = 50,
        start: int = 1,
        sort: str = "sim"
    ) -> Dict[str, Any]:
        """
        Search a specific category on Naver using NAVER API HUB (with fallback to legacy).
        Categories: news, blog, webkr, image, kin, local, cafearticle, encyc
        """
        if not self.client_id or not self.client_secret:
            return {"error": "네이버 Client ID와 Client Secret이 설정되지 않았습니다."}

        # NAVER API HUB URL: https://naverapihub.apigw.ntruss.com/search/v1/{category}
        url = f"{self.base_url}/{category}"
        params = {
            "query": query,
            "display": min(display, 100),
            "start": start,
            "sort": sort
        }

        if category == "local" and sort not in ["random", "comment"]:
            params["sort"] = "random"

        try:
            # Try NAVER API HUB first
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
            
            # If 401/404, check if legacy developers openapi works
            if response.status_code != 200:
                legacy_url = f"{settings.LEGACY_SEARCH_BASE_URL}/{category}.json"
                resp_legacy = requests.get(legacy_url, headers=self._get_legacy_headers(), params=params, timeout=10)
                if resp_legacy.status_code == 200:
                    response = resp_legacy

            if response.status_code == 200:
                data = response.json()
                return {
                    "category": category,
                    "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                    "total": data.get("total", 0),
                    "start": data.get("start", 1),
                    "display": data.get("display", 0),
                    "items": data.get("items", [])
                }
            else:
                try:
                    err_json = response.json()
                    error_msg = err_json.get("errorMessage") or err_json.get("error", {}).get("message") or response.text
                except Exception:
                    error_msg = response.text
                return {
                    "error": f"[{response.status_code}] {error_msg}",
                    "category": category,
                    "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                    "total": 0,
                    "items": []
                }
        except Exception as e:
            return {
                "error": f"요청 실패: {str(e)}",
                "category": category,
                "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                "total": 0,
                "items": []
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
