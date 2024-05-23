import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import IvrProcessor

st.set_page_config(
    page_title='IVR Unconnected Phone Numbers',
    layout="centered",    
    initial_sidebar_state="auto"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('IVR Unconnected Phone Numbers')

st.markdown(
    '''
    **NOTE:** This web app is meant to be used when all phone numbers for a given population is included in the sampling.
    '''
)

# Initialize session state variables if not already present
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = None
if 'process_complete' not in st.session_state:
    st.session_state['process_complete'] = False

# Setting up the file uploader widget
uploaded_files = st.file_uploader("Upload IVR Files (.csv format)",
                                    accept_multiple_files=True, 
                                    type=['csv', 'xlsx'], 
                                    help='You can upload multiple csv files at once')

# Update the session state with the uploaded file
if uploaded_files is not None:
    st.session_state['uploaded_files'] = uploaded_files
else:
    st.session_state['uploaded_files'] = False
    st.session_state['process_complete'] = False

if st.session_state['uploaded_files']:
    # Display the count of uploaded files
    st.write(f"Number of files uploaded: {len(uploaded_files)}")

    if st.button('Process'):
        # Process the files
        with st.spinner("Processing the files..."):

            # Initialize class
            ip = IvrProcessor()

            unconnected_phonenums = []
            total_cr = 0

            # Extract unconnected phone numbers only
            for uploaded_file in uploaded_files:

                ivr_file = ip.read_file(uploaded_file)

                unconnected_phonenum = ip.extract_unconnected_phonenum(ivr_file)
                unconnected_phonenums.append(unconnected_phonenum)

                cr_count = ip.calculate_total_cr(ivr_file)
                total_cr += cr_count

                # Store total CR value in session state
                st.session_state['total_cr'] = total_cr

            all_unconnected_phonenum = pd.concat(unconnected_phonenums, ignore_index=True).drop_duplicates()

            # Randomize the phone numbers sequence
            all_unconnected_phonenum = all_unconnected_phonenum.sample(len(all_unconnected_phonenum))

            # Store the output DF in session state
            st.session_state['all_unconnected_phonenum'] = all_unconnected_phonenum

            st.success("Files have been processed successfully ✨")

            st.write(f"Total CR: {st.session_state['total_cr']:,}")

            st.write(f"Total unconnected phone numbers: {len(st.session_state['all_unconnected_phonenum']):,}")

            # Display a snippet of the cleaned data randomly
            st.markdown("### Data Preview")
            st.dataframe(st.session_state['all_unconnected_phonenum'].sample(6))

            # st.session_state['total_cr'] = total_cr
            st.session_state['process_complete'] = True  # Set process complete flag

# Warning if 'Process' is clicked before file upload
if not st.session_state['uploaded_files'] and st.button("Process"):
    st.warning("Please upload your IVR raw files first.")

@st.experimental_fragment
def download_file(data, file_name):
    st.download_button(
        label = "Download file",
        data = data,
        file_name = file_name,
        mime = 'text/csv',
        key = 'download'
    )


# Show 'Download' button if the file has been processed
if st.session_state['uploaded_files'] and st.session_state['process_complete']:

    # Generate current date for file versioning
    formatted_date = datetime.now().strftime("%d%m%Y")

    # Default file name with current date
    default_filename = f'IVR_unconnected_phonenum_v{formatted_date}.csv'

    # Convert to csv
    data_as_csv = st.session_state['all_unconnected_phonenum'].to_csv(index=False).encode('utf-8')

    download_file(data_as_csv, default_filename)              