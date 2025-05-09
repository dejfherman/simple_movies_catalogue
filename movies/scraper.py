import httpx
from bs4 import BeautifulSoup
from django.db import transaction
from movies.models import Movie, Actor
from movies.utils import normalize_name, hash_url

BASE_CSFD_URL = "https://www.csfd.cz"


def scrape_movie_list_data():
    """
    Scrape actor and movie data from CSFD best movies list and save them into database.

    Intended to be used in a django command, hence the dual responsibility of fetching and saving.
    """
    movie_counter = 0

    # de-duplication checklist (assuming movies won't be duplicated in the source list)
    all_actor_hashes = set(Actor.objects.values_list("csfd_hash", flat=True))

    while movie_counter < 300:
        list_view_url = f"{BASE_CSFD_URL}/zebricky/filmy/nejlepsi/?from={movie_counter + 1}"
        movie_counter, all_actor_hashes = scrape_movies_from_list_page(list_view_url, movie_counter, all_actor_hashes)

    print(f"Total movies processed: {movie_counter}")


def scrape_movies_from_list_page(page_url: str, movie_counter: int, all_actor_hashes: set[str]):
    """
    Scrape actor and movie data from CSFD best movies list page and save them into database.

    Intended to be used in a django command, hence the dual responsibility of fetching and saving.
    """
    # get the soup
    r = httpx.get(page_url, follow_redirects=True)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    print(f"Opened page {page_url}")

    # walk the movies
    for detail_link_elem in soup.select("a.film-title-name"):
        if movie_counter >= 300:
            break

        movie_title = detail_link_elem.text.strip()
        print(f"Found movie: {movie_title}")
        movie_detail_href = detail_link_elem.get("href")

        if Movie.objects.filter(csfd_hash=hash_url(movie_detail_href)).exists():
            # condition for re-runs
            # movie and actor persistence should be atomic, so if movie exists, we can skip to next
            # assumes that actor lists in movie detail view don't change
            print("Movie already known, skipping.")
            movie_counter += 1
            continue

        movie_actors_dict = scrape_actors_from_detail_view(f"{BASE_CSFD_URL}{movie_detail_href}")
        print(f"Found {len(movie_actors_dict)} actors associated with the movie.")

        # de-duplication measure
        new_hashes = set(movie_actors_dict.keys()) - all_actor_hashes

        # persist movie data
        with transaction.atomic():
            movie = Movie.objects.create(
                name=movie_title,
                csfd_hash=hash_url(movie_detail_href),
            )
            Actor.objects.bulk_create([movie_actors_dict[h] for h in new_hashes])
            # refresh from db for PKs hydration
            persisted_actors = Actor.objects.filter(csfd_hash__in=movie_actors_dict.keys())
            movie.actors.add(*persisted_actors)
            all_actor_hashes.update(new_hashes)
            print(f"Movie saved along {len(new_hashes)} new actors.")

        movie_counter += 1

    return movie_counter, all_actor_hashes


def scrape_actors_from_detail_view(view_url: str) -> dict[str, Actor]:
    """
    Scrape actor names from a CSFD movie detail view and turn them into Actor objects. Returns a dict of Actor objects
    keyed by their csfd_hash.
    """
    # get the soup
    r = httpx.get(view_url, follow_redirects=True)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")

    # find the relevant element
    actors_div = None
    movie_info_elems = soup.select("#creators div")
    for el in movie_info_elems:
        h4 = el.find("h4")
        if h4 and h4.text == "Hrají:":
            actors_div = el
            break

    if actors_div is None:
        # a few movies don't have a "starring" section
        return {}

    # walk the actors data
    actors = {}
    for actor_link in actors_div.select("a:not(.more)"):
        name = actor_link.text.strip()
        rel_link = actor_link.get("href")
        actor_hash = hash_url(rel_link)
        norm_name = normalize_name(name)        # actors will be bulk_created, so on save hooks cannot be relied on
        actors[actor_hash] = Actor(name=name, csfd_hash=actor_hash, search_name=norm_name)

    return actors
