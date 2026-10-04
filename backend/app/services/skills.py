import re

ALIASES={
 "javascript":"javascript","js":"javascript","typescript":"typescript","ts":"typescript","react.js":"react","reactjs":"react","nextjs":"next.js","next.js":"next.js","nodejs":"node.js","node.js":"node.js","postgres":"postgresql","postgresql":"postgresql","scikit learn":"scikit-learn","sklearn":"scikit-learn","ml":"machine learning","machine learning":"machine learning","rest api":"rest api","restful api":"rest api"
}
SKILLS=sorted(set(ALIASES.values())|{"python","java","c++","sql","html","css","fastapi","node.js","docker","git","github","mongodb","firebase","pandas","numpy","scikit-learn","tensorflow","pytorch","aws","azure","linux","kubernetes","figma","tailwind","php","spring boot","data structures","algorithms","postgresql","machine learning","deep learning","generative ai","llm","rag"})

def normalize(text:str)->str:
    t=text.lower()
    for alias,canonical in sorted(ALIASES.items(),key=lambda x:-len(x[0])): t=re.sub(r"(?<!\\w)"+re.escape(alias)+r"(?!\\w)",canonical,t)
    return t

def extract_skills(text:str)->set[str]:
    t=normalize(text); return {s for s in SKILLS if re.search(r"(?<!\\w)"+re.escape(s)+r"(?!\\w)",t)}
