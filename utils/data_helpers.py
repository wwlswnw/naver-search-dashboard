import io
import pandas as pd
from typing import List, Dict, Any
from utils.text_cleaner import clean_html_text, format_naver_date

def search_items_to_df(category: str, items: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert raw search API items into a cleaned, structured DataFrame."""
    if not items:
        return pd.DataFrame()

    cleaned_items = []
    for item in items:
        cleaned_row = {
            "제목": clean_html_text(item.get("title", "")),
            "설명/내용": clean_html_text(item.get("description", "")),
            "링크": item.get("link", "")
        }

        if category == "news":
            cleaned_row["발행일"] = format_naver_date(item.get("pubDate", ""))
            cleaned_row["원문링크"] = item.get("originallink", "")
        elif category == "blog":
            cleaned_row["블로거"] = clean_html_text(item.get("bloggername", ""))
            cleaned_row["블로그링크"] = item.get("bloggerlink", "")
            cleaned_row["작성일"] = format_naver_date(item.get("postdate", ""))
        elif category == "cafearticle":
            cleaned_row["카페명"] = clean_html_text(item.get("cafename", ""))
            cleaned_row["카페링크"] = item.get("cafeurl", "")
        elif category == "image":
            cleaned_row["썸네일"] = item.get("thumbnail", "")
            cleaned_row["크기"] = f"{item.get('sizewidth', '')}x{item.get('sizeheight', '')}"
        elif category == "local":
            cleaned_row["카테고리"] = clean_html_text(item.get("category", ""))
            cleaned_row["전화번호"] = item.get("telephone", "")
            cleaned_row["주소"] = clean_html_text(item.get("address", ""))
            cleaned_row["도로명주소"] = clean_html_text(item.get("roadAddress", ""))
        elif category == "encyc":
            cleaned_row["썸네일"] = item.get("thumbnail", "")

        cleaned_items.append(cleaned_row)

    return pd.DataFrame(cleaned_items)

def datalab_trend_to_df(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert Datalab search trend response into a combined time-series DataFrame, ensuring all keywords are represented."""
    if not results:
        return pd.DataFrame()

    all_dfs = []
    base_dates = None

    # First pass: find full date index from non-empty result
    for res in results:
        data_points = res.get("data", [])
        if data_points:
            df = pd.DataFrame(data_points)
            if "period" in df.columns:
                base_dates = df["period"].values
                break

    for res in results:
        title = res.get("title", "Unknown")
        data_points = res.get("data", [])
        if data_points:
            df = pd.DataFrame(data_points)
            df = df.rename(columns={"period": "일자", "ratio": f"{title} (검색지수)"})
            all_dfs.append(df.set_index("일자"))
        elif base_dates is not None and len(base_dates) > 0:
            # Create a 0.0 baseline series for keywords with below-threshold volume
            df_zero = pd.DataFrame({
                "일자": base_dates,
                f"{title} (검색지수)": [0.0] * len(base_dates)
            })
            all_dfs.append(df_zero.set_index("일자"))

    if not all_dfs:
        return pd.DataFrame()

    combined_df = pd.concat(all_dfs, axis=1, join="outer").fillna(0.0).reset_index()
    combined_df["일자"] = pd.to_datetime(combined_df["일자"])
    return combined_df.sort_values("일자")

def to_excel_bytes(df_dict: Dict[str, pd.DataFrame]) -> bytes:

    """Generate Excel bytes from a dictionary of DataFrames."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in df_dict.items():
            safe_name = str(sheet_name)[:31] # Excel sheet length limit
            df.to_excel(writer, sheet_name=safe_name, index=False)
    return output.getvalue()
