import streamlit as st
import fitz  # PyMuPDF
from gtts import gTTS
from io import BytesIO

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()
    return pdf_text

# Function to convert text to speech
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Streamlit App
st.title("Podcast Generator from PDF")
st.write("Upload a PDF file, and this app will generate an audio version (podcast) for you.")

uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_pdf is not None:
    # Extract text from PDF
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
    
    # Display extracted text preview
    if pdf_text:
        st.write("**Preview of Extracted Text:**")
        st.write(pdf_text[:500] + "...")  # Show only the first 500 characters

        # Convert to speech
        with st.spinner("Converting text to audio..."):
            audio_data = text_to_speech(pdf_text)

        # Provide audio download
        st.audio(audio_data, format="audio/mp3")
        st.download_button(
            label="Download Podcast",
            data=audio_data,
            file_name="podcast.mp3",
            mime="audio/mp3"
        )
    else:
        st.error("No text found in the PDF file. Please try another file.")
