## 🔗 Deployed Application
https://youtuberag-thjtdyakbgaqiqkt8agfku.streamlit.app/



# YouTube Chatbot 

A **Streamlit web application** that allows users to ask questions about any YouTube video and get context-aware answers using AI.The app fetches video transcripts and uses embeddings for semantic search.

---

## Features 

- **YouTube Transcript Retrieval** – Fetches transcripts from YouTube videos (supports English).  
- **Context-Aware Q&A** – Ask questions about a video, and get answers based on the transcript.  
- **Semantic Search** – Uses vector embeddings to retrieve relevant chunks of transcript for accurate answers.  
- **Multiple Languages** – Supports English video transcripts.  
- **User-Friendly UI** – Built using Streamlit with forms and interactive input.  
- **Error Handling** – Displays errors for invalid links or videos without transcripts.  

---

## Technologies Used 

- **Python** – Programming language for the backend logic.  
- **Streamlit** – Frontend framework for building interactive web apps.  
- **YouTube Transcript API** – Fetch video transcripts programmatically.  
- **LangChain** – For textsplitting, vector store creation, and LLM interactions.  
- **FAISS** – Vector database for semantic search of transcript chunks.  
- **HuggingFace Embeddings** – Converts text into embeddings for semantic similarity.  
- **ChatGroq** – Large language model used for answering questions based on context.  
- **dotenv** – Manages API keys and environment variables securely.  
- **Regex** – For validating and extracting YouTube video IDs.  

