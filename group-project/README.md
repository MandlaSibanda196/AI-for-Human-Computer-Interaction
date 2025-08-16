# 🌲 US National Parks RAG Chatbot

A simple Retrieval Augmented Generation (RAG) chatbot built with Streamlit and Together AI. Ask questions about US National Parks and get AI-powered responses based on curated park information.

## Features

- **Clean Data**: Professionally formatted and fact-checked National Parks information
- **Smart RAG Implementation**: Uses sentence-transformers for embeddings and Together AI for generation
- **Always Uses AI**: google/gemma-3n-E4B-it model generates natural, contextual responses for every query
- **Source Attribution**: Shows which documents were used to generate responses
- **Interactive Chat**: Streamlit-based chat interface with conversation history
- **Cloud AI Integration**: Uses Together AI for high-quality response generation

## Quick Start

1. **Clone and Setup**
   ```bash
   cd group-project
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Get Together AI API Key**
   - Sign up at [together.ai](https://together.ai)
   - Navigate to your dashboard and create an API key
   - Copy the `env.example` file to `.env`:
     ```bash
     cp env.example .env
     ```
   - Edit the `.env` file and replace `your-together-ai-api-key-here` with your actual API key:
     ```
     TOGETHER_API_KEY=your-actual-api-key-here
     ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

4. **Start Chatting**
   - Open your browser to `http://localhost:8501`
   - Ask questions like "What parks are in California?" or "Tell me about Yellowstone"

## How It Works

1. **Document Processing**: Loads the consolidated parks data file and chunks it into meaningful sections
2. **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` to create vector embeddings
3. **Similarity Search**: Finds most relevant chunks using cosine similarity
4. **Response Generation**: Uses Together AI's google/gemma-3n-E4B-it model to create natural responses based on retrieved context

## Data Sources

**Single comprehensive data file:**
- `data/consolidated-parks.txt` - Complete consolidated information about all 63 US National Parks including:
  - Detailed descriptions, visitor numbers, and highlights for each park
  - Activities, features, and best times to visit
  - Parks organized by categories (mountain, desert, coastal, etc.)
  - Extreme records and planning information
  - Access and transportation details

**Data Quality:** The consolidated file has been professionally cleaned and formatted for optimal RAG performance, with consistent formatting, accurate information, and organized structure for efficient search and retrieval.

## Models Used

- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (CPU-friendly)
- **Text Generation**: `google/gemma-3n-E4B-it` (via Together AI API)

### Why Together AI?
- High-quality responses from state-of-the-art models
- Fast inference times
- Simple API integration
- Cost-effective for small to medium usage

## Project Structure

```
group-project/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── env.example        # Environment variables template
├── .gitignore         # Git ignore file
├── data/              # National parks text data
└── docs/              # Project documentation
```

## Customization

To modify the chatbot:
- **Change models**: Edit `MODEL_NAME` and `TOGETHER_MODEL` constants in `app.py`
- **Update data**: Modify `data/consolidated-parks.txt` or replace with your own comprehensive data file
- **Adjust chunking**: Modify `CHUNK_SIZE` and `OVERLAP` parameters
- **Update similarity threshold**: Change the threshold in `search_similar_chunks()`

## Requirements

- Python 3.10+
- 2GB+ RAM (for loading embedding models)
- Internet connection (for Together AI API and model downloads)
- Together AI API key (free tier available)

