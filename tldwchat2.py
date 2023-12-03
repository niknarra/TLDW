chat_history = []
temp_str = ""
import streamlit as st
from streamlit_player import st_player
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
import re
import ast
import chatbase as chat_db
import database as db


from streamlit_chat import message
#import PyPDF2
import csv
# Load CSV data
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#if 'generated' not in st.session_state:
#    st.session_state['generated'] = []
#if 'past' not in st.session_state:
#    st.session_state['past'] = []
#if 'messages' not in st.session_state:
#    st.session_state['messages'] = []
#if 'timestamps' not in st.session_state:
#    st.session_state['timestamps'] = []    
    

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

    detected_text = detected_text + "\n \n "
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


#def populate_chat_history(inp_csv_file):
#    with open(inp_csv_file) as file_obj:
#        reader_obj = csv.reader(file_obj)
#        for row in reader_obj:
#            if (len(row)>1) and row[0]!='' and row[1]!='':
#                #print(row)
#                st.session_state['past'].append(str(row[0]))
#                st.session_state['generated'].append(str(row[1]))
#            else:
#                pass
                


@st.cache_data
def load_data():
    return pd.read_csv('videos.csv',encoding='cp1252')

df = load_data()

# Function to display the main page
def display_main_page():
    st.title("TL;DW: Capturing the Core of Content")
    user_id = st.session_state['user_id']
    #st.subheader("Video Repository")
    category = st.sidebar.selectbox("Select a Category", ["All"] + list(df['category'].unique()))
    filtered_videos = df if category == "All" else df[df['category'] == category]
    
    # Using thumbnails for video selection
    cols = st.columns(2)  # Adjust based on desired grid size
    #col.image(str(row['thumbnail']), use_column_width=True, caption=row['video_name'])
    for index, row in filtered_videos.iterrows():
        col = cols[index % 2]
        col.image(str(row['thumbnail']), use_column_width=True, caption=row['video_name'])
        if col.button('Select', key=row['id']):
            st.session_state.selected_video = row
            st.session_state.page = 'video'
            video = st.session_state.selected_video
            result=chat_db.fetch_chat_history(video['id'],user_id)
            #print(result)
            for chat_rows in result:
                st.session_state['past'].append(str(chat_rows["user_message"]))
                st.session_state['generated'].append(str(chat_rows["bot_message"]))
            st.experimental_rerun()
            
        #print(row['thumbnail'])
        




def stick_it_good():

    # make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="column"] div:has(div.fixed-header) {
                    overflow-y: scroll;
                    height: 650px;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds_remaining = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds_remaining:02}"

def display_video_page():
    if st.sidebar.button("Back to Main Page"):
        st.session_state.page = 'main'
        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = []
        st.session_state['timestamps'] = []
        st.experimental_rerun()
    video = st.session_state.selected_video
    user_id = st.session_state['user_id']
    if (st.session_state.page != 'main'):
        detected_text = load_audio_video_context(video['video_context'], video['audio_context'])
        texts = text_splitter.create_documents([detected_text])
    
        directory = "index_store_new_"+str(video['id'])
        vector_index = FAISS.from_documents(texts, OpenAIEmbeddings())
        vector_index.save_local(directory)
    
        vector_index = FAISS.load_local("index_store_new_"+str(video['id']), OpenAIEmbeddings())
        retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        conv_interface = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0), retriever=retriever)
    col1, col2 = st.columns([2, 3])
    with col1:
        st.header(video['video_name'])
        #st.video(video['video_file'])
        #st.write('**Title:**', video['description'])
        container_video = st.container()
        stick_it_good()
        with container_video:
            if 'button' not in st.session_state:
                st.session_state.button = 0
            video_url = str(video['video_file'])
            #st.st_player(video_url)
            st_player(video_url, playing=True,config={"playerVars": {"start": int(st.session_state.button)}})
            #st.write('**Duration:**', video['duration'])
            st.write('**Video Summary:**', video['video_summary'])
            # Dropdown to select a keyword
            #print(video['key_words'])
            keyword_dict = ast.literal_eval(str(video['key_words']))
            selected_keyword = st.sidebar.selectbox("Select your prompt based on the keyword:", options=list(keyword_dict.keys()))
        
            # Display the sentences associated with the selected keyword
            if selected_keyword:
                for sentence in keyword_dict[selected_keyword]:
                    st.sidebar.code(sentence, language="python")
    with col2:
        def clear_chat_history(csv_file_name):
            print("clear chat")
            #st.session_state.page = 'main'
            st.session_state['generated'] = []
            st.session_state['past'] = []
            st.session_state['messages'] = []
            st.session_state['timestamps'] = []
            f = open(csv_file_name, "w+")
            f.close()
            #st.experimental_rerun()
        def click_button(timestep):
            st.session_state.button = int(timestep)
            #video_url = "https://youtu.be/_ZvnD73m40o"
            #st.st_player(video_url)
            #st_player(video_url, config={"playerVars": {"start": 100}})
            
        def create_grid(numbers, cols=8):
            # Calculate the required number of rows
            rows = -(-len(numbers) // cols)  # Ceiling division

            # Initialize the grid
            for i in range(rows):
                cols_list = st.columns(cols)
                for j in range(cols):
                    # Calculate the index in the numbers list
                    index = i * cols + j
                    if index < len(numbers):
                        # Create a button with the number
                        cols_list[j].button(str(convert_seconds_to_hms(int(numbers[index]))), on_click=click_button, args=(int(numbers[index]),))
                    else:
                        # Create an empty space
                        cols_list[j].empty()
        # condition_text_1 = """Assume you are an answer writing expert bot. 
        # Your task is to go through the above time-stamped video and audio context of the video. Extract relevant information from it, 
        # and answer the questions that will follow. PLease try to correlate between the above provided audio and video context 
        # while answering the questions. If the question is not relevant to the context provided, 
        # try to generalize your answer relevant to the above provided video and audio context or try to asnwer th question from your general knowledge, 
        # please dont say: "based on the context", "as per the provided context", "unfortunately, i connot asnwer the question", "i can not answer the question based on the provided audio/video trasncripts" while asnwering the questions, 
        # try asnwering the questions as much as possible \n\n  now, please asnwer this question if prossible provide video timestamps from where this content/asnwer is refered from 
        # (the timestamps in the context is in seconds format but to convert that format and provide the video timestamps in hours:minutes:seconds format) always cite your asnwer to a video timestamp whenever possible even when it is not asked in the question, please asnwer the question intutively and never say "based on the context", "as per the provided context", "unfortunately, i connot asnwer the question", "i can not answer the question based on the provided audio/video trasncripts" or other similar terms while asnwering the questions aslways try to provide some kind of answer \n QUESTION : """
        # but remember whenever you are mentioning a video timestamp in your asnwer always place them in between ** (i.e. if the video timestamp is 150 seconds place the 150 inyour answer as *150*).
        condition_text_1 = """Assume you are an answer writing expert bot. 
        Your task is to go through the above time-stamped video and audio context of the video. Extract relevant information from it, 
        and answer the questions that will follow. PLease try to correlate between the above provided audio and video context 
        while answering the questions. If the question is not relevant to the context provided, 
        try to generalize your answer relevant to the above provided video and audio context or try to asnwer th question from your general knowledge, 
        please dont say: "based on the context", "as per the provided context", "unfortunately, i connot asnwer the question", "i can not answer the question based on the provided audio/video trasncripts" while asnwering the questions, 
        try asnwering the questions as much as possible \n\n  now, please asnwer this question if prossible provide video timestamps from where this content/asnwer is refered from 
        (the timestamps in the context is in seconds and you provide the asnwer in seconds format only) if relevant cite your asnwer to a video timestamp whenever possible even when it is not explicitly asked in the question,  
        please asnwer the question intutively and never say "based on the context", "as per the provided context", "unfortunately, i connot asnwer the question", "i can not answer the question based on the provided audio/video trasncripts" or other similar terms while asnwering the questions aslways try to provide some kind of answer. please remember the timestamps you refer in the answer should only be in seconds format (i.e. 153.0 seconds etc.) \n QUESTION : """
        
        condition_text_2 = "please read the following text genrated by you, and extract the video timestamps mentioned in it, the extracted timestamps should only be in integer/float format (for example: 150.2, 67, 45 etc.), once you extract the video timestamps, give the resulting list of timestamps in a list format seperated by commas. only provide the list of timestamps (the timestamps in the list should be seperated by comma','), if no timestamps are found in the provided text, please return 'None'. TEXT:  "
        user_id = st.session_state['user_id']
        st.write("**Interact with the video here**")
        st.sidebar.button("clear chat history", on_click=clear_chat_history, args=(video['chat_history'],))
        # You can add chat functionality here.
        # As an example, let's create a simple chat box.
        response_container = st.container()
        # if len(temp_timestamps_int)>0:
        #     print("hi")
        # else:
        #     pass
        
        # container for text box
        container = st.container()
        stick_it_good()
        with container:
            #move_focus()
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_area("Input your prompt here:", key='input', height=100)
                submit_button = st.form_submit_button(label='Send')
                st.session_state['messages'].append({"role": "user", "content": user_input})
            
            
            if submit_button and user_input and (st.session_state.page != 'main'):
                chat_history = load_chathistory(video['chat_history'])
                #print(chat_history)
                #output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
                result = conv_interface({"question": condition_text_1 + user_input, "chat_history": chat_history})
                result_timestamps = conv_interface({"question": condition_text_2 + result["answer"], "chat_history": []})
                try:
                    #print(result_timestamps["answer"])
                    temp_timestamps = result_timestamps["answer"].split(",")
                    temp_timestamps_int = [int(float(num)) for num in temp_timestamps]
                    temp_timestamps_int = set(temp_timestamps_int)
                    temp_timestamps_int = list(temp_timestamps_int)
                    st.session_state['timestamps'].append(temp_timestamps_int)
                    print(st.session_state['timestamps'])
                except:
                    st.session_state['timestamps'].append([])
                
                st.session_state['messages'].append({"role": "assistant", "content": result["answer"]})
                st.session_state['past'].append(user_input)
                chat_db.insert_chat_message(video['id'], user_id, user_input, result["answer"])
                st.session_state['generated'].append(result["answer"])
                #with open(video['chat_history'], 'a') as f:
                #    writer = csv.writer(f)
                #    writer.writerows([(user_input, result["answer"])])
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))
                
                st.write("Navigate To: ")
                if len(st.session_state['timestamps'])>0:
                    if len(st.session_state['timestamps'][len(st.session_state['timestamps'])-1])>0:
                        create_grid(list(st.session_state['timestamps'][len(st.session_state['timestamps'])-1]))
                    else:
                        pass
                else:
                    pass
                
        

# Main App Logic
def controller():
    if not hasattr(st.session_state, 'page'):
        st.session_state.page = 'main'

    if st.session_state.page == 'main':
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []
        if 'timestamps' not in st.session_state:
            st.session_state['timestamps'] = [] 
        display_main_page()
    elif st.session_state.page == 'video':
        display_video_page()
