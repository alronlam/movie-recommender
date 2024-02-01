import abc
from typing import List

from recommender.models import MovieResult


class AsbtractRecommendationEngine:
    @abc.abstractmethod
    def recommend(self, query, k, **kwargs) -> List[MovieResult]:
        pass
