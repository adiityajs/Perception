import sqlite3
from pathlib import Path
import models
import PIL

import streamlit as st

import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Perception -A utility for object detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="
        display: inline-block;
        background: linear-gradient(to right, #ff8a00, #e52e71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 8px rgba(229, 46, 113, 0.5);
        ">
        Perception -A utility for object analysis
    </h1>
</div>
""", unsafe_allow_html=True)



st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 10px;
            text-align: center;
            margin: 0;
        }
    </style>
    <div class="footer">
        <p> with support of Aditya, Avijeet, Nitoya  <a href="#" target="_blank" ">Perception - A Utility for Object Analysis</a></p>
    </div>
    """,
    unsafe_allow_html=True
)


# Initialize session state for logged_in if not present
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# Sidebar Authentication
st.sidebar.markdown(
    """
    <div style="background: linear-gradient(to right, #ff8a00, #e52e71); padding: 10px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; text-align: center; margin: 0;">User Authentication</h2>
    </div>
    """, unsafe_allow_html=True
)

if not st.session_state['logged_in']:
    auth_mode = st.sidebar.radio("Choose Authentication Mode", ["Login", "Register"])

    if auth_mode == "Register":
        st.sidebar.subheader("Create a new account")
        new_username = st.sidebar.text_input("Username", key="reg_username")
        new_password = st.sidebar.text_input("Password", type="password", key="reg_password")
        if st.sidebar.button("Register"):
            if new_username and new_password:
                try:
                    models.register_user(new_username, new_password)
                    st.sidebar.success("User registered successfully!")
                except sqlite3.IntegrityError:
                    st.sidebar.error("Username already exists. Please choose a different username.")
            else:
                st.sidebar.error("Please enter a username and password.")

    elif auth_mode == "Login":
        st.sidebar.subheader("Login to your account")
        username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", type="password", key="login_password")
        if st.sidebar.button("Login"):
            user = models.login_user(username, password)
            if user:
                st.sidebar.success("Logged in successfully!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                models.log_activity(username, "User logged in")
                st.rerun()  # Update the UI
            else:
                st.sidebar.error("Invalid username or password.")
else:
    # Logged in: show username and logout button
    st.sidebar.write(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.rerun()

# Main Application Content
if st.session_state['logged_in']:
    # Model Options
    model_type = st.sidebar.radio("Select Task", ['Detection'])
    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100

    # Selecting Detection Or Segmentation
    if model_type == 'Detection':
        model_path = Path(settings.DETECTION_MODEL)

    # Load Pre-trained ML Model
    try:
        model = helper.load_model(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

    st.sidebar.markdown(
        """
        <hr style="border: none; border-top: 2px solid #ff8a00; margin: 10px 0;">
        <h2 style="text-align: center; ">Image/Video Config</h2>
        """,
        unsafe_allow_html=True
    )
    source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)

    source_img = None
    # If image is selected
    if source_radio == settings.IMAGE:
        source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        col1, col2 = st.columns(2)

        with col1:
            try:
                if source_img is None:
                    default_image_path = str(settings.DEFAULT_IMAGE)
                    default_image = PIL.Image.open(default_image_path)
                    col_left, col_center, col_right = st.columns([1,6,1])
                    with col_center:
                        st.image(default_image_path, caption="Image sample after detection", width=800)


                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(source_img, caption="Uploaded Image" ) #use_container_width=True)
            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)

        with col2:
            if source_img is None:
                pass
            else:
                if st.sidebar.button('Detect Objects'):
                    res = model.predict(uploaded_image, conf=confidence)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image' )#use_container_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")
                    models.log_activity(st.session_state['username'], "Detected objects on image")

    elif source_radio == settings.VIDEO:
        helper.play_stored_video(confidence, model)

    elif source_radio == settings.WEBCAM:
        helper.play_webcam(confidence, model)

    elif source_radio == settings.YOUTUBE:
        helper.play_youtube_video(confidence, model)

    else:
        st.error("Please select a valid source type!")
else:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-top: 400px;">
            <div style="padding: 4px; background: linear-gradient(45deg, #f3ec78, #af4261); border-radius: 16px;">
                <div style="text-align: center; font-size: 36px; font-weight: bold; padding: 20px; background-color: black; border-radius: 12px;">
                    Please login/register    to use the application.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


