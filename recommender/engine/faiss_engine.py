import json
from datetime import datetime

import numpy as np
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

from config import settings
from recommender.engine.base import AsbtractRecommendationEngine
from recommender.models import MovieResult


class LangchainFaissEngine(AsbtractRecommendationEngine):
    _instance = None

    BGE_PREFIX = "Represent this sentence for searching relevant movie descriptions: "

    @staticmethod
    def instance():
        if LangchainFaissEngine._instance is None:
            LangchainFaissEngine._instance = LangchainFaissEngine()
        return LangchainFaissEngine._instance

        # Loade Model

    def __init__(
        self,
        model_name=f"models/{settings.EMBEDDER_MODEL}",
        faiss_index_dir=settings.BASE_DIR
        / f"models/faiss_index_llm-embedder_title_overview_genres_keywords",
        append_bge_prefix=False,
    ):
        embeddings_cache_dir = (
            settings.BASE_DIR / f"models/runtime_cache/{settings.EMBEDDER_MODEL}",
        )
        self.model_name = model_name
        self.append_bge_prefix = append_bge_prefix
        self.embeddings_cache_dir = embeddings_cache_dir

        # Load Model
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        bge_embedding_model = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        # Load FAISS_INDEX
        self.db = FAISS.load_local(faiss_index_dir, bge_embedding_model)

    def search(self, query, k=30, threshold=-np.inf):
        if self.append_bge_prefix:
            query = self.BGE_PREFIX + query

        retriever = self.db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k,
                "score_threshold": threshold,
            },
        )

        docs = retriever.get_relevant_documents(query)
        data_dicts = [self.doc_to_dict(x) for x in docs]
        movies = [self.data_dict_to_movie(x) for x in data_dicts]

        return movies

    def data_dict_to_movie(self, data_dict):
        # Parse genre string
        data_dict["genres"] = [
            x["name"] for x in json.loads(data_dict.get("genres", "").replace("'", '"'))
        ]

        # Derived fields
        try:
            date_obj = datetime.strptime(data_dict["release_date"], "%Y-%m-%d")
            data_dict["year"] = str(date_obj.year)
        except Exception:
            data_dict["year"] = "Unknown"

        data_dict["poster_url"] = (
            f"https://image.tmdb.org/t/p/original{data_dict['poster_path']}"
            if data_dict["poster_path"]
            else ""
        )
        data_dict["imdb_url"] = (
            f"https://imdb.com/title/{data_dict['imdb_id']}/"
            if data_dict["imdb_id"]
            else ""
        )

        # Data cleaning - set ratings to 0 if blank
        data_dict["vote_average"] = (
            data_dict["vote_average"] if data_dict["vote_average"] else 0
        )
        data_dict["vote_count"] = (
            data_dict["vote_count"] if data_dict["vote_count"] else 0
        )

        result = MovieResult(**data_dict)
        return result

    def doc_to_dict(self, doc):
        # LangChain + FAISS just structures data in this way.
        # Text used for the search is in "page_content" (string with each key-value in a line).
        # Every other data col is in a metadata dict
        data = doc.page_content.split("\n")
        data_dict = {}
        for kv_tuple in data:
            try:
                key, value = kv_tuple.split(":", maxsplit=1)
                data_dict[key] = value
            except Exception:
                pass

        data_dict.update(doc.metadata)

        return data_dict
