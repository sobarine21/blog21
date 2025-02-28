import streamlit as st
import pymupdf as fitz  # PyMuPDF
from gtts import gTTS
from io import BytesIO

# Function to extract text from PDF file
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    total_pages = doc.page_count
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()
        # Provide feedback for each page processed
        yield page_num + 1, total_pages  # page_num starts at 0, so add 1 for display
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
    # Create a progress bar for file processing
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Start extracting text
    with st.spinner("Extracting text from PDF..."):
        try:
            text_generator = extract_text_from_pdf(uploaded_pdf)
            pdf_text = ""
            page_count = 0
            total_pages = 1  # Default to 1 page if file is empty (avoid division by 0)
            for page_num, total_pages in text_generator:
                page_count += 1
                pdf_text += f"Page {page_num} processed.\n"  # Optional debug log
                # Update progress bar proportionally
                progress_bar.progress(page_count / total_pages)
                status_text.text(f"Processing page {page_num} of {total_pages}...")
            if not pdf_text:
                raise Exception("No text found in the PDF.")
            st.success("Text extraction complete.")
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            pdf_text = None
    
    # If text extraction successful, convert text to speech
    if pdf_text:
        st.write("**Preview of Extracted Text:**")
        st.write(pdf_text[:500] + "...")  # Show only the first 500 characters

        # Convert to speech and show a progress bar for this task
        with st.spinner("Converting text to audio..."):
            try:
                audio_data = text_to_speech(pdf_text)
            except Exception as e:
                st.error(f"Error during text-to-speech conversion: {e}")
                audio_data = None

        if audio_data:
            # Provide audio playback and download options
            st.audio(audio_data, format="audio/mp3")
            st.download_button(
                label="Download Podcast",
                data=audio_data,
                file_name="podcast.mp3",
                mime="audio/mp3"
            )

    else:
        st.error("No text found in the PDF file. Please try another file.")
