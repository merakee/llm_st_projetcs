import streamlit as st
from st_code.st_base import STBase
from page_managers.dq_page_manager import DQPageManager, DQSessionKeys, DQSettings


# def update_settings(dqui_key):
#     value = st.session_state[dqui_key]
#     DQPageManager.update_settings(dqui_key, value)


# page config
STBase.set_page()
# Header
STBase.set_header(title="Document Query",
                  subheader="Upload txt document(s) and query the content")

# side bar
STBase.set_side_bar()

# set file list
DQPageManager.initialize_page()

uploader_container = st.empty()
file_info_container = st.empty()
embedding_options_container = st.empty()
embedding_info_container = st.empty()
query_container = st.empty()

if DQPageManager.display_file_uploader():
    with uploader_container.container():
        uploaded_files = st.file_uploader(
            "Upload txt file(s)", type="txt", accept_multiple_files=True)
    documents = DQPageManager.update_file_info(uploaded_files)

if DQPageManager.display_file_information():
    with file_info_container.container():
        file_info = DQPageManager.get_value_for_key(DQSessionKeys.dq_file_list)
        text = f"{len(file_info)} file(s) uploaded:"
        for info in file_info:
            text += f" {info['name']}  ({round(info['size']/1024)}kB ),"
        st.info(text[:-1])

if DQPageManager.display_file_process_options():
    with embedding_options_container.container():
        chunk_size = st.slider("Chunk Size",
                               min_value=DQSettings.Embeddings.chunk_size_min,
                               max_value=DQSettings.Embeddings.chunk_size_max,
                               step=DQSettings.Embeddings.chunk_size_step,
                               value=DQSettings.Embeddings.chunk_size_default,
                               key=DQSettings.Embeddings.chunk_size_key)
        chunk_overlap = st.slider("Chunk overlap (%)",
                                  min_value=DQSettings.Embeddings.chunk_overlap_min,
                                  max_value=DQSettings.Embeddings.chunk_overlap_max,
                                  step=DQSettings.Embeddings.chunk_overlap_step,
                                  value=DQSettings.Embeddings.chunk_overlap_default,
                                  key=DQSettings.Embeddings.chunk_overlap_key)
        embedding_type = st.selectbox('Select embedding type',
                                      (DQSettings.Embeddings.embedding_types),
                                      index=DQSettings.Embeddings.embedding_types.index(
                                          DQSettings.Embeddings.embedding_type_default.name),
                                      key=DQSettings.Embeddings.embedding_type_key)

        # DQPageManager.update_embedding_settings(
        #     chunk_size=chunk_size, chunk_overlap=chunk_overlap, embedding_type=embedding_type)
        pf_button = st.button("Process File(s)",
                              type="primary")
        if pf_button:
            with st.spinner("waiting"):
                DQPageManager.create_db(documents=documents)

if DQPageManager.display_query():
    uploader_container.empty()
    embedding_options_container.empty()
    with embedding_info_container.container():
        # embedding_settings = DQPageManager.get_value_for_key(
        #     DQSessionKeys.dq_embedding_settings)
        db_size = DQPageManager.get_vdb_size()
        text = f"Embedding type: {DQPageManager.get_value_for_key(DQSettings.Embeddings.embedding_type_key,is_raw=True)},"
        text += f"Chunk Size: {DQPageManager.get_value_for_key(DQSettings.Embeddings.chunk_size_key,is_raw=True)},"
        text += f"Chunk overlap: {DQPageManager.get_value_for_key(DQSettings.Embeddings.chunk_overlap_key,is_raw=True)}%,"
        if db_size:
            text += f"Total embeddings: {db_size[0]}, "
            text += f"Embddings size:   {db_size[1]}."
        else:
            text += f"No embedding stored"

        st.info(text)

    with query_container.container():
        st.selectbox('Select search type',
                     (DQSettings.Retriever.search_types),
                     index=DQSettings.Retriever.search_types.index(
                         DQSettings.Retriever.search_type_default),
                     key=DQSettings.Retriever.search_type_key)
        st.slider("Max match", min_value=DQSettings.Retriever.max_match_min,
                  max_value=DQSettings.Retriever.max_match_max,
                  step=DQSettings.Retriever.max_match_step,
                  value=DQSettings.Retriever.max_match_default,
                  key=DQSettings.Retriever.max_match_key)
        st.checkbox('Cite source', value=DQSettings.LLMResponse.cite_source_default,
                    key=DQSettings.LLMResponse.cite_source_key)

        with st.form('query_form'):
            query = st.text_area(
                'Enter query:')
            submitted = st.form_submit_button(
                'Submit')  # , type='primary')  # , on_click=run_llm, args=[text])
        if submitted:
            st.session_state[DQSessionKeys.dq_query_text.name] = query
            with st.spinner("waiting"):
                prompt, response, sources = DQPageManager.get_llm_response()
                st.write("Question")
                st.info(prompt)
                st.write("Answer")
                st.info(response)
                if sources:
                    for ind, source in enumerate(sources):
                        st.write(
                            f"\n{ind}. {source.metadata['name']} ************")
                        st.info(source.page_content)

    start_over = st.button("Start Over",
                           type="primary")  # , on_click=DQPageManager.start_over())
    if start_over:
        DQPageManager.start_over()
        # file_info_container.empty()
        # embedding_options_container.empty()
        # embedding_info_container.empty()
        # query_container.empty()
        st.rerun()


#                 st.write(get_splitter_settings())
#                 st.write(get_embedding_settings())

#         # if not st.session_state.done_upload:
#         #     with done_upload_container:
#         #         st.button("Done File Upload",
#         #                   type="primary", on_click=done_upload, args=[True])

#         # st.write(documents)
#         if pf_button:
#             with st.spinner("waiting"):
#                 st.session_state.vectordb = create_db(documents)

#     if DQPageManager.display_file_processing_information():
#         st.write(get_uploaded_files_info())

#     # if st.session_state.app_state == "create_db":
#     #     with st.spinner("waiting"):
#     #         create_db()

#     if DQPageManager.display_query_window_with_options():
#         # upload_files_container.empty()
#         # # with llm_container:
#         # st.slider("Search_type", min_value=200, max_value=8000,
#         #           step=200, value=st.session_state.splitter_setting["chunk_size"],
#         #           key="slider_chunk_size", on_change=update_splitter_settings)
#         st.slider("Max match", min_value=1, max_value=10,
#                   step=1, value=st.session_state.qa_setting["max_match"],
#                   key="slider_max_match", on_change=update_qa_settings)
#         st.checkbox('Cite source', key="llm_cite_sourse")

#         if DQPageManager.display_query_settings_information():
#             st.write(get_uploaded_files_info())

#         with st.form('query_form'):
#             text = st.text_area(
#                 'Enter query:')
#             submitted = st.form_submit_button(
#                 'Submit', type='primary')  # , on_click=run_llm, args=[text])
#         if submitted:  # st.session_state.app_state == "run_llm":
#             # st.session_state.app_state = "db_ready"
#             st.session_state.q_text = text
#             with st.spinner("waiting"):
#                 get_llm_response(query=st.session_state.q_text,
#                                  vectordb=st.session_state.vectordb)
#                 # st.write("Question")
#                 # st.info(st.session_state.q_text)
#                 # st.write("Answer")
#                 # st.info(response)
#         st.button("Start Over",
#                   type="primary", on_click=start_over)
