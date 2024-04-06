import pandas as pd
import numpy as np

def merger(df_list, phonenum_list):
    """
    Concatenates lists of DataFrames and renames a column.

    Parameters:
    - df_list (list of pd.DataFrame): List of DataFrames to be concatenated vertically.
    - phonenum_list (list of pd.DataFrame): List of phone number DataFrames to be concatenated vertically.

    Returns:
    - df_merge (pd.DataFrame): Concatenated DataFrame of df_list.
    - phonenum_combined (pd.DataFrame): Concatenated DataFrame of phonenum_list with 'PhoneNo' column renamed to 'phonenum'.
    """
    # Check if the lists are not empty before concatenating
    if df_list:
        df_merge = pd.concat(df_list, axis='index')
    else:
        df_merge = pd.DataFrame()  # Return an empty DataFrame if list is empty

    if phonenum_list:
        phonenum_combined = pd.concat(phonenum_list, axis='rows')
        phonenum_combined.rename(columns={'PhoneNo': 'phonenum'}, inplace=True)
    else:
        phonenum_combined = pd.DataFrame()  # Return an empty DataFrame if list is empty

    return df_merge, phonenum_combined



def extract_unconnected_phonenum(uploaded_file):
    """
    Process the uploaded CSV files to extract unconnected phone numbers. In other words, we want phone numbers that 
    didn't participate in the IVR survey yet.

    Parameters:
    - uploaded_file: A file-like object representing the uploaded CSV file.
                     This object must support file-like operations such as read.

    Returns:

    Note:
    - The function assumes the uploaded CSV has specific columns of interest, notably 'PhoneNo' and 'UserKeyPress'.
    - It is assumed that the second row of the CSV provides the column names for the data.
    """

    df = pd.read_csv(uploaded_file, skiprows=1, names=range(100), engine='python')

    df.dropna(axis='columns', how='all', inplace=True)

    df.columns = df.iloc[0]

    # Keep rows where its respective 'UserKeyPress' column is NA
    recycled_phonenum = df.loc[df['UserKeyPress'].isna()]

    recycled_phonenum = recycled_phonenum[['PhoneNo']]

    recycled_phonenum.rename(columns={'PhoneNo': 'phonenum'}, inplace=True)

    return recycled_phonenum