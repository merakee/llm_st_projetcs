# pyhton
from enum import Enum

# local
from st_code.st_util import STUtil
from lc_code.auth_manager import APIKey
from lc_code.auth_manager import APIType

# ST
import streamlit as st

# langchain


# implementation
class STSessionKeys(Enum):
    is_debug_on = 1
    selected_api = 2
    is_run_llm_on = 3
    openai_api_key = 4
    huggingface_api_key = 5
    openai_llm_manager = 6
    huggingface_llm_manager = 7


class STSessionManager:
    def __init__(self) -> None:
        pass

    @staticmethod
    def set_key(session_key, value):
        if session_key in [STSessionKeys.openai_api_key or STSessionKeys.huggingface_api_key]:
            return STSessionManager.set_api_key(value=value, session_key=session_key)
        st.session_state[session_key.name] = value
        return True

    def set_api_key(value, session_key=None):
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if session_key == STSessionKeys.openai_api_key or selected_api == APIType.OpenAI.name:
            api_key = APIKey(api_token=value,
                             api_type=APIType.OpenAI, tag="openai_llm")
            if not STUtil.is_api_key_valid(api_key):
                return False
            st.session_state[STSessionKeys.openai_api_key.name] = api_key
            return True
        elif session_key == STSessionKeys.huggingface_api_key or selected_api == APIType.HuggingFace.name:
            api_key = APIKey(api_token=value,
                             api_type=APIType.HuggingFace, tag="huggingface_llm")
            if not STUtil.is_api_key_valid(api_key):
                return False
            st.session_state[STSessionKeys.huggingface_api_key.name] = api_key
            return True

    def get_value_for_key(session_key):
        if not STSessionManager.is_key_set(session_key):
            return None
        return st.session_state[session_key.name]

    def get_api_key():
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI.name:
            return STSessionManager.get_value_for_key(STSessionKeys.openai_api_key)
        elif selected_api == APIType.HuggingFace.name:
            return STSessionManager.get_value_for_key(STSessionKeys.huggingface_api_key)
        return None

    def get_llm_manager():
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI.name:
            return STSessionManager.get_value_for_key(STSessionKeys.openai_llm_manager)
        elif selected_api == APIType.HuggingFace.name:
            return STSessionManager.get_value_for_key(STSessionKeys.huggingface_llm_manager)
        return None

    def clear_key(session_key, delete_key=False):
        if session_key == STSessionKeys.openai_api_key:
            st.session_state[STSessionKeys.openai_llm_manager.name] = None
            if delete_key:
                del st.session_state[STSessionKeys.openai_llm_manager.name]
        if session_key == STSessionKeys.huggingface_api_key:
            st.session_state[STSessionKeys.huggingface_llm_manager.name] = None
            if delete_key:
                del st.session_state[STSessionKeys.huggingface_llm_manager.name]

        if session_key.name in st.session_state:
            st.session_state[session_key.name] = None
            if delete_key:
                del st.session_state[session_key.name]

    def clear_api_key():
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI.name:
            STSessionManager.clear_key(STSessionKeys.openai_api_key)
        elif selected_api == APIType.HuggingFace.name:
            STSessionManager.clear_key(STSessionKeys.huggingface_api_key)

    def is_key_set(session_key):
        return session_key.name in st.session_state and st.session_state[session_key.name] is not None

    def is_api_key_set():
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI.name:
            return STSessionManager.is_key_set(STSessionKeys.openai_api_key)
        elif selected_api == APIType.HuggingFace.name:
            return STSessionManager.is_key_set(STSessionKeys.huggingface_api_key)
        return False

    def is_debug_on():
        return (STSessionKeys.is_debug_on.name in st.session_state) and (st.session_state[STSessionKeys.is_debug_on.name] == True)

    def llm_ready_to_run():
        return STSessionKeys.is_run_llm_on.name in st.session_state and st.session_state[
            STSessionKeys.is_run_llm_on.name]

    def get_api_options():
        return [APIType.OpenAI.name, APIType.HuggingFace.name]

    def get_selected_api_index():
        if not STSessionManager.is_key_set(STSessionKeys.selected_api):
            STSessionManager.set_key(
                STSessionKeys.selected_api, APIType.OpenAI.name)
        return STSessionManager.get_api_options().index(STSessionManager.get_value_for_key(STSessionKeys.selected_api))

    def is_llm_manager_set():
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI:
            return STSessionManager.is_key_set(STSessionKeys.openai_llm_manager)
        if selected_api == APIType.HuggingFace:
            return STSessionManager.is_key_set(STSessionKeys.huggingface_llm_manager)
        return False

    def set_llm_manager(llm_manager):
        selected_api = STSessionManager.get_value_for_key(
            STSessionKeys.selected_api)
        if selected_api == APIType.OpenAI.name:
            STSessionManager.set_key(
                STSessionKeys.openai_llm_manager, llm_manager)
        if selected_api == APIType.HuggingFace.name:
            STSessionManager.set_key(
                STSessionKeys.huggingface_llm_manager, llm_manager)
