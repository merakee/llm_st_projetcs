import os
import sys
import re
from dotenv import load_dotenv

# LLM
from langchain.llms import OpenAI
from langchain.llms.fake import FakeListLLM
from langchain.llms import HuggingFaceHub

# document loader
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

# splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embedding
# from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings

# Vector store
from langchain.vectorstores import Chroma

# Prompt
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

# Chain
# from langchain import hub
# , LLMMathChain, TransformChain, SequentialChain
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA

# local utility

load_dotenv()

# design steps
# 1. load a text document: size constraint
# 2. Chunk it with text splitter
# 3. Generate embegging
# 4. Store embedding in local store
# 5. Get quesitions
# 6. Retrive relevant vetors
# 7. Generate context
# 8. Create prompt
# 9. Get answer and display
# 10. Improve
#       1. List already uploaded files and ablity to pick
#       2. Show source docs
#       3. Interactive answers


class DocumentQuery():
    @staticmethod
    def get_documents(file_path=None, type="file"):
        # Load and process the text files
        if type == "file":
            if not file_path:
                file_path = "./testdata/singlefile/test_text.txt"
            loader = TextLoader(file_path)
        elif type == "dir":
            if not file_path:
                file_path = "./testdata/multiplefiles/"
            loader = DirectoryLoader(
                file_path, glob="./*.txt", loader_cls=TextLoader)
        else:
            raise NameError("Not a valid document type")

        documents = loader.load()
        return documents

    def document_from_text(text, info):
        doc = Document(page_content=text, metadata=info)
        return doc

    def get_texts(documents, chunk_size=1000, chunk_overlap_per=20):
        # splitting the text into
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=(chunk_overlap_per*chunk_size/100.0))
        texts = text_splitter.split_documents(documents)
        return texts

    def get_embedding_model(api_key=None, emb_model="huggingface"):
        if not api_key or emb_model == "huggingface":
            return DocumentQuery.get_hf_embedding_model()
        if api_key and emb_model == "openai":
            return OpenAIEmbeddings(openai_api_key=api_key)

        return None

    def get_hf_embedding_model():
        # MTEB English leaderboard  https://huggingface.co/spaces/mteb/leaderboard
        model_name = "hkunlp/instructor-large"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}
        iem = HuggingFaceInstructEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        return iem

    def get_embeddings(texts, api_key=None, emb_model="huggingface"):
        iem = DocumentQuery.get_embedding_model(
            api_key=api_key, emb_model=emb_model)
        embeddings = iem.embed_query(texts)
        return embeddings

    def get_vector_store(embedding, persist_directory='./vdb/chroma',  type="chroma"):
        # Embed and store the texts
        # Supplying a persist_directory will store the embeddings on disk
        vectordb = Chroma(persist_directory=persist_directory,
                          embedding_function=embedding)
        return vectordb

    def delete_vdb_dir(dir='./vdb/chroma/*'):
        os.system(f"rm -rf {dir}")

    def store_in_vector_store(texts, embedding, store_locally=True, persist_directory='./vdb/chroma',  type="chroma"):
        # Embed and store the texts
        # Supplying a persist_directory will store the embeddings on disk
        vectordb = Chroma.from_documents(documents=texts,
                                         embedding=embedding,
                                         persist_directory=persist_directory)
        if store_locally:
            vectordb.persist()
        vectordb = None
        return

    def create_vdb(documents, api_key=None, emb_model="huggingface", chunk_size=1000, chunk_overlap_per=20):
        texts = DocumentQuery.get_texts(
            documents=documents, chunk_size=chunk_size, chunk_overlap_per=chunk_overlap_per)
        embedding = DocumentQuery.get_embedding_model(
            api_key=api_key, emb_model=emb_model)
        vectordb = Chroma.from_documents(documents=texts,
                                         embedding=embedding)
        return vectordb, len(texts)

    def get_retriever(embedding, search_type="similarity", max_count=3):
        vectordb = DocumentQuery.get_vector_store(
            embedding=embedding)
        retriever = vectordb.as_retriever(
            search_kwargs={"k": max_count}, search_type=search_type)
        return retriever

    def get_chain(llm, retriever, chain_type="stuff", return_source_documents=True):
        # create the chain to answer questions
        qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                               chain_type=chain_type,
                                               retriever=retriever,
                                               return_source_documents=return_source_documents)
        return qa_chain

    def process_llm_response(llm_response, cite_sources=True):
        if cite_sources:
            print('\n\nSources:')
            ind = 1
            for source in llm_response["source_documents"]:
                print(f"\n{ind}. {source.metadata['source']} ************")
                print(source.page_content)
                ind += 1
        print(f"\n************\nQuery: {llm_response['query']}")
        print(f"\nResponse: {llm_response['result']}")

    def store_docs_in_db(file_path=None, type=None, api_key=None, emb_model="huggingface", chunk_size=1000, chunk_overlap_per=20):
        docs = DocumentQuery.get_documents(type=type)
        texts = DocumentQuery.get_texts(
            documents=docs, chunk_size=chunk_size, chunk_overlap_per=chunk_overlap_per)
        # print(len(texts))
        embedding = DocumentQuery.get_embedding_model(
            api_key=api_key, emb_model=emb_model)
        # print(len(embeddings))
        # print(texts)
        DocumentQuery.store_in_vector_store(
            texts=texts, embedding=embedding)

    def get_llm_response(llm, query, vectoredb, api_key, search_type="similarity", max_count=3):
        # llm = DocumentQuery.get_llm(api_key)
        retriever = vectoredb.as_retriever(
            search_kwargs={"k": max_count}, search_type=search_type)
        qa_chain = DocumentQuery.get_chain(llm=llm, retriever=retriever)
        llm_response = qa_chain(query)
        # DocumentQuery.process_llm_response(llm_response)
        return llm_response

    def test_hf_llm(api_token):
        question = "What is the best flour for pasta? "
        template = """Question: {question}
        Answer: Let's think step by step."""
        prompt = PromptTemplate(
            template=template, input_variables=["question"])

        # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
        llm = DocumentQuery.get_llm(api_token)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        answer = llm_chain.run(question)
        print(answer)
        return (answer)

    def test(llm, api_key, emb_model="huggingface", is_write=True, is_reset=False, run_prod=True):
        search_type = "similarity"  # mmr, similarity_score_threshold
        embedding = DocumentQuery.get_embedding_model(
            api_key=api_key, emb_model=emb_model)
        vectordb = DocumentQuery.get_vector_store(embedding=embedding)
        if is_reset:
            # print("Deleting Chroma colection: langchain")
            # vectordb.delete_collection()
            # print("Deleted Chroma colection: langchain")
            DocumentQuery.delete_vdb_dir()
        if is_write:
            documents = DocumentQuery.get_documents(type="dir")
            texts = DocumentQuery.get_texts(documents, chunk_size=1000)
            DocumentQuery.store_in_vector_store(
                texts=texts, embedding=embedding)
        # print(texts)
        query = "Which floor did Sue and Johnsy live?"
        query = "What is the size of the letter-box in the hall below?"
        response = DocumentQuery.get_llm_response(llm=llm,
                                                  query=query, vectoredb=vectordb, api_key=api_key, search_type=search_type, max_count=3)

        # print(response)

        DocumentQuery.process_llm_response(response, True)


def main():
    return


if __name__ == "__main__":
    main()
