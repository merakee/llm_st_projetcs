# pyhton
import os


# local


# langchain


# implementation


def st_save_uploadedfile(uploadedfile):
    with open(os.path.join("/tmp", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return True
