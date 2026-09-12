import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from config.settings import settings
from utils.data_helpers import search_items_to_df, to_excel_bytes

CHANNEL_BADGES = {
    "news": "📰 뉴스",
    "blog": "✍️ 블로그",
    "webkr": "🌐 웹문서",
    "image": "🖼️ 이미지",
    "kin": "🙋 지식iN",
    "local": "📍 지역(플레이스)",
    "cafearticle": "☕ 카페글",
    "encyc": "📚 백과사전"
}

def render_result_explorer(
    keywords: List[str],
    search_results_by_keyword: Dict[str, Dict[str, Any]]
):
    """Render native studio-style deep-dive search results explorer across 8 categories."""
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin: 2rem 0 1rem 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.5rem;">🔎</span>
                <h3 style="margin: 0; font-weight: 800; color: #1E1B4B; letter-spacing: -0.02em;">채널별 상세 검색 결과 탐색기</h3>
                <span style="background: #FAF5FF; color: #7E22CE; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; border: 1px solid #E9D5FF;">DEEP-DIVE EXPLORER</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Global Export Button
    col_exp1, col_exp2 = st.columns([4, 1.2])
    with col_exp2:
        all_dfs = {}
        for kw in keywords:
            for cat_key, cat_name in settings.SEARCH_CATEGORIES.items():
                items = search_results_by_keyword.get(kw, {}).get(cat_key, {}).get("items", [])
                if items:
                    sheet_key = f"{kw[:10]}_{cat_name}"[:30]
                    all_dfs[sheet_key] = search_items_to_df(cat_key, items)

        if all_dfs:
            excel_data = to_excel_bytes(all_dfs)
            st.download_button(
                label="📥 전체 엑셀(Excel) 다운로드",
                data=excel_data,
                file_name="naver_market_insight_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    # Tabs for 8 categories
    cat_keys = list(settings.SEARCH_CATEGORIES.keys())
    cat_labels = [f"{settings.SEARCH_CATEGORIES[k]}" for k in cat_keys]
    tabs = st.tabs(cat_labels)

    for i, cat_key in enumerate(cat_keys):
        cat_name = settings.SEARCH_CATEGORIES[cat_key]
        badge_label = CHANNEL_BADGES.get(cat_key, cat_name)
        
        with tabs[i]:
            sub_col1, sub_col2 = st.columns([3, 1])
            with sub_col1:
                selected_kw = st.selectbox(
                    f"'{cat_name}' 결과 확인할 키워드 선택",
                    options=keywords,
                    key=f"tab_kw_{cat_key}"
                )
            
            cat_data = search_results_by_keyword.get(selected_kw, {}).get(cat_key, {})
            items = cat_data.get("items", [])
            total_items = cat_data.get("total", 0)

            if cat_data.get("error"):
                st.error(f"오류: {cat_data.get('error')}")
                continue

            df = search_items_to_df(cat_key, items)

            with sub_col2:
                if not df.empty:
                    csv_data = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label=f"📄 {cat_name} CSV 다운",
                        data=csv_data,
                        file_name=f"naver_{selected_kw}_{cat_key}.csv",
                        mime="text/csv",
                        key=f"csv_btn_{cat_key}",
                        use_container_width=True
                    )

            st.caption(f"🏷️ **{badge_label}** | 총 검색된 문서 수: **{total_items:,}** 건 | 현재 수집 목록: **{len(items)}** 건")

            if not items:
                st.info(f"'{selected_kw}'에 대한 {cat_name} 결과가 없습니다.")
                continue

            if cat_key == "image":
                render_image_grid(items)
            elif cat_key == "local":
                render_local_cards(items)
            else:
                render_generic_cards(cat_key, items)

def render_image_grid(items: List[Dict[str, Any]]):
    """Render studio-style image grid."""
    cols = st.columns(4)
    for idx, item in enumerate(items):
        col = cols[idx % 4]
        with col:
            thumb = item.get("thumbnail", "")
            link = item.get("link", "")
            title = item.get("title", "이미지")
            
            with st.container(border=True):
                if thumb:
                    st.image(thumb, use_container_width=True)
                st.markdown(f"**[{title[:26]}...]({link})**" if len(title) > 26 else f"**[{title}]({link})**")
                w = item.get("sizewidth", "")
                h = item.get("sizeheight", "")
                if w and h:
                    st.caption(f"📐 {w} × {h} px")

def render_local_cards(items: List[Dict[str, Any]]):
    """Render studio-style local place cards."""
    from utils.text_cleaner import clean_html_text

    for item in items:
        title = clean_html_text(item.get("title", ""))
        category = clean_html_text(item.get("category", ""))
        road_addr = clean_html_text(item.get("roadAddress", ""))
        addr = clean_html_text(item.get("address", ""))
        tel = clean_html_text(item.get("telephone", ""))
        link = item.get("link", "")

        with st.container(border=True):
            head_col, cat_col = st.columns([3, 1])
            with head_col:
                if link:
                    st.markdown(f"#### 📍 [{title}]({link})")
                else:
                    st.markdown(f"#### 📍 {title}")
            with cat_col:
                if category:
                    st.caption(f"🏷️ `{category}`")

            info_col1, info_col2 = st.columns([3, 1.2])
            with info_col1:
                display_addr = road_addr if road_addr else addr
                if display_addr:
                    st.write(f"**주소:** {display_addr}")
                if tel:
                    st.caption(f"📞 **전화:** {tel}")
            with info_col2:
                if link:
                    st.link_button("🗺️ 네이버 지도/상세", link, use_container_width=True)

def render_generic_cards(cat_key: str, items: List[Dict[str, Any]]):
    """Render clean native container cards for News, Blog, Cafe, Kin, Webkr, Encyc."""
    from utils.text_cleaner import clean_html_text, format_naver_date

    for item in items:
        title = clean_html_text(item.get("title", ""))
        desc = clean_html_text(item.get("description", ""))
        link = item.get("link", "")
        origin_link = item.get("originallink", "")

        pub_date = ""
        if cat_key == "news":
            pub_date = format_naver_date(item.get("pubDate", ""))
        elif cat_key == "blog":
            pub_date = format_naver_date(item.get("postdate", ""))

        author_meta = ""
        if cat_key == "blog":
            blogger = clean_html_text(item.get("bloggername", ""))
            if blogger:
                author_meta = f"✍️ 블로거: {blogger}"
        elif cat_key == "cafearticle":
            cafe = clean_html_text(item.get("cafename", ""))
            if cafe:
                author_meta = f"☕ 카페: {cafe}"

        with st.container(border=True):
            head_col, date_col = st.columns([4, 1.2])
            with head_col:
                if link:
                    st.markdown(f"##### [{title}]({link})")
                else:
                    st.markdown(f"##### {title}")
            with date_col:
                if pub_date:
                    st.caption(f"🕒 {pub_date}")

            st.write(desc if desc else "내용 요약 없음")

            btn_col1, btn_col2, author_col = st.columns([1.2, 1.2, 3])
            with btn_col1:
                if link:
                    st.link_button("🔗 원문 보기", link, use_container_width=True)
            with btn_col2:
                if origin_link and origin_link != link:
                    st.link_button("📰 언론사 원문", origin_link, use_container_width=True)
            with author_col:
                if author_meta:
                    st.caption(author_meta)
