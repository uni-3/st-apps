import streamlit as st
import base64
import os


def upload_pdf_file():
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

    return uploaded_file

def display_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_contents = uploaded_file.read()
        st.pdf(pdf_contents, height="stretch")

def main():
    st.title("pdf viewer")
    file = upload_pdf_file()

    if file is not None:
        display_pdf(file)

main()
