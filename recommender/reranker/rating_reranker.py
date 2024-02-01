from typing import List

from recommender.models import MovieResult
from recommender.reranker.base import AbstractReranker


class RatingReranker(AbstractReranker):
    def rerank(self, movies: List[MovieResult], query, k=None) -> List[MovieResult]:
        reranked = list(
            sorted(
                movies,
                key=lambda movie: movie.vote_count * movie.vote_average,
                reverse=True,
            )
        )

        if k is not None:
            reranked = reranked[:k]

        return reranked
