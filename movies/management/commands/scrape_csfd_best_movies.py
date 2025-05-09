from django.core.management.base import BaseCommand
from movies.scraper import scrape_movie_list_data

class Command(BaseCommand):
    help = "Scrape movies and actors from the CSFD site and save to DB"

    def handle(self, *args, **options):
        self.stdout.write("Starting movie scrape...")
        scrape_movie_list_data()
        self.stdout.write(self.style.SUCCESS("Scraping complete."))
