from typing import List, Optional

from sqlalchemy.orm import scoped_session

from dao.model.movie import Movie


class MovieDAO:
    session: scoped_session

    def __init__(self, session: scoped_session) -> None:
        self.session = session

    def get_one(self, mid: int) -> Movie:
        return self.session.query(Movie).get(mid)

    def get_all(self,
                limit: Optional[int],
                offset: Optional[int],
                order_by: Optional[str]) -> List[Movie]:
        if limit is not None and offset is not None:
            if order_by is not None:
                return self.session.query(Movie).order_by(order_by).limit(limit).offset(offset)
            else:
                return self.session.query(Movie).limit(limit).offset(offset)
        if order_by is not None:
            return self.session.query(Movie).order_by(order_by)
        return self.session.query(Movie).all()

    def get_by_director_id(self,
                           val: int,
                           limit: Optional[int],
                           offset: Optional[int],
                           order_by: Optional[str]) -> List[Movie]:
        if limit is not None and offset is not None:
            if order_by is not None:
                return self.session.query(Movie).filter(Movie.director_id == val).\
                    order_by(order_by).limit(limit).offset(offset)
            else:
                return self.session.query(Movie).filter(Movie.director_id == val).limit(limit).offset(offset)
        if order_by is not None:
            return self.session.query(Movie).filter(Movie.director_id == val). \
                order_by(order_by)
        return self.session.query(Movie).filter(Movie.director_id == val)

    def get_by_genre_id(self,
                        val: int,
                        limit: Optional[int],
                        offset: Optional[int],
                        order_by: Optional[str]) -> List[Movie]:
        if limit is not None and offset is not None:
            if order_by is not None:
                return self.session.query(Movie).filter(Movie.genre_id == val). \
                    order_by(order_by).limit(limit).offset(offset)
            else:
                return self.session.query(Movie).filter(Movie.genre_id == val).limit(limit).offset(offset)
        if order_by is not None:
            return self.session.query(Movie).filter(Movie.genre_id == val). \
                order_by(order_by)
        return self.session.query(Movie).filter(Movie.genre_id == val)

    def get_by_year(self,
                    val: int,
                    limit: Optional[int],
                    offset: Optional[int]) -> List[Movie]:
        if limit is not None and offset is not None:
            return self.session.query(Movie).filter(Movie.year == val).limit(limit).offset(offset)
        return self.session.query(Movie).filter(Movie.year == val)

    def create(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, mid: int) -> None:
        movie: Movie = self.get_one(mid)
        self.session.delete(movie)
        self.session.commit()

    def update(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        return movie
