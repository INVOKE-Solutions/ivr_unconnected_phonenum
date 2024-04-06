import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from utils import extract_unconnected_phonenum

st.set_page_config(
    page_title='IVR Unconnected Phone Numbers',
    # page_icon=Image.open('./images/invoke_logo.png'),
    layout="centered",    
    initial_sidebar_state="auto",

)

st.title('IVR Unconnected Phone Numbers')

st.markdown('''
**NOTE:** This web app is meant to be used when all phone numbers for a given population is included in the sampling. 
'''
)

def run():

    # Check if data is already processed and available in session state
    if 'processed' not in st.session_state:
        st.session_state['processed'] = False
      
    if 'all_unconnected_phonenum' not in st.session_state:

        # Setting up the file uploader widget
        uploaded_files = st.file_uploader("Upload IVR Files (.csv format)", 
                                          accept_multiple_files=True, 
                                          type=['csv', 'xlsx'], 
                                          help='You can upload multiple csv files at once')

        # Display the count of uploaded files
        if uploaded_files:
            st.write(f"Number of files uploaded: {len(uploaded_files)}")

        if st.button('Process'):
            with st.spinner("Processing the files..."):

                st.session_state['unconnected_phonenum'] = []

                # Extract unconnected phone numbers only
                for uploaded_file in uploaded_files:
                    unconnected_phonenum = extract_unconnected_phonenum(uploaded_file)

                    st.session_state['unconnected_phonenum'].append(unconnected_phonenum)
                
                all_unconnected_phonenum = pd.concat(st.session_state['unconnected_phonenum'], ignore_index=True).drop_duplicates()

                st.session_state['all_unconnected_phonenum'] = all_unconnected_phonenum
                
                st.session_state['processed'] = True
    else:
        st.session_state['processed'] = False
        st.write('**:red[An error has occurred. Please reload the web app.]**')

    if st.session_state['processed']:
        st.success("Files have been processed successfully ✨")

    if st.session_state['processed']:
        # Display a snippet of the cleaned data
        st.markdown("### Data Preview")

        st.write(f"Total unconnected phone numbers: {len(all_unconnected_phonenum):,}")

        st.dataframe(st.session_state['all_unconnected_phonenum'].sample(6))

        # Current date for the filename
        formatted_date = datetime.now().strftime("%Y%m%d")

        # Format the default filename
        default_filename = f'IVR_unconnected_phonenum_v{formatted_date}.csv'

        # Use the default filename in the text input, allowing the user to edit it
        output_filename = st.text_input("Custom the file name before downloading if needed", value=default_filename)

        # Check if the output filename ends with '.csv', if not append '.csv'
        if not output_filename.lower().endswith('.csv'):
            output_filename += '.csv'

        # Download button
        data_as_csv = st.session_state['all_unconnected_phonenum'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download file",
            data=data_as_csv,
            file_name=output_filename,
            mime='text/csv'
        )
        
if __name__ == "__main__":
    run()