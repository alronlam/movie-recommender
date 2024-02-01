from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class MovieResult(BaseModel):
    title: str
    overview: str
    genres: List[str]
    year: str
    imdb_url: str
    poster_url: str
    vote_average: Optional[float] = Field(serialization_alias="rating")
    vote_count: Optional[int] = Field(serialization_alias="rating_count")
