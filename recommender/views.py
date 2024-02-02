# from rest_framework.response import Response
import json

from django.http import HttpResponse
from rest_framework.views import APIView

from recommender.engine.faiss_engine import LangchainFaissEngine
from recommender.reranker.crossencoder_reranker import CrossEncoderReranker
from recommender.reranker.popularity_reranker import PopularityReranker
from recommender.reranker.rating_reranker import RatingReranker


# Create your views here.
class MovieRecommendView(APIView):
    engine = LangchainFaissEngine.instance()
    popularity_reranker = PopularityReranker()
    rating_reranker = RatingReranker()
    crossencoder_reranker = CrossEncoderReranker()

    def get(self, request, format=None):
        # Get the query param
        query = request.query_params.get("query").strip()

        # Edge case: query is empty -> return empty
        if not query:
            return HttpResponse([], content_type="application/json")

        # Get recommendations
        movies = self.engine.search(query, k=100)

        # Re-rank
        movies = self.rating_reranker.rerank(movies=movies, query=query, k=15)
        movies = self.crossencoder_reranker.rerank(
            movies=movies, query=query, k=None, threshold=0.002
        )

        # Format Output
        results = [movie.model_dump() for movie in movies]
        results = json.dumps(results)

        return HttpResponse(results, content_type="application/json")
