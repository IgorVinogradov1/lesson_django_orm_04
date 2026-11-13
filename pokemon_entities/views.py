import json

from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]


def show_all_pokemons(request):
    current_time = timezone.now()
    pokemon_markers = []
    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })
        active_pokemons = PokemonEntity.objects.filter(pokemon=pokemon).exclude(appeared_at__gte=current_time).exclude(disappeared_at__lte=current_time)
        for pokemon_entity in active_pokemons:
            pokemon_markers.append({
                'lat': pokemon_entity.lat,
                'lon': pokemon_entity.lon,
                'image_url': img_url,
            })

    return render(request, 'mainpage.html', context={
        'pokemons': pokemons_on_page,
        'pokemon_markers': pokemon_markers,
        'moscow_center': MOSCOW_CENTER,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None

    current_time = timezone.now()
    pokemon_markers = []
    active_pokemons = PokemonEntity.objects.filter(pokemon=pokemon).exclude(appeared_at__gte=current_time).exclude(disappeared_at__lte=current_time)
    for pokemon_entity in active_pokemons:
        pokemon_markers.append({
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.lon,
            'image_url': img_url,
        })

    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'img_url': img_url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'entities': pokemon_markers,
    }

    if pokemon.previous_evolution:
        prev_evo = pokemon.previous_evolution
        requested_pokemon['previous_evolution'] = {
            'pokemon_id': prev_evo.id,
            'title_ru': prev_evo.title_ru,
            'img_url': request.build_absolute_uri(prev_evo.photo.url) if prev_evo.photo else None,
        }

    next_evo = pokemon.next_evolutions.first()
    if next_evo:
        requested_pokemon['next_evolution'] = {
            'pokemon_id': next_evo.id,
            'title_ru': next_evo.title_ru,
            'img_url': request.build_absolute_uri(next_evo.photo.url) if next_evo.photo else None,
        }

    return render(request, 'pokemon.html', context={
        'pokemon': requested_pokemon,
        'moscow_center': MOSCOW_CENTER,
    })