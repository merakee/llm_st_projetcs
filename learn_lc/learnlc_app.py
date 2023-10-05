import streamlit as st
import learnlc_llm as llmh

# Settings
PAGE_TITLE = "LLM Demo"
PAGE_ICON = ":robot_face:"
LAYOUT = "centered"

# page config
st.set_page_config(page_title=PAGE_TITLE,
                   page_icon=PAGE_ICON, layout=LAYOUT)

# Header
with st.container():
    st.title("LLM  App")
    st.subheader("for experiments")


# Body
with st.container():
    lc, rc = st.columns(2)
    with lc:
        st.write('Col 1')
    with rc:
        st.write('Col 2')


# footer
with st.container():
    st.write('Footer')
