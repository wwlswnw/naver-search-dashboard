import json
import requests
from typing import List, Dict, Any, Optional
from config.settings import settings

class NaverDatalabClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id.strip() if client_id else ""
        self.client_secret = client_secret.strip() if client_secret else ""
        self.url = settings.DATALAB_API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
            "Content-Type": "application/json"
        }

    def _get_legacy_headers(self) -> Dict[str, str]:
        return {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "Content-Type": "application/json"
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
        """
        Fetch search trend from NAVER API HUB / DataLab.
        - keywords: up to 5 keywords
        - start_date / end_date: 'YYYY-MM-DD'
        - time_unit: 'date', 'week', 'month'
        - device: '', 'pc', 'mo'
        - gender: '', 'm', 'f'
        - ages: list of age codes
        """
        if not self.client_id or not self.client_secret:
            return {"error": "네이버 Client ID와 Client Secret이 설정되지 않았습니다."}

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

        try:
            # 1. Try NAVER API HUB endpoint
            response = requests.post(
                self.url,
                headers=self._get_headers(),
                data=json.dumps(payload),
                timeout=10
            )

            # 2. Fallback to legacy endpoint if not 200
            if response.status_code != 200:
                resp_legacy = requests.post(
                    settings.LEGACY_DATALAB_BASE_URL,
                    headers=self._get_legacy_headers(),
                    data=json.dumps(payload),
                    timeout=10
                )
                if resp_legacy.status_code == 200:
                    response = resp_legacy

            if response.status_code == 200:
                return response.json()
            else:
                try:
                    err_json = response.json()
                    error_msg = (
                        err_json.get("errorMessage")
                        or err_json.get("errMsg")
                        or err_json.get("error", {}).get("message")
                        or response.text
                    )
                except Exception:
                    error_msg = response.text
                return {"error": f"[{response.status_code}] {error_msg}"}
        except Exception as e:
            return {"error": f"검색어 트렌드 API 요청 실패: {str(e)}"}
