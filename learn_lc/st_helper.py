import streamlit as st
import lang_chain_helper as llmh

# Settings
PAGE_TITLE = "LLM Demo"
PAGE_ICON = ":robot_face:"
LAYOUT = "centered"
MENU_ON = True
DEPLOY_ON = False
FOOTER_ON = False

# page config


# def set_cumsom_settings():
#     hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def set_custom_settings(menu_on=True, deploy_on=False, footer_on=False):
    hide_streamlit_style = "<style>"
    if not menu_on:
        hide_streamlit_style += """
        #MainMenu {visibility: hidden;}
        """
    if not deploy_on:
        hide_streamlit_style += """
        .stDeployButton {visibility: hidden;}
        """
    if not footer_on:
        hide_streamlit_style += """
        footer {visibility: hidden;}
        """
    hide_streamlit_style += """
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def set_page(page_title=PAGE_TITLE,
             page_icon=PAGE_ICON, layout=LAYOUT):
    st.set_page_config(page_title=PAGE_TITLE,
                       page_icon=PAGE_ICON, layout=LAYOUT)
    set_custom_settings(
        menu_on=MENU_ON, deploy_on=DEPLOY_ON, footer_on=FOOTER_ON)


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


def set_clear_button(api_container):
    with api_container.container():
        st.write("OpenAI Api Key Set")
        button_key = st.button(
            "Clear OpenAI Api Key", type="primary")
        st.checkbox('Run LLM', key="is_run_llm_on")
    return button_key


def set_side_bar():
    with st.sidebar:
        api_container = st.empty()

        if "openai_api_key" not in st.session_state:
            openai_api_key = api_container.text_input(
                "OpenAI API Key", type="password")
            # check if valid
            if openai_api_key:
                if llmh.LlmHelper.is_key_valid(openai_api_key):
                    st.session_state["openai_api_key"] = openai_api_key
                    set_clear_button(api_container=api_container)
                else:
                    # clear_api_key()
                    st.error(
                        ' Not a valid OpenAI API key! Please enter again.', icon='⛔️')

        else:
            button_key = set_clear_button(api_container=api_container)
            if button_key:
                del st.session_state.openai_api_key
                api_container.text_input("OpenAI API Key", type="password")

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
