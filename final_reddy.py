import streamlit as st
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
import torch

# Initialize the sentence embedding model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

st.title("Study Assistant")

# User inputs for main subject and subsections
main_subject = st.text_input("Enter the main subject:")
subsections = st.text_input("Enter the subsections you want to study:")

if main_subject and subsections:
    # Create the query based on user input
    query = f"{main_subject} {subsections} english"
    st.write(f"Searching for videos on: {query}")

    # YouTube API setup
    api_key = "AIzaSyByyiNnGHhxY2PYDIB5X8SaGAmX9lEGAMY"  # Use your YouTube API key
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
            part="statistics,snippet",
            id=",".join(video_ids)
        ).execute()

        for item in stats_response['items']:
            video_info = {
                "video_id": item['id'],
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "view_count": int(item['statistics'].get('viewCount', 0)),
                "like_count": int(item['statistics'].get('likeCount', 0)),
                "comment_count": int(item['statistics'].get('commentCount', 0)),
                "duration": int(item['snippet'].get('duration', 0))  # Dummy duration value
            }
            video_data.append(video_info)

        return video_data

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
            return similarity_score
        except Exception:
            return 0

    # Radio buttons for selection mode
    selection_mode = st.radio(
        "Select the type of video scoring method:",
        ('Overview', 'Top Rated', 'Detailed')
    )

    # Function to compute the final score based on selected mode
    def get_combined_score(video, topic, mode):
        engagement_score = video['view_count'] / 1000  # Normalized views
        subtitle_similarity = get_subtitle_similarity(video['video_id'], topic)
        likes_score = video['like_count'] / 1000  # Normalized likes
        duration_score = video['duration'] / 60  # Normalized time in minutes

        # Weights based on mode
        if mode == 'Overview':
            final_score = (0.6 * duration_score) + (0.3 * engagement_score) + (0.1 * likes_score)
        elif mode == 'Top Rated':
            final_score = (0.6 * engagement_score) + (0.4 * likes_score)
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

    # Get the best video based on the user input and selected mode
    best_video, final_score, engagement_score, subtitle_similarity, likes_score, duration_score = get_best_video(query, selection_mode)
    video_url = f"https://www.youtube.com/watch?v={best_video['video_id']}"
    st.write(f"Best video found: {best_video['title']}")
    st.write(f"Video URL: {video_url}")

    # Display reasoning in an expander (dropdown box)
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
