import pandas as pd
import pandas_profiling
from io import BytesIO
import streamlit as st

# Function to generate analytics report using Pandas Profiling
def generate_analytics_report(data):
    profile = pandas_profiling.ProfileReport(data)
    return profile.to_json()

# Function to read file and generate analytics report
def analyze_file(file, file_type):
    try:
        if file_type == 'csv':
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file, engine='openpyxl')

        # Generate analytics report
        analytics_report = generate_analytics_report(data)

        return analytics_report
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
def main():
    st.title("File Analytics App")

    uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        st.write("Analyzing file...")

        # Determine file type based on extension
        file_extension = uploaded_file.name.split('.')[-1]
        file_type = file_extension.lower()

        # Read the file and generate analytics report
        analytics_report = analyze_file(uploaded_file, file_type)

        # Display the report using Streamlit's JSON component
        st.json(analytics_report)

if __name__ == "__main__":
    main()
