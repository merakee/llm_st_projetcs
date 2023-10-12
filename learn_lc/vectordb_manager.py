# pyhton 
import os
from enum import Enum

# local 
from system_util import IncompleteSetupException

# langchain
# Vector store
from langchain.vectorstores import Chroma

# implementation 
class VDBType(Enum):
    chroma = 1
    faiss = 2

class VectorDBManager:
    def __init__(self, db_type=VDBType.chroma, embedding_model=None, persitent=True, db_dir=None):
        self.db_type = db_type
        self.embedding_model = embedding_model
        self.is_persitent = persitent
        if persitent and not db_dir:
            db_dir = './vdb/chroma/'
        self.db_dir = db_dir
        self.vdb = self.get_vector_store() if self.embedding_model else None
        self.retriver = self.get_retriever() if self.vdb else None

    def get_vector_store(self):
        # Embed and store the texts
        # Supplying a persist_directory will store the embeddings on disk
        if not self.embedding_model:
            raise IncompleteSetupException(
                "Embedding model not set. Please set the embedding model.")
        if self.is_persistentnot and not self.db_dir:
            raise IncompleteSetupException(
                "db dir not set. Persitent db needs dir. Please set the db dir.")

        if self.db_type == VDBType.chroma:
            if self.is_persistant:
                vectordb = Chroma(persist_directory=self.db_dir,
                                  embedding_function=self.embedding_model)
            else:
                vectordb = Chroma(embedding_function=self.embedding_model)
            return vectordb
        return None

    def delete_vdb_dir(self):
        if self.is_persitent and self.db_dir
            os.system(f"rm -rf {self.db_dir}")

    def embed_texts(self, texts):
        # Embed and store the texts
        # Supplying a persist_directory will store the embeddings on disk
        if not self.vdb:
            raise IncompleteSetupException(
                "Vector DB not set. Please set Vector DB")
        vcollection = self.vdb.from_documents(documents=texts)
        if self.is_persitent:
            if self.db_dir:
                vcollection.persist()
            else:
                raise IncompleteSetupException(
                    "db dir not set. Persitent db needs dir. Please set the db dir.")

    def get_retriever(self, search_type="similarity", max_count=3):
        if not self.vdb:
            raise IncompleteSetupException(
                "Vector DB not set. Please set Vector DB")
        retriever = self.vdb.as_retriever(
            search_kwargs={"k": max_count}, search_type=search_type)
        return retriever
