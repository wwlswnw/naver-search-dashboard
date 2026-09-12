import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root safely
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
try:
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH)
except Exception:
    pass

class Settings:
    # Default Credentials Fallback for Seamless Cloud Deployment
    DEFAULT_CLIENT_ID = "izyz5ioxfj"
    DEFAULT_CLIENT_SECRET = "71wxMTzbiYoUPXEE3OM8FTRX8A0q255oJc6848DB"

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
        """Get API credentials safely with zero KeyError risk: UI override -> st.secrets -> .env -> default fallback."""
        try:
            if ENV_PATH.exists():
                load_dotenv(dotenv_path=ENV_PATH, override=True)
        except Exception:
            pass
        
        # 1. Direct override from UI
        client_id = client_id_override.strip() if client_id_override else ""
        client_secret = client_secret_override.strip() if client_secret_override else ""

        # 2. Check st.secrets safely (Streamlit Community Cloud)
        if not client_id or not client_secret:
            try:
                import streamlit as st
                sec = getattr(st, "secrets", None)
                if sec is not None:
                    # Check direct keys
                    for k in ["NAVER_CLIENT_ID", "naver_client_id", "CLIENT_ID", "client_id", "ncp_client_id", "NCP_CLIENT_ID"]:
                        try:
                            val = sec.get(k)
                            if val:
                                client_id = client_id or str(val).strip().strip('"').strip("'")
                                break
                        except Exception:
                            pass
                    for k in ["NAVER_CLIENT_SECRET", "naver_client_secret", "CLIENT_SECRET", "client_secret", "ncp_client_secret", "NCP_CLIENT_SECRET"]:
                        try:
                            val = sec.get(k)
                            if val:
                                client_secret = client_secret or str(val).strip().strip('"').strip("'")
                                break
                        except Exception:
                            pass
            except Exception:
                pass

        # 3. Check local os.getenv (.env)
        try:
            if not client_id:
                client_id = os.getenv("NAVER_CLIENT_ID", "").strip()
            if not client_secret:
                client_secret = os.getenv("NAVER_CLIENT_SECRET", "").strip()
        except Exception:
            pass

        # 4. Fallback to default verified credentials
        if not client_id:
            client_id = Settings.DEFAULT_CLIENT_ID
        if not client_secret:
            client_secret = Settings.DEFAULT_CLIENT_SECRET

        return client_id, client_secret


settings = Settings()
