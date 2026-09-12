import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, List
from utils.data_helpers import datalab_trend_to_df

# Apple-inspired Palette
APPLE_PALETTE = [
    "#0071E3", # Apple Blue
    "#FF3B30", # Apple Red
    "#34C759", # Apple Green
    "#AF52DE", # Apple Purple
    "#FF9500", # Apple Amber
    "#5AC8FA", # Apple Cyan
]

def render_trend_charts(trend_data: Dict[str, Any], keywords: List[str]):
    """Render Apple-style Plotly trend charts with smooth curved splines and clean stats."""
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin: 1rem 0 1.2rem 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <h3 style="margin: 0; font-weight: 700; color: #1D1D1F; letter-spacing: -0.025em; font-size: 1.35rem;">네이버 검색어 트렌드 시계열 분석</h3>
                <span style="background: #E8E8ED; color: #1D1D1F; font-size: 0.72rem; font-weight: 700; padding: 3px 10px; border-radius: 980px;">DATALAB TREND</span>
            </div>
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
        color = APPLE_PALETTE[i % len(APPLE_PALETTE)]
        
        # Smooth Spline Line
        fig.add_trace(go.Scatter(
            x=df_trend["일자"],
            y=df_trend[col],
            mode="lines",
            name=kw_name,
            line=dict(width=3, color=color, shape="spline", smoothing=1.1),
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
            font=dict(size=12, color="#1D1D1F", family="-apple-system, sans-serif"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E5E5EA",
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F2F2F7",
            zeroline=False,
            showline=True,
            linecolor="#E5E5EA",
            tickfont=dict(size=11, color="#86868B")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F2F2F7",
            zeroline=False,
            showline=True,
            linecolor="#E5E5EA",
            title=dict(text="상대 검색 지수 (Max 100)", font=dict(size=12, color="#86868B")),
            tickfont=dict(size=11, color="#86868B")
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
