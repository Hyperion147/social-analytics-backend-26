from collections import Counter
from sqlalchemy.orm import Session
from app.models.post import Post

AGE_PROFILES = {
    "18-24 (Gen-Z / Students)": ["student", "undergrad", "college", "intern", "cs"],
    "25-34 (Professionals)": ["engineer", "developer", "founder", "manager", "pro", "analyst"],
    "35-50 (Senior Leads)": ["director", "lead", "architect", "senior", "head", "news"]
}

def compute_demographics_breakdown(db: Session) -> dict:
    bios = [p.author_bio for p in db.query(Post.author_bio).filter(Post.author_bio.isnot(None)).all()]
    total = len(bios) or 1
    
    age_counts = Counter({k: 0 for k in AGE_PROFILES})
    age_counts["Unclassified"] = 0
    
    for bio in bios:
        bio_lower = bio.lower()
        matched = False
        for segment, terms in AGE_PROFILES.items():
            if any(term in bio_lower for term in terms):
                age_counts[segment] += 1
                matched = True
                break
        if not matched:
            age_counts["Unclassified"] += 1
            
    return {seg: round((count / total) * 100, 1) for seg, count in age_counts.items()}