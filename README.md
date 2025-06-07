# ChaiCode Docs Bot

A simple chatbot that answers questions about ChaiCode documentation. It talks like Hitesh bhai and gives you proper sources for everything.

## What it does

- Ask questions about coding topics covered in ChaiCode
- Get answers in Hitesh's style (Hinglish, casual, helpful)
- See exactly which docs the answer came from
- Uses your own OpenAI API key (so it's free for you to run)

## Setup

You'll need Python and an OpenAI API key.

```bash
git clone <this-repo>
cd chaidocs
pip install -r requirements.txt
python embeddings.py  # run this once to setup the data
streamlit run streamlit_app.py
```

Open the app, enter your API key, and start asking questions.

## How it works

Basic RAG setup - documents are chunked and stored as embeddings. When you ask something, it finds relevant chunks and sends them to GPT along with Hitesh's personality prompt.

## Files

- `streamlit_app.py` - main app
- `chatengine.py` - handles the AI responses with personality 
- `vector_store.py` - manages the document search
- `chunks.json` - processed documentation data
- `embeddings.py` - script to create the embeddings

## Notes

- Bring your own OpenAI API key
- Works best with questions about topics Hitesh has covered
- The personality prompt is pretty detailed to get his style right
- Uses in-memory vector store so it's simple to run

Built this to help the ChaiCode community get quick answers. Not affiliated with Hitesh or his team.
