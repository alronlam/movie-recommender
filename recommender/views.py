# from rest_framework.response import Response
import json
import uuid

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from recommender.models import Movie
from recommender.serializers import MovieSerializer
from src.engine import SemanticSearchEngine


# Create your views here.
class MovieRecommendView(APIView):
    engine = SemanticSearchEngine.instance()

    def get(self, request, format=None):
        query = request.query_params.get("query")
        docs = self.engine.search(query, k=10)

        # TODO:
        movies = [Movie(title=doc["title"], overview=doc["overview"]) for doc in docs]
        results = serializers.serialize("json", movies)

        # this gives you a list of dicts
        results = serializers.serialize("python", movies)
        # now extract the inner `fields` dicts
        actual_data = [d["fields"] for d in results]
        # and now dump to JSON
        output = json.dumps(actual_data)

        # results = MovieSerializer(results, many=True)

        # dummy_data = [
        #     {
        #         "title": "The American Mall" + str(uuid.uuid4()),
        #         "overview": "The executive producers of High School Musical keep the good times rolling with this upbeat musical comedy set in the one place every American teenager's home away from home - the local shopping mall. Ally (Nina Dobrev) is an optimistic adolescent singer/songwriter whose hard working mother owns the mall music shop frequented by every teen in town. When Ally shares her music with Joey (Rob Mayes), a janitor in the mall who harbors rock star ambitions, she is thrilled to find someone who can truly relate to her songs as well as her heart. Trouble looms on the horizon, however, in the form of the mall owner's spoiled rotten daughter Madison (Autumn Reeser). Madison is the kind of girl who's used to getting whatever she wants, and what she wants now could prove disastrous for both Ally's ambitions, and her mother's popular music store.",
        #         "genres": ["Romance", "Comedy", "Drama", "Music"],
        #         "year": "2008",
        #         "imdbUrl": "https://imdb.com/title/tt1160313",
        #         "imageUrl": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/mDglbQwHIsOIvqSy0CwUihG8Y5J.jpg",
        #     },
        #     {
        #         "title": "True Confessions of a Hollywood Starlet",
        #         "overview": "A teen movie star attempts to overcome her addition to alcohol and salvage what's left of her career after passing out on the red carpet at her big Hollywood premiere and being sent to recover with her upbeat aunt in Indiana. Morgan Carter (Jo Jo) is only seventeen years old, but she's already on top of the world. But so much fame so early in life can yield unpredictable consequences, and when Morgan is sent to the hospital with alcohol poisoning, it's clear that she isn't ready to deal with the pressures of stardom. Whisked away to rehab as the paparazzi clamors for a picture and the press predicts her downfall, Morgan is sent by her mother and concerned manager to Indiana, far away from the temptations of Hollywood. Once there, the troubled starlet reluctantly starts to reconnect with her quirky Aunt Trudy (Valerie Bertinelli), who offers just the kind of unconditional support that the young girl needs to get her life - and career - back on track.",
        #         "genres": ["Drama", "Comedy", "Family"],
        #         "year": "1998",
        #         "imdbUrl": "https://imdb.com/title/tt1124401",
        #         "imageUrl": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/9AhcV0tblzJ1fp2rHAjW7yMqGz8.jpg",
        #     },
        #     {
        #         "title": "Classmates",
        #         "overview": "Feel-good movie about a college life of couple of friends and the consequences of a turning point which changed the life of each one of them.",
        #         "genres": [],
        #         "year": "2015",
        #         "imdbUrl": "https://imdb.com/title/tt4373868",
        #         "imageUrl": "https://media.themoviedb.org/t/p/w220_and_h330_face/xD4Mdz4KUPmYSJq7WrKj6hFStkl.jpg",
        #     },
        # ]
        return HttpResponse(output, content_type="application/json")
