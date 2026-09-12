import streamlit as st
from typing import Dict, Any, List
from components.sidebar import render_sidebar
from components.kpi_metrics import render_kpi_metrics
from components.trend_charts import render_trend_charts
from components.channel_analysis import render_channel_analysis
from components.result_explorer import render_result_explorer
from components.interpretation_guide import render_interpretation_guide
from components.advanced_analytics import render_advanced_analytics
from services.naver_search_client import NaverSearchClient
from services.naver_datalab_client import NaverDatalabClient




# 1. Page Configuration
st.set_page_config(
    page_title="NAVER Market Insight Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apple-inspired Minimalist Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Plus Jakarta Sans", "Noto Sans KR", "Helvetica Neue", sans-serif;
        -webkit-font-smoothing: antialiased;
        color: #1D1D1F;
    }

    /* Apple Canvas Background */
    .stApp {
        background-color: #F5F5F7;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 1360px;
    }

    /* Apple-style Hero Title */
    .apple-hero-container {
        margin-bottom: 1.8rem;
        padding: 0.5rem 0 0.8rem 0;
    }

    .apple-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E8E8ED;
        color: #1D1D1F;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 4px 12px;
        border-radius: 980px;
        margin-bottom: 0.6rem;
    }

    .apple-hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        color: #1D1D1F;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }

    .apple-hero-sub {
        color: #86868B;
        font-size: 1.02rem;
        font-weight: 400;
        letter-spacing: -0.01em;
        line-height: 1.5;
    }

    /* Apple Segmented Control Top Tabs */
    div[data-testid="stTabs"] > div[role="tablist"] {
        gap: 4px;
        background-color: #E8E8ED;
        padding: 4px;
        border-radius: 14px;
        border: none;
        margin-bottom: 1.5rem;
    }

    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        border-radius: 10px !important;
        color: #6E6E73 !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }

    /* Apple Card Containers */
    div[data-testid="stExpander"] {
        border-radius: 18px !important;
        border: 1px solid #E5E5EA !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 20px -2px rgba(0,0,0,0.03) !important;
        overflow: hidden;
    }

    /* Apple Primary Action Button */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #0071E3 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 980px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.6rem !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.28) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #0077ED !important;
        transform: scale(1.015) !important;
        box-shadow: 0 6px 18px rgba(0, 113, 227, 0.38) !important;
    }

    /* Sidebar Styling & Clean Typography */
    section[data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #E5E5EA !important;
        min-width: 320px !important;
    }

    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #1D1D1F !important;
        letter-spacing: -0.02em !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label span {
        white-space: nowrap !important;
        font-size: 0.88rem !important;
        word-break: keep-all !important;
        color: #1D1D1F !important;
    }

    /* Apple Pill Badges in Sidebar */
    section[data-testid="stSidebar"] div[data-testid="stPills"] button {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 5px 12px !important;
        border-radius: 980px !important;
        border: 1px solid #D2D2D7 !important;
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        transition: all 0.15s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stPills"] button[aria-pressed="true"] {
        background: #1D1D1F !important;
        color: #FFFFFF !important;
        border-color: #1D1D1F !important;
    }

    /* Native containers rounded border */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        border: 1px solid #E5E5EA !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Live Data Fetching Functions
def fetch_datalab_data(
    client_id: str,
    client_secret: str,
    keywords: tuple,
    start_date: str,
    end_date: str,
    time_unit: str,
    device: str,
    gender: str,
    ages: list = None
) -> Dict[str, Any]:
    datalab_client = NaverDatalabClient(client_id, client_secret)
    return datalab_client.get_search_trend(
        keywords=list(keywords),
        start_date=start_date,
        end_date=end_date,
        time_unit=time_unit,
        device=device,
        gender=gender,
        ages=ages
    )

def fetch_search_data(
    client_id: str,
    client_secret: str,
    keywords: tuple,
    display_count: int,
    sort_order: str,
    categories: list = None,
    exclude_keywords: list = None
) -> Dict[str, Dict[str, Any]]:
    search_client = NaverSearchClient(client_id, client_secret)
    all_results = {}
    for kw in keywords:
        all_results[kw] = search_client.search_all_categories(
            query=kw,
            display=display_count,
            sort=sort_order,
            categories=categories,
            exclude_keywords=exclude_keywords
        )
    return all_results

def main():
    # 1. Apple-style Hero Header
    st.markdown("""
        <div class="apple-hero-container">
            <div class="apple-badge">⚡ NAVER MARKET INSIGHT STUDIO</div>
            <div class="apple-hero-title">실시간 데이터로 읽는 시장의 흐름.</div>
            <div class="apple-hero-sub">
                8개 채널의 콘텐츠 반응도와 기간별 검색어 트렌드를 실시간으로 교차 분석하는 탐색적 데이터 분석 스튜디오입니다.
            </div>
        </div>
    """, unsafe_allow_html=True)


    # 2. Render Sidebar
    params = render_sidebar()

    client_id = params["client_id"]
    client_secret = params["client_secret"]
    keywords = params["keywords"]

    # Check API Keys
    if not client_id or not client_secret:
        st.warning("⚠️ **네이버 API 인증 키가 필요합니다.**")
        st.info(
            """
            **네이버 API 키 설정 안내:**
            1. [네이버 클라우드 플랫폼 NAVER API HUB](https://api.ncloud-docs.com/docs/naver-api-hub-overview)에서 어플리케이션을 등록합니다.
            2. 발급받은 `Client ID`와 `Client Secret`을 좌측 사이드바의 **🔑 네이버 API 인증 키 설정**에 입력하거나, 프로젝트 루트의 `.env` 파일에 저장해 주세요.
            """
        )
        return

    if not keywords:
        st.info("👈 **좌측 사이드바에서 분석하고 싶은 검색어를 쉼표(,)로 구분해 입력해 주세요!** (예: `다이어트, 단백질, 헬스` 또는 `아이폰, 갤럭시`)")
        st.markdown("""
<div style="background: #F8FAFC; border: 1.5px dashed #CBD5E1; border-radius: 16px; padding: 2rem; text-align: center; margin-top: 1rem;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧭</div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #1E293B;">실시간 네이버 마켓 인사이트를 탐색할 준비가 되었습니다!</div>
    <div style="font-size: 0.9rem; color: #64748B; margin-top: 0.3rem;">비교하고 싶은 키워드를 좌측에 입력하고 [🚀 인사이트 분석 시작]을 누르면 8개 채널 점유율, 시계열 트렌드, 4분면 매트릭스가 실시간으로 분석됩니다.</div>
</div>
""", unsafe_allow_html=True)
        return


    # 3. Data Fetching
    with st.spinner("네이버 API HUB로부터 실시간 데이터를 고속 수집 및 시각화 중입니다..."):
        try:
            trend_data = fetch_datalab_data(
                client_id=client_id,
                client_secret=client_secret,
                keywords=tuple(keywords),
                start_date=params["start_date"],
                end_date=params["end_date"],
                time_unit=params["time_unit"],
                device=params["device"],
                gender=params["gender"],
                ages=params.get("ages")
            )

            search_results = fetch_search_data(
                client_id=client_id,
                client_secret=client_secret,
                keywords=tuple(keywords),
                display_count=params["search_display_count"],
                sort_order=params["search_sort"],
                categories=params.get("selected_channels"),
                exclude_keywords=params.get("exclude_keywords")
            )
        except Exception as e:
            st.error(f"데이터 수집 중 오류가 발생했습니다: {str(e)}")
            return


    # 4. Top KPI Cards (Always visible)
    render_kpi_metrics(keywords, search_results, trend_data)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 5. Multi-Tab Studio Application Views
    main_tabs = st.tabs([
        "📊 1. 마켓 점유율 & 채널 분석",
        "📈 2. 시계열 트렌드 랩",
        "🔮 3. 심층 EDA 랩 (레이더·4분면·요일리듬)",
        "🔎 4. 채널별 콘텐츠 탐색기",
        "📖 5. 마켓 인사이트 가이드북"
    ])

    # Tab 1: Channel & Market Share Analysis
    with main_tabs[0]:
        render_channel_analysis(keywords, search_results)

    # Tab 2: Trend Time-Series Lab
    with main_tabs[1]:
        render_trend_charts(trend_data, keywords)

    # Tab 3: Advanced EDA Lab (Radar, 4-Quadrant Bubble, Weekly Rhythm)
    with main_tabs[2]:
        render_advanced_analytics(keywords, search_results, trend_data)

    # Tab 4: Deep-Dive Content Explorer
    with main_tabs[3]:
        render_result_explorer(
            keywords=keywords,
            search_results_by_keyword=search_results,
            start_date=params.get("start_date"),
            end_date=params.get("end_date"),
            filter_by_date=params.get("filter_by_date", True)
        )

    # Tab 5: Universal Interpretation Guide
    with main_tabs[4]:
        render_interpretation_guide()




if __name__ == "__main__":
    main()
