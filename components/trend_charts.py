import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, List
from utils.data_helpers import datalab_trend_to_df

# Vibrant Studio Palette
VIBRANT_PALETTE = [
    "#4F46E5", # Electric Indigo
    "#F43F5E", # Sunset Rose
    "#06B6D4", # Bright Cyan
    "#10B981", # Vivid Emerald
    "#F59E0B", # Vibrant Amber
    "#8B5CF6", # Purple Neon
]

def render_trend_charts(trend_data: Dict[str, Any], keywords: List[str]):
    """Render vibrant studio-style Plotly trend charts with smooth curved splines and interactive stats."""
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin: 1.5rem 0 0.75rem 0;">
            <span style="font-size: 1.5rem;">📈</span>
            <h3 style="margin: 0; font-weight: 800; color: #1E1B4B; letter-spacing: -0.02em;">네이버 검색어 트렌드 시계열 분석</h3>
            <span style="background: #EEF2FF; color: #4F46E5; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; border: 1px solid #C7D2FE;">DATALAB TREND</span>
        </div>
    """, unsafe_allow_html=True)

    if not trend_data or "error" in trend_data:
        err = trend_data.get("error", "데이터를 불러올 수 없습니다.") if trend_data else "트렌드 데이터가 없습니다."
        st.warning(f"⚠️ {err}")
        return

    results = trend_data.get("results", [])
    if not results:
        st.info("선택한 기간/조건에 해당하는 데이터랩 트렌드 데이터가 없습니다.")
        return

    df_trend = datalab_trend_to_df(results)
    if df_trend.empty:
        st.info("데이터랩 트렌드 포인트가 비어 있습니다.")
        return

    value_cols = [c for c in df_trend.columns if c != "일자"]
    
    fig = go.Figure()
    
    for i, col in enumerate(value_cols):
        kw_name = col.replace(" (검색지수)", "")
        color = VIBRANT_PALETTE[i % len(VIBRANT_PALETTE)]
        
        # Smooth Spline Line
        fig.add_trace(go.Scatter(
            x=df_trend["일자"],
            y=df_trend[col],
            mode="lines",
            name=kw_name,
            line=dict(width=3.5, color=color, shape="spline", smoothing=1.1),
            hovertemplate=f"<b>{kw_name}</b><br>일자: %{{x|%Y-%m-%d}}<br>검색지수: <b>%{{y:.1f}}</b><extra></extra>"
        ))

    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
            font=dict(size=12, color="#374151", family="Plus Jakarta Sans, sans-serif"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False,
            showline=True,
            linecolor="#E5E7EB",
            tickfont=dict(size=11, color="#6B7280")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F3F4F6",
            zeroline=False,
            showline=True,
            linecolor="#E5E7EB",
            title=dict(text="상대 검색 지수 (Max 100)", font=dict(size=12, color="#4B5563")),
            tickfont=dict(size=11, color="#6B7280")
        ),
        margin=dict(l=30, r=20, t=40, b=30),
        height=420
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Trend Statistics Cards & Table
    stats_list = []
    for col in value_cols:
        clean_name = col.replace(" (검색지수)", "")
        s = df_trend[col]
        stats_list.append({
            "키워드": clean_name,
            "평균 검색지수": round(s.mean(), 1),
            "최대 피크지수": round(s.max(), 1),
            "최저 검색지수": round(s.min(), 1),
            "변동성 (표준편차)": round(s.std(), 1) if len(s) > 1 else 0.0,
            "최근 지수": round(s.iloc[-1], 1) if not s.empty else 0.0
        })

    df_stats = pd.DataFrame(stats_list)
    with st.expander("📊 키워드별 트렌드 수치 요약 테이블 보기", expanded=False):
        st.dataframe(
            df_stats.style.background_gradient(cmap="Blues", subset=["평균 검색지수", "최대 피크지수"]),
            use_container_width=True,
            hide_index=True
        )
