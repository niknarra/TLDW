import streamlit as st

st.set_page_config(page_title="TLDW", page_icon=":zap:", layout="wide")

import tldwchat2
import db2 as db
import streamlit_authenticator as stauth
import random

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

image_path = 'TLDW logo.png'

#st.set_page_config(page_title="TLDW", page_icon=":zap:", layout="wide")

greetings = ["Hello", "Bonjour", "Hola", "Hallo", "Ciao", "こんにちは", "안녕하세요", "Привет", "Olá", "नमस्ते", "你好", "مرحبا", "నమస్కారం"]

descriptions = ["Long videos? Ain't nobody got time for that! Welcome to your new sanctuary, TL;DW, where we cut to the chase faster than a ninja on a sugar rush.", "Say goodbye to the endless video scroll! At TL;DW, we believe life's too short for long videos. Dive in for the short, sweet, and super!"]

questions = ["Who is the speaker or presenter in the video?", "Are there key dates or events mentioned in the video?", "What is the point of this video?",  "Are there any notable quotes or statements in the video?", "What are the underlying themes or messages in the video?"]

selected_greeting = random.choice(greetings)
selected_description = random.choice(descriptions)
selected_question = random.choice(questions)

# Function to check login (Placeholder for actual authentication logic)
def check_login(username, password):
    return True  # Replace with actual authentication logic

# Initialize session state
if 'username' not in st.session_state:
    st.session_state['username'] = None
    st.session_state['full_name'] = None
    st.session_state['user_id'] = None
    st.session_state['profile'] = None

def logout():
    st.session_state['username'] = None
    st.session_state['full_name'] = None
    st.session_state['user_id'] = None
    st.session_state['profile'] = None

if st.session_state['username']:
    st.sidebar.image(image_path, width=125)
    st.sidebar.write(f"Hello, {st.session_state['full_name']}!")
    #st.sidebar.write(f"Hello, {st.session_state['user_id']}!")
    #st.sidebar.write(f"Hello, You are a {st.session_state['profile']}!")
    tldwchat2.controller()
    
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()
    
else:
# Sidebar for login
    colT1,colT2 = st.columns([6,8])
    with colT2:
        st.title(selected_greeting)
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.title(selected_description)
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.title("You can ask TL;DW anything,")
    colT3,colT4 = st.columns([0.3,8])
    with colT4:
        st.subheader(selected_question)
        
    with st.sidebar:
        st.image(image_path, width=125)
        st.write("Login")
        username = st.text_input("Username", key='login_username', placeholder="Enter your username")
        password = st.text_input("Password", type="password", key='login_password', placeholder="Password here")
        if st.button("Login"):
            if username and password:
                if db.verify_user(username, password):
                    full_name = db.get_user_fullname(username)
                    user_id = db.get_user_id(username)
                    profile = db.get_user_profile(username)
                    st.session_state['username'] = username
                    st.session_state['full_name'] = full_name
                    st.session_state['user_id'] = user_id
                    st.session_state['profile'] = profile
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")
            st.rerun()

            
        st.write("New here? Sign up!")
        new_name = st.text_input("Full Name", key='signup_name')
        new_username = st.text_input("Username", key='signup_username')
        new_password = st.text_input("Password", type="password", key='signup_password')
        new_email = st.text_input("Email", key='signup_email')
        new_profile = st.selectbox(
            "What describes you best?",
            ("Student", "Teacher", "Working Professional", "Researcher", "Educator", "Content Creator", "Other"),
            key='signup_profile'
        )
        if st.button("Register", key='signup_button'):
            if new_username and new_password and new_name and new_email:
                if not db.get_user(new_username):
                    db.insert_user(new_username, new_name, new_password, new_email, new_profile)
                    st.success("You have successfully registered.")
                else:
                    st.error("Username already exists.")
            else:
                st.error("Please fill in all the fields.")

# Main page content
#st.write("Welcome to TL;DW")  # Default welcome message

# Check if user is logged in

