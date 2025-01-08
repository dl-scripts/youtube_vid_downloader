import streamlit as st
from pytube import YouTube
import re

def download_video(url, quality='highest'):
    try:
        # Validate URL
        if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', url):
            raise ValueError("Invalid YouTube URL")
        
        yt = YouTube(url)
        
        # Select stream based on quality
        if quality == 'highest':
            stream = yt.streams.get_highest_resolution()
        elif quality == 'lowest':
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(res=quality).first()
        
        # Download video
        stream.download()
        return yt.title

    except ValueError as ve:
        return f"Error: {str(ve)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title('YouTube Video Downloader')

url = st.text_input('Enter YouTube video URL')
qualities = ['highest', 'lowest', '360p', '720p', '1080p']
quality = st.selectbox('Select video quality', qualities)

if st.button('Download'):
    if url:
        title = download_video(url, quality)
        if "Error" in title:
            st.error(title)
        else:
            st.success(f'Video "{title}" has been downloaded successfully!')
    else:
        st.error('Please enter a valid YouTube URL')
