# text_extractor_app.py

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import requests
from bs4 import BeautifulSoup

# Function to extract text from YouTube video
def extract_youtube_transcript(video_url, language_code):
    video_id = video_url.split("v=")[-1]
    available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    
    try:
        transcript = available_transcripts.find_transcript([language_code])
        return ' '.join([entry['text'] for entry in transcript.fetch()])
    except NoTranscriptFound:
        return f"No transcripts found for the selected language '{language_code}'. Available languages: {available_transcripts.languages}"
    except Exception as e:
        return str(e)

# Function to extract text from blog post URL
def extract_blog_text(blog_url):
    response = requests.get(blog_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([para.get_text() for para in paragraphs])

# Streamlit app interface
st.set_page_config(page_title="Text Extractor", layout="centered")  # Centered layout

# Add title and description
st.title("🎤 Text Extractor from YouTube and Blogs 🌐")
st.write("Select an option below to extract text from a YouTube video or a blog post.")

# Dropdown for source selection
source_type = st.selectbox("Select Source Type:", ["YouTube Video", "Blog Post"])

# Input field based on the selected source
url = st.text_input("Enter URL:")

# Language dropdown
language_options = ["en", "hi", "ur", "fr", "es", "de"]
language = st.selectbox("Select Language:", language_options)

# Button to extract text
if st.button("Extract Text"):
    if url:
        try:
            if source_type == "YouTube Video":
                transcript_text = extract_youtube_transcript(url, language)
                st.subheader("Transcript:")
                st.write(transcript_text)

                # Add a button to download the transcript
                st.download_button(
                    label="Download Transcript",
                    data=transcript_text,
                    file_name="transcript.txt",
                    mime="text/plain"
                )
            else:
                blog_text = extract_blog_text(url)
                st.subheader("Blog Text:")
                st.write(blog_text)

                # Add a button to download the blog text
                st.download_button(
                    label="Download Blog Text",
                    data=blog_text,
                    file_name="blog_text.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error extracting text: {e}")
    else:
        st.warning("Please enter a valid URL.")

# Add custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f0f8ff;
            color: #333;
            max-width: 700px;  /* Set a maximum width */
            margin: 0 auto;  /* Center the app */
        }
        .stButton > button {
            background-color: #1e90ff;
            color: white;
        }
        h1 {
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        h2 {
            color: #4682b4;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add animations
st.balloons()
