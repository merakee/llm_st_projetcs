import streamlit as st
import st_helper as sth
import lang_chain_helper as llmh
# page config
sth.set_page()
# Header
sth.set_header(title="Ask a question")


# side bar
sth.set_side_bar()

with st.form('my_form'):
    text = st.text_area(
        'Enter text:', 'What is the most populated city?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        run_llm = "is_run_llm_on" in st.session_state and st.session_state.is_run_llm_on
        if "openai_api_key" in st.session_state:
            with st.spinner("waiting"):
                prompt, response = llmh.AskQuestion.get_response(
                    prompt=text, api_key=st.session_state.openai_api_key, run_llm=run_llm)
        else:
            prompt = text
            response = "No API key set. LLM not run."
        st.write("Prompt:")
        st.info(prompt)
        st.write("AI Response:")
        st.info(response)
