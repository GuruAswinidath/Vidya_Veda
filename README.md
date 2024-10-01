

# 📚 VidyaVeda – Empowering Learning with Personalized AI

🚀 **Overview**  
This project proposes an innovative mobile application that leverages Generative AI (GenAI) to personalize the learning experience for students. The app tackles the challenge of information overload by allowing users to specify a topic and then curating relevant video lectures with timestamps for specific subtopics. GenAI further personalizes learning by generating clear and concise notes from video lectures and uploaded PDFs. Interactive quizzes tailored to the chosen concept solidify understanding, while performance analysis reports provide valuable insights into strengths and weaknesses. This app empowers students to become active participants in their education by fostering personalized learning, enhanced efficiency, deeper understanding, and self-directed learning.

---

## 🎯 **Key Features**

### 🎥 Video Recommendation & Summarization
- Recommends relevant videos based on a specific topic.
- Summarizes video transcripts for easier content review.

### 📝 Quiz Generation & Evaluation
- Automatically generates quizzes based on video content or study materials.
- Provides performance evaluation and feedback for student improvement.

### 🤖 AI Chatbot
- Real-time conversational AI to answer student queries.
- Supports follow-up questions for detailed clarification.

### 📂 Content Management
- Upload study materials like PDFs and extract their text for use in quizzes or notes.
  
### 📊 Report Generation
- Creates detailed performance reports, tracking student progress over time.
  
### 🔍 RAG Model Integration
- Retrieves relevant external content to augment AI responses, ensuring better contextual understanding.

---

## 🛠 **Tech Stack**

- **Backend Framework**: Flask/Django  
- **Frontend**: Streamlit  
- **NLP Libraries**: Transformers, OpenAI API, Spacy, NLTK  
- **Data Processing**: Pandas, PyPDF2  
- **Vector Search**: FAISS for efficient vector-based searches  
- **Machine Learning**: Scikit-learn, OpenAI  
- **Quiz & Report Management**: Custom logic for quiz generation and report creation  

---

## 🗂 **Project Structure**

```bash
├── video_processor.py       # Handles video recommendation and transcript summarization
├── quiz_generator.py        # Generates and evaluates quizzes
├── ai_chatbot.py            # Implements the AI chatbot for answering queries
├── content_manager.py       # Manages uploaded content like PDFs and extracts text
├── nlp_module.py            # Provides text summarization and tokenization functions
├── rag_model.py             # Implements RAG (Retrieve and Generate) for document retrieval and response generation
├── report_generator.py      # Generates student performance reports

```
---

### **File Descriptions and Program skeleton**

Please Refer `vidya_veda.py` file

#### `video_processor.py`
Contains the `VideoProcessor` class for recommending videos and generating summaries based on video transcripts. It fetches transcripts from external APIs or local databases for further processing.
```bash
class VideoProcessor:
    # video_data  # stores the recommended videos for a topic
    # transcripts  # stores the video transcripts

    def recommend_videos(topic):
        #Function to fetch and recommend videos based on the input topic.
        #It connects to external APIs or local video databases and filters the most relevant content.
        pass

    def summarize_video(video_id):
        #Function to generate a summary of a video by fetching its transcript and using NLP models to summarize it.
        pass

    def fetch_transcript(video_id):
        #Function to extract the transcript of a video using the OpenAI API or another service.
        #This transcript will be used for summarization and quiz generation.
        pass
```


#### `quiz_generator.py`
Defines the `QuizGenerator` class, which creates quizzes from provided topics or video summaries and evaluates student answers. It provides personalized feedback based on performance.
```bash
class QuizGenerator:
    # quiz_questions  # stores the generated questions for the quiz
    # quiz_answers  # stores the correct answers for evaluation

    def create_quiz(topic):
        #Function to generate quiz questions based on the summarized content of the videos or input topic.
        #Uses templates or predefined formats for multiple choice questions (MCQs).
        pass

    def evaluate_quiz(student_answers, correct_answers):
        #Function to evaluate the student's answers by comparing them to the correct answers.
        #Returns the score and feedback based on the student's performance.
        pass
```

#### `ai_chatbot.py`
Implements the `ChatBot` class that powers the interactive AI chatbot. The chatbot leverages large language models to respond to student queries and handle follow-up questions.
```bash
class ChatBot:
    # chatbot_model  # stores the pre-trained large language model for answering queries

    def __init__():
        # Initialize the chatbot model with an LLM
        pass

    def ask_question(topic):
        #Function that allows students to ask topic-related questions.
        #Uses a language model to generate answers based on the provided context.
        pass

    def handle_follow_up(question):
        #Function that handles follow-up questions from students based on previous answers.
        pass
```


#### `content_manager.py`
Manages the uploading of study materials, including PDFs, and extracts text for summarization and quiz generation.
```bash
class ContentManager:
    # uploaded_content  # stores the uploaded PDFs, notes, or books
    # extracted_text  # stores text extracted from uploaded files

    def upload_material(file_path):
        #Function to handle the upload of study materials like PDFs.
        #Extracts text from the files using PyPDF2 or other relevant libraries.
        pass

    def generate_notes(extracted_text):
        #Function to summarize and convert the extracted text into study notes.
        #The summarized notes are organized and made available to students.
        pass
```

#### `nlp_module.py`
Includes functions for text summarization and tokenization, essential for preprocessing study materials before quiz generation or chatbot responses.

```bash
class NLPModule:
    # processed_text  # stores text after pre-processing and tokenization
    # summarized_text  # stores the summarized version of the input text

    def summarize_text(text):
        #Function to generate a summary of the given text using natural language processing techniques.
        #Uses transformers and other NLP models for summarization.
        pass

    def tokenize_text(text):
        #Function to tokenize input text for further processing or analysis.
        #Can be used for question generation or answer extraction.
        pass
```

#### `rag_model.py`
Implements the RAG (Retrieve and Generate) system, which retrieves relevant documents from external sources to generate more contextually accurate AI responses.
```bash
class RAGModel:
    # retrieved_content  # stores the relevant information retrieved from external sources
    # generated_content  # stores the content generated using the retrieved data

    def retrieve_content(query):
        """
        Function to retrieve relevant content from external sources or internal databases based on a query.
        This information will be used to augment the AI's responses.
        """
        pass

    def generate_response(query, context):
        """
        Function to generate a response using both the retrieved content and a generative language model.
        """
        pass

    def embed_query(query):
        """
        Function to convert the query into a vector representation (embedding).
        This is typically done using a pre-trained language model.
        """
        pass

    def search_vectordb(embedding):
        """
        Function to search a vector database using the query embedding.
        This function retrieves the most relevant documents or information based on the similarity of embeddings.
        """
        pass

    def embed_documents(documents):
        """
        Function to convert a list of documents into their vector representations (embeddings).
        This is typically done using a pre-trained language model.
        """
        pass

    def store_in_vectordb(embeddings, documents):
        """
        Function to store document embeddings and their corresponding documents in a vector database.
        This allows for efficient retrieval of relevant documents based on query embeddings.
        """
        pass
```

#### `report_generator.py`
Generates detailed performance reports for students, summarizing quiz scores and providing feedback. It also tracks performance trends over time.
```bash
class ReportGenerator:
    # student_reports  # stores individual student reports with their performance metrics

    def generate_performance_report(student_id, quiz_scores):
        #Function to create a report of the student's quiz performance, including scores and feedback.
        #The report is generated in CSV format and can be downloaded by the student.
        pass

    def aggregate_results(student_id):
        #Function to aggregate quiz results and show overall performance over time.
        #Displays trends in student performance to track improvement.
        pass
```

---

## 📦 **Dependencies**

Ensure the following packages are installed:

```txt
langchain==0.0.144
PyPDF2==3.0.1
streamlit==1.21.0
openai==0.27.0
faiss-cpu==1.7.3
tiktoken==0.3.1
tokenizers==0.13.3
scikit-learn==1.2.2


