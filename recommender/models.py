from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    poster_url = models.CharField(max_length=255)
    release_date = models.DateField()
    genres = models.JSONField(default=[])
    imdb_url = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    # @property
    # def imdb_url(self):
    #     return f"https://imdb.com/title/{self.imdb_id}"


# class Genre(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
