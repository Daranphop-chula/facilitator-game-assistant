import json, pathlib, sys
import numpy as np
import anthropic
from sentence_transformers import SentenceTransformer

ROOT = pathlib.Path(__file__).resolve().parent
MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

question = " ".join(sys.argv[1:])
emb = np.load(ROOT / "index" / "emb.npy")
chunks = json.loads((ROOT / "index" / "chunks.json").read_text())

q = SentenceTransformer(MODEL).encode([question], normalize_embeddings=True)[0]
top = np.argsort(emb @ q)[::-1][:6]
context = "\n\n".join(f"[p.{chunks[i]['page']}] {chunks[i]['text']}" for i in top)

msg = anthropic.Anthropic().messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1000,
    system="Answer in Thai using ONLY the book excerpts given. Recommend games, explain how to play, cite page numbers like (p.46). If the excerpts do not cover it, say so.",
    messages=[{"role": "user", "content": f"Excerpts:\n{context}\n\nQuestion: {question}"}],
)
print(msg.content[0].text)
