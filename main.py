import streamlit as st

from dashboard import apps, components
from dashboard.utils.page import page_group

def main():
    page = page_group("p")

    with st.sidebar:
        st.title("Calculation Gallery")

        with st.expander("✨ APPS", True):
            page.item("Streamlit gallery", apps.gallery, default=True)
            page.item("Mortgage Calculator", apps.mortgage)
        with st.expander("🧩 COMPONENTS", True):
            page.item("Ace editor", components.ace_editor)
            page.item("Disqus", components.disqus)
            page.item("Elements⭐", components.elements)
            page.item("Pandas profiling", components.pandas_profiling)
            page.item("Quill editor", components.quill_editor)
            page.item("React player", components.react_player)

    page.show()

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="🎈", layout="wide")
    main()