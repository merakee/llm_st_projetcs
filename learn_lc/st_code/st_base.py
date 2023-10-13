import streamlit as st
from st_code.st_util import STUtil
from st_code.st_session_manager import STSessionManager
from st_code.st_session_manager import STSessionKeys


# Settings
PAGE_TITLE = "LLM Demo"
PAGE_ICON = ":robot_face:"
LAYOUT = "centered"
MENU_ON = True
DEPLOY_ON = False
FOOTER_ON = False


class STBase:
    def __init__(self) -> None:
        pass

    @staticmethod
    def selected_api():
        return STSessionManager.get_value_for_key(STSessionKeys.selected_api)

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
        STBase.set_custom_settings(
            menu_on=MENU_ON, deploy_on=DEPLOY_ON, footer_on=FOOTER_ON)

    # Header

    def set_header(title=None, subheader=None):
        with st.container():
            if title:
                st.title(title)
            if subheader:
                st.subheader(subheader)
            # st.divider()
            if STSessionManager.is_debug_on():
                st.write("Debug info:")
                st.write(st.session_state)

    def set_clear_button(container):
        with container.container():
            st.write(f"{STBase.selected_api()} Api Key Set")
            button_key = st.button(
                f"Clear {STBase.selected_api()} Api Key", type="primary")
            st.checkbox('Run LLM', value=STSessionManager.get_value_for_key(
                STSessionKeys.is_run_llm_on), key=STSessionKeys.is_run_llm_on.name)
        return button_key

    def set_side_bar():
        with st.sidebar:
            st.selectbox('Select LLM API to use',
                         (STSessionManager.get_api_options()), index=STSessionManager.get_selected_api_index(),
                         key=STSessionKeys.selected_api.name)

            api_key_container = st.empty()
            if not STSessionManager.is_api_key_set():
                api_key = api_key_container.text_input(
                    f"Enter {STBase.selected_api()} API Key", type="password")
                # check if valid
                if api_key:
                    if STSessionManager.set_api_key(api_key):
                        # clear_api_key()
                        STBase.set_clear_button(
                            container=api_key_container)
                    else:
                        st.error(
                            f"Not a valid {STBase.selected_api()} API key! Please enter again.", icon='⛔️')

            else:
                button_key = STBase.set_clear_button(
                    container=api_key_container)
                if button_key:
                    STSessionManager.clear_api_key()
                    api_key_container.text_input(
                        f"Enter {STBase.selected_api()} API Key", type="password")
            if (STUtil.show_debug_option()):
                st.checkbox('Debug', value=STSessionManager.get_value_for_key(
                    STSessionKeys.is_debug_on), key=STSessionKeys.is_debug_on.name)


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
