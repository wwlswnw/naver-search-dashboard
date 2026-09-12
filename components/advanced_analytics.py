import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
from config.settings import settings
from utils.data_helpers import datalab_trend_to_df

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

def render_advanced_analytics(
    keywords: List[str],
    search_results_by_keyword: Dict[str, Dict[str, Any]],
    trend_data: Dict[str, Any]
):
    """Render exciting deep-dive EDA charts: Radar, 4-Quadrant Bubble Matrix, and Weekly/Monthly Rhythm Heatmap."""
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin: 0.5rem 0 1rem 0;">
            <span style="font-size: 1.5rem;">🔮</span>
            <h3 style="margin: 0; font-weight: 800; color: #1E1B4B; letter-spacing: -0.02em;">마켓 인사이트 심층 EDA 랩</h3>
            <span style="background: linear-gradient(135deg, #EEF2FF, #FAF5FF); color: #4F46E5; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; border: 1px solid #C7D2FE;">ADVANCED LAB</span>
        </div>
        <p style="color: #64748B; font-size: 0.9rem;">
            단순 수치 조회를 넘어 <strong>수요-공급 밸런스, 8채널 침투 프로필, 요일별 소비자 행동 리듬</strong>을 다각도로 발굴하는 심층 분석 공간입니다.
        </p>
    """, unsafe_allow_html=True)

    tab_radar, tab_quadrant, tab_rhythm = st.tabs([
        "🕸️ 1. 8채널 다각형 레이더 차트",
        "🚀 2. 수요 vs 공급 4분면 매트릭스",
        "📅 3. 요일별 소비 리듬 히트맵"
    ])

    # -------------------------------------------------------------
    # 1. 8-Channel Radar Profile Chart
    # -------------------------------------------------------------
    with tab_radar:
        st.markdown("#### 🕸️ 키워드별 8개 채널 침투 프로필 (Radar Spider Chart)")
        st.caption("각 키워드가 어떤 채널(블로그/카페/뉴스/지식iN 등)에 특화되어 확산되었는지 채널별 점유 비중을 다각형으로 비교합니다.")

        categories = list(settings.SEARCH_CATEGORIES.keys())
        cat_labels = [settings.SEARCH_CATEGORIES[k] for k in categories]

        fig_radar = go.Figure()

        for idx, kw in enumerate(keywords):
            cat_data = search_results_by_keyword.get(kw, {})
            raw_counts = []
            for cat_key in categories:
                c_res = cat_data.get(cat_key, {})
                raw_counts.append(c_res.get("total", 0) if isinstance(c_res, dict) else 0)
            
            total_sum = sum(raw_counts)
            if total_sum > 0:
                # Percentage share per channel
                shares = [(c / total_sum) * 100 for c in raw_counts]
            else:
                shares = [0] * len(categories)

            # Close radar loop
            r_vals = shares + [shares[0]]
            theta_vals = cat_labels + [cat_labels[0]]

            color = VIBRANT_PALETTE[idx % len(VIBRANT_PALETTE)]

            fig_radar.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=theta_vals,
                fill='toself',
                name=kw,
                line=dict(color=color, width=2.5),
                opacity=0.4
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(60, 100)],
                    tickfont=dict(size=10, color="#94A3B8"),
                    gridcolor="#F1F5F9"
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color="#1E293B", family="Plus Jakarta Sans, sans-serif")
                ),
                bgcolor="#FAFAFC"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40),
            height=450
        )

        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

        # Channel Profile Diagnostic Tags
        st.markdown("##### 🏷️ 키워드별 채널 성격 진단")
        cols = st.columns(len(keywords))
        for idx, kw in enumerate(keywords):
            with cols[idx]:
                cat_data = search_results_by_keyword.get(kw, {})
                channel_map = {settings.SEARCH_CATEGORIES[k]: cat_data.get(k, {}).get("total", 0) for k in categories}
                top_ch = max(channel_map, key=channel_map.get) if channel_map else "-"
                
                archetype = "종합 균형형"
                if top_ch in ["블로그", "카페글"]:
                    archetype = "🔥 커뮤니티 바이럴형 (B2C)"
                elif top_ch in ["뉴스", "웹문서"]:
                    archetype = "📰 언론 보도/산업형 (B2B)"
                elif top_ch == "지식iN":
                    archetype = "🙋 고객 질문/고민 집중형"
                elif top_ch in ["이미지", "지역(플레이스)"]:
                    archetype = "📍 로컬/비주얼 탐색형"

                with st.container(border=True):
                    st.markdown(f"**{kw}**")
                    st.caption(f"주력 채널: `{top_ch}`")
                    st.write(f"**{archetype}**")

    # -------------------------------------------------------------
    # 2. Demand vs Supply 4-Quadrant Bubble Matrix
    # -------------------------------------------------------------
    with tab_quadrant:
        st.markdown("#### 🚀 수요 vs 공급 4분면 기회 매트릭스 (Demand-Supply Gap)")
        st.caption("X축(검색어 트렌드 관심도 - 수요)과 Y축(콘텐츠 발행량 - 공급)을 교차하여 블루오션 영역과 과열 경쟁 영역을 발굴합니다.")

        trend_results = trend_data.get("results", []) if trend_data else []
        df_trend = datalab_trend_to_df(trend_results)

        matrix_rows = []
        for kw in keywords:
            # 1. Demand = Average trend ratio (0~100)
            kw_col = f"{kw} (검색지수)"
            if not df_trend.empty and kw_col in df_trend.columns:
                avg_demand = df_trend[kw_col].mean()
            else:
                avg_demand = 0.0

            # 2. Supply = Total content volume (Blog + Cafe + Webkr)
            cat_data = search_results_by_keyword.get(kw, {})
            blog_cnt = cat_data.get("blog", {}).get("total", 0)
            cafe_cnt = cat_data.get("cafearticle", {}).get("total", 0)
            web_cnt = cat_data.get("webkr", {}).get("total", 0)
            news_cnt = cat_data.get("news", {}).get("total", 0)
            total_supply = blog_cnt + cafe_cnt + web_cnt

            matrix_rows.append({
                "키워드": kw,
                "평균 검색 수요 (지수)": round(avg_demand, 1),
                "콘텐츠 공급량 (건)": total_supply,
                "뉴스 보도량 (건)": news_cnt
            })

        df_matrix = pd.DataFrame(matrix_rows)

        if not df_matrix.empty and df_matrix["콘텐츠 공급량 (건)"].sum() > 0:
            mid_x = df_matrix["평균 검색 수요 (지수)"].mean() if df_matrix["평균 검색 수요 (지수)"].max() > 0 else 50
            mid_y = df_matrix["콘텐츠 공급량 (건)"].mean() if df_matrix["콘텐츠 공급량 (건)"].max() > 0 else 1000

            fig_bubble = px.scatter(
                df_matrix,
                x="평균 검색 수요 (지수)",
                y="콘텐츠 공급량 (건)",
                size="뉴스 보도량 (건)",
                color="키워드",
                text="키워드",
                size_max=45,
                color_discrete_sequence=VIBRANT_PALETTE,
                template="plotly_white"
            )

            # Add Quadrant Divider Lines
            fig_bubble.add_vline(x=mid_x, line_dash="dash", line_color="#CBD5E1")
            fig_bubble.add_hline(y=mid_y, line_dash="dash", line_color="#CBD5E1")

            fig_bubble.update_traces(textposition='top center')
            fig_bubble.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#F3F4F6",
                    title=dict(text="콘텐츠 공급량 (블로그+카페+웹 건수)", font=dict(size=12, color="#4B5563"))
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="#F3F4F6",
                    title=dict(text="검색 수요 관심도 (데이터랩 평균 지수)", font=dict(size=12, color="#4B5563"))
                ),
                margin=dict(l=30, r=30, t=30, b=30),
                height=430
            )

            st.plotly_chart(fig_bubble, use_container_width=True, config={'displayModeBar': False})

            # Quadrant Interpretations Guide Box
            q_cols = st.columns(4)
            with q_cols[0]:
                with st.container(border=True):
                    st.markdown("**🚀 우하단: 블루오션 기회**")
                    st.caption("수요는 높은데 콘텐츠 공급이 적어, 진입 시 빠른 상위 노출 및 트래픽 선점이 가능한 영역")
            with q_cols[1]:
                with st.container(border=True):
                    st.markdown("**⚔️ 우상단: 레드오션 격전**")
                    st.caption("수요와 공급이 모두 높은 시장. 차별화된 키워드 세부 조합(롱테일) 전략 필요")
            with q_cols[2]:
                with st.container(border=True):
                    st.markdown("**💤 좌하단: 틈새/잠재 시장**")
                    st.caption("현재는 검색량과 콘텐츠 모두 적으나, 장기적 선점 또는 특정 타깃용 니치 마켓")
            with q_cols[3]:
                with st.container(border=True):
                    st.markdown("**📢 좌상단: 공급 과열 주의**")
                    st.caption("소비자 검색은 적은데 공급/보도자료만 많은 상태. 마케팅 비용 효율 점검 필요")
        else:
            st.info("4분면 매트릭스를 구성하기 위한 트렌드 및 콘텐츠 수치가 부족합니다.")

    # -------------------------------------------------------------
    # 3. Weekly & Monthly Search Rhythm Heatmap
    # -------------------------------------------------------------
    with tab_rhythm:
        st.markdown("#### 📅 요일별 소비 리듬 히트맵 (Weekly Search Rhythm)")
        st.caption("소비자들이 어떤 요일(월~일)에 해당 키워드를 집중적으로 검색하는지 소비 타이밍 리듬을 분석합니다.")

        trend_results = trend_data.get("results", []) if trend_data else []
        df_trend = datalab_trend_to_df(trend_results)

        if not df_trend.empty and "일자" in df_trend.columns:
            df_trend["요일"] = df_trend["일자"].dt.day_name()
            df_trend["요일번호"] = df_trend["일자"].dt.dayofweek # 0: Mon, 6: Sun

            day_names_kr = {
                "Monday": "1. 월요일",
                "Tuesday": "2. 화요일",
                "Wednesday": "3. 수요일",
                "Thursday": "4. 목요일",
                "Friday": "5. 금요일",
                "Saturday": "6. 토요일",
                "Sunday": "7. 일요일"
            }
            df_trend["요일명"] = df_trend["요일"].map(day_names_kr)

            val_cols = [c for c in df_trend.columns if " (검색지수)" in c]
            
            # Pivot table: Day of Week x Keywords (Average Ratio)
            day_pivot = df_trend.groupby("요일명")[val_cols].mean()
            day_pivot.columns = [c.replace(" (검색지수)", "") for c in day_pivot.columns]
            day_pivot = day_pivot.sort_index()

            # Vibrant Full-Width Heatmap using go.Heatmap
            fig_heat = go.Figure(data=go.Heatmap(
                z=day_pivot.values,
                x=list(day_pivot.columns),
                y=list(day_pivot.index),
                colorscale="Viridis",
                text=day_pivot.values.round(1),
                texttemplate="%{text}",
                textfont=dict(size=14, color="white"),
                colorbar=dict(title=dict(text="평균 검색지수", font=dict(size=11, color="#475569"))),
                hoverongaps=False,
                hovertemplate="<b>%{x}</b><br>%{y}<br>평균 검색지수: <b>%{z:.1f}</b><extra></extra>"
            ))

            fig_heat.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                xaxis=dict(
                    type='category',
                    side='top',
                    tickfont=dict(size=13, color="#1E1B4B", family="Plus Jakarta Sans, sans-serif")
                ),
                yaxis=dict(
                    type='category',
                    autorange='reversed',
                    tickfont=dict(size=12, color="#374151")
                ),
                margin=dict(l=40, r=40, t=50, b=30),
                height=380
            )

            st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})


            # Timing Strategy Insights
            st.markdown("##### ⏱️ 요일별 마케팅 & 콘텐츠 발행 타이밍 제안")
            cols_rhythm = st.columns(len(day_pivot.columns))
            for idx, kw in enumerate(day_pivot.columns):
                with cols_rhythm[idx]:
                    s = day_pivot[kw]
                    peak_day = s.idxmax()
                    peak_val = s.max()
                    lowest_day = s.idxmin()
                    
                    with st.container(border=True):
                        st.markdown(f"**{kw}**")
                        st.write(f"🔥 최고 피크: **{peak_day.split('. ')[-1]}** ({peak_val:.1f})")
                        st.caption(f"💤 최저 요일: {lowest_day.split('. ')[-1]}")
                        if "토" in peak_day or "일" in peak_day:
                            st.info("💡 주말 여가/쇼핑 타깃팅 추천")
                        else:
                            st.success("💡 주중 업무/출퇴근 타깃팅 추천")
        else:
            st.info("요일별 리듬을 분석하기 위한 시계열 일간 데이터가 없습니다. (사이드바에서 분석 단위를 '일간(Date)'으로 설정해 주세요.)")
