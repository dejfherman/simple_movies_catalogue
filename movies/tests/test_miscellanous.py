from django.test import TestCase, SimpleTestCase
from django.db.utils import IntegrityError
from movies.utils import normalize_name
from movies.models import Movie, Actor
from movies.tests.utils import mock_csfd_hash

class NormalizeNameTests(SimpleTestCase):
    def test_normalize_string(self):
        self.assertEqual(normalize_name("Černý"), "cerny")
        self.assertEqual(normalize_name("Přelet nad kukaččím hnízdem"), "prelet nad kukaccim hnizdem")
        self.assertEqual(normalize_name("Star Wars: Epizoda IV - Nová naděje"), "star wars: epizoda iv - nova nadeje")


class TestModelSaving(TestCase):
    def setUp(self):
        self.mocked_hash = mock_csfd_hash()

    def test_actor_hash_not_empty(self):
        with self.assertRaisesMessage(IntegrityError,'NOT NULL constraint failed'):
            Actor.objects.create(name="Bruce Willis")

    def test_actor_hash_unique(self):
        Actor.objects.create(name="Adam Černý", csfd_hash=self.mocked_hash)
        with self.assertRaisesMessage(IntegrityError,'UNIQUE constraint failed'):
            Actor.objects.create(name="Bruce Willis", csfd_hash=self.mocked_hash)

    def test_movie_hash_not_empty(self):
        with self.assertRaisesMessage(IntegrityError,'NOT NULL constraint failed'):
            Movie.objects.create(name="Pelíšky")

    def test_movie_hash_unique(self):
        Movie.objects.create(name="Beetlejuice", csfd_hash=self.mocked_hash)
        with self.assertRaisesMessage(IntegrityError,'UNIQUE constraint failed'):
            Movie.objects.create(name="Pelíšky", csfd_hash=self.mocked_hash)

    def test_actor_name_not_empty(self):
        # because of on-save processing, this exception is not from the db layer
        with self.assertRaisesMessage(ValueError,'Name must not be empty'):
            Actor.objects.create()

    def test_actor_generates_search_name(self):
        actor = Actor.objects.create(name="Adam Černý", csfd_hash=self.mocked_hash)
        self.assertTrue(actor.search_name)          # not empty

    def test_movie_name_not_empty(self):
        # because of on-save processing, this exception is not from the db layer
        with self.assertRaisesMessage(ValueError,'Name must not be empty'):
            Movie.objects.create()

    def test_movie_generates_search_name(self):
        movie = Movie.objects.create(name="Přelet nad kukaččím hnízdem", csfd_hash=self.mocked_hash)
        self.assertTrue(movie.search_name)          # not empty
