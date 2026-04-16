import streamlit as st
import pandas as pd

# Configure the Streamlit page layout and title
st.set_page_config(page_title="Data Cleaner Pro", page_icon="🧹", layout="wide")

# App header and description
st.title("Data Cleaner Express 🧹")
st.write("A fast and interactive tool to clean your CSV files in one click.")

# Provide a file uploader widget for CSV files
uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    try:
        # Load the uploaded CSV into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        
        # Display original data dimensions and a preview
        st.subheader("Data Preview (Before)")
        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
        st.dataframe(df.head(20))
        
        # UI settings for data cleaning options
        st.subheader("⚙️ Cleaning Options")
        
        # Toggle option to remove duplicate rows
        drop_duplicates = st.checkbox("Remove duplicate rows")
        
        # Selection menu for missing value handling strategies
        na_action = st.radio(
            "How would you like to handle missing values (NaN)?",
            ["Do nothing", 
             "Drop rows with missing values (Data Loss)", 
             "Fill with column average (Numerical columns only)"]
        )
            
        # Execute cleaning process when the user clicks the button
        if st.button("Start Cleaning 🚀"):
            
            # Create a copy of the dataframe to preserve the original data
            df_clean = df.copy()
            
            # Handle deduplication
            if drop_duplicates:
                df_clean = df_clean.drop_duplicates()
                
            # Handle missing values (NaN) based on user selection
            if na_action == "Drop rows with missing values (Data Loss)":
                # Drop any row containing at least one missing value
                df_clean = df_clean.dropna()
            elif na_action == "Fill with column average (Numerical columns only)":
                # Identify numerical columns to avoid calculating the mean on text/categorical data
                numeric_cols = df_clean.select_dtypes(include=['number']).columns
                
                # Impute missing values in numerical columns using the respective column's mean
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
                
            # Display the cleaned data preview and new dimensions
            st.subheader("✨ Data Preview (After)")
            st.write(f"**Remaining Rows:** {df_clean.shape[0]}")
            st.dataframe(df_clean.head())
            
            # Convert the cleaned dataframe back to CSV format for download
            csv = df_clean.to_csv(index=False).encode('utf-8')
            
            # Provide a download button for the processed file
            st.download_button(
                label="⬇️ Download Cleaned File",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv",
            )
            
    except Exception as e:
        # Handle potential file reading or processing errors gracefully
        st.error(f"An error occurred while reading the file. Error: {e}")
