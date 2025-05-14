from ninja import NinjaAPI
from movies.api import api_router as movies_api_router

api = NinjaAPI()
api.add_router("/movies/", movies_api_router)
