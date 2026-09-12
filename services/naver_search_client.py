import requests
import hashlib
import urllib.parse
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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _get_legacy_headers(self) -> Dict[str, str]:
        cid = str(self.client_id).strip().strip('"').strip("'")
        csec = str(self.client_secret).strip().strip('"').strip("'")
        return {
            "X-Naver-Client-Id": cid,
            "X-Naver-Client-Secret": csec,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _get_direct_search_url(self, category: str, query: str) -> str:
        """Return the exact direct search link on Naver for the specific category."""
        encoded = urllib.parse.quote(query)
        urls = {
            "news": f"https://search.naver.com/search.naver?where=news&query={encoded}&sm=tab_opt&sort=1",
            "blog": f"https://search.naver.com/search.naver?where=blog&query={encoded}",
            "cafearticle": f"https://search.naver.com/search.naver?where=article&query={encoded}",
            "kin": f"https://search.naver.com/search.naver?where=kin&query={encoded}",
            "webkr": f"https://search.naver.com/search.naver?where=web&query={encoded}",
            "image": f"https://search.naver.com/search.naver?where=image&query={encoded}",
            "local": f"https://map.naver.com/p/search/{encoded}",
            "encyc": f"https://terms.naver.com/search.naver?query={encoded}"
        }
        return urls.get(category, f"https://search.naver.com/search.naver?query={encoded}")

    def _generate_mock_items(self, category: str, query: str, display: int = 30) -> Dict[str, Any]:
        """Generate realistic mock data with direct search links to Naver."""
        base_hash = int(hashlib.md5(f"{category}_{query}".encode()).hexdigest(), 16)
        total_counts = {
            "news": 125000 + (base_hash % 850000),
            "blog": 980000 + (base_hash % 4500000),
            "webkr": 2400000 + (base_hash % 9000000),
            "image": 3100000 + (base_hash % 12000000),
            "kin": 450000 + (base_hash % 1500000),
            "local": 4500 + (base_hash % 25000),
            "cafearticle": 1500000 + (base_hash % 6000000),
            "encyc": 1200 + (base_hash % 8000)
        }
        total = total_counts.get(category, 500000)
        direct_link = self._get_direct_search_url(category, query)

        items = []
        templates = {
            "news": [
                f"[단독] '{query}' 시장 급성장... 업계 선두 기업들 신기술 경쟁 본격화",
                f"2026년 하반기 트렌드 분석: '{query}' 중심으로 소비자 반응 폭발",
                f"전문가가 분석한 '{query}'의 미래 전망과 핵심 체크포인트 3가지",
                f"글로벌 시장 강타한 '{query}' 열풍, 국내 시장 파급 효과는?",
                f"'{query}' 관련 신규 정책 발표... 시장 참여자들의 기대감 고조"
            ],
            "blog": [
                f"[솔직 후기] 직접 체험해본 '{query}', 장점과 단점 완벽 정리!",
                f"'{query}' 입문자를 위한 필수 가이드 (내돈내산 3개월 비교 후기)",
                f"초보자도 10분 만에 마스터하는 '{query}' 꿀팁 총정리",
                f"요즘 가장 핫한 '{query}' 실사용 리뷰와 추천 조합",
                f"'{query}' 선택 전 반드시 확인해야 할 5가지 팁"
            ],
            "cafearticle": [
                f"[질문/정보] 회원님들은 '{query}' 보통 어디서 구매하시나요?",
                f"'{query}' 실사용자 모임 - 요즘 인기 있는 모델 추천 부탁드립니다",
                f"오늘자 '{query}' 특가 정보 및 커뮤니티 할인 코드 공유합니다",
                f"'{query}' 2주 사용해본 후기 및 다른 회원님들과 비교 토론",
                f"초보 회원들을 위한 '{query}' 유의사항 Q&A 정리"
            ],
            "kin": [
                f"Q. '{query}' 시작하려고 하는데 어떤 제품/방법이 제일 좋나요?",
                f"Q. 요즘 '{query}'가 유행이라던데 부작용이나 주의할 점이 있나요?",
                f"Q. '{query}' 비교 추천 부탁드립니다 (가성비 vs 프리미엄)",
                f"Q. '{query}' 관련 자격증이나 공부는 어떻게 시작하나요?",
                f"Q. '{query}' 평균 가격대와 유지 비용이 궁금합니다."
            ],
            "webkr": [
                f"{query} 공식 가이드 & 최신 데이터 백서 - Market Insights",
                f"위키피디아: {query}의 정의, 역사 및 최신 기술 응용 사례",
                f"글로벌 리서치: {query} 시장 규모 및 연평균 성장률(CAGR) 보고서",
                f"{query} 아키텍처 및 산업 생태계 개요 - 공식 포털",
                f"2026 {query} 트렌드 리포트 및 소비자 행동 데이터 분석"
            ],
            "encyc": [
                f"두산백과: {query} (개념 및 학술적 분류 체계)",
                f"IT용어사전: {query}의 표준 기술 규격과 핵심 원리",
                f"한국민족문화대백과: {query}의 발전 과정과 역사적 의의"
            ],
            "local": [
                f"강남구 {query} 전문 스튜디오 본점 (역삼역 3번 출구)",
                f"홍대 {query} 플래그십 라운지 & 쇼룸 (연남동)",
                f"판교 {query} R&D 혁신 센터 (테크노밸리)",
                f"성수동 {query} 팝업 스토어 & 복합 문화공간",
                f"부산 서면 {query} 영남 지사 및 체험관"
            ],
            "image": [
                "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&q=80",
                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500&q=80",
                "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&q=80",
                "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500&q=80"
            ]
        }

        sample_titles = templates.get(category, templates["news"])
        for idx in range(min(display, 15)):
            t_idx = idx % len(sample_titles)
            title = sample_titles[t_idx]
            if category == "image":
                items.append({
                    "title": f"{query} 고화질 비주얼 이미지 #{idx+1}",
                    "link": direct_link,
                    "thumbnail": sample_titles[idx % len(sample_titles)],
                    "sizeheight": "400",
                    "sizewidth": "600"
                })
            elif category == "local":
                items.append({
                    "title": title,
                    "link": direct_link,
                    "category": f"서비스/전문점 > {query}",
                    "description": f"{query} 관련 최신 서비스 및 전문 매장입니다.",
                    "telephone": f"02-{1000 + idx}-{5000 + idx}",
                    "address": f"서울특별시 강남구 테헤란로 {100 + idx}",
                    "roadAddress": f"서울특별시 강남구 테헤란로 {100 + idx}길 5"
                })
            else:
                items.append({
                    "title": title,
                    "link": direct_link,
                    "originallink": direct_link,
                    "description": f"<b>{query}</b>에 대한 실시간 최신 정보와 사용자 분석 리포트입니다. 최근 시장에서 <b>{query}</b>에 대한 관심이 급증하며 다양한 콘텐츠와 피드백이 생성되고 있습니다.",
                    "pubDate": (datetime.now() - timedelta(hours=idx * 6)).strftime("%a, %d %b %Y %H:%M:00 +0900")
                })

        return {
            "category": category,
            "category_name": settings.SEARCH_CATEGORIES.get(category, category),
            "total": total,
            "start": 1,
            "display": len(items),
            "items": items,
            "is_demo": True
        }

    def search_category(
        self,
        category: str,
        query: str,
        display: int = 50,
        start: int = 1,
        sort: str = "sim"
    ) -> Dict[str, Any]:
        """Search a specific category on Naver using NAVER API HUB with robust link resolution."""
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
            # 1. Try NAVER API HUB (NCP) with generous timeout
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=12)
            
            # 2. Try Legacy endpoint if needed
            if response.status_code != 200:
                legacy_url = f"{settings.LEGACY_SEARCH_BASE_URL}/{category}.json"
                resp_legacy = requests.get(legacy_url, headers=self._get_legacy_headers(), params=params, timeout=12)
                if resp_legacy.status_code == 200:
                    response = resp_legacy

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                # Ensure all items have valid non-empty links
                for it in items:
                    if not it.get("link"):
                        it["link"] = self._get_direct_search_url(category, query)
                return {
                    "category": category,
                    "category_name": settings.SEARCH_CATEGORIES.get(category, category),
                    "total": data.get("total", 0),
                    "start": data.get("start", 1),
                    "display": data.get("display", 0),
                    "items": items,
                    "is_demo": False
                }
            else:
                return self._generate_mock_items(category, query, display)
        except Exception:
            return self._generate_mock_items(category, query, display)

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
