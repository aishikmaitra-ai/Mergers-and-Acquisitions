import streamlit as st
import os
from groq import Groq
from data_ingestion import handle_file,handled_file,handling_file,hand,scrollable_window


# theme = st.radio("Theme", ["Dark", "Light"])
# mode=st.slider("Theme",min_value=0,max_value=1,value=0)
# if mode==0:
#     theme="Dark"
# else:
#     theme="Light"
mode = st.toggle("Theme")
if mode:
    theme="Light"
else:
    theme="Dark"

# if theme == "Light":
#     st.markdown("""
#         <style>

#         /* White background */
#         .stApp {
#             background-color: #ffffff;
#         }

#         /* All normal text → BLACK */
#         .stApp p,
#         .stApp label,
#         .stApp span,
#         .stApp div,
#         .stApp h1,
#         .stApp h2,
#         .stApp h3,
#         .stApp h4,
#         .stApp h5 {
#             color: #000000 !important;
#         }

#         /* ALL BUTTONS → force white text, no exceptions */
#         button,
#         button *,
#         button p,
#         button span,
#         button div,
#         [data-testid="baseButton-primary"],
#         [data-testid="baseButton-secondary"],
#         [data-testid="baseButton-tertiary"] {
#             color: #ffffff !important;
#         }

#         /* NORMAL BUTTONS → BLACK background */
#         .stButton > button {
#             background-color: #000000 !important;
#             border-radius: 8px;
#             border: none;
#         }

#         /* PRIMARY BUTTONS → RED background */
#         [data-testid="baseButton-primary"] {
#             background-color: #e41621 !important;
#             border-radius: 8px;
#             border: none;
#         }

#         /* Hover effects */
#         .stButton > button:hover {
#             background-color: #333333 !important;
#         }

#         [data-testid="baseButton-primary"]:hover {
#             background-color: #c1121a !important;
#         }
#         /* NUCLEAR OVERRIDE - force white on everything inside buttons */
#         button, 
#         button p, 
#         button span, 
#         button div, 
#         button label,
#         .stButton button,
#         .stButton button p,
#         .stButton button span,
#         [data-testid="baseButton-primary"] p,
#         [data-testid="baseButton-secondary"] p,
#         [data-testid="baseButton-primary"] span,
#         [data-testid="baseButton-secondary"] span {
#             color: #ffffff !important;
#             -webkit-text-fill-color: #ffffff !important;
#         }
        
#         /* FILE UPLOADER BUTTON → force white text */
#         [data-testid="stFileUploader"] button,
#         [data-testid="stFileUploader"] button p,
#         [data-testid="stFileUploader"] button span {
#             color: #ffffff !important;
#             -webkit-text-fill-color: #ffffff !important;
#         }

#         </style>
#         """, unsafe_allow_html=True)
if theme == "Light":
    st.markdown("""
        <style>

        /* White background */
        .stApp {
            background-color: #ffffff;
        }

        /* All normal text → BLACK */
        .stApp p,
        .stApp label,
        .stApp span,
        .stApp div,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5 {
            color: #000000 !important;
        }

        /* FILE UPLOADER BOX → light gray, border, shadow */
        [data-testid="stFileUploader"] {
            background-color: #f2f2f2 !important;
            border: 1.5px solid #cccccc !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10) !important;
            padding: 8px 12px !important;
            transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
        }

        /* FILE UPLOADER BOX → hover interactive effect */
        [data-testid="stFileUploader"]:hover {
            border-color: #888888 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
            cursor: pointer;
        }

        /* File uploader inner dropzone */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #f2f2f2 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* File uploader text → black */
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] div,
        [data-testid="stFileUploaderDropzoneInstructions"] * {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        /* SELECTBOX → light gray, border, shadow */
        [data-testid="stSelectbox"] > div > div {
            background-color: #f2f2f2 !important;
            border: 1.5px solid #cccccc !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10) !important;
            transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
        }

        /* SELECTBOX hover */
        [data-testid="stSelectbox"] > div > div:hover {
            border-color: #888888 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
        }

        /* SELECTBOX text → black */
        [data-testid="stSelectbox"] span,
        [data-testid="stSelectbox"] div {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        /* SIDEBAR → white background */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
        }

        /* SIDEBAR text → black */
        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] a {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* SIDEBAR active/selected nav item → light gray highlight */
        [data-testid="stSidebar"] [aria-selected="true"],
        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background-color: #f2f2f2 !important;
            border-radius: 8px !important;
        }

        /* SIDEBAR nav links hover */
        [data-testid="stSidebarNavLink"]:hover {
            background-color: #f2f2f2 !important;
            border-radius: 8px !important;
        }

        /* SIDEBAR collapse arrow → black */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* ALL BUTTONS → force white text */
        button,
        button *,
        button p,
        button span,
        button div,
        button label,
        .stButton button,
        .stButton button p,
        .stButton button span,
        [data-testid="baseButton-primary"],
        [data-testid="baseButton-secondary"],
        [data-testid="baseButton-tertiary"],
        [data-testid="baseButton-primary"] p,
        [data-testid="baseButton-secondary"] p,
        [data-testid="baseButton-primary"] span,
        [data-testid="baseButton-secondary"] span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        /* NORMAL BUTTONS → BLACK background */
        .stButton > button {
            background-color: #000000 !important;
            border-radius: 8px;
            border: none;
            transition: background-color 0.2s ease !important;
        }

        /* PRIMARY BUTTONS → RED background */
        [data-testid="baseButton-primary"] {
            background-color: #e41621 !important;
            border-radius: 8px;
            border: none;
        }

        /* Hover effects */
        .stButton > button:hover {
            background-color: #333333 !important;
        }

        [data-testid="baseButton-primary"]:hover {
            background-color: #c1121a !important;
        }

        /* FILE UPLOADER BUTTON → white text */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploader"] button p,
        [data-testid="stFileUploader"] button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        </style>
        """, unsafe_allow_html=True)
#     st.markdown("""
#     <style>
#     :root {
#         --text-color: #470814;
#     }
#     :button {
#         color: #ee0832;
#     }

#     /* This targets the main app background */
#     .stApp {
#         background-color: #f5f5f5;
#     }

#     /* This forces ALL labels, headers, and radio button text to your dark color */
#     .stApp p, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3 {
#         color: #470814 !important;
#     }

#     /* This specifically fixes the radio button (Dark/Light) text color */
#     div[data-testid="stWidgetLabel"] p {
#         color: #470814 !important;
#     }
#     /* File uploader text color */
#     div[data-testid="stFileUploader"] p,
#     div[data-testid="stFileUploader"] span,
#     div[data-testid="stFileUploader"] label {
#         color: #470814 !important;
#     </style>
#     """, unsafe_allow_html=True)
# if theme == "Light":
#     st.markdown("""
#     <style>
#     :root {
#         --primary-color:#281fa8;
#         --text-color: #470814;
#         --secondary-background-color:#09030e;
#     }

#     .stApp {
#         background-color:#f5f5f5;
#         color:#470814;
#     }
#     </style>
#     """, unsafe_allow_html=True)

st.title("AI Dashboard")
st.set_page_config(layout="wide")

col1,col2=st.columns(2)
#row1,row2=st.rows(2)

# pages_dir = os.path.join(os.getcwd(), "pages")
# if os.path.exists(pages_dir):
#     st.write("Files found in pages/:", os.listdir(pages_dir))
# else:
#     st.error("The 'pages' folder was not found in the current directory!")



# st.subheader("Data Ingestion")
# uploaded_files = st.file_uploader("Upload your ERP documents", accept_multiple_files=True)

# if uploaded_files:
#     st.session_state["uploaded_files"] = uploaded_files
#     selected_file = st.selectbox(
#         "Select a file to view:",
#         options=uploaded_files,
#         format_func=lambda x: x.name
#     )
#     st.write("---")      
    
#     if selected_file:
#         st.write(f"**Viewing:** {selected_file.name}")
#         st.write(f"File type: {'docx' if selected_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' else selected_file.type}")
#         content,file_type = hand(selected_file)
        
#         if content is not None:
#             scrollable_window(content,file_type)

st.subheader("Data Ingestion")

uploaded_files = st.file_uploader(
    "Upload your ERP documents",
    accept_multiple_files=True,
    key="file_upload"
)

# Save files
if uploaded_files:
    st.session_state["uploaded_files"] = uploaded_files

# Reload files if returning to page
if "uploaded_files" in st.session_state:
    uploaded_files = st.session_state["uploaded_files"]

# Continue only if files exist
if uploaded_files:

    selected_file = st.selectbox(
        "Select a file to view:",
        options=uploaded_files,
        format_func=lambda x: x.name
    )

    st.write("---")

    if selected_file:
        st.write(f"**Viewing:** {selected_file.name}")

        st.write(
            f"File type: {'docx' if selected_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' else selected_file.type}"
        )

        content, file_type = hand(selected_file)

        if content is not None:
            scrollable_window(content, file_type)

st.subheader("ERP Auditing")
audit_page = os.path.join("pages", "ERP_Auditing_page.py")

if st.button("Audit",type="primary"):
    st.switch_page(audit_page)

st.subheader("Synergy Module")
synergy_page=os.path.join("pages","synergy.py")

if st.button("View Synergy",type="primary"):
    st.switch_page(synergy_page)



