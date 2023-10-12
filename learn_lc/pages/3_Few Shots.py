import streamlit as st
import st_helper as sth
import lang_chain_helper as llmh

# methods


def format_response(text):
    response = ""
    if not response:
        response = "LLM not called"
    return response


# page config
sth.set_page()
# Header
sth.set_header(title="LLM Exp", subheader="to be implemented")

# side bar
sth.set_side_bar()
