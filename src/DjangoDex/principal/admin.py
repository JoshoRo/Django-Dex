from django.contrib import admin
from .models import Pokemon

# Register your models here.

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_1', 'type_2', 'evolves_from')
    search_fields = ('name', 'id')
    list_filter = ('type_1', 'type_2')