import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re
from PIL import Image  # Add this import at the top

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def show_login_page():
    # Create columns for centering
    col1, col2, col3 = st.columns([1,1,1])
    
    with col2:
        # Reduced vertical space at top
        st.markdown("<br>", unsafe_allow_html=True)  # Reduced from 3 <br> to 1
        
        # Centered login container with border and margin-top adjustment
        st.markdown("""
            <div style='padding: 5px; 
                        border: 2px solid red; 
                        border-radius: 10px; 
                        text-align: center;
                        margin: auto;
                        margin-top: -38px;'>  
            <h1 style="color: red;">Login Required</h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        password = st.text_input("Enter password", type="password")
        
        # Center the login button
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Login", use_container_width=True):
                if not email or not password or not name:
                    st.error("Please fill in all fields")
                    return False
                if not is_valid_email(email):
                    st.error("Please enter a valid email address")
                    return False
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.rerun()
    return False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = None

st.set_page_config(page_title="Data Sweeper Python Mindset Assignment-1", page_icon=":bar_chart:", layout="wide")

#Custom CSS
st.markdown(
    """
    <style>
    st.App{
        background-color: black;
        color: white;
    }
    .sidebar .sidebar-content {
        color: white;
    }
    [data-testid="stSidebarNav"] {
        color: red !important;
    }
    .st-emotion-cache-10trblm {
        color: red;
    }
    /* Hide sidebar scroll */
    [data-testid="stSidebar"] {
        overflow-y: hidden !important;
    }
    /* Adjust sidebar width */
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 200px;
        max-width: 200px;
    }
    /* Remove padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
     """,
    unsafe_allow_html=True
)

# Check login status
if not st.session_state.logged_in:
    show_login_page()
else:
    # Sidebar with red title and welcome message at top
    st.sidebar.markdown('<p style="color: red; font-size: 20px; font: bold">🧭Navigation</p>', unsafe_allow_html=True)
    st.sidebar.markdown(f"Welcome, {st.session_state.user_name}!")
    
    # Logout button right after welcome message
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_name = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation radio in middle
    page = st.sidebar.radio("Choose a section:", ["Upload & Process", "Image Convert", "About"])
    
    # Create space before logout button
    st.sidebar.markdown("<br>" * 10, unsafe_allow_html=True)
    
    if page == "About":
        st.markdown('<h1 style="color: red;">⚽ About Data Sweeper</h1>', unsafe_allow_html=True) 
        st.write("""This app converts CSV, Excel, and image files to PNG, JPEG, and WEBP formats with built-in data cleaning and transformation
        
        Features:
        - File format conversion
        - Data cleaning
        - Basic visualization
        - Image Converter
        """)
    
    elif page == "Image Convert":
        st.markdown('<h1 style="color: red;">🖼️ Image Converter</h1>', unsafe_allow_html=True)
        st.write("Convert your images between different formats.")
        
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image")
            
            col1, col2 = st.columns(2)
            with col1:
                target_format = st.radio("Convert to:", ["PNG", "JPEG", "WEBP"])
            
            with col2:
                if st.button("Convert Image"):
                    buf = BytesIO()
                    if target_format == "PNG":
                        image.save(buf, format="PNG")
                        mime = "image/png"
                        file_ext = ".png"
                    elif target_format == "JPEG":
                        image.save(buf, format="JPEG")
                        mime = "image/jpeg"
                        file_ext = ".jpg"
                    else:  # WEBP
                        image.save(buf, format="WEBP")
                        mime = "image/webp"
                        file_ext = ".webp"
                    
                    buf.seek(0)
                    file_name = os.path.splitext(uploaded_image.name)[0] + file_ext
                    
                    st.download_button(
                        label=f"Download converted image as {target_format}",
                        data=buf,
                        file_name=file_name,
                        mime=mime
                    )
    
    else:
        # Main content
        st.markdown('<h1 style="color: red;">💿Data Sweeper Python Mindset Assignment-1</h1>', unsafe_allow_html=True)
        st.write("Transform your file between CVS and Excel formats with built-in data cleaning and transformation features.")

        # File upload
        uploaded_file = st.file_uploader("Upload your files (accepted formats: .csv, .xlsx)", type=["csv", "xlsx"], accept_multiple_files=True)

        if uploaded_file:
            for file in uploaded_file:
                file_ext = os.path.splitext(file.name)[-1].lower()
                
                if file_ext == ".csv":
                    df = pd.read_csv(file)
                elif file_ext == ".xlsx":
                    df = pd.read_excel(file)
                else:
                    st.error(f"Unsupported file type: {file_ext}")
                    continue

                # File preview
                st.write("🔍Preview the head of the Dataframe")
                st.dataframe(df.head())
                
                # Data cleaning options
                st.subheader("🧹Data Cleaning Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Remove duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("✅Duplicates removed successfully")
                
                with col2:
                    if st.button(f"Fill missing values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅Missing values have been filled!")

                # Data visualization
                st.subheader("📊Data Visualization")
                st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])

                # Conversion Options
                st.subheader("🔄Conversion Options")
                conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
                if st.button(f"Convert {file.name}"):
                    buffer = BytesIO()
                    if conversion_type == "CSV":
                        df.to_csv(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".csv")
                        mime_type = "text/csv"
                    
                    elif conversion_type == "Excel":
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlsx")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)
                    
                    st.download_button(
                        label=f"Download {file_name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type  # Changed from mine_type to mime_type
                    )

            st.success("🎉 All Files processed successfully!")