<p align="center">
  <strong><font size="+10">📚 Vidya Veda</font></strong>
</p>

# 📚 AI-Powered Educational Platform

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



### **File Descriptions**

#### `video_processor.py`
Contains the `VideoProcessor` class for recommending videos and generating summaries based on video transcripts. It fetches transcripts from external APIs or local databases for further processing.

#### `quiz_generator.py`
Defines the `QuizGenerator` class, which creates quizzes from provided topics or video summaries and evaluates student answers. It provides personalized feedback based on performance.

#### `ai_chatbot.py`
Implements the `ChatBot` class that powers the interactive AI chatbot. The chatbot leverages large language models to respond to student queries and handle follow-up questions.

#### `content_manager.py`
Manages the uploading of study materials, including PDFs, and extracts text for summarization and quiz generation.

#### `nlp_module.py`
Includes functions for text summarization and tokenization, essential for preprocessing study materials before quiz generation or chatbot responses.

#### `rag_model.py`
Implements the RAG (Retrieve and Generate) system, which retrieves relevant documents from external sources to generate more contextually accurate AI responses.

#### `report_generator.py`
Generates detailed performance reports for students, summarizing quiz scores and providing feedback. It also tracks performance trends over time.

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


