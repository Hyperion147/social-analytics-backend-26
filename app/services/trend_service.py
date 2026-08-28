import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.post import Post

def extract_hashtags_and_keywords(text: str) -> list[str]:
    # Extract explicit hashtags or dominant topic words
    tags = re.findall(r"#\w+", text)
    return [t.lower() for t in tags]

def compute_trend_velocity(db: Session) -> list[dict]:
    now = datetime.now(timezone.utc)
    t_mid = now - timedelta(hours=3)
    t_start = now - timedelta(hours=6)
    
    # Recent window posts (T0)
    recent_posts = db.query(Post).filter(Post.created_at >= t_mid).all()
    # Past window posts (T-1)
    past_posts = db.query(Post).filter(Post.created_at >= t_start, Post.created_at < t_mid).all()
    
    recent_counts = Counter()
    for p in recent_posts:
        recent_counts.update(extract_hashtags_and_keywords(p.text))
        
    past_counts = Counter()
    for p in past_posts:
        past_counts.update(extract_hashtags_and_keywords(p.text))
        
    all_topics = set(recent_counts.keys()).union(set(past_counts.keys()))
    trends = []
    
    for topic in all_topics:
        c_recent = recent_counts.get(topic, 0)
        c_past = past_counts.get(topic, 0)
        
        # Velocity = percentage increase
        if c_past == 0:
            velocity_pct = float(c_recent * 100)
        else:
            velocity_pct = round(((c_recent - c_past) / c_past) * 100.0, 2)
            
        trends.append({
            "topic": topic,
            "frequency": c_recent + c_past,
            "current_window_count": c_recent,
            "velocity_percentage": velocity_pct,
            "status": "rising" if velocity_pct > 20 else "stable"
        })
        
    # Sort by velocity and frequency
    return sorted(trends, key=lambda x: (x["velocity_percentage"], x["frequency"]), reverse=True)[:5]