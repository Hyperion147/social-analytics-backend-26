import re
from collections import Counter
from sqlalchemy.orm import Session
from app.models.post import Post

LOCATION_KEYWORDS = {
    "India (North)": ["delhi", "noida", "gurgaon", "punjab", "lucknow", "chandigarh", "jaipur"],
    "India (South)": ["bengaluru", "bangalore", "hyderabad", "chennai", "kerala", "mysore"],
    "India (West)": ["mumbai", "pune", "gujarat", "ahmedabad"],
    "India (East)": ["kolkata", "patna", "bhubaneswar", "assam"],
    "International": ["usa", "uk", "california", "london", "canada", "germany", "singapore"]
}

AGE_PROFILES = {
    "18-24 (Gen-Z / Students)": ["student", "undergrad", "college", "intern", "cs"],
    "25-34 (Professionals)": ["engineer", "developer", "founder", "manager", "pro", "analyst"],
    "35-50 (Senior Leads)": ["director", "lead", "architect", "senior", "head", "news"]
}

def compute_demographics_breakdown(db: Session) -> dict:
    posts = db.query(Post.author_bio, Post.language).all()
    total = len(posts) or 1
    
    age_counts = Counter({k: 0 for k in AGE_PROFILES})
    age_counts["Unclassified"] = 0

    geo_counts = Counter({k: 0 for k in LOCATION_KEYWORDS})
    geo_counts["Other / Undefined"] = 0

    lang_counts = Counter()

    for bio, lang in posts:
        lang_counts[lang or "en"] += 1
        if not bio:
            age_counts["Unclassified"] += 1
            geo_counts["Other / Undefined"] += 1
            continue
            
        bio_lower = bio.lower()
        
        # Age inference
        matched_age = False
        for segment, terms in AGE_PROFILES.items():
            if any(term in bio_lower for term in terms):
                age_counts[segment] += 1
                matched_age = True
                break
        if not matched_age:
            age_counts["Unclassified"] += 1
            
        # Geographic inference
        geo_matched = False
        for region, cities in LOCATION_KEYWORDS.items():
            if any(city in bio_lower for city in cities):
                geo_counts[region] += 1
                geo_matched = True
                break
        if not geo_matched:
            geo_counts["Other / Undefined"] += 1

    return {
        "age_distribution": {k: round((v / total) * 100, 1) for k, v in age_counts.items()},
        "geographic_distribution": {k: round((v / total) * 100, 1) for k, v in geo_counts.items()},
        "language_distribution": {k: round((v / total) * 100, 1) for k, v in lang_counts.items()}
    }