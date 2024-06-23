import numpy as np
import pandas as pd

class IvrProcessor:
    def __init__(self):
        pass

    def read_file(self, uploaded_file) -> pd.DataFrame:
        """
        Read the uploaded CSV file, clean it, and return a DataFrame.
        
        Parameters:
        uploaded_file: Path to the uploaded CSV file.

        Returns:
        A cleaned pandas DataFrame.
        """
        
        df = pd.read_csv(uploaded_file, skiprows=1, names=range(100), engine='python')

        # Drop empty columns
        df.dropna(axis='columns', how='all', inplace=True)

        # Assign the first row as the column names
        df.columns = df.iloc[0]

        # Drop the original row that had been assigned as column names
        df = df.iloc[1:]

        return df

    def extract_unconnected_phonenum(self, df) -> pd.DataFrame:
        """
        Process the uploaded IVR raw results to extract unconnected phone numbers. In other words, we want phone numbers that 
        didn't participate in the IVR survey yet.

        Parameters:
        df: The pandas DataFrame containing IVR results.

        Returns:
        A pandas DataFrame with unconnected phone numbers.

        Note:
        - The function assumes the uploaded CSV has specific columns of interest, notably 'PhoneNo' and 'UserKeyPress'.
        - It is assumed that the second row of the CSV provides the column names for the data.
        """

        # Keep rows where 'UserKeyPress' is NA and select 'PhoneNo' column
        recycled_phonenum = df.loc[df['UserKeyPress'].isna(), ['PhoneNo']]

        # Rename to follow usual convention
        recycled_phonenum.rename(columns={'PhoneNo': 'phonenum'}, inplace=True)

        return recycled_phonenum
    
    def calculate_total_pickup(self, df) -> int:
        """
        Calculate the total number of picked-up calls based on non-NA 'UserKeyPress' values.

        Parameters:
        df: The pandas DataFrame containing IVR results.

        Returns:
        The count of picked-up calls.
        """    
        # Count rows where 'UserKeyPress' is not NA
        pickup_count = df['UserKeyPress'].notna().sum()

        return pickup_count

    def calculate_total_cr(self, df) -> int:
        """
        Calculate the total number of complete responses based on non-empty 'UserKeyPress' values.

        Parameters:
        df: The pandas DataFrame containing IVR results.

        Returns:
        The count of complete responses.
        """

        # Replace non-keypresses with NaN and count non-NA rows
        complete_keypress = df.replace(r'FlowNo_\d{1,2}=$', np.NaN, regex=True)

        complete_keypress.dropna(inplace=True)

        cr_count = len(complete_keypress)

        return cr_count

