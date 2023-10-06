import streamlit as st
import lang_chain_helper as llmh

# Settings
PAGE_TITLE = "LLM Demo"
PAGE_ICON = ":robot_face:"
LAYOUT = "centered"

# page config


# def set_cumsom_settings():
#     hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def set_page(page_title=PAGE_TITLE,
             page_icon=PAGE_ICON, layout=LAYOUT):
    st.set_page_config(page_title=PAGE_TITLE,
                       page_icon=PAGE_ICON, layout=LAYOUT)
    # hide_streamlit_style = """
    #         <style>
    #         /* #MainMenu {visibility: hidden;} */
    #         footer {visibility: hidden;}
    #         </style>
    #         """
    # st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Header
def set_header(title=None, subheader=None):
    with st.container():
        if title:
            st.title(title)
        if subheader:
            st.subheader(subheader)
        # st.divider()
        if not "is_debug_on" in st.session_state:
            st.session_state["is_debug_on"] = False
        if st.session_state["is_debug_on"]:
            st.write("Debug info:")
            st.write(st.session_state)


def clear_api_key():
    st.write("button clicked")
    if "openai_api_key" in st.session_state:
        del st.session_state.openai_api_key

# side bar


def set_side_bar():
    with st.sidebar:
        if "openai_api_key" in st.session_state:
            button_key = st.button("Clear OpenAI Api Key", type="primary")
            st.checkbox('Run LLM', key="is_run_llm_on")
            if button_key:
                del st.session_state.openai_api_key
        else:
            openai_api_key = st.sidebar.text_input(
                "OpenAI API Key", type="password")
            # check if valid
            if openai_api_key:
                if llmh.LlmHelper.is_key_valid(openai_api_key):
                    st.session_state["openai_api_key"] = openai_api_key
                else:
                    # clear_api_key()
                    st.warning(
                        'Not valid OpenAI API key! Please enter again.', icon='⚠')

        st.checkbox('Debug', key="is_debug_on")


# # Body
# with st.container():
#     lc, rc = st.columns(2)
#     with lc:
#         st.write('Col 1')
#     with rc:
#         st.write('Col 2')


# # footer
# with st.container():
#     st.write('Footer')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
