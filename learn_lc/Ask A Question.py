# pyhton

# ST
import streamlit as st

# local
from st_code.st_base import STBase
from page_managers.aq_page_manager import AQPageManager

# implementation
#


# page config
STBase.set_page()
# Header
STBase.set_header(title="Ask a question")


# side bar
STBase.set_side_bar()

with st.form('ask_a_quesion_form'):
    prompt = st.text_area(
        'Enter text:', 'What is the most populated city?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner("waiting"):
            response = AQPageManager.get_llm_response(prompt=prompt)[0]
        st.write("Prompt:")
        st.info(prompt)
        st.write("AI Response:")
        st.info(response)
