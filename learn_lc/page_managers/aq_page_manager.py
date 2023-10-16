# pyhton


# local
from st_code.st_session_manager import STSessionManager
from app_managers.llm_manager import LLMManager

# langchain


# implementation
class AQPageManager:
    @staticmethod
    def get_llm_response(prompt):
        # check if api_keyis set
        if not STSessionManager.is_api_key_set():
            response = "API Key not set. LLM not run"
            return response, prompt
        # check if run llm is set
        if not STSessionManager.llm_ready_to_run():
            response = "I am not real LLM. Check the \" Run LLM\" option to run LLM"
            return response, prompt

        if not STSessionManager.is_llm_manager_set():
            # print(STSessionManager.get_api_key())
            llm = LLMManager.get_llm(STSessionManager.get_api_key())
            # print(llm)
            llm_manager = LLMManager(llm)
            STSessionManager.set_llm_manager(llm_manager)

        llm_manager = STSessionManager.get_llm_manager()
        try:
            response = llm_manager.llm(prompt)
        except Exception as e:
            response = e

        return response, prompt
