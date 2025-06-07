# ☕ ChaiCode Docs Bot

A smart AI chatbot that answers questions about ChaiCode documentation using RAG (Retrieval Augmented Generation). Built with Hitesh Choudhary's teaching personality and expertise.

## 🚀 Features

- **AI-Powered Responses** - Uses OpenAI GPT-4o-mini for fast, accurate answers
- **RAG Implementation** - Searches through ChaiCode documentation for relevant context
- **Hitesh's Personality** - Responds in Hitesh Choudhary's signature Hinglish style
- **Source Citations** - Every answer includes clickable source references
- **User API Keys** - Secure - you use your own OpenAI API key
- **Modern UI** - Clean, responsive Streamlit interface
- **Fast Performance** - Optimized with caching for quick responses

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Internet connection

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chaidocs
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Run the embeddings (first time only)**
   ```bash
   uv run python embeddings.py
   # or
   python embeddings.py
   ```

4. **Start the app**
   ```bash
   uv run streamlit run streamlit_app.py
   # or
   streamlit run streamlit_app.py
   ```

## 🎯 Usage

1. **Open the app** in your browser (usually `http://localhost:8501`)
2. **Enter your OpenAI API key** when prompted
3. **Start chatting!** Ask any questions about ChaiCode documentation
4. **View sources** - Click on source links to see where answers come from

## 📁 Project Structure

```
├── streamlit_app.py      # Main Streamlit application
├── chatengine.py         # Chat engine with Hitesh's personality
├── vector_store.py       # Qdrant vector database integration
├── embeddings.py         # Script to create embeddings
├── ingestion.py          # Documentation ingestion script
├── chunks.json           # Pre-processed documentation chunks
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🤖 How It Works

1. **Document Processing** - ChaiCode docs are chunked and embedded
2. **Vector Search** - User questions are matched against doc embeddings
3. **Context Retrieval** - Most relevant chunks are retrieved
4. **AI Generation** - OpenAI generates responses with Hitesh's personality
5. **Source Attribution** - Responses include clickable source links

## 🔧 Technology Stack

- **Frontend:** Streamlit
- **AI Model:** OpenAI GPT-4o-mini
- **Vector DB:** Qdrant (in-memory)
- **Embeddings:** OpenAI text-embedding-3-large
- **Language:** Python 3.8+

## 🛡️ Privacy & Security

- **Your API key stays with you** - Never stored on servers
- **Session-based** - Keys only stored in browser session
- **No data collection** - Your conversations aren't saved
- **Local processing** - Runs entirely on your machine

## 🎨 Customization

Want to modify the bot's personality or add your own docs?

1. **Edit personality** - Modify the system prompt in `chatengine.py`
2. **Add documents** - Update `ingestion.py` with your content
3. **Change UI** - Customize styling in `streamlit_app.py`

## 🚀 Deployment

### Streamlit Cloud
1. Fork this repository
2. Connect to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy directly from GitHub

### Docker
```bash
# Build image
docker build -t chaidocs-bot .

# Run container
docker run -p 8501:8501 chaidocs-bot
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 About

Built with ❤️ for the ChaiCode community. This bot helps developers quickly find answers from Hitesh Choudhary's vast educational content.

### Connect
- **YouTube:** [Chai aur Code](https://www.youtube.com/@chaiaurcode)
- **Website:** [ChaiCode](https://chaicode.com)

---

**Note:** This is a community project and not officially affiliated with Hitesh Choudhary or Chai aur Code.
