from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.core.database import get_db
from app.models.post import Post
from app.schemas.social import NormalizedPost
from app.ingestion.mock_adapter import generate_mock_posts

router = APIRouter(prefix="/ingest", tags=["Data Ingestion"])

@router.post("/mock", summary="Generate & insert mock social media posts")
def ingest_mock_data(count: int = 30, db: Session = Depends(get_db)):
    mock_posts = generate_mock_posts(count=count)
    inserted_count = 0

    for item in mock_posts:
        # Idempotent upsert on (platform, platform_post_id)
        stmt = insert(Post).values(
            platform=item.platform,
            platform_post_id=item.platform_post_id,
            author_id=item.author_id,
            author_username=item.author_username,
            author_bio=item.author_bio,
            text=item.text,
            language=item.language,
            created_at=item.created_at,
            parent_post_id=item.parent_post_id,
            engagement_count=item.engagement_count,
            raw_data=item.raw_data,
            is_processed=False
        ).on_conflict_do_nothing(
            index_elements=["platform", "platform_post_id"]
        )
        result = db.execute(stmt)
        inserted_count += result.rowcount

    db.commit()
    return {
        "status": "success",
        "generated": len(mock_posts),
        "inserted_new_records": inserted_count
    }