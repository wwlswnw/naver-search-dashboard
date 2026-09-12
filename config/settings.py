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
    # Verified Working Production Credentials (NAVER API HUB)
    DEFAULT_CLIENT_ID = "20n73mmo06"
    DEFAULT_CLIENT_SECRET = "aMj7RJAcdTNNvjgrk6MjT6iUFKczLBwp3rcVRiA9"

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
        """Get API credentials: UI override -> .env -> verified default credentials."""
        # 1. Direct override from UI (if user typed something in UI)
        if client_id_override and client_id_override.strip() and client_secret_override and client_secret_override.strip():
            return client_id_override.strip(), client_secret_override.strip()

        # 2. Check local .env
        client_id = ""
        client_secret = ""
        try:
            if ENV_PATH.exists():
                load_dotenv(dotenv_path=ENV_PATH, override=True)
            cid_env = os.getenv("NAVER_CLIENT_ID", "").strip()
            csec_env = os.getenv("NAVER_CLIENT_SECRET", "").strip()
            # If valid new key in .env
            if cid_env and cid_env != "izyz5ioxfj":
                client_id = cid_env
                client_secret = csec_env
        except Exception:
            pass

        # 3. Check st.secrets (ignore deprecated old key if present)
        if not client_id or not client_secret:
            try:
                import streamlit as st
                sec = getattr(st, "secrets", None)
                if sec is not None:
                    cid_sec = str(sec.get("NAVER_CLIENT_ID", "")).strip().strip('"').strip("'")
                    csec_sec = str(sec.get("NAVER_CLIENT_SECRET", "")).strip().strip('"').strip("'")
                    if cid_sec and cid_sec != "izyz5ioxfj" and csec_sec:
                        client_id = cid_sec
                        client_secret = csec_sec
            except Exception:
                pass

        # 4. Enforce Verified Working Credentials
        if not client_id or client_id == "izyz5ioxfj":
            client_id = Settings.DEFAULT_CLIENT_ID
        if not client_secret or client_secret == "71wxMTzbiYoUPXEE3OM8FTRX8A0q255oJc6848DB":
            client_secret = Settings.DEFAULT_CLIENT_SECRET

        return client_id, client_secret


settings = Settings()
