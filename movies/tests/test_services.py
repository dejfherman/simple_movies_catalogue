from django.test import TestCase
from movies.models import Movie
from movies.services import find_by_name_match
from movies.tests.utils import mock_csfd_hash_set


class SearchServiceTest(TestCase):
    def setUp(self):
        hashes = mock_csfd_hash_set(2)
        self.ep4 = Movie.objects.create(
            name="Star Wars: Epizoda IV - Nová naděje",
            csfd_hash=hashes.pop(),
        )
        self.ep3 = Movie.objects.create(
            name="Star Wars: Epizoda III - Pomsta Sithů",
            csfd_hash=hashes.pop(),
        )

    def test_find_one(self):
        movie_ids = set(find_by_name_match(Movie, "Nová naděje").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep4.pk})

    def test_find_multiple(self):
        movie_ids = set(find_by_name_match(Movie, "Star Wars").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep3.pk, self.ep4.pk})

    def test_find_case_insensitive(self):
        movie_ids = set(find_by_name_match(Movie, "star wars").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep3.pk, self.ep4.pk})

    def test_find_norm_accents(self):
        movie_ids = set(find_by_name_match(Movie, "nova nadeje").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep4.pk})

    def test_find_special_char(self):
        movie_ids = set(find_by_name_match(Movie, "-").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep3.pk, self.ep4.pk})

    def test_find_surrounding_whitespace(self):
        movie_ids = set(find_by_name_match(Movie, " Star Wars: Epizoda IV - Nová naděje ").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep4.pk})

    def test_find_conflate_whitespace(self):
        movie_ids = set(find_by_name_match(Movie, "Star       Wars").values_list("pk", flat=True))
        self.assertSetEqual(movie_ids, {self.ep3.pk, self.ep4.pk})
