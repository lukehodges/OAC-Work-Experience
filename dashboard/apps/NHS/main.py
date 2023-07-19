import streamlit as st

from streamlit import session_state as state

def main():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.selectbox(options=["one","two"], label=""
                     )
        st.text("here")
    with col2:
        st.text("here")