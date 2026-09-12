import json
import urllib.request
import requests
from typing import List, Dict, Any, Optional
from config.settings import settings

class NaverDatalabClient:
    def __init__(self, client_id: str = "", client_secret: str = ""):
        self.client_id = (client_id.strip() if client_id else "") or settings.DEFAULT_CLIENT_ID
        self.client_secret = (client_secret.strip() if client_secret else "") or settings.DEFAULT_CLIENT_SECRET
        self.url = settings.DATALAB_API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        cid = str(self.client_id).strip().strip('"').strip("'")
        csec = str(self.client_secret).strip().strip('"').strip("'")
        return {
            "X-NCP-APIGW-API-KEY-ID": cid,
            "X-NCP-APIGW-API-KEY": csec,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def _get_legacy_headers(self) -> Dict[str, str]:
        cid = str(self.client_id).strip().strip('"').strip("'")
        csec = str(self.client_secret).strip().strip('"').strip("'")
        return {
            "X-Naver-Client-Id": cid,
            "X-Naver-Client-Secret": csec,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def get_search_trend(
        self,
        keywords: List[str],
        start_date: str,
        end_date: str,
        time_unit: str = "date",
        device: Optional[str] = None,
        gender: Optional[str] = None,
        ages: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Fetch search trend from NAVER API HUB using dual-strategy HTTP connection."""
        keyword_groups = []
        for kw in keywords[:5]:
            trimmed = kw.strip()
            if trimmed:
                keyword_groups.append({
                    "groupName": trimmed,
                    "keywords": [trimmed]
                })

        if not keyword_groups:
            return {"error": "유효한 검색어가 없습니다."}

        payload: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "keywordGroups": keyword_groups
        }

        if device and device in ["pc", "mo"]:
            payload["device"] = device
        if gender and gender in ["m", "f"]:
            payload["gender"] = gender
        if ages:
            payload["ages"] = ages

        json_bytes = json.dumps(payload).encode('utf-8')
        headers = self._get_headers()

        # Strategy 1: urllib.request POST
        try:
            req = urllib.request.Request(self.url, data=json_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    data["is_demo"] = False
                    return data
        except Exception:
            pass

        # Strategy 2: requests.post
        try:
            r = requests.post(self.url, headers=headers, data=json.dumps(payload), timeout=12)
            if r.status_code == 200:
                data = r.json()
                data["is_demo"] = False
                return data
        except Exception:
            pass

        # Strategy 3: Legacy endpoint
        try:
            r_leg = requests.post(settings.LEGACY_DATALAB_BASE_URL, headers=self._get_legacy_headers(), data=json.dumps(payload), timeout=12)
            if r_leg.status_code == 200:
                data = r_leg.json()
                data["is_demo"] = False
                return data
        except Exception:
            pass

        return {"error": "데이터랩 검색어 트렌드를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요."}
