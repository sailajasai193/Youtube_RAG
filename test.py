import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

st.title(" YouTube Chatbot")
load_dotenv() 

def is_youtube_link(url):
    youtube_regex = (
        r"(https?://)?(www\.)?"
        r"(youtube\.com|youtu\.be)/"
        r"(watch\?v=|embed/|shorts/)?"
        r"([A-Za-z0-9_-]{11})"
    )
    return re.match(youtube_regex, url)

def extract_video_id(url):
    pattern = (
        r"(?:https?:\/\/)?(?:www\.)?"
        r"(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)"
        r"([A-Za-z0-9_-]{11})"
    )
    match = re.search(pattern, url)
    return match.group(1) if match else None



youtube_link = st.text_input("Enter YouTube link")
submit_link = st.button("Submit Link")



if submit_link:
    if not is_youtube_link(youtube_link):
        st.error("Invalid YouTube link")
    else:
        video_id = extract_video_id(youtube_link)
        st.success("Thank You! You can ask Queries now")

        try:
            fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=['hi', 'en'])
            transcript_list = fetched_transcript.to_raw_data()
            transcript = " ".join(chunk["text"] for chunk in transcript_list)

            
            st.session_state.transcript = transcript

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            chunks = splitter.create_documents([transcript])

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            vector_store = FAISS.from_documents(chunks, embeddings)
            st.session_state.retriever = vector_store.as_retriever(
                search_type="similarity", search_kwargs={"k": 4}
            )


        except TranscriptsDisabled:
            st.error(" Transcripts are disabled for this video")
        except Exception as e:
            st.error(f"Error: {e}")


if "retriever" in st.session_state:
    st.subheader("Ask your question")

    with st.form("qa_form"):
        query = st.text_input("Your Query")
        ask = st.form_submit_button("Ask")

    if ask and query.strip():
        docs = st.session_state.retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

        response = llm.invoke(
            f"Context:\n{context}\n\nQuestion:\n{query}"
        )

        st.markdown("### Answer")
        st.write(response.content)
