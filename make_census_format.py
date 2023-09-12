import pandas as pd
import numpy as np
import pickle
import streamlit as st
import base64
from io import BytesIO
import os
from datetime import date


def read_file(file):
    if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file, header = 1)
    elif file.type == "application/vnd.ms-excel":
        df = pd.read_excel(file, header = 1)
    elif file.type == "text/csv":
        df = pd.read_csv(file, header = 1)
    else:
        raise ValueError("Unsupported file format. Only XLSX, XLS, and CSV files are supported.")
    return df





def main():    
    def add_agency_by_location(df):
        if 'Location' in df.columns:
            df['Agency'] = np.where(df['Location'] == 'California - San Diego', 'San Diego, CA',
                                    np.where(df['Location'] == 'Virginia - Caring Angels', 'Winchester, VA',
                                             np.where(df['Location'] == 'West Virginia', 'Martinsburg, WV',
                                                      np.where(df['Location'] == 'Virginia - Countryside', 'Sterling, VA',
                                                               np.where(df['Location'] == 'Virginia - Hillside Hospice', 'Hillside Hospice',
                                                                        np.where(df['Location'] == 'PathWell Health - WV', 'Martinsburg, WV',
                                                                                np.where(df['Location'] == 'PathWell Health - VA', 'Winchester, VA',
                                                                                         np.where(df['Location'] == 'PathWell Health - VA Countryside', 'Sterling, VA',
                                                                                                  np.where(df['Location'] == 'PathWell Health - VA Hillside', 'Hillside Hospice',
                                                                                                           np.where(df['Location'] == 'PathWell Health - VA Hospice', 'Hillside Hospice',
                                                                                                                    'Fairfield, CT'))))))))))
                                                                                         
                                                                        
        else:
            df['Agency'] = 'Fairfield, CT'
        return df
    

    def remove_location_column(df):
        if 'Location' in df.columns:
            df.drop('Location', axis=1, inplace=True)
        return df

    # File Upload
    file = st.file_uploader("Upload file", type=["xlsx", "xls", "csv"])
    if file is not None:
        df = read_file(file)
        df = add_agency_by_location(df)
        df = remove_location_column(df)
        df = df.rename(columns={'Job Type':'Department', 'Agency':'Location', 'B) FT/PD/PRN':'B) FT/Part Time/Per Diem'})
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
            
            # Convert to CSV format
            csv_data = BytesIO()
            if file_extension == 'xlsx' or file_extension == 'xls':
                df.to_csv(csv_data, index=False, encoding='utf-8')
                csv_file_extension = 'csv'
            elif file_extension == 'csv':
                csv_data = excel_data
                csv_file_extension = file_extension
            else:
                st.warning("Unsupported file format. Unable to convert to CSV.")
                return
            
            csv_data.seek(0)
            b64_csv = base64.b64encode(csv_data.read()).decode()
            
            today = date.today().strftime("%Y-%m-%d")
            file_name = os.path.splitext(file.name)[0]

            href_csv = f'<a href="data:application/octet-stream;base64,{b64_csv}" download="{today}_{file_name}.{csv_file_extension}">Download Updated Data (CSV)</a>'
            st.markdown(href_csv, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
