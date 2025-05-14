from django.test import TestCase
from django.urls import reverse
from movies.models import Movie, Actor
from movies.tests.utils import mock_csfd_hash, mock_csfd_hash_set


class SearchViewTest(TestCase):
    def setUp(self):
        Actor.objects.create(name="Adam Černý", csfd_hash=mock_csfd_hash())
        Movie.objects.create(name="Černý jestřáb sestřelen", csfd_hash=mock_csfd_hash())

    def test_search_returns_normalized_match(self):
        response = self.client.get(reverse('search'), {'q': 'cerny'})
        self.assertContains(response, "Adam Černý")
        self.assertContains(response, "Černý jestřáb sestřelen")

    def test_search_empty_query(self):
        response = self.client.get(reverse('search'), {})
        self.assertEqual(response.status_code, 200)


class DetailViewTest(TestCase):
    def setUp(self):
        random_hashes = mock_csfd_hash_set(size=4)
        Actor.objects.create(name="Adam Černý", csfd_hash=random_hashes.pop())
        Movie.objects.create(name="Černý jestřáb sestřelen", csfd_hash=random_hashes.pop())
        actor2 = Actor.objects.create(name="Bruce Willis", csfd_hash=random_hashes.pop())
        movie2 = Movie.objects.create(name="Smrtonosná past", csfd_hash=random_hashes.pop())
        movie2.actors.add(actor2)

        self.actor_pk = actor2.pk
        self.movie_pk = movie2.pk

    def test_actor_detail_returns_related(self):
        response = self.client.get(reverse('actor_detail', kwargs={'pk': self.actor_pk}))
        self.assertContains(response, "Bruce Willis")
        self.assertContains(response, "Smrtonosná past")
        self.assertNotContains(response, "Černý jestřáb sestřelen")

    def test_movie_detail_returns_related(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': self.movie_pk}))
        self.assertContains(response, "Smrtonosná past")
        self.assertContains(response, "Bruce Willis")
        self.assertNotContains(response, "Adam Černý")
