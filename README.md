# Facilitator Game Assistant

AI with local knowledge: a Thai-language assistant that recommends facilitation games
using **only** the content of the book "อาวุธลับกระบวนกร 50 เกมนันทนาการ" (50 recreation games).

## Team
- Daranphop Riwlertsirikul (Santa Claus) - 6858040056

## Topic
A user describes the situation (group size, time, goal such as icebreaking or building
closeness) and the assistant recommends suitable games with how-to-play instructions,
grounded in retrieved passages from the book (RAG).

## How it works
1. `src/ingest.py` extracts text from the PDF, splits it into chunks, embeds them locally
   (multilingual sentence-transformers) and saves an index.
2. `src/ask.py` embeds the question, retrieves the top chunks and asks an LLM to answer
   using only those chunks, citing page numbers.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # never commit this
```
Put the book PDF at `data/book.pdf` (not included in this repo for copyright reasons).

```bash
python src/ingest.py
python src/ask.py "เกมละลายพฤติกรรม 40 คน ใช้เวลา 15 นาที"
```

## Evaluation idea
Compare answers with and without the book: does the model invent games, and are the
cited pages correct?
