import streamlit as st
import feedparser
from datetime import datetime
import time

st.set_page_config(
    page_title="India Business News Dashboard",
    page_icon="📰",
    layout="wide"
)

# ============================================
# NEWS FETCHING FUNCTION
# ============================================

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_google_news():
    """Fetch live business news from Google News India RSS"""
    try:
        # India Business section RSS feed
        rss_url = "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-IN&gl=IN&ceid=IN:en"
        
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            return {"success": False, "error": "No articles found in feed"}
        
        articles = []
        for entry in feed.entries[:15]:  # Limit to 15 articles
            articles.append({
                "title": entry.get("title", "No title"),
                "summary": entry.get("summary", "No summary available."),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "Unknown") if hasattr(entry, "source") else "Google News"
            })
        
        return {"articles": articles, "success": True}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================
# UI LAYOUT
# ============================================

st.title("📰 India Business News")
st.markdown("Live headlines from Google News India — Business Section")
st.markdown("---")

# Fetch news
news_data = fetch_google_news()

# ============================================
# DISPLAY NEWS
# ============================================

if news_data["success"]:
    articles = news_data["articles"]
    
    st.success(f"Loaded {len(articles)} articles")
    
    for i, article in enumerate(articles):
        # Clean the summary (Google News often adds HTML)
        summary = article["summary"]
        # Remove HTML tags if present
        if "<" in summary and ">" in summary:
            import re
            summary = re.sub(r'<[^>]+>', '', summary)
        if len(summary) > 300:
            summary = summary[:300] + "..."
        
        with st.expander(f"**{article['title']}**"):
            st.write(summary)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"Published: {article['published']}")
            with col2:
                if article["link"]:
                    st.markdown(f"[Read more →]({article['link']})")
        
        st.markdown("---")
else:
    st.error(f"Could not load news: {news_data.get('error', 'Unknown error')}")
    st.info("This may be a temporary issue. Try refreshing the page.")

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.header("⚙️ About")
    st.markdown("**Source:** Google News India (Business)")
    st.markdown("**Feed:** Top stories from Indian business publications")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh News"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("Data updates every 10 minutes. Google News RSS is free and requires no API key.")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
