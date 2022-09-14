from typing import Dict, Any, List, Optional

from dao.model.movie import Movie

from dao.movie import MovieDAO

from config import Config


class MovieService:
    dao: MovieDAO

    def __init__(self, dao: MovieDAO) -> None:
        self.dao = dao

    def get_one(self, mid: int) -> Movie:
        return self.dao.get_one(mid)

    def get_all(self,
                filters: Dict[str, Any],
                page: Optional[int] = None,
                status: Optional[str] = None) -> List[Movie]:
        if page:
            limit: Optional[int] = Config.ITEMS_ON_PAGE * page
            offset: Optional[int] = limit - Config.ITEMS_ON_PAGE
        else:
            limit, offset = None, None
        order_by = None
        if status == "new":
            order_by = Movie.year.desc()
        if filters.get("director_id") is not None:
            return self.dao.get_by_director_id(filters.get("director_id"), limit, offset, order_by)
        elif filters.get("genre_id") is not None:
            return self.dao.get_by_genre_id(filters.get("genre_id"), limit, offset, order_by)
        elif filters.get("year") is not None:
            return self.dao.get_by_year(filters.get("year"), limit, offset)
        else:
            return self.dao.get_all(limit, offset, order_by)

    def create(self, movie_d: Dict[str, Any]) -> Movie:
        movie: Movie = Movie(**movie_d)
        return self.dao.create(movie)

    def update(self, movie_id: int, movie_d: Dict[str, Any]):
        movie_by_id: Movie = self.dao.get_one(movie_id)
        for k, v in movie_d.items():
            setattr(movie_by_id, k, v)
        return self.dao.update(movie_by_id)

    def partially_update(self, movie_id: int, movie_d: Dict[str, Any]):
        movie_by_id: Movie = self.dao.get_one(movie_id)
        if "title" in movie_d:
            movie_by_id.title = movie_d.get("title")
        if "description" in movie_d:
            movie_by_id.description = movie_d.get("description")
        if "trailer" in movie_d:
            movie_by_id.trailer = movie_d.get("trailer")
        if "year" in movie_d:
            movie_by_id.year = movie_d.get("year")
        if "rating" in movie_d:
            movie_by_id.rating = movie_d.get("rating")
        if "genre_id" in movie_d:
            movie_by_id.genre_id = movie_d.get("genre_id")
        if "director_id" in movie_d:
            movie_by_id.director_id = movie_d.get("director_id")
        self.dao.update(movie_by_id)

    def delete(self, mid: int) -> None:
        self.dao.delete(mid)
