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
    page_title="네이버 마켓 인사이트 스튜디오",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS - Modern Studio Dashboard Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans KR', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Studio Hero Title Gradient */
    .studio-hero-title {
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 40%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }

    /* Top Level Main Tabs Styling */
    div[data-testid="stTabs"] > div[role="tablist"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
    }

    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.25rem !important;
        border-radius: 10px !important;
        color: #64748B !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }

    /* Expander Styling */
    div[data-testid="stExpander"] {
        border-radius: 14px !important;
        border: 1.5px solid #E2E8F0 !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }

    /* Primary Button Styling */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
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
    # 1. Vibrant Studio Hero Header
    st.markdown("""
        <div style="margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.2rem;">
                <span style="background: linear-gradient(135deg, #4F46E5, #7C3AED); color: white; font-size: 0.75rem; font-weight: 800; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.05em;">STUDIO EDITION</span>
                <span style="color: #64748B; font-size: 0.85rem; font-weight: 600;">NAVER MARKET INSIGHT EDA</span>
            </div>
            <div class="studio-hero-title">⚡ 네이버 마켓 인사이트 스튜디오</div>
            <div style="color: #475569; font-size: 0.95rem; font-weight: 500;">
                8개 채널의 콘텐츠 반응도와 기간별 검색어 트렌드를 실시간으로 교차 분석하는 탐색적 데이터 분석(EDA) 스튜디오입니다.
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
