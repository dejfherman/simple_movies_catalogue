from django.db.models import QuerySet
from movies.models import NameIndexedModel
from movies.utils import normalize_name

def find_by_name_match(model: NameIndexedModel, name: str) -> QuerySet[NameIndexedModel]:
    """
    Returns a queryset of existing model instances with names matching the input str ordered by search relevance.
    """
    norm_name = normalize_name(name)
    return model.objects.filter(search_name__contains=norm_name)
