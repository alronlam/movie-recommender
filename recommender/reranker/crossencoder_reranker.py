from typing import List

import numpy as np
from loguru import logger
from sentence_transformers import CrossEncoder

from recommender.models import MovieResult
from recommender.reranker.base import AbstractReranker


class CrossEncoderReranker(AbstractReranker):

    _instance = None

    @staticmethod
    def instance():
        if CrossEncoderReranker._instance is None:
            CrossEncoderReranker._instance = CrossEncoderReranker()
        return CrossEncoderReranker._instance

    def __init__(self, model_name="models/cross-encoder/ms-marco-MiniLM-L-12-v2"):
        self.cross_encoder = CrossEncoder(model_name)

    def rerank(
        self,
        movies: List[MovieResult],
        query,
        k=None,
        threshold=-np.inf,
        weight_by_rating=False,
        debug=False,
    ) -> List[MovieResult]:

        # Compute the similarity scores for query x movie combinantions
        sentence_combinations = [
            [query, CrossEncoderReranker.movie_to_ce_str(movie)] for movie in movies
        ]
        similarity_scores = self.cross_encoder.predict(sentence_combinations)

        # Re-rank
        sim_scores_argsort = list(reversed(np.argsort(similarity_scores)))
        reranked = [(movies[idx], similarity_scores[idx]) for idx in sim_scores_argsort]

        # Print the scores
        if debug:
            logger.debug("***********Reranker Scores\n")
            logger.debug("Query:", query)
            for movie, score in reranked:
                logger.debug(f"{score:.6f}\t{movie.title}")
            logger.debug("***********")

        # Exclude those with scores below threshold, and select top K
        reranked = [(movie, score) for movie, score in reranked if score >= threshold]

        # Weight by rating if applicable
        if weight_by_rating:
            movies = [movie for movie, score in reranked]
            scores = [score for movie, score in reranked]

            # Re-score by combining re-ranker score and movie ratings
            normalized_scores = CrossEncoderReranker.rescale_scores(scores)
            similarity_scores = [
                score * (movie.vote_count * movie.vote_average / 10)
                for movie, score in zip(movies, normalized_scores)
            ]
            sim_scores_argsort = list(reversed(np.argsort(similarity_scores)))
            reranked = [
                (movies[idx], similarity_scores[idx]) for idx in sim_scores_argsort
            ]

        if k is not None:
            reranked = reranked[:k]

        if debug:
            logger.debug("*********** Re-scaled Scores")
            logger.debug("Query:", query)
            for movie, score in reranked:
                logger.debug(f"{score:.6f}\t{movie.title}")
            logger.debug("***********")

        movies = [tuple[0] for tuple in reranked]
        return movies

    @staticmethod
    def rescale_scores(old_scores):
        # Sort the old_scores and get the ranks
        sorted_indices = sorted(
            range(len(old_scores)), key=lambda k: old_scores[k], reverse=True
        )
        ranks = np.zeros(len(old_scores), dtype=int)
        ranks[sorted_indices] = np.arange(len(old_scores)) + 1

        # Calculate decaying scores based on rank
        decay_factor = 0.9
        new_scores = [decay_factor ** (rank - 1) for rank in ranks]

        return new_scores

    @staticmethod
    def movie_to_ce_str(movie):
        genre_str = ",".join(movie.genres)
        ce_str = f"""
        Overview: {movie.overview}
        Title:{movie.title}
        Key Themes:{movie.keywords_human_readable}
        Genres:{genre_str}
        """
        return ce_str
