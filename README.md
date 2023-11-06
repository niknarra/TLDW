# TLDW

### Project Introduction: 
Online video platforms contain a massive amount of content, with video lengths ranging from a few minutes to over an hour. However, studies show most viewers prefer videos to be concise, with ideal lengths under 20 minutes and a sweet spot of 3-6 minutes. Despite this preference for brevity, users often struggle to efficiently extract key information from lengthy videos. The long form content challenges people's short attention spans - research indicates our average attention span when consuming digital media has shrunk to just 47 seconds today. Viewers frequently rewind and re-watch segments to try to pick out important details, which increases cognitive load. There is a clear need for solutions that can distill key content from lengthy videos into short, information-dense summaries tailored to users' limited time and attention. Viewers need to grasp key details from videos without spending excessive time watching full videos. Enabling easy access to interact and extract crucial details on demand would greatly enhance the knowledge consumption process when dealing with expansive video content. Tackling these challenges will allow online video platforms to better align with users' preferences for concise and efficient learning. 

### Brief Overview: 
The proposed ‘TL;DW’ application integrates video and audio processing capabilities, natural language processing techniques, and an interactive user interface. The application pre-processes input videos by extracting key frames and generating captions for them using a video-frame captioning module inspired by the BLIP model [6]. These frame-level captions are stored as "Context-1". In parallel, the application samples and transcribes the video's audio into text transcripts using OpenAI's Whisper model [7]. The audio transcripts are stored as "Context-2", linked to timestamp information. When a user selects a video, the application retrieves the corresponding contextual information from the database for that video. This contextual data is then fed into a large language model (LLM) to facilitate interactive summarization and question answering. The user can have a natural conversation with the LLM through the application's interface to obtain video insights.
Through the application's interactive user interface, users can engage with the fine-tuned large language model to ask questions related to the video content. To reduce cognitive load for users, the interface provides options to review previous conversations with the system.
The core AI techniques powering the video summarization and question answering capabilities are video-frame captioning, audio transcription, and key-frame extraction. By leveraging state-of-the-art large language models, the system can effectively analyze long temporal context from the video and generate abstractive summaries and meaningful insights. This allows for an interactive conversation with the video content rather than passive watching.
The proposed TL;DW application enables generating concise summaries by extracting key frames, captioning them, and transcribing audio to build a rich contextual database for each video. This context is processed by the large language model to produce succinct summarizations. The conversational interface allows users to efficiently interact with the video content by asking questions and accessing insights from the video context, without needing to watch the full video.
![Alt text](https://github.com/niknarra/TLDW/blob/main/TLDW%20pipeline.png)
[Project Live Demo](https://tldwapp.streamlit.app/)

## Running the code in your local environment:
#### Dependency Installation
* Make sure you have Python > 3.9
* Install the dependecies using ``` pip install -r requirements.txt ```
* Once the dependecies are insstalled, run ```streamlit run .\complete_TLDW_demo_V1.py```

#### The following is the description of the main python code ```complete_TLDW_demo_V1.py```
1. `streamlit`: This is the main framework used for building the web app. It provides functions to create interactive widgets and to manage the app's state.

2. `langchain` library components:
   - `FAISS`: Utilized for efficient similarity search and retrieval of vectors.
   - `ChatOpenAI`: Interface for the OpenAI chat model, likely used for generating responses.
   - `OpenAIEmbeddings`: To convert text into embeddings using OpenAI's model.
   - `RecursiveCharacterTextSplitter`: To split long texts into smaller chunks suitable for processing.
   - `RetrievalQA`, `ConversationalRetrievalChain`: Components for building a retrieval-based QA system where the chatbot retrieves information to answer questions.

3. `os`: To interact with the operating system, for example, setting an environment variable for the OpenAI API key.

4. `csv`: To read and write CSV files, which in this context are used to store chat histories and video/audio metadata.

5. `pandas`: For handling data in a tabular form, here used to load video data.

6. `streamlit_chat`: To add chat functionality to the Streamlit app.

The code includes several functions:
- `load_audio_video_context()`: This function reads CSV files containing video frame captions and audio transcriptions, then concatenates them into a single text, preparing it as context for the chatbot.
- `load_chathistory()`: Reads a CSV file containing a chat history and returns it as a list.
- `populate_chat_history()`: Appends chat history from a CSV file into the Streamlit session state.
- `load_data()`: Loads video data from a CSV file into a pandas DataFrame.
- `display_main_page()`: Renders the main page of the app, which includes video selection.
- `display_video_page()`: Shows selected video details and provides an interface for chat interaction.

The `@st.cache_data` decorator likely caches the loaded data to improve performance, and `st.set_page_config(layout="wide")` sets the layout of the Streamlit page to wide mode. The environment variable for the `OPENAI_API_KEY` is set, which is necessary for authentication with OpenAI's API.

The app's state management is done through Streamlit's session state (`st.session_state`), holding the generated responses, past inputs, and messages. This state persists across reruns of the app, allowing for a continuous chat experience.

The app provides an interface for users to interact with a video by asking questions, which are then answered by the chatbot using the loaded context. It is designed to handle video playback, display video metadata, and manage the interaction between the user and the system.


Pseudo Code of the main functionality:
```python
INITIALIZE empty list chat_history
SET temp_str to empty string
IMPORT streamlit as st
IMPORT necessary modules from langchain (FAISS, ChatOpenAI, OpenAIEmbeddings, RecursiveCharacterTextSplitter, RetrievalQA, ConversationalRetrievalChain)
IMPORT os, csv, pandas as pd
IMPORT message from streamlit_chat

DEFINE function load_audio_video_context(input_video_csv, input_audio_csv)
    INITIALIZE detected_text with instructions for the bot
    READ video CSV file and APPEND frame-wise captions to detected_text
    READ audio CSV file and APPEND speech-to-text transcriptions to detected_text
    RETURN detected_text

DEFINE function load_chathistory(chathistory_csv)
    READ chathistory_csv and RETURN chat history list

DEFINE function populate_chat_history(inp_csv_file)
    READ inp_csv_file and APPEND chat history to session state

SET Streamlit page configuration
SET environment variable for OpenAI API key

CREATE text_splitter instance with specified chunk size and overlap

INITIALIZE Streamlit session state variables for 'generated', 'past', and 'messages' if not present

DEFINE function load_data()
    READ CSV and RETURN as pandas DataFrame

DEFINE function display_main_page()
    DISPLAY title and subheader in Streamlit
    ALLOW selection of video category
    FILTER videos based on selected category
    DISPLAY video thumbnails and names, and handle video selection

DEFINE function display_video_page()
    HANDLE navigation back to main page
    LOAD and DISPLAY selected video details
    SET up chat functionality with input and response containers
    IF user submits input and page is not main:
        LOAD chat history from CSV
        GENERATE response using conversational retrieval chain
        APPEND messages to session state
        WRITE new chat history to CSV

IF selected page in session state is 'main'
    CALL display_main_page()
ELSE
    CALL display_video_page()
```
