import streamlit as st
from api_calling import note_generator, audio_transcript, Quize_generator
from PIL import Image
from markdown import markdown
from bs4 import BeautifulSoup

# Tittle
st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Controls")
    
    # Images
    images = st.file_uploader(
        "Upload the photos of your note",
        type=['jpg','png','jpeg'],
        accept_multiple_files=True
    )
    
    if images:
        pil_images = [Image.open(img) for img in images]
    
    if images:
        if len(images) > 3:
            st.warning("Upload at max 3 images")
        else:
            st.subheader("Uploaded images")
            col = st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)
                    
    # Difficulty
    selected_option = st.selectbox(
        "Enter the difficulty of your Quiz",
        ("Easy","Medium","Hard"),
        index=None
    )
    
    if selected_option:
        st.markdown(f"You selected **{selected_option}** as your difficulty")
    
    pressed = st.button("Click the button to initiate ai",type="primary")
    
        
if pressed:
    if not images:
        st.error("Upload atlest 1 image")
    if not selected_option:
        st.error("Select a difficulty")
        
    if images and selected_option:
        # Note
        with st.container(border=True):
            st.subheader("Your note")
            with st.spinner("Ai is writing note for you..."):
                genareted_note = note_generator(pil_images)
                st.markdown(genareted_note)
            
        # Audio transcript
        with st.container(border=True):
            st.subheader("Audio Transcription")
            html = markdown(genareted_note)
            clened_note = BeautifulSoup(html,"html.parser").get_text()
            with st.spinner("Audio transcript genareting..."):
                genareted_audio = audio_transcript(clened_note)
                st.audio(genareted_audio)
            
        # Quiz
        with st.container(border=True):
            st.subheader(f"Quiz Difficulty ({selected_option})")
            with st.spinner("Quizes are generating..."):
                quize = Quize_generator(pil_images,selected_option)
                st.markdown(quize)
            
            