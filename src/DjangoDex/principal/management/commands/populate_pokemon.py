from django.core.management.base import BaseCommand
import requests
from principal.models import Pokemon

class Command(BaseCommand):
    help = 'Popula la base de datos con Pokémon de la quinta generación'

    def handle(self, *args, **kwargs):
        for pokemon_id in range(494, 650):  # Quinta generación
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/")
            data = response.json()

            species_url = data['species']['url']
            species_response = requests.get(species_url)
            species_data = species_response.json()

            evolves_from = None
            if species_data['evolves_from_species']:
                evolves_from_name = species_data['evolves_from_species']['name']
                try:
                    evolves_from = Pokemon.objects.get(name=evolves_from_name)
                except Pokemon.DoesNotExist:
                    pass

            pokemon = Pokemon.objects.create(
                id=data['id'],
                name=data['name'],
                sprite=data['sprites']['front_default'],
                type_1=data['types'][0]['type']['name'],
                type_2=data['types'][1]['type']['name'] if len(data['types']) > 1 else None,
                hp=data['stats'][0]['base_stat'],
                attack=data['stats'][1]['base_stat'],
                defense=data['stats'][2]['base_stat'],
                special_attack=data['stats'][3]['base_stat'],
                special_defense=data['stats'][4]['base_stat'],
                speed=data['stats'][5]['base_stat'],
                weight=data['weight'] / 10,  # En kg
                height=data['height'] / 10,  # En metros
                abilities=', '.join([ability['ability']['name'] for ability in data['abilities']]),
                evolves_from=evolves_from
            )

            if evolves_from:
                evolves_from.evolves_to.add(pokemon)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with Generation V Pokémon'))