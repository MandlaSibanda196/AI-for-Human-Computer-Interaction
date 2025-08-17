Group Project Proposal 

Course: 2025 Summer - Artificial Intelligence for Human-Computer Interaction (MSAI-631-B01) 
 Project Title: Conversational Chatbot for U.S. National Parks 

  

Overview 

This group project explores the application of Human-Computer Interaction (HCI) principles through the development of a conversational agent that helps users learn about national parks in the United States. The chatbot will accept natural language queries, retrieve relevant passages from a knowledge base of national park summaries, and respond conversationally using a Retrieval-Augmented Generation (RAG) pipeline. 

  

The project aims to showcase how AI models combined with thoughtful interaction design can facilitate a smooth, informative, and intuitive user experience. Our solution simulates a real-world use case in travel, education, or tourism support, where users might want to ask questions like: 
 “Which national parks are in California?” 
 “Tell me about Yellowstone’s wildlife.” 
 “What are the most visited parks?” 

 

By combining simple file-based knowledge with embedding-based retrieval and conversational UI via Streamlit, we will build a lightweight but effective proof-of-concept chatbot. 

Project Construction 

The project will be built entirely using open-source tools and local environments. The chatbot will be developed on personal laptops and tested both locally and in Google Colab to ensure platform flexibility. The knowledge base will be a plain-text file containing summarized facts and details about national parks (e.g., name, location, features, notable facts). We will scrap data from a list of relevant online sources like: 

https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States 

https://www.national-park.com/list-of-national-parks-in-the-united-states-2020/ 

https://www.leeabbamonte.com/north-america/national-parks/all-63-us-national-parks-ranked.html 

https://www.wellplannedjourney.com/list-of-national-parks-by-state/ 

 

We will use this to make our knowledge base. This structure aligns with free-tier constraints and makes the project easy to deploy and demonstrate. 

 

For deployment, we will use Streamlit, a Python-based open-source framework for interactive web applications. Streamlit provides an accessible interface for users and is compatible with the conversational memory logic we intend to implement. 

 

Version Control 

We will use GitHub as our version control platform. A public repository will be created and shared with the instructor. The GitHub repository will contain all source code, documentation, environment setup instructions, and sample data files. All group members will commit to the repository regularly to ensure transparency and collaboration. 

 

Tools, Libraries, and Software 

We will use the following tools and libraries: 

Streamlit – for the web interface and chat component 

LangChain – to manage retrieval chains and conversational context 

FAISS – to store and retrieve vector embeddings efficiently 

Sentence-Transformers (all-MiniLM-L6-v2) – for text embeddings 

Python Standard Libraries – for data loading, parsing, and preprocessing 

Pandas – for any tabular manipulations if needed 

Google Colab – for prototyping and testing in the cloud (if needed) 

 

All tools are free to use and compatible with local or low-resource environments. 

 

Candidate Models 

The following models are under consideration for the chatbot pipeline: 

Embedding Model: 

sentence-transformers/all-MiniLM-L6-v2 – Lightweight and effective for sentence similarity. 

Language Model (for response generation or summarization): 

https://huggingface.co/Qwen/Qwen1.5-110B-Chat 

https://huggingface.co/mistralai/Mixtral-8x22B-v0.1 

https://huggingface.co/google/gemma-2b 

 

We will start with a non-generative response format (retrieval only) and layer in generation capability as a stretch goal. 

 

Group Member Contributions 

Our team consists of three members who will divide responsibilities as follows: 

Mandlenkosi Sibanda – Handles frontend development using Streamlit and designs the interaction flow. 

Kumar Abhinav – Manages embedding, chunking, FAISS index creation, and model integration. 

Siddhartha Prithvi Chebiyyam – Develops the knowledge base, manages GitHub versioning, and documents the technical workflow. 

 

All members will contribute to writing the final report and preparing the presentation. 

 

 