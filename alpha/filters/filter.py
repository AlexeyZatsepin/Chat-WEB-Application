from django import template
from ..models import Profile

obj = template.Library()


@obj.filter
def get_photo(user):
    x = Profile.objects.get(user=user)
    return x.image
