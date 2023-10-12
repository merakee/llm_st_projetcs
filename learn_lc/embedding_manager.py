

# open ai embedding model: text-embedding-ada-002
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