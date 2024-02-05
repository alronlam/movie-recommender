from typing import List

import numpy as np
from loguru import logger
from sentence_transformers import CrossEncoder

from recommender.models import MovieResult
from recommender.reranker.base import AbstractReranker


class CrossEncoderReranker(AbstractReranker):
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-12-v2"):
        self.cross_encoder = CrossEncoder(model_name)

    def rerank(
        self, movies: List[MovieResult], query, k=None, threshold=-np.inf
    ) -> List[MovieResult]:

        # Compute the similarity scores for query x movie combinantions
        sentence_combinations = [
            [query, CrossEncoderReranker.movie_to_ce_str(movie)] for movie in movies
        ]
        similarity_scores = self.cross_encoder.predict(sentence_combinations)

        # Exclude those with scores below threshold
        filtered = [
            (movie, score)
            for movie, score in zip(movies, similarity_scores)
            if score >= threshold
        ]

        # Re-rank
        sim_scores_argsort = list(reversed(np.argsort(similarity_scores)))
        reranked = [filtered[idx] for idx in sim_scores_argsort]

        # Print the scores
        logger.debug("***********")
        logger.debug("Query:", query)
        for movie, score in reranked:
            logger.debug(f"{score:.6f}\t{movie.title}")
        logger.debug("***********")

        if k is not None:
            reranked = reranked[:k]

        return reranked

    @staticmethod
    def movie_to_ce_str(movie):
        genre_str = ",".join(movie.genres)
        ce_str = f"""
        Key Themes:{movie.keywords_human_readable}
        Genres:{genre_str}
        Overview: {movie.overview}
        Title:{movie.title}
        """
        return ce_str
