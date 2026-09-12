import streamlit as st
from datetime import date, timedelta
from typing import Tuple, List, Dict, Any
from config.settings import settings

def render_sidebar() -> Dict[str, Any]:
    """Render the sidebar controls and return the configured search parameters."""
    st.sidebar.title("🔍 검색 & 분석 설정")
    st.sidebar.markdown("---")

    # 1. API Credentials
    env_id, env_secret = settings.get_credentials()
    has_env = bool(env_id and env_secret)

    with st.sidebar.expander("🔑 네이버 API 인증 키 설정 (브라우저 전용)", expanded=not has_env):
        if has_env:
            st.success("✅ `.env` 파일에서 API 키를 불러왔습니다.")
            custom_id = st.text_input("Client ID (재지정 시 입력)", value="", type="password")
            custom_secret = st.text_input("Client Secret (재지정 시 입력)", value="", type="password")
        else:
            st.info("🔒 키는 브라우저 메모리에만 유지되며 파일에 저장되지 않습니다.")
            st.markdown("[👉 네이버 개발자 센터에서 키 발급받기](https://developers.naver.com/apps/#/register)")
            custom_id = st.text_input("Client ID", value="", type="password", placeholder="네이버 Client ID (약 20자리)")
            custom_secret = st.text_input("Client Secret", value="", type="password", placeholder="네이버 Client Secret")

        client_id = custom_id.strip() if custom_id.strip() else env_id
        client_secret = custom_secret.strip() if custom_secret.strip() else env_secret

    st.sidebar.markdown("### 🏷️ 검색어 입력")
    keyword_input = st.sidebar.text_input(
        "검색어 (쉼표 `,` 로 구분)",
        value="",
        placeholder="예: 다이어트, 단백질, 헬스",
        help="최대 5개까지 입력 가능합니다. (데이터랩 트렌드 API 기준)"
    )

    keywords = [k.strip() for k in keyword_input.split(",") if k.strip()]


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
        value=30,
        step=10,
        help="각 채널(뉴스/블로그/카페 등)별로 가져올 최신/관련 문서 수 (최대 100건)"
    )

    search_sort = st.sidebar.radio(
        "검색 정렬 기준",
        options=["sim", "date"],
        format_func=lambda x: "관련도순 (sim)" if x == "sim" else "최신순 (date)",
        horizontal=True
    )

    search_button = st.sidebar.button("🚀 인사이트 분석 시작", use_container_width=True, type="primary")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "keywords": keywords,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "time_unit": time_unit,
        "device": device_opt if device_opt else None,
        "gender": gender_opt if gender_opt else None,
        "search_display_count": search_display_count,
        "search_sort": search_sort,
        "search_button": search_button
    }
