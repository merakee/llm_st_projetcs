import streamlit as st
from st_code.st_base import STBase
from lc_pages.lc_what_to_watch import LCWhatToWatch
from lc_pages.lc_what_to_watch import WTWSessionManager
from lc_pages.lc_what_to_watch import WTWSessionKeys

# page config
STBase.set_page()
# Header
STBase.set_header(title="What To Watch?")
# side bar
STBase.set_side_bar()

# body
with st.container():
    st.write("Template:")
    st.info(LCWhatToWatch.get_template())
    st.selectbox('What type of show?', LCWhatToWatch.get_type_list(), index=LCWhatToWatch.get_index_for_key(
        WTWSessionKeys.whattowatch_type), key=WTWSessionKeys.whattowatch_type.name)
    st.selectbox('What genre?', LCWhatToWatch.get_genre_list(),
                 index=LCWhatToWatch.get_index_for_key(
        WTWSessionKeys.whattowatch_genre), key=WTWSessionKeys.whattowatch_genre.name)
    st.slider('Number of suggestions', min_value=1,
              max_value=10, value=LCWhatToWatch.get_whattowatch_count(), key=WTWSessionKeys.whattowatch_count.name)
    button = st.button("Get suggestions:")
    if button:
        response, prompt = LCWhatToWatch.get_llm_response()
        st.write("Prompt:")
        st.info(prompt)
        st.write("AI Suggesions:")
        st.info(response)
