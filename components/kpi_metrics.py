import streamlit as st
from typing import Dict, Any, List

def render_kpi_metrics(
    keywords: List[str],
    search_results_by_keyword: Dict[str, Dict[str, Any]],
    trend_data: Dict[str, Any]
):
    """Render vibrant studio-style KPI metrics cards using clean Streamlit columns."""
    # Calculate metrics
    keyword_totals = {}
    for kw in keywords:
        total_items = 0
        cat_data = search_results_by_keyword.get(kw, {})
        for cat_info in cat_data.values():
            if isinstance(cat_info, dict):
                total_items += cat_info.get("total", 0)
        keyword_totals[kw] = total_items

    top_keyword = max(keyword_totals, key=keyword_totals.get) if keyword_totals else "-"
    top_volume = keyword_totals.get(top_keyword, 0)
    all_volume_sum = sum(keyword_totals.values())

    trend_results = trend_data.get("results", []) if trend_data else []
    peak_kw = "-"
    peak_date = "-"
    if trend_results:
        max_ratio = -1
        for res in trend_results:
            kw_title = res.get("title", "")
            for dp in res.get("data", []):
                r = dp.get("ratio", 0)
                if r > max_ratio:
                    max_ratio = r
                    peak_kw = kw_title
                    peak_date = dp.get("period", "")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kw_subtext = ', '.join(keywords[:2]) + ('...' if len(keywords) > 2 else '')
        st.markdown(f"""
<div style="background: #FFFFFF; border-radius: 18px; padding: 1.25rem 1.35rem; border: 1px solid #E5E5EA; box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #86868B; letter-spacing: 0.04em;">분석 키워드</span>
        <span style="background: #F2F2F7; color: #0071E3; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 980px;">TARGETS</span>
    </div>
    <div style="font-size: 1.95rem; font-weight: 800; color: #1D1D1F; margin-top: 0.45rem; letter-spacing: -0.03em;">
        {len(keywords)} <span style="font-size: 1.05rem; font-weight: 600; color: #86868B;">개</span>
    </div>
    <div style="font-size: 0.82rem; color: #86868B; margin-top: 0.35rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {kw_subtext}
    </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        vol_display = format_kpi_volume(all_volume_sum)
        st.markdown(f"""
<div style="background: #FFFFFF; border-radius: 18px; padding: 1.25rem 1.35rem; border: 1px solid #E5E5EA; box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #86868B; letter-spacing: 0.04em;">8개 채널 총 문서량</span>
        <span style="background: #E8F8EE; color: #34C759; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 980px;">TOTAL</span>
    </div>
    <div style="font-size: 1.85rem; font-weight: 800; color: #1D1D1F; margin-top: 0.45rem; letter-spacing: -0.03em;">
        {vol_display} <span style="font-size: 1.05rem; font-weight: 600; color: #86868B;">건</span>
    </div>
    <div style="font-size: 0.8rem; color: #86868B; margin-top: 0.35rem; font-weight: 500;">
        누적 합계 ({all_volume_sum:,} 건)
    </div>
</div>
""", unsafe_allow_html=True)

    with col3:
        top_vol_display = format_kpi_volume(top_volume)
        st.markdown(f"""
<div style="background: #FFFFFF; border-radius: 18px; padding: 1.25rem 1.35rem; border: 1px solid #E5E5EA; box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #86868B; letter-spacing: 0.04em;">최다 점유 키워드</span>
        <span style="background: #F5EEFC; color: #AF52DE; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 980px;">LEADER</span>
    </div>
    <div style="font-size: 1.7rem; font-weight: 800; color: #1D1D1F; margin-top: 0.45rem; letter-spacing: -0.02em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {top_keyword}
    </div>
    <div style="font-size: 0.8rem; color: #86868B; margin-top: 0.35rem; font-weight: 500;">
        점유량 {top_vol_display} 건
    </div>
</div>
""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
<div style="background: #FFFFFF; border-radius: 18px; padding: 1.25rem 1.35rem; border: 1px solid #E5E5EA; box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #86868B; letter-spacing: 0.04em;">트렌드 최대 피크</span>
        <span style="background: #FFF4E5; color: #FF9500; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 980px;">PEAK</span>
    </div>
    <div style="font-size: 1.6rem; font-weight: 800; color: #1D1D1F; margin-top: 0.45rem; letter-spacing: -0.02em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {peak_kw if peak_kw != '-' else '데이터 없음'}
    </div>
    <div style="font-size: 0.8rem; color: #86868B; margin-top: 0.35rem; font-weight: 500;">
        {peak_date if peak_date != '-' else '기간 내 분석'} (지수 100)
    </div>
</div>
""", unsafe_allow_html=True)

