# TLDW

### Project Introduction: 
Online video platforms contain a massive amount of content, with video lengths ranging from a few minutes to over an hour. However, studies show most viewers prefer videos to be concise, with ideal lengths under 20 minutes and a sweet spot of 3-6 minutes. Despite this preference for brevity, users often struggle to efficiently extract key information from lengthy videos. The long form content challenges people's short attention spans - research indicates our average attention span when consuming digital media has shrunk to just 47 seconds today. Viewers frequently rewind and re-watch segments to try to pick out important details, which increases cognitive load. There is a clear need for solutions that can distill key content from lengthy videos into short, information-dense summaries tailored to users' limited time and attention. Viewers need to grasp key details from videos without spending excessive time watching full videos. Enabling easy access to interact and extract crucial details on demand would greatly enhance the knowledge consumption process when dealing with expansive video content. Tackling these challenges will allow online video platforms to better align with users' preferences for concise and efficient learning. 

### Brief Overview: 
The proposed ‘TL;DW’ application integrates video and audio processing capabilities, natural language processing techniques, and an interactive user interface. The application pre-processes input videos by extracting key frames and generating captions for them using a video-frame captioning module inspired by the BLIP model [6]. These frame-level captions are stored as "Context-1". In parallel, the application samples and transcribes the video's audio into text transcripts using OpenAI's Whisper model [7]. The audio transcripts are stored as "Context-2", linked to timestamp information. When a user selects a video, the application retrieves the corresponding contextual information from the database for that video. This contextual data is then fed into a large language model (LLM) to facilitate interactive summarization and question answering. The user can have a natural conversation with the LLM through the application's interface to obtain video insights.
Through the application's interactive user interface, users can engage with the fine-tuned large language model to ask questions related to the video content. To reduce cognitive load for users, the interface provides options to review previous conversations with the system.
The core AI techniques powering the video summarization and question answering capabilities are video-frame captioning, audio transcription, and key-frame extraction. By leveraging state-of-the-art large language models, the system can effectively analyze long temporal context from the video and generate abstractive summaries and meaningful insights. This allows for an interactive conversation with the video content rather than passive watching.
The proposed TL;DW application enables generating concise summaries by extracting key frames, captioning them, and transcribing audio to build a rich contextual database for each video. This context is processed by the large language model to produce succinct summarizations. The conversational interface allows users to efficiently interact with the video content by asking questions and accessing insights from the video context, without needing to watch the full video.
![TL;DW Low Level Design] (https://github.com/niknarra/TLDW/blob/main/TLDW%20pipeline.png)
[Project Live Demo](https://tldwapp.streamlit.app/)

## Running the code in your local environment:
## Dependency Installation
* Make sure you have Python > 3.9
* Install the dependecies using ``` pip install -r requirements.txt ```
* Once the dependecies are insstalled, run ```streamlit run .\complete_TLDW_demo_V1.py```

```python

```
