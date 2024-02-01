import abc
from typing import List

from recommender.models import MovieResult


class AbstractReranker:
    @abc.abstractmethod
    def rerank(
        self, movies: List[MovieResult], query, k=None, *args, **kwargs
    ) -> List[MovieResult]:
        pass
