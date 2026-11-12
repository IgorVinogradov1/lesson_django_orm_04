import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]


def show_all_pokemons(request):
    current_time = timezone.now()
    pokemon_markers = []
    for pokemon in Pokemon.objects.all():
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = None
        active_pokemons = PokemonEntity.objects.filter(pokemon=pokemon).exclude(appeared_at__gte=current_time).exclude(disappeared_at__lte=current_time)
        for pokemon_entity in active_pokemons:
            pokemon_markers.append({
                "lat": pokemon_entity.lat,
                "lon": pokemon_entity.lon,
                "image_url": img_url,
            })   

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'pokemons': pokemons_on_page,
        'pokemon_markers': pokemon_markers,
        'moscow_center': MOSCOW_CENTER,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    return render(request, 'pokemon.html', context={
        'pokemon': requested_pokemon,
        'moscow_center': MOSCOW_CENTER,
    })