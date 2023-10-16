import streamlit as st
from st_code.st_base import STBase
from page_managers.wtw_page_manager import WTWPageManager, WTWSessionKeys

# page config
STBase.set_page()
# Header
STBase.set_header(title="What To Watch?")
# side bar
STBase.set_side_bar()

# body
with st.container():
    st.write("Template:")
    st.info(WTWPageManager.get_template())
    st.selectbox('What type of show?', WTWPageManager.get_type_list(), index=WTWPageManager.get_index_for_key(
        WTWSessionKeys.whattowatch_type), key=WTWSessionKeys.whattowatch_type.name)
    st.selectbox('What genre?', WTWPageManager.get_genre_list(),
                 index=WTWPageManager.get_index_for_key(
        WTWSessionKeys.whattowatch_genre), key=WTWSessionKeys.whattowatch_genre.name)
    st.slider('Number of suggestions', min_value=1,
              max_value=10, value=WTWPageManager.get_whattowatch_count(), key=WTWSessionKeys.whattowatch_count.name)
    button = st.button("Get suggestions:")
    if button:
        response, prompt = WTWPageManager.get_llm_response()
        st.write("Prompt:")
        st.info(prompt)
        st.write("AI Suggesions:")
        st.info(response)
