import requests
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Pokemon,EvolutionLine

def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def index(request):
    generation_5_pokemon = []
    for pokemon_id in range(494, 650):
        data = get_pokemon_data(pokemon_id)
        if data:
            generation_5_pokemon.append({
                'id': data['id'],
                'name': data['name'],
                'sprite': data['sprites']['front_default'],
                'types': [type_info['type']['name'] for type_info in data['types']]
            })

    context = {'generation_5_pokemon': generation_5_pokemon}
    return render(request, 'principal/index.html', context)

def pokemon_detail(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    evolution_line = EvolutionLine.objects.filter(pokemon=pokemon).first()
    
    if evolution_line:
        evolution_sprites = evolution_line.sprites.split(',')
        evolution_names = evolution_line.evolutions.split(',')
    else:
        evolution_sprites = []
        evolution_names = []

    context = {
        'pokemon': pokemon,
        'evolution_sprites': evolution_sprites,
        'evolution_names': evolution_names,
    }
    return render(request, 'principal/pokemon_detail.html', context)