import pandas as pd
import pandas_profiling
from openpyxl import load_workbook
from io import BytesIO
import streamlit as st

# Function to generate analytics report using Pandas Profiling
def generate_analytics_report(data):
    profile = pandas_profiling.ProfileReport(data)
    return profile.to_json()

# Function to read Excel file and generate analytics report
def analyze_excel(file):
    try:
        # Load Excel file
        wb = load_workbook(file)
        sheet = wb.active

        # Load data into a Pandas DataFrame
        data = pd.DataFrame(sheet.values, columns=[cell.value for cell in sheet[1]])

        # Generate analytics report
        analytics_report = generate_analytics_report(data)

        return analytics_report
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
def main():
    st.title("Excel Analytics App")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        st.write("Analyzing Excel file...")

        # Read the Excel file and generate analytics report
        analytics_report = analyze_excel(uploaded_file)

        # Display the report using Streamlit's JSON component
        st.json(analytics_report)

if __name__ == "__main__":
    main()
