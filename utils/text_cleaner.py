import re
import html
from datetime import datetime

def clean_html_text(raw_html: str) -> str:
    """Remove HTML tags like <b> and unescape HTML entities (&quot;, &amp;, etc.)."""
    if not raw_html:
        return ""
    # Strip HTML tags
    clean_text = re.sub(r"<[^>]+>", "", str(raw_html))
    # Unescape HTML entities
    clean_text = html.unescape(clean_text)
    return clean_text.strip()

def format_naver_date(date_str: str) -> str:
    """Format various Naver API date strings to standard YYYY-MM-DD HH:MM format."""
    if not date_str:
        return "-"
    
    # Example format: 'Wed, 09 Sep 2026 18:20:00 +0900' (News)
    try:
        dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        pass

    # Example format: '20260909' (Blog postdate)
    if len(date_str) == 8 and date_str.isdigit():
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    return str(date_str)
