# pyhton
from enum import Enum
# local

# langchain
# document loader
from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import DirectoryLoader

# splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# implementation


class DocumentUploadType(Enum):
    file = 1
    folder = 2


class FileType(Enum):
    txt = 1
    md = 2
    pdf = 3
    jpg = 4
    csv = 5


class DocumentUtil:
    def __init__(self, upload_type, file_path, file_type):
        self.upload_type = upload_type
        self.file_path = file_path
        self.file_type = file_type

    def get_documents(self):
        # Load and process the text files
        if self.type == DocumentUploadType.file:
            if self.file_type == FileType.txt:
                loader = TextLoader(self.file_path)
            if self.file_type == FileType.csv:
                loader = CSVLoader(self.file_path)
            else:
                loader = UnstructuredFileLoader(self.file_path)
        elif self.type == DocumentUploadType.folder:
            file_s = f"./*.{self.file_type.name}"
            if self.file_type == FileType.txt:
                loader = DirectoryLoader(
                    self.file_path, glob=file_s, loader_cls=TextLoader)
            elif self.file_type == FileType.csv:
                loader = DirectoryLoader(
                    self.file_path, glob=file_s, loader_cls=CSVLoader)
            else:
                loader = DirectoryLoader(
                    self.file_path, glob=file_s, loader_cls=UnstructuredFileLoader)

        documents = loader.load()
        return documents

    @staticmethod
    def document_from_text(text, info):
        doc = Document(page_content=text, metadata=info)
        return doc

    def get_default_file_path():
        return "./testdata/singlefile/test_text.txt"

    def get_default_dir_path():
        return "./testdata/multiplefiles/"

    def chunk_documents(documents, chunk_size=1000, chunk_overlap_per=20):
        # splitting the text into
        chunk_overlap = (chunk_overlap_per*chunk_size/100.0)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(documents)
        return texts
