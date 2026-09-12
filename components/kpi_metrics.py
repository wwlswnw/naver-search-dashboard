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
<div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 16px; padding: 1.25rem 1.25rem; border: 1.5px solid #C7D2FE; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);">
    <div style="font-size: 0.85rem; font-weight: 700; color: #4338CA; text-transform: uppercase; letter-spacing: 0.05em;">
        🎯 분석 키워드
    </div>
    <div style="font-size: 1.85rem; font-weight: 800; color: #1E1B4B; margin-top: 0.4rem; letter-spacing: -0.02em;">
        {len(keywords)} <span style="font-size: 1rem; font-weight: 600; color: #4F46E5;">개</span>
    </div>
    <div style="font-size: 0.8rem; color: #6366F1; margin-top: 0.3rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {kw_subtext}
    </div>
</div>
""", unsafe_allow_html=True)

    def format_kpi_volume(val: int) -> str:
        if val >= 100_000_000:
            eok = val // 100_000_000
            man = (val % 100_000_000) // 10_000
            return f"{eok}억 {man:,}만"
        elif val >= 10_000:
            return f"{val // 10_000:,}만"
        return f"{val:,}"

    with col2:
        vol_display = format_kpi_volume(all_volume_sum)
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border-radius: 16px; padding: 1.25rem 1.25rem; border: 1.5px solid #BBF7D0; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);">
    <div style="font-size: 0.85rem; font-weight: 700; color: #065F46; text-transform: uppercase; letter-spacing: 0.05em;">
        📊 8개 채널 총 문서량
    </div>
    <div style="font-size: 1.65rem; font-weight: 800; color: #064E3B; margin-top: 0.4rem; letter-spacing: -0.02em;">
        {vol_display} <span style="font-size: 0.95rem; font-weight: 600; color: #10B981;">건</span>
    </div>
    <div style="font-size: 0.78rem; color: #059669; margin-top: 0.3rem; font-weight: 500;">
        누적 합계 ({all_volume_sum:,} 건)
    </div>
</div>
""", unsafe_allow_html=True)

    with col3:
        top_vol_display = format_kpi_volume(top_volume)
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%); border-radius: 16px; padding: 1.25rem 1.25rem; border: 1.5px solid #FECDD3; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.08);">
    <div style="font-size: 0.85rem; font-weight: 700; color: #9F1239; text-transform: uppercase; letter-spacing: 0.05em;">
        🏆 최다 발행 키워드
    </div>
    <div style="font-size: 1.55rem; font-weight: 800; color: #881337; margin-top: 0.4rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {top_keyword}
    </div>
    <div style="font-size: 0.78rem; color: #E11D48; margin-top: 0.3rem; font-weight: 600;">
        총 {top_vol_display} 건 ({top_volume:,} 건)
    </div>
</div>
""", unsafe_allow_html=True)


    with col4:
        st.markdown(f"""
<div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-radius: 16px; padding: 1.25rem 1.25rem; border: 1.5px solid #FDE68A; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.08);">
    <div style="font-size: 0.85rem; font-weight: 700; color: #92400E; text-transform: uppercase; letter-spacing: 0.05em;">
        🔥 트렌드 최대 피크
    </div>
    <div style="font-size: 1.5rem; font-weight: 800; color: #78350F; margin-top: 0.4rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {peak_kw if peak_kw != '-' else '데이터 없음'}
    </div>
    <div style="font-size: 0.8rem; color: #D97706; margin-top: 0.3rem; font-weight: 600;">
        {peak_date if peak_date != '-' else '기간 내 분석'} (지수 100)
    </div>
</div>
""", unsafe_allow_html=True)
