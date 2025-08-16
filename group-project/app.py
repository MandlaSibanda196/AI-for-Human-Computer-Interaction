import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from together import Together
import os
from pathlib import Path
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="US National Parks RAG Chatbot",
    page_icon="🌲",
    layout="centered"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOGETHER_MODEL = "google/gemma-3n-E4B-it" 

CHUNK_SIZE = 300
OVERLAP = 50

@st.cache_resource
def load_models():
    """Load the embedding model and initialize Together AI client"""
    try:
        embedding_model = SentenceTransformer(MODEL_NAME)
        together_client = Together()
        
        return embedding_model, together_client
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

@st.cache_data
def load_and_process_data():
    """Load and process the consolidated national parks data"""
    data_file = Path("data/consolidated-parks.txt")
    
    if not data_file.exists():
        st.error("Consolidated parks data file not found!")
        return [], []
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        st.error(f"Could not load data file: {e}")
        return [], []
    
    chunks = []
    sections = content.split('\n\n')
    
    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) > 100:
            if "annual visitors" in section and ("National Park" in section or "Park (" in section):
                chunks.append({
                    'text': section,
                    'source': 'consolidated-parks.txt',
                    'chunk_id': f"park_{i}"
                })
            elif any(keyword in section.lower() for keyword in ['california', 'desert parks', 'mountain parks', 'coastal parks', 'for families', 'for photography', 'best times']):
                chunks.append({
                    'text': section,
                    'source': 'consolidated-parks.txt', 
                    'chunk_id': f"section_{i}"
                })
    
    return chunks, [chunk['text'] for chunk in chunks]

@st.cache_data
def create_embeddings(_embedding_model, chunk_texts):
    """Create embeddings for all chunks"""
    if not chunk_texts:
        return np.array([])
    
    try:
        embeddings = _embedding_model.encode(chunk_texts, show_progress_bar=True)
        return embeddings
    except Exception as e:
        st.error(f"Error creating embeddings: {e}")
        return np.array([])

def search_similar_chunks(query, embedding_model, embeddings, chunks, top_k=3):
    """Search for similar chunks using cosine similarity"""
    if len(embeddings) == 0:
        return []
    
    try:
        # Encode query
        query_embedding = embedding_model.encode([query])
        
        # Calculate similarities
        similarities = np.dot(query_embedding, embeddings.T)[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.15:
                results.append({
                    'chunk': chunks[idx],
                    'similarity': similarities[idx]
                })
        
        return results
    except Exception as e:
        st.error(f"Error in search: {e}")
        return []

def generate_response(query, search_results, together_client=None):
    """Generate response using Together AI based on search results"""
    if not search_results:
        return "I couldn't find relevant information about that topic in the National Parks database."
    
    context_parts = []
    for result in search_results[:3]:
        chunk_text = result['chunk']['text'][:400]
        source = result['chunk']['source']
        context_parts.append(f"{chunk_text}")
    
    context = "\n\n".join(context_parts)
    fallback_response = f"Here are the relevant National Parks for your question:\n\n"
    
    for i, result in enumerate(search_results[:3], 1):
        chunk_text = result['chunk']['text'].strip()
        source = result['chunk']['source']
        similarity = result['similarity']
        
        if "annual visitors" in chunk_text and "National Park" in chunk_text:
            lines = chunk_text.split('\n')
            park_name = lines[0] if lines else chunk_text[:100]
            
            description = ""
            for line in lines[1:4]:
                if line.startswith("Description:"):
                    description = line.replace("Description:", "").strip()
                    break
            
            if description:
                fallback_response += f"**{park_name}**\n{description}\n\n"
            else:
                sentences = chunk_text.split('. ')
                excerpt = '. '.join(sentences[:2])
                if not excerpt.endswith('.'):
                    excerpt += '.'
                fallback_response += f"**{excerpt}**\n\n"
        else:
            sentences = chunk_text.split('. ')
            excerpt = '. '.join(sentences[:2])
            if not excerpt.endswith('.'):
                excerpt += '.'
            fallback_response += f"{excerpt}\n\n"
    
    fallback_response += "*This information was retrieved from the National Parks database.*"
    if together_client:
        try:
            with st.spinner("Generating response..."):
                response = together_client.chat.completions.create(
                    model=TOGETHER_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful National Parks expert. Answer questions about US National Parks using only the provided context. Be concise, informative, and helpful. Focus on practical information for visitors."
                        },
                        {
                            "role": "user", 
                            "content": f"Context:\n{context}\n\nQuestion: {query}\n\nPlease provide a helpful answer based on the context above."
                        }
                    ],
                    max_tokens=200,
                    temperature=0.7,
                    top_p=0.9
                )
                
                if response and response.choices and len(response.choices) > 0:
                    ai_response = response.choices[0].message.content.strip()
                    if len(ai_response) > 20:
                        return ai_response
                        
        except Exception as e:
            st.warning(f"AI generation failed: {str(e)[:100]}")
    
    return fallback_response

def main():
    st.title("🌲 US National Parks RAG Chatbot")
    st.markdown("Ask questions about US National Parks! This chatbot uses RAG (Retrieval Augmented Generation) to find relevant information.")
    
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This is a simple RAG application that:
        - Uses sentence-transformers for embeddings
        - Searches through consolidated National Parks data
        - Generates responses using Together AI (google/gemma-3n-E4B-it)
        """)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    if not os.getenv("TOGETHER_API_KEY"):
        st.error("⚠️ **Together AI API Key Required**")
        st.markdown("""
        To use this chatbot, you need to set up a Together AI API key:
        
        1. Sign up at [together.ai](https://together.ai)
        2. Get your API key from your dashboard
        3. Set the environment variable: `export TOGETHER_API_KEY="your-api-key"`
        4. Or create a `.env` file with: `TOGETHER_API_KEY=your-api-key`
        """)
        st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.spinner("Loading models and data..."):
        embedding_model, together_client = load_models()
        if embedding_model is None:
            st.stop()
        
        chunks, chunk_texts = load_and_process_data()
        if not chunks:
            st.stop()
        
        embeddings = create_embeddings(embedding_model, chunk_texts)
        if len(embeddings) == 0:
            st.stop()
    
    st.success(f"✅ Loaded {len(chunks)} text chunks from consolidated National Parks data")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about National Parks..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching and generating response..."):
                search_results = search_similar_chunks(
                    prompt, embedding_model, embeddings, chunks
                )
                
                response = generate_response(prompt, search_results, together_client)
                
                st.markdown(response)
                if search_results:
                    with st.expander("📚 Sources"):
                        for i, result in enumerate(search_results[:3]):
                            st.write(f"**Source {i+1}:** {result['chunk']['source']}")
                            st.write(f"**Similarity:** {result['similarity']:.3f}")
                            st.write(f"**Text:** {result['chunk']['text'][:200]}...")
                            st.divider()
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
