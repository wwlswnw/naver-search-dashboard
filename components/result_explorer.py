import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List
from config.settings import settings
from utils.data_helpers import search_items_to_df, to_excel_bytes
from utils.text_cleaner import parse_naver_datetime

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

def filter_items_by_date(items: List[Dict[str, Any]], start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Filter search items to only include those within the specified date range."""
    if not start_date:
        return items
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) if end_date else datetime.now()
    except Exception:
        return items
    
    filtered = []
    for it in items:
        raw_date = it.get("pubDate") or it.get("postdate")
        if raw_date:
            dt = parse_naver_datetime(raw_date)
            if dt:
                if dt >= start_dt and dt <= end_dt:
                    filtered.append(it)
            else:
                filtered.append(it)
        else:
            filtered.append(it)
    return filtered

def render_result_explorer(
    keywords: List[str],
    search_results_by_keyword: Dict[str, Dict[str, Any]],
    start_date: str = None,
    end_date: str = None,
    filter_by_date: bool = True
):
    """Render native studio-style deep-dive search results explorer across 8 categories with date filtering."""
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
    col_exp1, col_exp2 = st.columns([4, 1.4])
    with col_exp2:
        all_dfs = {}
        for kw in keywords:
            for cat_key, cat_name in settings.SEARCH_CATEGORIES.items():
                items = search_results_by_keyword.get(kw, {}).get(cat_key, {}).get("items", [])
                if filter_by_date and start_date:
                    items = filter_items_by_date(items, start_date, end_date)
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
            raw_items = cat_data.get("items", [])
            total_items = cat_data.get("total", 0)

            if cat_data.get("error"):
                st.error(f"오류: {cat_data.get('error')}")
                continue

            # 1. Date filter
            if filter_by_date and start_date and cat_key in ["news", "blog", "cafearticle"]:
                items = filter_items_by_date(raw_items, start_date, end_date)
                filter_badge = f" | 🛡️ **기간 필터 ({start_date} ~ {end_date})**"
            else:
                items = raw_items
                filter_badge = ""

            # 2. In-Tab Granular Secondary Filter Bar
            with st.expander("🔍 결과 내 세부 필터 (실시간 재검색 / 출처 필터)", expanded=False):
                sec_col1, sec_col2, sec_col3 = st.columns([2, 1.5, 1])
                
                with sec_col1:
                    sub_search_query = st.text_input(
                        "🔤 결과 내 키워드 검색",
                        value="",
                        placeholder="제목 또는 내용에 포함된 단어 입력",
                        key=f"sub_search_{cat_key}_{selected_kw}"
                    )
                
                # Source / Domain extraction
                sources = ["전체 출처"]
                if cat_key == "news":
                    for it in items:
                        link_val = it.get("originallink") or it.get("link", "")
                        from urllib.parse import urlparse
                        try:
                            netloc = urlparse(link_val).netloc.replace("www.", "")
                            if netloc and netloc not in sources:
                                sources.append(netloc)
                        except Exception:
                            pass
                elif cat_key == "blog":
                    for it in items:
                        bname = it.get("bloggername", "").strip()
                        if bname and bname not in sources:
                            sources.append(bname)
                elif cat_key == "cafearticle":
                    for it in items:
                        cname = it.get("cafename", "").strip()
                        if cname and cname not in sources:
                            sources.append(cname)

                with sec_col2:
                    if len(sources) > 1:
                        selected_source = st.selectbox(
                            "📰 출처 / 매체별 필터",
                            options=sources[:30],
                            key=f"source_filter_{cat_key}_{selected_kw}"
                        )
                    else:
                        selected_source = "전체 출처"

                with sec_col3:
                    sort_order = st.selectbox(
                        "정렬 순서",
                        options=["기본순", "최신순", "오래된순"],
                        key=f"sort_order_{cat_key}_{selected_kw}"
                    )

            # Apply secondary filters
            if sub_search_query.strip():
                sq = sub_search_query.strip().lower()
                items = [
                    it for it in items
                    if sq in str(it.get("title", "")).lower() or sq in str(it.get("description", "")).lower()
                ]

            if selected_source != "전체 출처":
                if cat_key == "news":
                    items = [it for it in items if selected_source in (it.get("originallink") or it.get("link", ""))]
                elif cat_key == "blog":
                    items = [it for it in items if it.get("bloggername", "").strip() == selected_source]
                elif cat_key == "cafearticle":
                    items = [it for it in items if it.get("cafename", "").strip() == selected_source]

            if sort_order == "최신순":
                items = sorted(items, key=lambda x: x.get("pubDate") or x.get("postdate") or "", reverse=True)
            elif sort_order == "오래된순":
                items = sorted(items, key=lambda x: x.get("pubDate") or x.get("postdate") or "", reverse=False)

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

            st.caption(f"🏷️ **{badge_label}** | 총 검색 문서: **{total_items:,}** 건 | 현재 필터 목록: **{len(items)}** 건{filter_badge}")

            if not items:
                st.info(f"'{selected_kw}'에 대한 {cat_name} 결과 중 필터 조건에 부합하는 항목이 없습니다.")
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
                primary_link = origin_link if (cat_key == "news" and origin_link) else link
                if primary_link:
                    st.markdown(f"##### [{title}]({primary_link})")
                else:
                    st.markdown(f"##### {title}")
            with date_col:
                if pub_date:
                    st.caption(f"🕒 {pub_date}")

            st.write(desc if desc else "내용 요약 없음")

            btn_col1, btn_col2, author_col = st.columns([1.5, 1.5, 2.5])
            with btn_col1:
                if cat_key == "news" and origin_link:
                    st.link_button("📰 언론사 원문 기사", origin_link, use_container_width=True)
                elif link:
                    st.link_button("🔗 원문 보기", link, use_container_width=True)
            with btn_col2:
                if cat_key == "news" and link and link != origin_link:
                    st.link_button("🟢 네이버 뉴스", link, use_container_width=True)
                elif origin_link and origin_link != link:
                    st.link_button("🔗 관련 원문", origin_link, use_container_width=True)
            with author_col:
                if author_meta:
                    st.caption(author_meta)
