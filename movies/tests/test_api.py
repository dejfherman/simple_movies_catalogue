from django.test import TestCase
from movies.models import Movie, Actor
from movies.tests.utils import mock_csfd_hash

# a hack to offset how ninja routes don't play nice with regular django routing
BASE_API_PATH = "/api/movies"

class LivesearchEndpointTest(TestCase):
    def setUp(self):
        Actor.objects.create(name="Adam Černý", csfd_hash=mock_csfd_hash())
        Movie.objects.create(name="Černý jestřáb sestřelen", csfd_hash=mock_csfd_hash())

    def test_search_returns_normalized_match(self):
        # ninja offers TestClient that should be useful here, but for reasons too deeply ingrained to figure out
        # at the moment it has trouble recognizing expected GET params and will always behave as if q=""
        response = self.client.get(f"{BASE_API_PATH}/livesearch", {"q": "cerny"})
        self.assertContains(response, "Adam Černý")
        self.assertContains(response, "Černý jestřáb sestřelen")

    def test_search_empty_query(self):
        response = self.client.get(f"{BASE_API_PATH}/livesearch")
        self.assertEqual(response.status_code, 200)
