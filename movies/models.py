from django.db import models
from movies.utils import normalize_name


class NameIndexedModel(models.Model):
    name = models.CharField(max_length=100, default=None)
    search_name = models.CharField(max_length=200, editable=False, db_index=True, default=None)

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("Name must not be empty")
        new_name = normalize_name(self.name)
        if self.search_name != new_name:
            self.search_name = new_name
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Actor(NameIndexedModel):
    csfd_hash = models.CharField(max_length=32, unique=True, editable=False, default=None)


class Movie(NameIndexedModel):
    csfd_hash = models.CharField(max_length=32, unique=True, editable=False, default=None)
    actors = models.ManyToManyField(Actor, related_name='movies')
