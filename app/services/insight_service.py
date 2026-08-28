def generate_ai_insight_summary(sentiment_stats: dict, top_trend: dict, top_influencer: dict, demographics: dict) -> str:
    lead_topic = top_trend.get("topic", "general discussions")
    velocity = top_trend.get("velocity_percentage", 0)
    top_author = top_influencer.get("id", "Key opinion leaders")
    dominant_sentiment = max(sentiment_stats, key=sentiment_stats.get) if sentiment_stats else "neutral"
    
    summary = (
        f"Real-time monitoring detects a dominant {dominant_sentiment.upper()} sentiment bias ({sentiment_stats.get(dominant_sentiment, 0)}%). "
        f"Discussions are actively led by topic '{lead_topic}' showing a {velocity}% growth velocity. "
        f"Propagation analysis identifies {top_author} as the primary influence node across cross-platform communities."
    )
    return summary