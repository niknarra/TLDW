chat_history = []
temp_str = ""
import streamlit as st
#from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os
#import PyPDF2
import csv
import streamlit as st
import pandas as pd
#from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os
from streamlit_chat import message
#import PyPDF2
import csv
# Load CSV data
st.set_page_config(layout="wide")
os.environ["OPENAI_API_KEY"] = "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"

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
    

def load_audio_video_context(input_video_csv, input_audio_csv):
    detected_text = "Assume you are an answer writing expert bot. Your task is to go through the below provided time-stamped video and audio context of a video. PLease try to correlate between the above provided audio and video context while answering the questions. Please dont say based on the context while asnwering the questions, try asnwering the questions as much as possible " + "\n \n"
    detected_text = detected_text + " the following are the input video's frame-wise captions annotated with respect to video timestamps in seconds : \n"

    linecount = 0
    with open(input_video_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #print(row)
            if linecount != 0:
                if len(row)>0:
                    detected_text = detected_text + row[1] + '\n'
            linecount = linecount + 1


    detected_text = detected_text + "\n Now, the following are the input video's audio (speech-to-text) trasncriptions generated with respect to video timestamps in seconds : \n \n"

    linecount_1 = 0
    with open(input_audio_csv, newline='') as csvfile_1:
        spamreader_1 = csv.reader(csvfile_1)
        for row_1 in spamreader_1:
            if linecount_1 != 0:
            #print(row_1)
                if len(row_1)>0:
                    detected_text = detected_text + row_1[1] + ' to ' + row_1[2] + ' seconds audio trasncription is : ' + row_1[3] + '\n'
            linecount_1 = linecount_1 +1

    detected_text = detected_text + "\n \n " + "Assume you are an answer writing expert bot. Your task is to go through the above time-stamped video and audio context of a video. Extract relevant information from it, and answer the questions that will follow. PLease try to correlate between the above provided audio and video context while answering the questions. If the question is not relevant to the context provided, try to generalize your answer relevant to the above provided video and audio context, please dont say based on the context while asnwering the questions, try asnwering the questions as much as possible " + "\n"
    
    return detected_text

def load_chathistory(chathistory_csv):
    return_list = []
    temp_linecount = 0
    with open(chathistory_csv) as csv_history:
        reader_temp = csv.reader(csv_history)
        for temp_row in reader_temp:
            if temp_linecount != 0:
                if len(temp_row)>0:
                    return_list.append((temp_row[0], temp_row[1]))
            temp_linecount = temp_linecount+1
    csv_history.close()
    return return_list


def populate_chat_history(inp_csv_file):
    with open(inp_csv_file) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            if (len(row)>1) and row[0]!='' and row[1]!='':
                #print(row)
                st.session_state['past'].append(str(row[0]))
                st.session_state['generated'].append(str(row[1]))
            else:
                pass
                


@st.cache_data
def load_data():
    return pd.read_csv('videos.csv',encoding='cp1252')

df = load_data()

# Function to display the main page
def display_main_page():
    st.title("TL;DW")
    st.subheader("Video Repository")
    category = st.selectbox("Select a category", ["All"] + list(df['category'].unique()))
    filtered_videos = df if category == "All" else df[df['category'] == category]
    
    # Using thumbnails for video selection
    cols = st.columns(3)  # Adjust based on desired grid size
    for index, row in filtered_videos.iterrows():
        col = cols[index % 3]
        if col.button('select', key=row['id']):
            st.session_state.selected_video = row
            st.session_state.page = 'video'
            video = st.session_state.selected_video
            populate_chat_history(video['chat_history'])
            st.experimental_rerun()
        print(row['thumbnail'])
        col.image(str(row['thumbnail']), use_column_width=True, caption=row['video_name'])

# Function to display the video details and playback page
def display_video_page():
    if st.button("Back to Main Page"):
        st.session_state.page = 'main'
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = []
        st.experimental_rerun()
    video = st.session_state.selected_video
    if (st.session_state.page != 'main'):
        detected_text = load_audio_video_context(video['video_context'], video['audio_context'])
        texts = text_splitter.create_documents([detected_text])
    
        directory = "index_store_new_"+str(video['id'])
        vector_index = FAISS.from_documents(texts, OpenAIEmbeddings())
        vector_index.save_local(directory)
    
        vector_index = FAISS.load_local("index_store_new_"+str(video['id']), OpenAIEmbeddings())
        retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        conv_interface = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0), retriever=retriever)
    col1, col2 = st.columns([3, 5])
    with col1:
        st.title(video['video_name'])
        st.video(video['video_file'])
        #st.video('https://www.youtube.com/watch?v=_ZvnD73m40o')
        st.write('**Duration:**', video['duration'])
        st.write('**Description:**', video['description'])
    with col2:
        
        st.subheader("Interact with the video here")
        # You can add chat functionality here.
        # As an example, let's create a simple chat box.
        response_container = st.container()
        # container for text box
        container = st.container()
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_area("Input your prompt here:", key='input', height=100)
                submit_button = st.form_submit_button(label='Send')
                st.session_state['messages'].append({"role": "user", "content": user_input})
        
            if submit_button and user_input and (st.session_state.page != 'main'):
                chat_history = load_chathistory(video['chat_history'])
                print(chat_history)
                #output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
                result = conv_interface({"question": user_input, "chat_history": chat_history})
                print(result["answer"])
                st.session_state['messages'].append({"role": "assistant", "content": result["answer"]})
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(result["answer"])
                with open(video['chat_history'], 'a') as f:
                    writer = csv.writer(f)
                    writer.writerows([(user_input, result["answer"])])
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))

# Main App Logic
if not hasattr(st.session_state, 'page'):
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    display_main_page()
elif st.session_state.page == 'video':
    display_video_page()