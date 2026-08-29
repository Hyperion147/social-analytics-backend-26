@router.post("/batch-live", summary="Fetch live data across multiple subreddits and Telegram channels simultaneously")
async def ingest_batch_live(db: Session = Depends(get_db)):
    reddit_adapter = RedditAdapter()
    telegram_adapter = TelegramAdapter()
    
    subreddits = ["technology", "artificial", "MachineLearning", "dataisbeautiful"]
    channels = ["techcrunch", "durov", "telegram"]
    
    all_posts = []
    
    for sub in subreddits:
        posts = await reddit_adapter.fetch_posts(query=sub, limit=15)
        all_posts.extend(posts)
        
    for ch in channels:
        posts = await telegram_adapter.fetch_posts(query=ch, limit=15)
        all_posts.extend(posts)
        
    inserted_count = 0
    for item in all_posts:
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
        res = db.execute(stmt)
        inserted_count += res.rowcount
        
    db.commit()
    return {
        "status": "success",
        "total_sources_queried": len(subreddits) + len(channels),
        "total_fetched": len(all_posts),
        "newly_inserted": inserted_count
    }