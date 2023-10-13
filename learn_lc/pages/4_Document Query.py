import streamlit as st
from st_code.st_base import STBase
import lc_code.lang_chain_helper as llmh


# page config
STBase.set_page()
# Header
STBase.set_header(title="Document Query",
                  subheader="Upload txt document(s) and query the content")

# side bar
STBase.set_side_bar()

# set file list


def initialize_page():
    if 'file_list' not in st.session_state:
        st.session_state.file_list = []
    if 'app_state' not in st.session_state:
        st.session_state.app_state = "upload"
    if "splitter_setting" not in st.session_state:
        st.session_state.splitter_setting = {"chunk_size": 100,
                                             "chunk_overlap": 10}
    if "embedding_setting" not in st.session_state:
        st.session_state.embedding_setting = {"embedding_size": 732,
                                              "total_embeddings": 200}

    if "qa_setting" not in st.session_state:
        st.session_state.qa_setting = {'search_type': 'similarity',
                                       "max_match": 3}
    if "llm_cite_soruce" not in st.session_state:
        st.session_state.llm_cite_source = False

    if 'vectordb' not in st.session_state:
        st.session_state.vectordb = None

    if 'q_text' not in st.session_state:
        st.session_state.q_text = ""


def start_over():
    st.session_state.app_state = "upload"


def file_uploaded():
    st.session_state.app_state = "process_file"


def process_file():
    st.session_state.app_state = "create_db"


def update_splitter_settings():
    st.session_state.splitter_setting = {"chunk_size": st.session_state.slider_chunk_size,
                                         "chunk_overlap": st.session_state.slider_chunk_overlap}


def update_qa_settings():
    # st.session_state.qa_setting = {"serach_type": st.session_state.slider_search_type,
    #                                      "max_match": st.session_state.slider_max_match}
    st.session_state.qa_setting['max_match'] = st.session_state.slider_max_match


def create_db(documents):
    # texts = llmh.DocumentQuery.get_texts_from_documents(
    #     documents=documents,
    #     chunk_size=st.session_state.splitter_setting["chunk_size"],
    #     chunk_overlap_per=st.session_state.splitter_setting["chunk_overlap"]
    # )
    vectordb, total_embeddings = llmh.DocumentQuery.create_vdb(
        documents=documents,
        chunk_size=st.session_state.splitter_setting["chunk_size"],
        chunk_overlap_per=st.session_state.splitter_setting["chunk_overlap"]
    )

    # st.write(texts)
    st.session_state.embedding_setting['total_embeddings'] = total_embeddings
    st.session_state.app_state = "db_ready"
    return vectordb


def run_llm(text):
    st.session_state.app_state = "run_llm"
    st.session_state.q_text = text


def get_uploaded_files_info():
    text = "Uploaded files: "
    for info in st.session_state.file_list:
        text += f" {info['name']} ({info['size']}),"
    text = text[:-1]
    return text


def get_splitter_settings():
    text = "Text Splitter:\n"
    text += f"Chunk size: {st.session_state.splitter_setting['chunk_size']}, Chunk overlap: {st.session_state.splitter_setting['chunk_overlap']}%"
    return text


def get_embedding_settings():
    text = "Embedding:\n"
    text += f"Embedding size: {st.session_state.embedding_setting['embedding_size']}, Total embeddings: {st.session_state.embedding_setting['total_embeddings']}"
    return text


def get_qa_settings():
    text = "QA Settings:\n"
    text += f"Search type:{st.session_state.qa_setting['search_type']}, "
    text += f"Max match: {st.session_state.qa_setting['max_match']}, "
    text += f"Cite Soruce: {st.session_state.qa_setting['cite_source']}"
    return text


def get_api_key():
    if llmh.SystemHelper.is_production():
        # in production
        if "openai_api_key" in st.session_state:
            return st.session_state.openai_api_key
        else:
            return None
    else:
        # in dev and test and the rest
        api_key = llmh.LlmHelper.get_local_api_key()
        return api_key


def format_response(response):
    # print(response)
    st.subheader("Question")
    st.info(st.session_state.q_text)
    st.subheader("Answer")
    if response:
        st.info(response['result'])
        if st.session_state.llm_cite_sourse:
            st.subheader('\n\nSources:')
            ind = 1
            for source in response["source_documents"]:
                # print(source.__class__)
                st.success(f"{ind}. {source.metadata['name']}")
                st.info(source.page_content)
                ind += 1
    else:
        st.warning("LLM not run")


def get_llm_response(query, vectordb):
    response = {}
    if not vectordb:
        response['result'] = "No vecotor db set"
    else:
        api_key = get_api_key()
        if api_key:
            search_type = st.session_state.qa_setting["search_type"]
            max_match = st.session_state.qa_setting["max_match"]
            response = llmh.DocumentQuery.get_llm_response(
                query=query, vectoredb=vectordb, api_key=api_key, search_type=search_type, max_count=max_match)
        else:
            response['result'] = "No API key set. LLM not run."

    format_response(response)


initialize_page()

with st.container():
    # upload_files_container = st.empty()
    # file_container = st.empty()
    # process_file_container = st.empty()
    # query_container = st.empty()
    # process_llm_container = st.empty()
    # llm_container = st.empty()
    if st.session_state.app_state in ["upload", "process_file"]:
        uploaded_files = st.file_uploader(
            "Upload txt file(s)", type="txt", accept_multiple_files=True, on_change=file_uploaded)
        # file_list = st.session_state.file_list
        documents = []
        for upoaded_file in uploaded_files:
            # st.write(upoaded_file)
            file_text = str(upoaded_file.read(), "utf-8")
            file_info = {'name': upoaded_file.name,
                         'size': upoaded_file.size, "type": upoaded_file.type}
            documents.append(llmh.DocumentQuery.document_from_text(
                text=file_text, info=file_info))
            st.session_state.file_list.append(file_info)
        # st.write(documents)
        # sth.save_file(uploadedfile=upoaded_file)

    if st.session_state.app_state != "upload":
        with st.container():
            st.write(get_uploaded_files_info())
            if st.session_state.app_state in ["process_file", "create_db", "db_ready"]:
                st.write(get_splitter_settings())
                st.write(get_embedding_settings())

        # if not st.session_state.done_upload:
        #     with done_upload_container:
        #         st.button("Done File Upload",
        #                   type="primary", on_click=done_upload, args=[True])
    if st.session_state.app_state == "process_file":
        st.slider("Chunk Size", min_value=100, max_value=4000,
                  step=100, value=st.session_state.splitter_setting["chunk_size"],
                  key="slider_chunk_size", on_change=update_splitter_settings)
        st.slider("Chunk overlap (%)", min_value=0, max_value=100,
                  step=5, value=st.session_state.splitter_setting["chunk_overlap"],
                  key="slider_chunk_overlap", on_change=update_splitter_settings)
        pf_button = st.button("Process File(s)",
                              type="primary")  # , on_click=process_file)
        # st.write(documents)
        if pf_button:
            with st.spinner("waiting"):
                st.session_state.vectordb = create_db(documents)

    # if st.session_state.app_state == "create_db":
    #     with st.spinner("waiting"):
    #         create_db()

    if st.session_state.app_state in ["db_ready"]:
        # upload_files_container.empty()
        # # with llm_container:
        # st.slider("Search_type", min_value=200, max_value=8000,
        #           step=200, value=st.session_state.splitter_setting["chunk_size"],
        #           key="slider_chunk_size", on_change=update_splitter_settings)
        st.slider("Max match", min_value=1, max_value=10,
                  step=1, value=st.session_state.qa_setting["max_match"],
                  key="slider_max_match", on_change=update_qa_settings)
        st.checkbox('Cite source', key="llm_cite_sourse")

        with st.form('query_form'):
            text = st.text_area(
                'Enter query:')
            submitted = st.form_submit_button(
                'Submit', type='primary')  # , on_click=run_llm, args=[text])
        if submitted:  # st.session_state.app_state == "run_llm":
            # st.session_state.app_state = "db_ready"
            st.session_state.q_text = text
            with st.spinner("waiting"):
                get_llm_response(query=st.session_state.q_text,
                                 vectordb=st.session_state.vectordb)
                # st.write("Question")
                # st.info(st.session_state.q_text)
                # st.write("Answer")
                # st.info(response)
        st.button("Start Over",
                  type="primary", on_click=start_over)
