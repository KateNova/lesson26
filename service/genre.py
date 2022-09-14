from typing import Dict, Any, List, Optional

from config import Config
from dao.genre import GenreDAO
from dao.model.genre import Genre


class GenreService:
    dao: GenreDAO

    def __init__(self, dao: GenreDAO) -> None:
        self.dao = dao

    def get_one(self, gid: int) -> Genre:
        return self.dao.get_one(gid)

    def get_all(self, page: Optional[int] = None) -> List[Genre]:
        if page:
            limit: Optional[int] = Config.ITEMS_ON_PAGE * page
            offset: Optional[int] = limit - Config.ITEMS_ON_PAGE
        else:
            limit, offset = None, None
        return self.dao.get_all(limit, offset)

    def create(self, genre_d: Dict[str, Any]) -> Genre:
        genre: Genre = Genre(**genre_d)
        return self.dao.create(genre)

    def update(self, genre_id: int, genre_d: Dict[str, Any]) -> Genre:
        genre_by_id: Genre = self.dao.get_one(genre_id)
        for k, v in genre_d.items():
            setattr(genre_by_id, k, v)
        return self.dao.update(genre_by_id)

    def partially_update(self, genre_id: int, genre_d: Dict[str, Any]) -> Genre:
        genre_by_id: Genre = self.dao.get_one(genre_id)
        if "name" in genre_d:
            genre_by_id.name = genre_d.get("name")
        self.dao.update(genre_by_id)

    def delete(self, gid: int) -> None:
        self.dao.delete(gid)
