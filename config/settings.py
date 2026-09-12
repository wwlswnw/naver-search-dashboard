import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    # NAVER API HUB Endpoints (Official New NCP Standard)
    APIHUB_BASE_URL = "https://naverapihub.apigw.ntruss.com"
    SEARCH_API_BASE_URL = "https://naverapihub.apigw.ntruss.com/search/v1"
    DATALAB_API_BASE_URL = "https://naverapihub.apigw.ntruss.com/search-trend/v1/search"
    
    # Legacy Endpoints (Fallback)
    LEGACY_SEARCH_BASE_URL = "https://openapi.naver.com/v1/search"
    LEGACY_DATALAB_BASE_URL = "https://openapi.naver.com/v1/datalab/search"

    SEARCH_CATEGORIES = {
        "news": "뉴스",
        "blog": "블로그",
        "webkr": "웹문서",
        "image": "이미지",
        "kin": "지식iN",
        "local": "지역(플레이스)",
        "cafearticle": "카페글",
        "encyc": "백과사전"
    }

    @staticmethod
    def get_credentials(client_id_override: str = None, client_secret_override: str = None):
        """Get API credentials, preferring UI inputs if provided, else fallback to .env."""
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        client_id = client_id_override.strip() if client_id_override else os.getenv("NAVER_CLIENT_ID", "").strip()
        client_secret = client_secret_override.strip() if client_secret_override else os.getenv("NAVER_CLIENT_SECRET", "").strip()
        return client_id, client_secret


settings = Settings()
