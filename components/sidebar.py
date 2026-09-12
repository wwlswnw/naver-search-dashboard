import streamlit as st
from datetime import date, timedelta
from typing import Tuple, List, Dict, Any
from config.settings import settings

def render_sidebar() -> Dict[str, Any]:
    """Render the sidebar controls and return the configured search parameters."""
    st.sidebar.title("🔍 검색 & 분석 설정")
    st.sidebar.markdown("---")

    # Initialize Search History in Session State
    if "search_history" not in st.session_state:
        st.session_state.search_history = [
            "신규정책, 하반기",
            "아이폰, 갤럭시",
            "다이어트, 단백질",
            "인공지능, 챗봇, 생성형 AI"
        ]

    if "current_keywords" not in st.session_state:
        st.session_state.current_keywords = "신규정책, 하반기"

    # 1. API Credentials
    env_id, env_secret = settings.get_credentials()
    has_env = bool(env_id and env_secret)

    with st.sidebar.expander("🔑 네이버 API 인증 키 상태", expanded=not has_env):
        if has_env:
            st.success("✅ 네이버 API 인증 키가 정상 연결되었습니다.")
            override_key = st.checkbox("다른 API 키로 직접 변경하기", value=False)
            if override_key:
                custom_id = st.text_input("새 Client ID", value="", key="custom_cid")
                custom_secret = st.text_input("새 Client Secret", value="", key="custom_csec")
            else:
                custom_id, custom_secret = "", ""
        else:
            st.info("🔒 네이버 API 인증 키를 입력해 주세요.")
            custom_id = st.text_input("Client ID", value="", key="manual_cid")
            custom_secret = st.text_input("Client Secret", value="", key="manual_csec")

        client_id = custom_id.strip() if custom_id.strip() else env_id
        client_secret = custom_secret.strip() if custom_secret.strip() else env_secret

    st.sidebar.markdown("### 🏷️ 검색어 입력")

    # Quick Select from History / Presets
    history_options = ["직접 입력"] + st.session_state.search_history
    selected_history = st.sidebar.selectbox(
        "🕒 최근 검색어 / 빠른 선택",
        options=history_options,
        index=0,
        help="이전에 검색했던 키워드를 클릭 한 번으로 빠르게 다시 불러옵니다."
    )

    default_kw_value = selected_history if selected_history != "직접 입력" else st.session_state.current_keywords

    keyword_input = st.sidebar.text_input(
        "검색 키워드 (쉼표 `,` 로 구분)",
        value=default_kw_value,
        placeholder="예: 신규정책, 하반기 또는 아이폰, 갤럭시",
        help="최대 5개까지 입력 가능합니다."
    )

    keywords = [k.strip() for k in keyword_input.split(",") if k.strip()]

    # Save to history if new
    if keyword_input and keyword_input not in st.session_state.search_history:
        st.session_state.search_history.insert(0, keyword_input)
        if len(st.session_state.search_history) > 8:
            st.session_state.search_history.pop()

    st.session_state.current_keywords = keyword_input

    st.sidebar.markdown("### 📅 기간 및 트렌드 옵션")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "시작일",
            value=date.today() - timedelta(days=90),
            min_value=date(2016, 1, 1),
            max_value=date.today()
        )
    with col2:
        end_date = st.date_input(
            "종료일",
            value=date.today(),
            min_value=date(2016, 1, 1),
            max_value=date.today()
        )

    # Date Filter Checkbox
    filter_by_date = st.sidebar.checkbox(
        "🛡️ 설정 기간(시작일 이후) 콘텐츠만 보기",
        value=True,
        help="시작일 이전에 작성된 오래된 과거 글(2016~2019년 등)을 검색 결과에서 자동으로 제외합니다."
    )

    time_unit = st.sidebar.selectbox(
        "트렌드 분석 단위",
        options=["date", "week", "month"],
        format_func=lambda x: {"date": "일간 (Date)", "week": "주간 (Week)", "month": "월간 (Month)"}[x],
        index=0
    )

    st.sidebar.markdown("### 🎯 타깃팅 세부 필터 (데이터랩)")
    with st.sidebar.expander("기기 / 성별 세부 필터", expanded=False):
        device_opt = st.selectbox(
            "기기 구분",
            options=["", "pc", "mo"],
            format_func=lambda x: {"": "전체", "pc": "PC", "mo": "모바일"}[x]
        )
        gender_opt = st.selectbox(
            "성별 구분",
            options=["", "m", "f"],
            format_func=lambda x: {"": "전체", "m": "남성", "f": "여성"}[x]
        )

    st.sidebar.markdown("### ⚙️ 검색 수집 옵션")
    search_display_count = st.sidebar.slider(
        "카테고리별 수집 건수",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
        help="각 채널(뉴스/블로그/카페 등)별로 가져올 문서 수"
    )

    search_sort = st.sidebar.radio(
        "검색 정렬 기준",
        options=["date", "sim"],
        format_func=lambda x: "최신순 (date) - 추천" if x == "date" else "관련도순 (sim)",
        index=0,
        horizontal=True
    )

    search_button = st.sidebar.button("🚀 인사이트 분석 시작", use_container_width=True, type="primary")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "keywords": keywords,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "start_date_obj": start_date,
        "end_date_obj": end_date,
        "filter_by_date": filter_by_date,
        "time_unit": time_unit,
        "device": device_opt if device_opt else None,
        "gender": gender_opt if gender_opt else None,
        "search_display_count": search_display_count,
        "search_sort": search_sort,
        "search_button": search_button
    }
