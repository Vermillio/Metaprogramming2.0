
class Movie:
    def __init__(self, name='', year=0):
        self.name = name
        self.year = year


class MovieList:
    def __init__(self, name=''):
        self.name = name
        self.movies = [Movie(name="Fight Club", year=1999), Movie(name="Lux Aeterna", year=2019), Movie(name="Generation P", year=2012)]


class User:
    def __init__(self):
        self.name = "Anna"
        self.email = "tmp@gmail.com"
        self.likes = MovieList("likes")
