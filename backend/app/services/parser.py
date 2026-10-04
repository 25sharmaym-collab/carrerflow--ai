from pathlib import Path
from io import BytesIO
from pypdf import PdfReader
from docx import Document

ALLOWED={".pdf",".docx",".txt"}

def extract_text(filename: str, data: bytes) -> str:
    ext=Path(filename).suffix.lower()
    if ext not in ALLOWED: raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
    if ext==".txt": text=data.decode("utf-8", errors="ignore")
    elif ext==".pdf": text="\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(data)).pages)
    else:
        doc=Document(BytesIO(data)); text="\n".join(p.text for p in doc.paragraphs)
    text="\n".join(line.strip() for line in text.splitlines() if line.strip())
    if len(text)<20: raise ValueError("The uploaded document does not contain enough readable text.")
    return text[:100000]

def sections(text: str) -> dict[str,str]:
    headings={"summary":"summary","objective":"summary","education":"education","experience":"experience","work experience":"experience","projects":"projects","skills":"skills","certifications":"certifications","achievements":"achievements"}
    out={k:"" for k in set(headings.values())}; current="summary"
    for line in text.splitlines():
        key=headings.get(line.lower().strip().rstrip(":"))
        if key: current=key; continue
        out[current]=(out[current]+" "+line).strip()
    return out
