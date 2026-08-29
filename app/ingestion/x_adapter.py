import random
from datetime import datetime, timedelta, timezone
from app.schemas.social import NormalizedPost
from app.ingestion.base import BaseSocialAdapter

TWITTER_AUTHORS = [
    {"handle": "ai_researcher_x", "bio": "AI Ethics Researcher | Bengaluru, India", "id": "usr_x_ai_res"},
    {"handle": "tech_reporter", "bio": "Tech Journalist | New Delhi, India", "id": "usr_x_reporter"},
    {"handle": "dev_advocate", "bio": "Developer Relations & Cloud Engineer", "id": "usr_x_dev"},
    {"handle": "policy_watch", "bio": "Digital Rights & Governance Analyst", "id": "usr_x_policy"}
]

TWEET_TEMPLATES = [
    "The surge in #TechPolicy adoption across sectors is unprecedented. Thoughts? @tech_reporter",
    "Observing significant network latency and platform drops today. #TechOutage",
    "Excited to announce our open-source benchmark for #AI safety tools! @ai_researcher_x",
    "Audience sentiment shifts rapidly when governance isn't transparent. #CyberSecPolicy",
    "Great discussions at the national hackathon regarding data sovereignty! #StudentsInTech"
]

class XAdapter(BaseSocialAdapter):
    async def fetch_posts(self, query: str = "tech", limit: int = 15) -> list[NormalizedPost]:
        posts = []
        base_time = datetime.now(timezone.utc) - timedelta(hours=3)
        
        for i in range(limit):
            author = random.choice(TWITTER_AUTHORS)
            text = random.choice(TWEET_TEMPLATES)
            created_at = base_time + timedelta(minutes=i * 8)
            
            posts.append(
                NormalizedPost(
                    platform="x",
                    platform_post_id=f"x_{int(created_at.timestamp())}_{i}",
                    author_id=author["id"],
                    author_username=author["handle"],
                    author_bio=author["bio"],
                    text=text,
                    language="en",
                    created_at=created_at,
                    parent_post_id=f"x_parent_{i-1}" if i % 3 == 0 else None,
                    engagement_count={
                        "likes": random.randint(10, 450),
                        "shares": random.randint(5, 120),
                        "comments": random.randint(2, 60)
                    },
                    raw_data={"source": "x_adapter", "query": query}
                )
            )
        return posts