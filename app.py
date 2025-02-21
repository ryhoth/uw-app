import streamlit as st

def main():
    st.title("Commercial Multifamily Underwriting")
    st.write("Welcome to your web-based underwriting tool!")
    
    # Basic File Upload
    uploaded_file = st.file_uploader("Upload your Excel underwriting model", type=["xlsm", "xlsx"])
    if uploaded_file:
        st.success("File uploaded successfully! More features coming soon.")

if __name__ == "__main__":
    main()
