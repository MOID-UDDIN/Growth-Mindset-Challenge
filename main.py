import streamlit as st
import pandas as pd
from io import BytesIO

def setup_ui():
    st.set_page_config(page_title="Convert & Clean Data", layout="wide")
    st.markdown(
        """
        <style>
            .css-1d391kg {background-color: #f4f4f4;}
            .stButton>button {background-color: #4CAF50; color: white; font-size: 16px;}
            .stDownloadButton>button {background-color: #ff9800; color: white; font-size: 16px;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Convert & Clean Data")
    st.write("Upload your CSV and Excel Files to clean, analyze & convert formats effortlessly 🚀")

def process_file(file):
    ext = file.name.split(".")[-1]
    df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
    
    st.subheader(f"🔍 {file.name} - Preview")
    st.dataframe(df.head())
    
    if st.checkbox(f"Fill Missing Values - {file.name}"):
        df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
        st.success("Missing values filled successfully!")
        st.dataframe(df.head())
    
    selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
    df = df[selected_columns]
    st.dataframe(df.head())
    
    if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
    
    return df, ext

def download_file(df, file, ext):
    format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
    if st.button(f"⬇️ Download {file.name} as {format_choice}"):
        output = BytesIO()
        if format_choice == "CSV":
            df.to_csv(output, index=False)
            mime = "text/csv"
            new_name = file.name.replace(ext, "csv")
        else:
            df.to_excel(output, index=False)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            new_name = file.name.replace(ext, "xlsx")
        output.seek(0)
        st.download_button("⬇️ Download File", file_name=new_name, data=output, mime=mime)
    

def main():
    setup_ui()
    files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)
    
    if files:
        for file in files:
            df, ext = process_file(file)
            download_file(df, file, ext)
            st.success("Processing Completed! 🎉")

if __name__ == "__main__":
    main()
