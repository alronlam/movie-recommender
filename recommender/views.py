# from rest_framework.response import Response
import json
import time

from django.http import HttpResponse
from loguru import logger
from rest_framework.views import APIView

from config import settings
from recommender.engine.faiss_engine import LangchainFaissEngine
from recommender.reranker.crossencoder_reranker import CrossEncoderReranker
from recommender.reranker.rating_reranker import RatingReranker


# Create your views here.
class MovieRecommendView(APIView):
    engine = LangchainFaissEngine.instance()
    rating_reranker = RatingReranker()
    crossencoder_reranker = CrossEncoderReranker.instance()

    def get(self, request, format=None):
        # Get the query params
        query = request.query_params.get("query").strip()
        ranking = request.query_params.get("ranking").strip()
        weight_by_rating = ranking.lower() == "popularity"

        # Edge case: query is empty -> return empty
        if not query:
            return HttpResponse([], content_type="application/json")

        # Get candidates
        retrieval_start = time.time()
        movies = self.engine.search(query, k=150, threshold=0.0)
        retrieval_end = time.time()

        # Filter to popular movies according to ratings
        rating_start = time.time()
        movies = self.rating_reranker.rerank(movies=movies, query=query, k=50)
        rating_end = time.time()

        # Re-rank with cross-encoder for relevance
        reranker_start = time.time()
        movies = self.crossencoder_reranker.rerank(
            movies=movies,
            query=query,
            k=None,
            threshold=-9.0,
            weight_by_rating=weight_by_rating,
            debug=settings.DEBUG,
        )
        reranker_end = time.time()

        logger.debug(f"Retrieval: {retrieval_end-retrieval_start:.2f}s")
        logger.debug(f"Rating Re-ranking: {rating_end-rating_start:.2f}s")
        logger.debug(f"CE Re-ranking: {reranker_end-reranker_start:.2f}s")

        # Format Output
        results = [movie.model_dump() for movie in movies]
        results = json.dumps(results)

        return HttpResponse(results, content_type="application/json")
