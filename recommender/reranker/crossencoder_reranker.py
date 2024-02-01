from typing import List

import numpy as np
from sentence_transformers import CrossEncoder

from recommender.models import MovieResult
from recommender.reranker.base import AbstractReranker


class CrossEncoderReranker(AbstractReranker):
    def __init__(self, model_name="BAAI/bge-reranker-base"):
        self.cross_encoder = CrossEncoder(model_name)

    def rerank(
        self, movies: List[MovieResult], query, k=None, *args, **kwargs
    ) -> List[MovieResult]:
        sentence_combinations = [
            [query, ",".join(movie.genres) + " " + movie.title + " " + movie.overview]
            for movie in movies
        ]

        # Compute the similarity scores for these combinations
        similarity_scores = self.cross_encoder.predict(sentence_combinations)

        # Sort the scores in decreasing order
        sim_scores_argsort = list(reversed(np.argsort(similarity_scores)))

        # Exclude 0 values
        reranked_filtered = [
            movies[i] for i in sim_scores_argsort if similarity_scores[i] > 0.002
        ]
        scores_filtered = [
            similarity_scores[i]
            for i in sim_scores_argsort
            if similarity_scores[i] > 0.002
        ]

        # Print the scores
        print("***********")
        print("Query:", query)
        for movie, score in zip(reranked_filtered, scores_filtered):
            print(f"{score:.6f}\t{movie.title}")
        print("***********")

        if k is not None:
            reranked_filtered = reranked_filtered[:k]

        return reranked_filtered
