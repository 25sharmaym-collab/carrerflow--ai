from app.services.skills import extract_skills
from app.services.ats import ats_check

def analyze(resume:str,jd:str)->dict:
    rs=extract_skills(resume); js=extract_skills(jd)
    required=js
    preferred=set()
    low=jd.lower()
    if "preferred" in low or "nice to have" in low:
        # Conservative: skills after the preferred marker are treated as preferred when present.
        tail=low[max(low.rfind("preferred"),low.rfind("nice to have")):]
        preferred=extract_skills(tail)
        required=js-preferred
    matched=sorted(rs & required); missing=sorted(required-rs); pref=sorted(rs & preferred)
    required_score=(len(matched)/len(required)*70) if required else 70
    preferred_score=(len(pref)/len(preferred)*20) if preferred else 20
    evidence=min(10, len(rs)*1.0)
    score=round(min(100,required_score+preferred_score+evidence))
    ats,warnings=ats_check(resume,required)
    suggestions=[f"Add a truthful project or experience example showing {s}." for s in missing[:6]]
    if not suggestions: suggestions.append("Quantify project impact and explain the technical decisions you made.")
    questions=[f"Explain how you used {s} in a project." for s in matched[:4]]
    questions += [f"How would you learn or apply {s} for this role?" for s in missing[:3]]
    return {"match_score":score,"matched_skills":matched,"missing_skills":missing,"preferred_matches":pref,"ats_score":ats,"ats_warnings":warnings,"suggestions":suggestions,"interview_questions":questions[:7]}
