import streamlit as st
from pytube import YouTube
import pytube.request

# Set a custom User-Agent header
pytube.request.default_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def download_video(url, quality='highest'):
    try:
        # Validate URL
        if not "youtube.com" in url and not "youtu.be" in url:
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

    except Exception as e:
        # Return detailed error message
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
