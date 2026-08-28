from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.sentiment import SentimentResult
from app.models.network import NetworkEdge
from app.services.sentiment_service import analyze_sentiment_and_emotion
from app.services.network_service import extract_network_interactions

def run_analytics_pipeline(db: Session, batch_size: int = 50) -> dict:
    unprocessed_posts = (
        db.query(Post)
        .filter(Post.is_processed == False)
        .limit(batch_size)
        .all()
    )
    
    if not unprocessed_posts:
        return {"status": "idle", "processed_count": 0}
        
    processed_count = 0
    new_edges = []
    
    for post in unprocessed_posts:
        # 1. Infer Sentiment & Emotion
        nlp_out = analyze_sentiment_and_emotion(post.text)
        sentiment_entry = SentimentResult(
            post_id=post.id,
            sentiment=nlp_out["sentiment"],
            emotion=nlp_out["emotion"],
            confidence=nlp_out["confidence"],
            model_version=nlp_out["model_version"]
        )
        db.merge(sentiment_entry)
        
        # 2. Extract Edges
        interactions = extract_network_interactions(post)
        for edge_data in interactions:
            new_edges.append(NetworkEdge(**edge_data))
            
        post.is_processed = True
        processed_count += 1
        
    if new_edges:
        db.bulk_save_objects(new_edges)
        
    db.commit()
    
    return {
        "status": "completed",
        "processed_count": processed_count,
        "edges_created": len(new_edges)
    }