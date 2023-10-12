# pyhton
import os
import re
from enum import Enum
from dotenv import load_dotenv

# local

# langchain


# implementation

load_dotenv()


class DeploymentType(Enum):
    DEV = 1
    TEST = 2
    PROD = 3
    NOT_SET = 4


class DeploymentManager:
    def __init__(self):
        self.env = os.getenv("DEPLOYMENT_ENV")
        if not self.env:
            self.env = DeploymentType.NOT_SET.name

    def is_prod(self):
        return self.env == DeploymentType.PROD.name

    def is_dev(self):
        return self.env == DeploymentType.DEV.name

    def is_test(self):
        return self.env == DeploymentType.TEST.name

    def is_dev_or_test(self):
        return self.is_dev() or self.is_test()

    def is_set(self):
        return self.env and self.env != DeploymentType.NOT_SET.name


class APIType(Enum):
    openai = 1
    huggingface = 2


class APIKey:
    def __init__(self, api_token, api_type, tag):
        self.api_token = api_token
        self.api_type = api_type
        self.tag = tag


class AuthManager:
    def __init__(self):
        self.api_key_store = {}

    def add_to_api_store(self, api_key):
        if api_key.tag in self.api_key_store:
            return False
        self.api_key_store[api_key.tag] = api_key
        return True

    def get_api_key_from_store(self, tag):
        if tag not in self.api_key_store:
            return None
        return self.api_key_store[tag]

    def update_api_key_in_store(self, api_key):
        if api_key.tag not in self.api_key_store:
            return False
        self.api_key_store[api_key.tag] = api_key
        return True

    def delete_api_key_from_store(self, api_key):
        if api_key.tag not in self.api_key_store:
            return False
        self.api_key_store.pop(api_key.tag)
        return True

    def get_local_api_key(api_type):
        if api_type == APIType.openai:
            api_key = os.getenv("OPENAI_API_KEY")
        elif type == APIType.huggingface:
            api_key = os.getenv("HFHUB_API_KEY")
        else:
            api_key = None

        return api_key

    def is_key_format_valid(api_key):
        if api_key.api_type == APIType.openai:
            # match: sk-[20 characters]T3BlbkFJ[20 characters].
            return bool(re.fullmatch(r"sk-[^_\\w]{20}T3BlbkFJ[^_\\w]{20}", api_key.api_token))
        if api_key.api_type == APIType.huggingface:
            # match: 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
            return bool(re.fullmatch(r"hf_[a-zA-Z]{34}", api_key.api_token))
