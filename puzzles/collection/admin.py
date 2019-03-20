from django.contrib import admin
from .models import (
    Puzzle,
    Collection,
    AbstractClue,
)

admin.site.register(Puzzle)
admin.site.register(Collection)
admin.site.register(AbstractClue)
