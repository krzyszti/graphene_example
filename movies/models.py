import datetime

from django.db import models

from movies.helpers import get_movie_data_from_ombd


class Movie(models.Model):
    title = models.CharField(max_length=128)
    year = models.IntegerField(default=1970)
    rated = models.CharField(max_length=16)
    released = models.DateField()
    runtime = models.CharField(max_length=16)
    genre = models.TextField()
    director = models.CharField(max_length=128)
    writer = models.CharField(max_length=128)
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    awards = models.TextField()
    metascore = models.IntegerField()
    imdb_rating = models.FloatField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        additional_data = get_movie_data_from_ombd(self.title)

        self.year = self.year or int(additional_data.get('year', 0))
        self.rated = additional_data.get('rated', '')
        self.released = datetime.datetime.strptime(additional_data.get('released', '01 Jan 1970'), '%d %b %Y').date()
        self.runtime = additional_data.get('runtime', '')
        self.genre = additional_data.get('genre', '')
        self.director = additional_data.get('director', '')
        self.writer = additional_data.get('writer', '')
        self.actors = additional_data.get('actors', '')
        self.plot = additional_data.get('plot', '')
        self.language = additional_data.get('language', '')
        self.country = additional_data.get('country', '')
        self.awards = additional_data.get('awards', '')
        self.metascore = int(additional_data.get('metascore', 0))
        self.imdb_rating = float(additional_data.get('imdbrating', 0))

        super(Movie, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)


class Comment(models.Model):
    body = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
