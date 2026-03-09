import streamlit as st
from dashboard import theme

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

# if "uploaded_files" in st.session_state:
#     file = st.session_state["uploaded_files"]
#     st.write("Using file:", file.name)
# else:
#     st.warning("Upload a file first.")

if "uploaded_files" in st.session_state:
    files = st.session_state["uploaded_files"]

    for file in files:
        st.write("Using file:", file.name)
else:
    st.warning("Upload a file first.")
st.title("Welcome to the Synergy Page!")
st.write("You successfully navigated here.")

st.markdown(
"""
Synergy refers to the idea that the combined effect of multiple elements working together is greater than the sum of their individual contributions. In simple terms, when people, teams, technologies, or organizations collaborate effectively, they can achieve outcomes that would be difficult or impossible to reach independently. Synergy often arises from complementary strengths, shared goals, and coordinated effort, allowing resources and skills to be used more efficiently.

In a business context, synergy is commonly discussed during partnerships, mergers, and acquisitions. Companies expect synergy when combining operations because the integrated organization may reduce costs, expand market reach, improve innovation, or enhance productivity. For example, one company might contribute strong technology while another provides market access or operational expertise. When these strengths are combined strategically, the overall value created can exceed what either company could generate alone.

Synergy also applies beyond business environments, including teamwork, scientific collaboration, and interdisciplinary problem-solving. When individuals with diverse knowledge and perspectives work together, they often generate more creative solutions and better decisions. Effective communication, trust, and alignment of objectives are key factors that enable synergy, ensuring that collaboration produces meaningful and sustainable results.

"""
)

if st.button("Back to Home"):
    st.switch_page("dashboard.py")