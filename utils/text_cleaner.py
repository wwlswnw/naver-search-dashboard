import re
import html
from datetime import datetime
from typing import Optional

def clean_html_text(raw_html: str) -> str:
    """Remove HTML tags like <b> and unescape HTML entities (&quot;, &amp;, etc.)."""
    if not raw_html:
        return ""
    # Strip HTML tags
    clean_text = re.sub(r"<[^>]+>", "", str(raw_html))
    # Unescape HTML entities
    clean_text = html.unescape(clean_text)
    return clean_text.strip()

def parse_naver_datetime(date_str: str) -> Optional[datetime]:
    """Parse Naver API date strings to datetime object."""
    if not date_str:
        return None
    
    # News: 'Wed, 09 Sep 2026 18:20:00 +0900'
    try:
        return datetime.strptime(date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
    except Exception:
        pass

    # Blog: '20260909'
    if len(str(date_str)) == 8 and str(date_str).isdigit():
        try:
            return datetime.strptime(str(date_str), "%Y%m%d")
        except Exception:
            pass

    # Standard: '2026-09-09'
    try:
        return datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
    except Exception:
        pass

    return None

def format_naver_date(date_str: str) -> str:
    """Format various Naver API date strings to standard YYYY-MM-DD HH:MM format."""
    if not date_str:
        return "-"
    
    dt = parse_naver_datetime(date_str)
    if dt:
        # If it has hours/minutes
        if " " in date_str or ":" in date_str:
            return dt.strftime("%Y-%m-%d %H:%M")
        return dt.strftime("%Y-%m-%d")

    return str(date_str)
