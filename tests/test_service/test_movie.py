from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1,
                    title='movie_1',
                    description='some description',
                    trailer='some trailer',
                    year=1992,
                    rating=9.0,
                    genre_id=1,
                    director_id=1)
    movie_2 = Movie(id=2,
                    title='movie_2',
                    description='some description',
                    trailer='some trailer',
                    year=1980,
                    rating=7.0,
                    genre_id=1,
                    director_id=2)
    movie_3 = Movie(id=3,
                    title='movie_3',
                    description='some description',
                    trailer='some trailer',
                    year=1962,
                    rating=6.0,
                    genre_id=2,
                    director_id=3)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie != None
        assert movie.id != None

    def test_get_all(self):
        movies = self.movie_service.get_all(filters={})
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "movie_4",
            "description": "some description",
            "trailer": "some trailer",
            "year": 1990,
            "rating": 5.5,
            "genre_id": 2,
            "director_id": 3
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "title": "movie_555",
            "description": "some description",
            "trailer": "some trailer",
            "year": 1960,
            "rating": 5.5,
            "genre_id": 2,
            "director_id": 3
        }
        self.movie_service.update(2, movie_d)
