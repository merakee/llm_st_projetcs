import streamlit as st
import st_helper as sth
import lang_chain_helper as llmh

# page config
sth.set_page()
# Header
sth.set_header(title="What To Watch?")
# side bar
sth.set_side_bar()

# body
with st.container():
    st.write("Template:")
    st.info(llmh.WhatToWatch.get_template())
    st.selectbox('What type of show?', ('TV Show', 'Movie',
                 'TV Show or Movie'), key="whattowatch_type")
    st.selectbox('What genre?', ('Drama', 'Comedy', 'Action', 'Documentary', 'Reality TV', 'Sci-fi', 'Crime', 'Animation', 'Game Show'),
                 key="whattowatch_genre")
    st.slider('Number of suggestions', 1,
              10, 3, key="whattowatch_count")
    button = st.button("Get suggestions:")
    if button:
        run_llm = "is_run_llm_on" in st.session_state and st.session_state.is_run_llm_on
        prompt = llmh.WhatToWatch.get_prompt(count=st.session_state.whattowatch_count, type=st.session_state.whattowatch_type,
                                             genre=st.session_state.whattowatch_genre)
        if "openai_api_key" in st.session_state:
            with st.spinner("waiting"):
                response = llmh.WhatToWatch.get_response(prompt=prompt, api_key=st.session_state.openai_api_key,
                                                         run_llm=run_llm)
        else:
            response = "No API key set. LLM not run."
        st.write("Prompt:")
        st.info(prompt)
        st.write("AI Suggesions:")
        st.info(response)
