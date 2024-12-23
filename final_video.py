import streamlit as st
from streamlit_player import st_player
import json
import os
import isodate

from transformers import pipeline
import yt_dlp
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
import torch

from transcribe import pipeline

# Initialize the sentence embedding model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

st.title("VidyaVeda – Empowering Learning with Personalized AI")

# User inputs for main subject and subsections
main_subject = st.text_input("Enter the main subject:")
subsections = st.text_input("Enter the subsections you want to study:")

if main_subject and subsections:
    # Create the query based on user input
    query = f"{main_subject} {subsections} english"
    st.write(f"Searching for videos on: {query}")

    # YouTube API setup
    api_key = "AIzaSyByyiNnGHhxY2PYDIB5X8SaGAmX9lEGAMY"  
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Function to search YouTube videos based on the topic
    def get_video_data(topic):
        
        search_response = youtube.search().list(
            q=topic,
            part="snippet",
            type="video",
            maxResults=10,
            order="relevance",
            videoCategoryId="27",  # Education category (optional)
            relevanceLanguage="en"
        ).execute()

        video_data = []
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        stats_response = youtube.videos().list(
            part="statistics,snippet,contentDetails",  # Add 'contentDetails' to part
            id=",".join(video_ids)
        ).execute()

        for item in stats_response['items']:
            video_info = {
                "video_id": item['id'],
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "view_count": int(item['statistics'].get('viewCount', 0)),
                "duration": item['contentDetails']['duration'],
                "like_count": int(item['statistics'].get('likeCount', 0)) # Use get() to handle missing 'likeCount' # Add this line to get duration
            }

            video_data.append(video_info)

        return video_data
    transc = None
    # Function to compute subtitle similarity
    def get_subtitle_similarity(video_id, topic):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            subtitles = " ".join([item['text'] for item in transcript])

            topic_embedding = model.encode(topic)
            subtitle_embedding = model.encode(subtitles)

            similarity_score = torch.nn.functional.cosine_similarity(
                torch.tensor(topic_embedding).unsqueeze(0),
                torch.tensor(subtitle_embedding).unsqueeze(0)
            ).item()
            f = open("file.txt","w")
            f.write(subtitles)

            transc = subtitles
            return similarity_score
        except Exception:
            return 0
    selection_mode = st.radio(
        "Select the type of video scoring method:",
        ("select",'Overview', 'Top Rated', 'Detailed')
    )



    # Function to compute the final score
    def get_combined_score(video, topic, mode):
        def parse_duration(duration):
            parsed_duration = isodate.parse_duration(duration)
            return parsed_duration.total_seconds()
        duration_score = parse_duration(video['duration'])

        engagement_score = video['view_count'] / 1000  # Normalized views
        subtitle_similarity = get_subtitle_similarity(video['video_id'], topic)
        likes_score = video['like_count'] / 1000
         # Normalized likes
        # duration_score = video['duration'] 

        duration_score = float(duration_score) # Duration is already in minutes
        if mode =="select":
            st.write('select the options below')
        # For Overview: Give higher score for shorter videos
        if mode == 'Overview':
            if duration_score > 0:
                duration_score = 1 / duration_score  # Invert duration score (lower time gets higher score)
            final_score = (0.2 * duration_score) + (0.4 * engagement_score) + (0.4 * likes_score)

        # For Top Rated: Focus on engagement and likes
        elif mode == 'Top Rated':
            final_score = (0.6 * engagement_score) + (0.4 * likes_score)

        # For Detailed: Give higher score for longer videos
        elif mode == 'Detailed':
            final_score = (0.6 * duration_score) + (0.3 * engagement_score) + (0.1 * likes_score)

        else:
            final_score = 0  # Fallback if no mode matches

        return final_score, engagement_score, subtitle_similarity, likes_score, duration_score

    # Find the best video based on engagement and subtitle relevance
    def get_best_video(topic, mode):
        videos = get_video_data(topic)
        scored_videos = []

        for video in videos:
            final_score, engagement_score, subtitle_similarity, likes_score, duration_score = get_combined_score(video, topic, mode)
            scored_videos.append((video, final_score, engagement_score, subtitle_similarity, likes_score, duration_score))

        scored_videos.sort(key=lambda x: x[1], reverse=True)
        best_video = scored_videos[0]
        return best_video

    best_video, final_score, engagement_score, subtitle_similarity, likes_score, duration_score = get_best_video(query, selection_mode)
    video_url = f"https://www.youtube.com/watch?v={best_video['video_id']}"
    st.write(f"Best video found: {best_video['title']}")
    st.write(f"Video URL: {video_url}")


    with st.expander("Why was this video recommended?"):
        st.write(f"**Engagement Metrics**")
        st.write(f"- Views: {best_video['view_count']}")
        st.write(f"- Likes: {best_video['like_count']}")
        st.write(f"- Duration: {best_video['duration']} minutes")
        st.write(f"Engagement Score: {engagement_score:.2f}")

        st.write(f"\n**Content Relevance**")
        st.write(f"Subtitle similarity to the topic '{query}': {subtitle_similarity:.2f}")

        st.write(f"\n**Final Score**")
        st.write(f"The overall score of this video is: {final_score:.2f}")
        st.write(f"**Mode Selected**: {selection_mode}")
        st.write("This video was selected based on its combination of engagement and relevant content based on your selected mode.")

    if video_url:
        st.write("Downloading and processing the video...")

        def download_audio(url):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded_video.%(ext)s',  # Save file with this name
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '32',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        try:
            download_audio(video_url)
            st.success("Audio downloaded successfully!")
            mp3_file = 'downloaded_video.mp3'

            # Run the transcription pipeline on the downloaded MP3
            st.write("Starting transcription...")
            pipeline(mp3_file)

            st.write("Transcription and highlight generation completed!")

            # Load generated highlights and chapters
            file_highlights = 'highlights.json'
            file_chapters = 'chapters.json'
            url = video_url

            placeholder = st.empty()
            with placeholder.container():
                st_player(url, playing=False, muted=True)

            mode = st.sidebar.selectbox("Summary Mode", ("Highlights", "Chapters"))

            def get_btn_text(start_ms):
                seconds = int((start_ms / 1000) % 60)
                minutes = int((start_ms / (1000 * 60)) % 60)
                hours = int((start_ms / (1000 * 60 * 60)) % 24)
                return f'{hours:02d}:{minutes:02d}:{seconds:02d}' if hours > 0 else f'{minutes:02d}:{seconds:02d}'

            def add_btn(start_ms, key):
                start_s = start_ms / 1000
                if st.button(get_btn_text(start_ms), key):
                    url_time = url + '&t=' + str(start_s) + 's'
                    with placeholder.container():
                        st_player(url_time, playing=True, muted=False)

            # Load and display highlights or chapters
            st.subheader("Highlights")
            with open(file_highlights, 'r') as f:
                data = json.load(f)
            results = data['results']

            cols = st.columns(3)
            n_buttons = 0
            for res_idx, res in enumerate(results):
                text = res['text']
                timestamps = res['timestamps']
                col_idx = res_idx % 3
                with cols[col_idx]:

                    st.write(text.capitalize())
                    for t in timestamps:
                        start_ms = t['start']
                        add_btn(start_ms, n_buttons)
                        n_buttons += 1
                        break


        except Exception as e:
            st.error(f"An error occurred: {e}")
        
        st.subheader("Summary")
        f = open("file.txt","r")
        some = f.read()
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM



        # Load the trained model and tokenizer

        tokenizer = AutoTokenizer.from_pretrained("your_model_directory")

        model = AutoModelForSeq2SeqLM.from_pretrained("your_model_directory")

        def summarize(blog_post):

            # Tokenize the input blog post

            inputs = tokenizer(blog_post, max_length=1024, truncation=True, return_tensors="pt")

            summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            # Decode the summary

            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary

        summary = summarize(some)
        st.write(summary)
