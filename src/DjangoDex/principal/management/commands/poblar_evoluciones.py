import requests
from django.core.management.base import BaseCommand
from principal.models import Pokemon, EvolutionLine

class Command(BaseCommand):
    help = 'Poblar el modelo EvolutionLine usando la PokeAPI'

    def handle(self, *args, **kwargs):
        pokemon_list = Pokemon.objects.all()
        
        for pokemon in pokemon_list:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon.id}/')
            if response.status_code == 200:
                data = response.json()
                evolution_chain_url = data['evolution_chain']['url']

                response_chain = requests.get(evolution_chain_url)
                if response_chain.status_code == 200:
                    chain_data = response_chain.json()['chain']
                    evolution_names = []
                    sprite_urls = []
                    current_chain = chain_data
                    
                    while current_chain:
                        species_name = current_chain['species']['name']
                        evolution_names.append(species_name.capitalize())
                        
                        # Obtener la URL del sprite
                        response_pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{species_name.lower()}/')
                        if response_pokemon.status_code == 200:
                            sprite_url = response_pokemon.json()['sprites']['front_default']
                            sprite_urls.append(sprite_url)
                        
                        current_chain = current_chain['evolves_to'][0] if current_chain['evolves_to'] else None
                    
                    evolution_line = " - ".join(evolution_names)
                    sprite_line = ",".join(sprite_urls)

                    EvolutionLine.objects.create(pokemon=pokemon, evolutions=evolution_line, sprites=sprite_line)
                    self.stdout.write(self.style.SUCCESS(f'Evolución de {pokemon.name} guardada como {evolution_line}'))
            else:
                self.stdout.write(self.style.ERROR(f'Error obteniendo datos para {pokemon.name}'))