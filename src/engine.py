import json

from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

from config import settings


class SemanticSearchEngine:
    _instance = None

    @staticmethod
    def instance(model_name="BAAI/bge-small-en"):
        if SemanticSearchEngine._instance is None:
            _instance = SemanticSearchEngine("BAAI/bge-small-en")
        return _instance

    def __init__(self, model_name):
        self.model_name = model_name
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        bge_embedding_model = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        store = LocalFileStore(settings.BASE_DIR / "data/cache/")

        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            bge_embedding_model, store, namespace="BAAI-bge-large-en"
        )

        FAISS_INDEX_PATH = settings.BASE_DIR / "data/faiss_index"
        self.db = FAISS.load_local(FAISS_INDEX_PATH, self.embedder)

    def search(self, query, k=50, score_threshold=0.5):
        retriever = self.db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k,
                "score_threshold": score_threshold,
            },
        )

        docs = retriever.get_relevant_documents(query)
        docs = [self.doc_to_dict(doc) for doc in docs]

        return docs

    def doc_to_dict(self, doc):
        data = doc.page_content.split("\n")
        data_dict = {}
        for kv_tuple in data:
            try:
                key, value = kv_tuple.split(":", maxsplit=1)
                data_dict[key] = value
            except Exception:
                pass

        data_dict["genres"] = json.loads(data_dict["genres"].replace("'", '"'))

        return data_dict
