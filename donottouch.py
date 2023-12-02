#test version with complete UAuth(login, reg, pass_reset) and TLDW Redirection with user chats db
#Everything is working fine as of Dec 1 12AM
#Issue - Request Sent upon logging in.

import streamlit as st
import streamlit_authenticator as stauth
import database as db

st.set_page_config(page_title="TLDW", page_icon=":zap:", layout="wide")

import tldwchat

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state for registration form visibility
if 'show_login' not in st.session_state:
    st.session_state['show_login'] = True
if 'authenticated_user_name' not in st.session_state:
    st.session_state['authenticated_user_name'] = None
    
# Function to register a new user
def show_registration_form():
    st.title("We are about to change your world, we hope!")
    with st.form("Register", clear_on_submit=True):
        name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        password_confirmation = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email")
        profile = st.selectbox(
            "What describes you best?",
            ("Student", "Teacher", "Working Professional", "Researcher", "Educator", "Content Creator", "Other")
        )

        submitted = st.form_submit_button("Register")
        if submitted:
            if password != password_confirmation:
                st.error("Passwords do not match.")
                return

            # Hash the password
            hashed_password = stauth.Hasher([password]).generate()[0]

            # Save the new user to the database
            if not db.get_user(username):
                db.insert_user(username, name, hashed_password,email,profile)
                st.success("You have successfully registered.")
                st.session_state['show_register'] = False
            else:
                st.error("Username already exists.")
                return
    if st.button("Back to Login"):
        st.session_state['show_login'] = True

# Function for the login form
def show_login_form():
    st.title("Welcome back! Pick up right where you left off!")
    name, authentication_status, username = authenticator.login("Login", "main")
    
    if authentication_status == False:
        st.error("Incorrect username or password. Please try again.")

    if authentication_status:
        user_id = db.get_user_id(username)
        st.session_state['authentication_status'] = True
        st.session_state['current_page']= 'home'
        st.session_state['authenticated_user_name'] = name
        st.session_state['authenticated_user_id'] = user_id
        show_main_page()
    else:
        st.write("Don't have an account?")
        if st.button("Sign up"):
            st.session_state['show_login'] = False
            
    if authentication_status:
        st.session_state['authentication_status'] = True
        st.session_state['authenticated_user_name'] = name
        
#Reset
def show_forgot_password_form():
    st.title("We're human afterall...")
    email = st.text_input("Enter your registered email address")

    if st.button("Reset Password"):
        user = db.get_user_by_email(email)
        if user:
            st.session_state['reset_user'] = user
            st.session_state['show_forgot_password_form'] = False
            st.session_state['show_reset_password_form'] = True
        else:
            st.error("No user found with the given email address.")

    if st.button("Back to Login"):
        st.session_state['show_login'] = True
        st.session_state['show_forgot_password_form'] = False

def show_reset_password_form():
    st.title("Reset your password")
    new_password = st.text_input("Enter your new password", type="password")
    confirm_new_password = st.text_input("Confirm your new password", type="password")

    if st.button("Update Password"):
        if new_password == confirm_new_password:
            # Hash the new password and update in the database
            hashed_new_password = stauth.Hasher([new_password]).generate()[0]
            db.update_user_password(st.session_state['reset_user']['key'], hashed_new_password)
            st.success("Your password has been reset successfully.")
            st.session_state['show_reset_password_form'] = False
            st.session_state['show_login'] = True

            if st.button("Return to Login"):
                st.session_state['show_login'] = True
                st.session_state['show_reset_password_form'] = False
                
        else:
            st.error("Passwords do not match.")

# Homepage function
def show_main_page():
    #print("display_main_page called")  # Debug
    user_name = st.session_state.get('authenticated_user_name', 'Unknown User')
    user_id = st.session_state.get('authenticated_user_id')
    st.sidebar.title(f"Welcome {user_name}!")
    #st.sidebar.title(f"ID {user_id}")
    tldwchat.controller()
    
    authenticator. logout ("Logout", "sidebar")
        
# Initialize session state for authentication status
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Fetch user data from database
users = db.fetch_all_users()
usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

# Setup the authenticator
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "tldwapp", "abcdef", cookie_expiry_days=1)

if __name__ == "__main__":
    if st.session_state.get('show_reset_password_form'):
        show_reset_password_form()
    elif st.session_state.get('show_forgot_password_form'):
        show_forgot_password_form()
    elif st.session_state.get('authentication_status'):
        show_main_page()
    elif st.session_state.get('show_login', True):
        show_login_form()
        if st.button("Forgot Password?"):
            st.session_state['show_login'] = False
            st.session_state['show_forgot_password_form'] = True
    else:
        show_registration_form()
