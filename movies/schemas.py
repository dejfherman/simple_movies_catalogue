from ninja import Schema

class CineItem(Schema):
    id: int
    name: str

class SearchResults(Schema):
    actors: list[CineItem]
    movies: list[CineItem]
