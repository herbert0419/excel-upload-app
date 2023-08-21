import base64
from io import BytesIO
import pandas as pd
import pandas_profiling
from openpyxl import load_workbook
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to generate analytics report using Pandas Profiling
def generate_analytics_report(data):
    profile = pandas_profiling.ProfileReport(data)
    return profile.to_json()

# Function to read file and generate analytics report
def analyze_file(file, file_extension):
    try:
        if file_extension == "xlsx" or file_extension == "xls":
            # Load Excel file
            wb = load_workbook(file)
            sheet = wb.active

            # Load data into a Pandas DataFrame
            data = pd.DataFrame(sheet.values, columns=[cell.value for cell in sheet[1]])

        elif file_extension == "csv":
            # Load CSV file
            data = pd.read_csv(file)

        # Generate analytics report
        analytics_report = generate_analytics_report(data)

        return data, analytics_report
    except Exception as e:
        return None, f"An error occurred: {e}"
    
def export_all_figures_to_base64(figures):
    figure_data = []
    for figure in figures:
        buffer = BytesIO()
        figure.savefig(buffer, format="png")
        buffer.seek(0)
        figure_data.append(base64.b64encode(buffer.read()).decode())
    return figure_data


# Streamlit UI
def main():
    st.title("Data Analytics App")

    uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        st.write("Analyzing file...")

        file_extension = uploaded_file.name.split(".")[-1].lower()

        # Read the file and generate analytics report
        data, analytics_report = analyze_file(uploaded_file, file_extension)

        if data is not None:
            # Display the analytics report using Streamlit's JSON component
            st.json(analytics_report)

            # Display the data in tabular form
            st.subheader("Data Table")
            st.dataframe(data)

            # Display summary statistics for numeric columns
            st.subheader("Summary Statistics for Numeric Columns")
            st.write(data.describe())

            # Display correlation heatmap for numeric columns
            st.subheader("Correlation Heatmap for Numeric Columns")
            numeric_columns = data.select_dtypes(include="number").columns
            correlation_matrix = data[numeric_columns].corr()
            sns.set(style="white")
            plt.figure(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0)
            st.pyplot(plt)
            heatmap_figure = plt.gcf()
            st.pyplot(heatmap_figure)

            # Display distribution plots for numeric columns
            st.subheader("Distribution Plots for Numeric Columns")
            for column in numeric_columns:
                plt.figure(figsize=(8, 5))
                sns.histplot(data[column], kde=True)
                plt.title(f"Distribution of {column}")
                st.pyplot(plt)

            # Display count plots for categorical columns
            st.subheader("Count Plots for Categorical Columns")
            categorical_columns = data.select_dtypes(include="object").columns
            for column in categorical_columns:
                plt.figure(figsize=(8, 5))
                sns.countplot(data=data, x=column)
                plt.xticks(rotation=45)
                plt.title(f"Count of {column}")
                st.pyplot(plt)

            # Display pair plot for numeric columns
            st.subheader("Pair Plot for Numeric Columns")
            sns.pairplot(data[numeric_columns])
            st.pyplot(plt)

            # Display box plots for numeric columns
            st.subheader("Box Plots for Numeric Columns")
            for column in numeric_columns:
                plt.figure(figsize=(8, 5))
                sns.boxplot(data=data, y=column)
                plt.title(f"Box Plot of {column}")
                st.pyplot(plt)

            # Display export button for the report
            st.subheader("Export Report and Figures")
            export_button = st.button("Export Analytics Report and Figures")
            if export_button:
                all_figures = [heatmap_figure]  # Add other figures here
                export_data_and_figures(analytics_report, all_figures)


def export_data_and_figures(analytics_report, figures):
    # Convert JSON report to bytes
    report_bytes = analytics_report.encode("utf-8")

    # Create a download link for the report
    b64_report = base64.b64encode(report_bytes).decode()
    href_report = f'<a href="data:application/octet-stream;base64,{b64_report}" download="analytics_report.json">Download Report</a>'

    # Convert all figures to base64
    figure_data = export_all_figures_to_base64(figures)
    figure_links = [f'<a href="data:image/png;base64,{data}" download="figure_{i}.png">Download Figure {i}</a>' for i, data in enumerate(figure_data, 1)]

    st.markdown(href_report, unsafe_allow_html=True)
    for link in figure_links:
        st.markdown(link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
