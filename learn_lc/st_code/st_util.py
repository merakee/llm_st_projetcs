# pyhton


# local
from app_managers.auth_manager import DeploymentManager
from app_managers.auth_manager import AuthManager


# langchain


# implementation

class STUtil:
    def __init__(self) -> None:
        pass

    @staticmethod
    def show_debug_option():
        return not DeploymentManager().is_prod()

    def is_api_key_valid(api_key):
        return AuthManager.is_key_format_valid(api_key)

    # def st_save_uploadedfile(uploadedfile):
    #     with open(os.path.join("/tmp", uploadedfile.name), "wb") as f:
    #         f.write(uploadedfile.getbuffer())
    #     return True

    # def save_file(uploadedfile):
    #     if llmh.SystemHelper.st_save_uploadedfile(uploadedfile):
    #         return st.success(f"Saved File: {uploadedfile.name} to '\\tmp'")
