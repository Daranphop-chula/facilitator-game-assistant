import json, pathlib
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
CHUNK, OVERLAP = 800, 150

reader = PdfReader(ROOT / "data" / "book.pdf")
chunks = []
for page_no, page in enumerate(reader.pages, start=1):
    text = (page.extract_text() or "").strip()
    for i in range(0, len(text), CHUNK - OVERLAP):
        piece = text[i:i + CHUNK]
        if len(piece) > 50:
            chunks.append({"page": page_no, "text": piece})

emb = SentenceTransformer(MODEL).encode([c["text"] for c in chunks], normalize_embeddings=True)
out = ROOT / "index"
out.mkdir(exist_ok=True)
np.save(out / "emb.npy", emb)
(out / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False))
print(f"{len(chunks)} chunks indexed")
