# from rest_framework.response import Response
import json

from django.http import HttpResponse
from rest_framework.views import APIView

from src.engine import SemanticSearchEngine


# Create your views here.
class MovieRecommendView(APIView):
    engine = SemanticSearchEngine.instance()

    def get(self, request, format=None):
        query = request.query_params.get("query")
        docs = self.engine.search(query, k=10)

        data = []
        for doc in docs:
            data_dict = {
                "title": doc["title"],
                "overview": doc["overview"],
                "genres": doc["genres"],
                "year": doc["release_date"][:4],
                "poster_url": doc["poster_url"],
                "imdb_url": doc["imdb_url"],
            }
            data.append(data_dict)

        output = json.dumps(data)

        return HttpResponse(output, content_type="application/json")
