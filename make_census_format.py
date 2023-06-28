import pandas as pd
import numpy as np
import pickle
import streamlit as st
import base64
from io import BytesIO
import os


def read_file(file):
    if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file)
    elif file.type == "application/vnd.ms-excel":
        df = pd.read_excel(file)
    elif file.type == "text/csv":
        df = pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format. Only XLSX, XLS, and CSV files are supported.")
    return df


def main():
    def remove_location_column(df):
        if 'Location' in df.columns:
            df.drop('Location', axis=1, inplace=True)
        return df

    # File Upload
    file = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])
    if file is not None:
        df = read_file(file)
        df = remove_location_column(df)
        df = df.rename(columns={'Job Type':'Department', 'Agency':'Location'})
        df['Employee Type'] = None
        df['Salary or Hourly Rate'] = None
        df['Key - FT/PT/PD'] = None
        df['Key - Pay Type'] = None
        df['Reported on'] = pd.Timestamp.now().date()
        df['Reported on'] = pd.to_datetime(df['Reported on'])
        df = df[['Employee Number', 'Name', 'Employee Type', 'Department', 'Status',
        'Hire Date', 'A) W2 or 1099',
        'B) FT/Part Time/Per Diem', 'C) Pay Type', 'Salary or Hourly Rate', 'D) Productivity',
        'E) Availability', 'F) Coverage Areas','Key - FT/PT/PD', 'Key - Pay Type', 'Reported on', 'Location']]
        
        # Download button
        excel_data = BytesIO()
        if file is not None:
            file_extension = os.path.splitext(file.name)[1][1:].lower()
            if file_extension == 'xlsx' or file_extension == 'xls':
                df.to_excel(excel_data, index=False, encoding='utf-8', engine='xlsxwriter')
            elif file_extension == 'csv':
                df.to_csv(excel_data, index=False, encoding='utf-8')
            else:
                st.warning("Unsupported file format. Unable to download.")
                return
            
            excel_data.seek(0)
            b64_excel = base64.b64encode(excel_data.read()).decode()
            href_excel = f'<a href="data:application/octet-stream;base64,{b64_excel}" download="{file.name}">Download Updated Data ({file.name})</a>'
            st.markdown(href_excel, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
