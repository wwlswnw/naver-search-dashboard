import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
from config.settings import settings

VIBRANT_PALETTE = [
    "#4F46E5", # Indigo
    "#F43F5E", # Rose
    "#06B6D4", # Cyan
    "#10B981", # Emerald
    "#F59E0B", # Amber
    "#8B5CF6", # Purple
    "#EC4899", # Pink
    "#3B82F6", # Blue
]

def format_korean_number(val: int) -> str:
    """Format large numbers into clean Korean readable units (e.g. 5,565만, 1.2억)."""
    if val >= 100_000_000:
        return f"{val / 100_000_000:.1f}억"
    elif val >= 10_000:
        val_man = val / 10_000
        if val_man >= 100:
            return f"{val_man:,.0f}만"
        else:
            return f"{val_man:.1f}만"
    elif val > 0:
        return f"{val:,}"
    return "0"

def render_channel_analysis(
    keywords: List[str],
    search_results_by_keyword: Dict[str, Dict[str, Any]]
):
    """Render vibrant studio-style channel volume comparisons and share donut chart."""
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin: 1.5rem 0 0.75rem 0;">
            <span style="font-size: 1.5rem;">🏢</span>
            <h3 style="margin: 0; font-weight: 800; color: #1E1B4B; letter-spacing: -0.02em;">8개 채널별 검색 점유율 및 문서량 비교</h3>
            <span style="background: #F0FDF4; color: #059669; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; border: 1px solid #BBF7D0;">CHANNEL SHARE</span>
        </div>
    """, unsafe_allow_html=True)

    rows = []
    for kw in keywords:
        cat_data = search_results_by_keyword.get(kw, {})
        for cat_key, cat_name in settings.SEARCH_CATEGORIES.items():
            cat_res = cat_data.get(cat_key, {})
            total_count = cat_res.get("total", 0) if isinstance(cat_res, dict) else 0
            rows.append({
                "키워드": kw,
                "채널코드": cat_key,
                "채널": cat_name,
                "문서수": total_count,
                "표시단위": format_korean_number(total_count)
            })

    if not rows:
        st.info("채널별 데이터가 없습니다.")
        return

    df_channel = pd.DataFrame(rows)

    col1, col2 = st.columns([3, 2])

    with col1:
        # Grouped Bar chart with clean Korean unit labels and ample bar spacing
        fig_bar = px.bar(
            df_channel,
            x="채널",
            y="문서수",
            color="키워드",
            barmode="group",
            text="표시단위",
            color_discrete_sequence=VIBRANT_PALETTE,
            custom_data=["문서수"]
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont=dict(size=11, weight="bold"),
            cliponaxis=False,
            hovertemplate="<b>%{x}</b> | %{data.name}<br>누적 문서량: <b>%{customdata[0]:,} 건</b><extra></extra>"
        )
        fig_bar.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            bargap=0.28,
            bargroupgap=0.12,
            yaxis=dict(
                showgrid=True,
                gridcolor="#F3F4F6",
                title=dict(text="문서 수 (건)", font=dict(size=12, color="#4B5563")),
                tickfont=dict(size=11, color="#6B7280"),
                tickformat="~s"
            ),
            xaxis=dict(
                title=None,
                tickfont=dict(size=12, color="#1F2937", family="Plus Jakarta Sans, sans-serif")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#E5E7EB",
                borderwidth=1
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            height=410
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with col2:
        # Donut Chart with Vibrant Styling
        selected_kw_donut = st.selectbox(
            "점유율 상세 분석 키워드",
            options=keywords,
            key="donut_kw_select"
        )
        df_sub = df_channel[df_channel["키워드"] == selected_kw_donut]

        fig_donut = px.pie(
            df_sub,
            values="문서수",
            names="채널",
            hole=0.55,
            color_discrete_sequence=VIBRANT_PALETTE
        )
        fig_donut.update_traces(
            textposition='auto',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>문서 수: %{value:,} 건 (%{percent})<extra></extra>",
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig_donut.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False,
            height=360,
            annotations=[dict(
                text=f"<b>{selected_kw_donut}</b>",
                x=0.5, y=0.5,
                font_size=15,
                showarrow=False,
                font_color="#1E1B4B"
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})


    # Cross-tab summary matrix
    with st.expander("📋 키워드 x 8개 채널별 문서량 피벗 테이블 보기", expanded=False):
        pivot_df = df_channel.pivot_table(
            index="키워드",
            columns="채널",
            values="문서수",
            aggfunc="sum",
            fill_value=0
        )
        pivot_df["총합계"] = pivot_df.sum(axis=1)
        st.dataframe(
            pivot_df.style.format("{:,.0f}").background_gradient(cmap="Purples", subset=["총합계"]),
            use_container_width=True
        )
