import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set the Streamlit page configuration
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.write("Transform your files CSS and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # Extract file extension
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the file depending on its extension
        if file_ext == ".csv":
            df = pd.read_csv(file)

        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display basic information about the uploaded file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Display a preview of the first few rows of the dataframe
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean Data for: {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Remove Missing Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

        # Column selection for conversion
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        if columns:
            df = df[columns]
        else:
            st.error("No columns selected!")

        # Data visualization options
        st.subheader("📊 Data visualization")
        if st.checkbox(f"Show Visualization for: {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            color = st.color_picker("Pick A Color", "#00f900")
            st.write("The current color is", color)

        # Conversion options (CSV or Excel)
        st.subheader("♋ Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"🔽 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        st.success("🎉 All files processed!")
