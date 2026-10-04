import re

def ats_check(text:str, required:set[str])->tuple[int,list[str]]:
    words=text.split(); warnings=[]; score=100
    low=text.lower()
    if len(words)<150: warnings.append("Resume is short; add relevant project or experience evidence."); score-=15
    if len(words)>1200: warnings.append("Resume is long; reduce non-essential content."); score-=15
    for h in ("education","experience","projects","skills"):
        if h not in low: warnings.append(f"Missing clear {h} section."); score-=10
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+",text): warnings.append("No email address detected."); score-=10
    if required and not (extract:=sum(1 for s in required if s in low)):
        warnings.append("No job-relevant skills were detected in the resume."); score-=20
    return max(0,score),warnings
