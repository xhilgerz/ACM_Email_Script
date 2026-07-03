import streamlit as st
import numpy as np
from Interface.ACM_Email_Interface import ACM_User_Interface
from Interface.Test_User_Interface import Test_User_Interface



def main():
    
    st.title("ACM Email Script")
    
    set_up_gui()
    st.button("Generate Scripts", on_click=generate_file_clicked)
    st.button("Generate Heatmaps", on_click=heatmap_button_clicked)

    st.button("Script", on_click=script_dialog)




def set_up_gui():

    
    if "file" not in st.session_state:
        uploaded_file = st.file_uploader(
            label="Upload CSV", 
            type="csv", 
            accept_multiple_files=False,
            key="file_uploader"  # explicit unique key
        )
        if uploaded_file is not None:
            st.session_state.file = uploaded_file
    else:
        st.success(f"File uploaded: {st.session_state.file.name}")
        if st.button("Upload different file"):
            del st.session_state.file

def generate_file_clicked():
    if "file" not in st.session_state:
        st.warning("Please upload a file first")
        return
    
    Test_User_Interface.post_sign_up_csv(st.session_state.file.name)
    

    pass

def heatmap_button_clicked():
    if "file" not in st.session_state:
        st.warning("Please upload a file first")
        return

    print("heatmap button clicked")
    df = Test_User_Interface.get_heatmap_df(st.session_state.file)
    st.dataframe(df, use_container_width=True)

@st.dialog("Script",dismissible=False)
def script_dialog():
    if "script" not in st.session_state:
        st.session_state.script = "This is a text script for testing....."
    
    st.text_input("Edit Script", value=st.session_state.script, key="script_input")
    
    if st.button("Save"):
        st.session_state.script = st.session_state.script_input 
        st.rerun()