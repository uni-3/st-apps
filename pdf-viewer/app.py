import streamlit as st
import base64
import os


def upload_pdf_file():
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    if uploaded_file is None:
        st.write("Please upload a PDF file.")
    return uploaded_file

def display_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_contents = uploaded_file.read()
        pdf_base64 = base64.b64encode(pdf_contents).decode('utf-8')
        encoded_pdf = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="800" height="600" type="application/pdf">'
        st.markdown(encoded_pdf, unsafe_allow_html=True)

        return encoded_pdf
    else:
        st.write("No PDF file uploaded.")
        st.write(pdf_contents, unsafe_allow_html=True)


def prepare_default_file():
    default_file_path = "/path/to/default/file.pdf"  # Replace with the path to your default file
    if os.path.exists(default_file_path):
        default_file = open(default_file_path, "rb")
        return default_file
    else:
        return None

def main():
    file = upload_pdf_file()

    if file is not None:
        display_pdf(file)

main()
